# import fitz

from pdfminer.high_level import extract_text



def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
    
if __name__ == "__main__":
    path = "test.pdf"
    text = extract_text_from_pdf(path)
