import pdfplumber

def extract_text_pdf(file):
    text=""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            sentence=page.extract_text()

            if sentence:
                text=text+sentence+"\n"
    return text
