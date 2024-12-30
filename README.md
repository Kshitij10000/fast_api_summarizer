# Earnings Transcript Summary API

This FastAPI-based service summarizes corporate earnings transcripts into structured JSON categories.  It's hosted on an AWS EC2 instance and leverages Google's Gemini AI model for advanced summarization.

## API URL

`http://50.17.51.41/earnings_transcript_summary/`

## Features

* Summarizes transcripts into categories like financial performance, market dynamics, expansion plans, environmental risks, and regulatory changes.
* Supports both text and PDF input.
* Outputs structured JSON summaries.
* Integrates Google Gemini AI for enhanced summarization.

## Technical Stack

* **Framework:** FastAPI
* **Hosting:** AWS EC2
* **Key Libraries:**
    * `fastapi`
    * `PyPDF2` (PDF text extraction)
    * `google-cloud-aiplatform` (Google AI integration)
    * `vertexai`
    * `python-dotenv` (environment variable management)


## Environment Setup

**Requirements:**

* Python 3.x
* Libraries listed in `requirements.txt`

**Installation Steps:**

1. Clone the repository: `https://github.com/Kshitij10000/fast_api_summarizer.git`
2. Create and activate a virtual environment: `python3 -m venv env` and `source env/bin/activate` (or `env\Scripts\activate` on Windows)
3. Install dependencies: `pip install -r requirements.txt`
4. Configure `.env`:
    * Add your Google API key: `GOOGLE_API_KEY='your_google_api_key'`
5. Start the server: `uvicorn main:app --host 0.0.0.0 --port 8000`


## API Endpoints

**1. Root Endpoint:**

* **Method:** `GET`
* **URL:** `/`
* **Returns:** List of available endpoints and descriptions.

**2. Text-based Summary:**

* **Method:** `POST`
* **URL:** `/earnings_transcript_summary/`
* **Input (JSON):**
```json
{
  "company_name": "Patym",
  "transcript_text": "...Earnings call transcript text here..."
}
content_copy
download
Use code with caution.
Markdown

Response (JSON):

{
  "company_name": "Patym",
  "financial_performance": "...",
  "market_dynamics": "...",
  "expansion_plans": "...",
  "environmental_risks": "...",
  "regulatory_or_policy_changes": "..."
}
content_copy
download
Use code with caution.
Json

3. PDF-based Summary:

Method: POST

URL: /earnings_transcript_summary_from_pdf/

Input:

company_name (String): Name of the company.

pdf_file (File): Uploaded PDF file.

Response (JSON): Same as Text-based Summary response.

Usage Guide (Postman)

Create a POST request.

Set the URL to the appropriate endpoint.

Select "Raw" and "JSON" in the body tab.

Paste the JSON input.

Click "Send".

JSON Input Validation

Ensure proper JSON formatting.

Validate inputs for special characters and malformed data.

Development Details

main.py: FastAPI application and endpoints.

summarization_service.py: Summarization logic using Google AI.

clean_pdf.py: PDF text extraction and cleaning.

.env: Environment variables.

requirements.txt: Project dependencies.

Summarization Workflow

Input validation (Pydantic).

PDF text extraction and cleaning (PyPDF2).

Token count validation (Google AI).

Summarization (Google Gemini).

JSON response.

Known Issues

JSON Input Errors: Ensure valid JSON.

Token Limits: Transcripts over 20,000 tokens are not processed.

PDF Issues: Non-text PDFs may fail text extraction.

content_copy
download
Use code with caution.
