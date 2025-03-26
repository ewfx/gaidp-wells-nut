import os
import pandas as pd
import fitz
import requests
import re
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import List

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
TEXT_TO_REGEX_MODEL = "google/flan-t5-xxl"  # Better for instruction following
TABLE_EXTRACTION_MODEL = "microsoft/tapex-base-finetuned-wtq"  # Table processing model


@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    """Process PDF and convert all matching tables"""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are accepted")

    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Extract all matching tables
    dfs = extract_target_tables(pdf_path)

    if not dfs:
        raise HTTPException(400, "No tables with both 'MDRM' and 'Allowable Values' columns found")

    # Process all tables
    final_df = pd.concat(dfs, ignore_index=True)

    if "Allowable Values" in final_df.columns:
        final_df["RegEx Pattern"] = final_df["Allowable Values"].apply(generate_regex_pattern)

    csv_filename = file.filename.replace(".pdf", ".csv")
    csv_path = os.path.join(OUTPUT_FOLDER, csv_filename)
    final_df.to_csv(csv_path, index=False)

    return {
        "message": f"Processed {len(dfs)} tables successfully",
        "download_url": f"/download/{csv_filename}"
    }


def extract_target_tables(pdf_path: str) -> List[pd.DataFrame]:
    """Extract all tables containing both required columns"""
    doc = fitz.open(pdf_path)
    matching_tables = []

    for page in doc:
        tables = page.find_tables()
        if tables.tables:
            for table in tables:
                df = table.to_pandas()
                cols_lower = [str(col).lower() for col in df.columns]

                if all(x in cols_lower for x in ["mdrm", "allowable values"]):
                    # Standardize column names across tables
                    df.columns = [col.strip().title() for col in df.columns]
                    matching_tables.append(df)

    doc.close()
    return matching_tables


def generate_regex_pattern(text: str) -> str:
    """Convert text to regex using Hugging Face model with enhanced prompting"""
    try:
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

        # Improved prompt with examples
        prompt = f"""Convert this text validation rule to a standard regular expression.
        Examples:
        - "10-digit number" → ^\\d{10}$
        - "YYYY-MM-DD format" → ^\\d{{4}}-\\d{{2}}-\\d{{2}}$
        - "Letters and numbers only" → ^[A-Za-z0-9]+$
        Input: {text}
        Regex:"""

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{TEXT_TO_REGEX_MODEL}",
            headers=headers,
            json={
                "inputs": prompt,
                "parameters": {
                    "max_length": 50,
                    "temperature": 0.1,
                    "num_return_sequences": 1
                }
            },
            timeout=30
        )
        response.raise_for_status()

        result = response.json()[0]['generated_text'].strip()

        # Post-process the output
        cleaned_regex = result.split("→")[-1].split("Regex:")[-1].strip()
        if not cleaned_regex.startswith("^"):
            cleaned_regex = f"^{cleaned_regex}"
        if not cleaned_regex.endswith("$"):
            cleaned_regex = f"{cleaned_regex}$"

        # Validate regex syntax
        re.compile(cleaned_regex)
        return cleaned_regex

    except Exception as e:
        return enhanced_rule_based_regex(text)


def enhanced_rule_based_regex(text: str) -> str:
    """Improved rule-based converter with common patterns"""
    patterns = {
        r"\b\d+\s*characters\b": lambda m: f"^.{{{m.group(0).split()[0]}}}$",
        r"\bdd/mm/yyyy\b": r"^\d{2}/\d{2}/\d{4}$",
        r"\bmm/dd/yyyy\b": r"^\d{2}/\d{2}/\d{4}$",
        r"\brequired\b": r"^.+$",
        r"\boptional\b": r"^.*$",
        r"\bemail\b": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        r"\bphone number\b": r"^\+?[0-9\s-]{7,}$",
        r"\bzip code\b": r"^\d{5}(?:-\d{4})?$",
    }

    text_lower = text.lower()
    for pattern, handler in patterns.items():
        match = re.search(pattern, text_lower)
        if match:
            return handler(match) if callable(handler) else handler

    # Fallback to simple rules
    if "date" in text_lower:
        return r"^\d{4}-\d{2}-\d{2}$"
    if "number" in text_lower:
        return r"^\d+$"
    if "alphanumeric" in text_lower:
        return r"^[A-Za-z0-9]+$"

    return r"^.*$"  # Default match-all pattern


@app.get("/download/{filename}")
async def download_csv(filename: str):
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=filename)
    raise HTTPException(404, "File not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)