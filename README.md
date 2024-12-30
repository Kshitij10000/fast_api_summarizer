# Earnings Transcript Summary API

This FastAPI-based service summarizes corporate earnings transcripts into structured JSON categories. It's hosted on an AWS EC2 instance and leverages Google's Gemini AI model for advanced summarization.

## Features

* Summarizes transcripts into categories like:
    * Financial performance
    * Market dynamics
    * Expansion plans
    * Environmental risks
    * Regulatory changes
* Supports both text and PDF input.
* Outputs structured JSON summaries.
* Uses Google Gemini AI for enhanced summarization.

## API Usage

**Base URL:** `http://50.17.51.41/earnings_transcript_summary/`

**1. Text-based Summary:**

* **Method:** `POST`
* **Endpoint:** `/earnings_transcript_summary/`
* **Request Body (JSON):**
```json
{
  "company_name": "Patym",
  "transcript_text": "...Earnings call transcript text here..."
}
```

Response Body (JSON):
```json
{
  "company_name": "Patym",
  "financial_performance": "...",
  "market_dynamics": "...",
  "expansion_plans": "...",
  "environmental_risks": "...",
  "regulatory_or_policy_changes": "..."
}
```
2. PDF-based Summary:

Method: POST

Endpoint: 
```bash
/earnings_transcript_summary_from_pdf/
```

Request Body (Multipart Form Data):
company_name (String): Name of the company.
pdf_file (File): The PDF file to upload.

Response Body (JSON): Same as Text-based Summary response.

Technical Details

```bash
Framework: FastAPI
Hosting: AWS EC2
Key Libraries: fastapi, PyPDF2, google-cloud-aiplatform, vertexai, python-dotenv
```

Source Code: 
```bash
https://github.com/Kshitij10000/fast_api_summarizer.git
```

Installation & Setup

Clone the repository:
git clone https://github.com/Kshitij10000/fast_api_summarizer.git



Create a virtual environment:
```bash
python3 -m venv env 
source env/bin/activate  # On Windows: env\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up environment variables: Create a .env file and add your Google API key:
```bash 
GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
```


Run the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Known Issues
JSON Input Errors: Ensure valid JSON input.
Token Limits: Transcripts exceeding 20,000 tokens are not processed.
PDF Issues: Non-text PDFs (e.g., scanned documents) may have text extraction issues.


