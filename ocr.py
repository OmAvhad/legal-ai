from PIL import Image
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
import fitz
import io

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Om Avhad\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


def ocr(uploaded_file):
    # Check if the file is a PDF
    if uploaded_file.type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # Check if the page contains any text
                    text += page_text + "\n"  # Concatenate text with a newline
                else:
                    print(f"Warning: No text found on page {page.page_number}")
        if text == "":

            uploaded_file.seek(0)  # Reset file pointer to the beginning
            pdf_bytes = uploaded_file.read()

            # Create a PDF document from the bytes
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

            text = ""

            # Loop through the pages and convert them to images
            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)

                # Render page as an image (convert to pixel map)
                pix = page.get_pixmap()

                # Convert pixmap to PIL Image
                image = Image.open(io.BytesIO(pix.tobytes("png")))

                # Perform OCR on the image
                text += pytesseract.image_to_string(image)

            pdf_document.close()

        return text

    # Load the image
    img = Image.open(uploaded_file)

    # Perform OCR
    text = pytesseract.image_to_string(img)

    return text
