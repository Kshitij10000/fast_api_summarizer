# summarizer_service.py

import google.generativeai as genai
from typing import Dict
import os
from dotenv import load_dotenv
import json
import logging  
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY not found.")

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def summarize_text(company_name: str, transcript_text: str) -> Dict[str, str]:
    prompt = f"""
        You are provided with an earnings call transcript of a company.
        The company name is {company_name}.
        Ensure that the transcript pertains to {company_name}.
        Your task is to summarize the transcript into specific categories. 
        The summary MUST be returned in valid JSON format ONLY. 
        Do not provide any introductory text, code fences, or explanations outside the JSON. 
        Do not enclose the JSON within markdown code blocks.
        Strictly adhere to the following JSON structure, ensuring all fields are present, even if empty. 
        If a category is not mentioned in the transcript, use an empty string "" for its value.

        Transcript:
        {transcript_text}

        Output Format:
        {{
        "company_name": "{company_name}",
        "financial_performance": "SHORT SUMMARY OF FINANCIAL PERFORMANCE HERE",
        "market_dynamics": "SHORT SUMMARY OF MARKET DYNAMICS HERE",
        "expansion_plans": "SHORT SUMMARY OF EXPANSION PLANS HERE",
        "environmental_risks": "SHORT SUMMARY OF ENVIRONMENTAL RISKS HERE",
        "regulatory_or_policy_changes": "SHORT SUMMARY OF REGULATORY OR POLICY CHANGES HERE"
        }}
        """

    try:
        response = model.generate_content(prompt)
        summary_text = response.text.strip()
        logger.info(f"AI Model Response: {summary_text}")  # Log the response

        # Step 1: Remove code fences if present
        summary_text = remove_code_fences(summary_text)

        # Step 2: Extract JSON using regex if necessary
        summary_json_str = extract_json(summary_text)

        # Step 3: Parse the JSON string into a dictionary
        summary = json.loads(summary_json_str)
        return summary

    except json.JSONDecodeError as jde:
        logger.error(f"JSON Decode Error: {jde}")
        logger.error(f"Response Text: {response.text}")  # Log the problematic response
        raise ValueError("Failed to parse AI model response into JSON.")
    except Exception as e:
        logger.error(f"Error during summarization: {e}")
        raise ValueError("Summary could not be generated due to an error.")

def remove_code_fences(text: str) -> str:
    """
    Removes code fences (e.g., ```json and ```) from the response text.
    """
    # Pattern to match ```json or ``` followed by any characters and ending with ```
    code_fence_pattern = re.compile(r'^```json\s*|\s*```$', re.MULTILINE)
    cleaned_text = code_fence_pattern.sub('', text).strip()
    if cleaned_text != text:
        logger.info("Code fences removed from the AI response.")
    return cleaned_text

def extract_json(text: str) -> str:
    """
    Extracts JSON object from the text using regex.
    """
    # This regex matches the first JSON object in the text
    json_pattern = re.compile(r'\{.*\}', re.DOTALL)
    match = json_pattern.search(text)
    if match:
        json_str = match.group()
        logger.info("JSON object extracted from the AI response.")
        return json_str
    else:
        logger.error("No JSON object found in the AI response.")
        raise ValueError("Failed to extract JSON from AI model response.")




# summarize_text = summarize_text("realiance", "Reliance Industries reported a revenue growth of 10% this quarter, driven by increased demand in the telecommunications sector. The company plans to expand its 5G infrastructure across major cities. However, environmental concerns have been raised regarding its new refinery project. Additionally, recent regulatory changes may impact its operational costs.")
# print(summarize_text)