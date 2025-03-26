In order to run the app make sure we have the below libraries in place

Make sure pip3 and python3 installed

1. export HUGGINGFACE_API_KEY=your_api_key_here
2. pip3 install "fitz[pymupdf] pandas fastapi uvicorn requests python-multipart"
3. pip3 install pandas
4. pip3 install fitz
5. pip3 install fastapi
6. pip3 install requests
7. pip3 install ydata_profiling


python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload (command to execute app.py in local)


http://127.0.0.1:8000/docs#/default/upload_pdf_upload_pdf__post   (Swagger URL)


To Execute the GEN AI Data Profiling App
1. Open the genAI.py