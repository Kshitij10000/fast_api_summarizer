# clean_pdf.py 

import re
import PyPDF2

def clean_pdf_text(text):
    # remove comments
    text = re.sub(r'#.*', '', text)
    
    # remove blank lines
    text = re.sub(r'^\s*$', '', text, flags=re.MULTILINE)

    # remove undefined placeholders (e.g., 'nums', 'target', specific variable assignments)
    text = re.sub(r'nums\s*=\s*\[.*?\]', '', text)
    text = re.sub(r'target\s*=\s*\d+', '', text)
    text = re.sub(r'l1\s*=\s*\[.*?\]', '', text)
    text = re.sub(r'l2\s*=\s*\[.*?\]', '', text)

    # replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)

    # remove leading/trailing whitespace
    text = text.strip()

    return text


# def extract_plan_string(cleaned_text):
#   # Your logic to extract a structured plan string from cleaned_text for conversion to JSON
#   # This example just returns the entire cleaned text
#     return cleaned_text


def process_pdf_file(filepath):
    try:
       
        with open(filepath, 'rb') as file:
            # read the binary data
            pdf_binary_data = file.read()
            # create a PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)

            # extract text from all pages
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()  
    except FileNotFoundError:
        return "Error: File not found."
    except PyPDF2.errors.PdfReadError:
        return "Error: Could not read or decode the PDF file."
    
    cleaned_text = clean_pdf_text(pdf_text)
    # plan_string = extract_plan_string(cleaned_text)
    
    return cleaned_text

# # Example usage:
# filepath = r"C:\Users\kshit\Downloads\Earning Call Transcript - Dr Lal Pathlabs.pdf"
# plan = process_pdf_file(filepath)
# print(plan)