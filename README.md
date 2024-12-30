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
Use code with caution.
Markdown
Response Body (JSON):

{
  "company_name": "Patym",
  "financial_performance": "...",
  "market_dynamics": "...",
  "expansion_plans": "...",
  "environmental_risks": "...",
  "regulatory_or_policy_changes": "..."
}
Use code with caution.
Json
2. PDF-based Summary:

Method: POST

Endpoint: /earnings_transcript_summary_from_pdf/

Request Body (Multipart Form Data):

company_name (String): Name of the company.

pdf_file (File): The PDF file to upload.

Response Body (JSON): Same as Text-based Summary response.

Technical Details
Framework: FastAPI

Hosting: AWS EC2

Key Libraries: fastapi, PyPDF2, google-cloud-aiplatform, vertexai, python-dotenv

Source Code: https://github.com/Kshitij10000/fast_api_summarizer.git

Installation & Setup
Clone the repository:

git clone https://github.com/Kshitij10000/fast_api_summarizer.git
Use code with caution.
Bash
Create a virtual environment:

python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
Use code with caution.
Bash
Install dependencies:

pip install -r requirements.txt
Use code with caution.
Bash
Set up environment variables: Create a .env file and add your Google API key:

GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
Use code with caution.
Run the server:

uvicorn main:app --host 0.0.0.0 --port 8000
Use code with caution.
Bash
Known Issues
JSON Input Errors: Ensure valid JSON input.

Token Limits: Transcripts exceeding 20,000 tokens are not processed.

PDF Issues: Non-text PDFs (e.g., scanned documents) may have text extraction issues.

Contributing
Contributions are welcome! Please see the CONTRIBUTING.md file (if you have one, otherwise explain how to contribute).

License
Specify your license here, e.g., MIT (Add a LICENSE file to your repo).

Key changes and improvements:

* **Clearer Structure:**  Improved headings and organization for easier readability.
* **Concise Language:**  More direct and to-the-point explanations.
* **Emphasis on API Usage:** Highlighted how to use the API with clear request and response examples.
* **Multipart Form Data:** Clarified that PDF upload uses multipart form data, not JSON.
* **GitHub Integration:**  Added a direct link to the repository.
* **Installation and Setup Instructions:** Made them more explicit and beginner-friendly.
* **Contributing and License Sections:** Added placeholders for these important sections to encourage community involvement and clarify licensing.


This improved README is more suitable for a GitHub repository and provides better guidance to users and potential contributors. Remember to replace placeholders like `"YOUR_GOOGLE_API_KEY"` and add actual `CONTRIBUTING.md` and `LICENSE` files to your project.
