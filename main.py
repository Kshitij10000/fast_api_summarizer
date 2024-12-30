#main.py

#import all libraries

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel , Field , field_validator
from vertexai.preview import tokenization
import logging
from summarization_service import summarize_text 
from clean_pdf import process_pdf_file
import tempfile
import os
from pydantic import ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Define the model name for tokenization
MODEL_NAME = "gemini-1.5-flash"

#Initialize the tokenizer
try:
    tokenizer = tokenization.get_tokenizer_for_model(MODEL_NAME)
    logger.info(f"Tokenizer initialized for model {MODEL_NAME} successfully")
except Exception as e:
    logger.error(f"Error in initializing tokenizer for model {MODEL_NAME}: {e}")
    raise RuntimeError(f"Tokenizer failed for model {MODEL_NAME}")    


class TranscriptionInput(BaseModel):
    company_name: str = Field(..., example="Reliance Industries")
    transcript_text: str = Field(..., example="YOUR TRANSCRIPT TEXT HERE")

    @field_validator("transcript_text")
    def check_token_limit(cls, v):
        if not v.strip():
            raise ValueError("transcript_text cannot be empty")
        
        # Count tokens 
        try:
            result = tokenizer.count_tokens(v)
            if result.total_tokens > 20000:
                raise ValueError(
                    f"transcript_text exceeds the maximum allowed token limit of 20,000 tokens. "
                    f"Current token count: {result.total_tokens}."
                )
            logger.info(f"Token count for transcript_text: {result.total_tokens}")
        except Exception as e:
            logger.error(f"Error in token count for transcript_text: {e}")
            raise ValueError(f"Error in token count for transcript_text: {e}")
        return v    


class TranscriptionSummary(BaseModel):
    company_name: str
    financial_performance: str
    market_dynamics: str
    expansion_plans: str
    environmental_risks: str
    regulatory_or_policy_changes: str

@app.post("/earnings_transcript_summary/", response_model=TranscriptionSummary)
async def summarize_transcript(input: TranscriptionInput):
    logger.info(f"Received request for summarizing transcript for company: {input.company_name}")
    try:
        summaries = summarize_text(company_name=input.company_name, transcript_text=input.transcript_text)
    except ValueError as ve:
        logger.error(f"Summarization error: {ve}")
        raise HTTPException(status_code=502, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")

    logger.info(f"Transcript summarized successfully for company: {input.company_name}") 
    return summaries  


# New Endpoint: Summarize from PDF
@app.post("/earnings_transcript_summary_from_pdf/", response_model=TranscriptionSummary)
async def summarize_transcript_from_pdf(
    company_name: str = Form(..., example="Reliance Industries"),
    pdf_file: UploadFile = File(...)
):
    logger.info(f"Received request for summarizing PDF transcript for company: {company_name}")
    
    # Validate file type
    if pdf_file.content_type != "application/pdf":
        logger.error("Uploaded file is not a PDF.")
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    
    try:
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp_file_path = tmp.name
            content = await pdf_file.read()
            tmp.write(content)
            logger.info(f"PDF file saved temporarily at {tmp_file_path}")
        
        # Process the PDF to extract and clean text
        cleaned_text = process_pdf_file(tmp_file_path)
        if "Error:" in cleaned_text:
            logger.error(f"PDF processing error: {cleaned_text}")
            raise HTTPException(status_code=400, detail=cleaned_text)
        
        logger.info("PDF text extracted and cleaned successfully.")
        
    except Exception as e:
        logger.error(f"Error processing PDF file: {e}")
        raise HTTPException(status_code=500, detail="Failed to process the uploaded PDF file.")
    finally:
        # Ensure the temporary file is deleted
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
            logger.info(f"Temporary file {tmp_file_path} deleted.")
    
    
    # Create TranscriptionInput instance with validation
    try:
        transcription_input = TranscriptionInput(company_name=company_name, transcript_text=cleaned_text)
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=ve.errors())
    
    # Summarize the transcript
    try:
        summaries = summarize_text(company_name=transcription_input.company_name, transcript_text=transcription_input.transcript_text)
    except ValueError as ve:
        logger.error(f"Summarization error: {ve}")
        raise HTTPException(status_code=502, detail=str(ve))
    except Exception as e:
        logger.error(f"Unexpected error during summarization: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred during summarization.")
    
    logger.info(f"PDF transcript summarized successfully for company: {company_name}")
    return summaries