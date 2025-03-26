## WellsNut team 
### Code contributed by: Naresh kumar, Santhosh Kumar, Sonali, Shrikanth Rao and Kiran
# Gen AI-Based Data Profiling System

## Overview
The Gen AI-Based Data Profiling System is a user-friendly application designed to validate, clean, and profile datasets using advanced technologies like Python, regex, and automated data profiling tools. It ensures efficient data management and error handling, providing detailed insights into dataset properties.

## Functional Workflow
### Login & User Authentication
- Users start with a **Login Window** to enter credentials and select a role (Admin/User).
- Upon successful authentication:
  - Admins are redirected to the **Admin Home Screen**.

### Uploading Data & Rules
- Admin can upload:
  - **CSV Data File**: Contains records to be profiled.
  - **Rules File**: Includes regex expressions for validation.
- Uploaded files are stored in a **predefined directory** for processing.

### Applying Rules & Profiling Data
- The system's **genRegex module**:
  - Reads the uploaded data and rules.
  - Applies regex patterns to validate fields and filter invalid data.
- Outputs:
  - **Filtered Dataset**: Saved as `result.csv`.
  - **Data Profile Report**: Generated using `ydata_profiling` and saved as `data_profile_report.html`.

## Technologies Used
- **Python**: Core programming language for system development.
- **Tkinter**: GUI framework for creating the user interface.
- **Pandas**: Used for data processing and manipulation.
- **ydata_profiling**: Enables automated data profiling.
- **Regex (re module)**: Validates and filters dataset fields.

## Error Handling & Validation
- Ensures:
  - Uploaded files are **valid CSV files**.
  - Datasets are **non-empty** before applying rules.
  - Regex patterns are **correctly formatted**.
- Provides **user-friendly error messages** via message boxes.

## Output & Reports
- **Filtered CSV File**: `result.csv` containing the cleaned dataset.
- **Data Profile Report**: `data_profile_report.html` with detailed insights into dataset properties.

## Future Enhancements
- **Role-Based Access Control**: Enhance security by implementing user roles (Admin/User).
- **Graphical Data Insights**: Visualize profiling results for better interpretation.
- **AI-Driven Anomaly Detection**: Detect anomalies and enrich profiling results.
- **Web-Based UI**: Transition from Tkinter to a web-based interface for accessibility and scalability.

## Setup & Installation
1. Install Python (version >= 3.8).
2. Install the required Python libraries:
   ```bash
   pip install pandas tkinter ydata-profiling


