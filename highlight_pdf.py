import fitz  # PyMuPDF
import re
import os
import tempfile

def normalize_text(text):
    """Normalize text by converting to lowercase and removing extra spaces."""
    return re.sub(r'\s+', ' ', text.lower().strip())

def merge_bounding_boxes(bounding_boxes):
    """Merge multiple bounding boxes into a single bounding box."""
    x0 = min(box.x0 for box in bounding_boxes)
    y0 = min(box.y0 for box in bounding_boxes)
    x1 = max(box.x1 for box in bounding_boxes)
    y1 = max(box.y1 for box in bounding_boxes)
    return fitz.Rect(x0, y0, x1, y1)

def highlight_text_in_pdf(pdf_file, text_list, padding=5):
    """
    Highlight specific phrases in the PDF with one box per entry.
    Returns the path to the highlighted PDF.
    """
    # Create a temporary file for the highlighted PDF
    temp_dir = tempfile.mkdtemp()
    output_path = os.path.join(temp_dir, "highlighted_output.pdf")
    
    # Save uploaded file to temporary location
    temp_input = os.path.join(temp_dir, "input.pdf")
    with open(temp_input, "wb") as f:
        f.write(pdf_file.getvalue())

    # Open the PDF
    pdf_document = fitz.open(temp_input)
    words_highlighted = 0

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)

        # Iterate over the input phrases to find matches
        for input_text in text_list:
            normalized_input = normalize_text(input_text)

            # Search for occurrences of the phrase on the page
            instances = page.search_for(input_text)

            if instances:
                # Group all bounding boxes into a single one for the entire entry
                combined_rect = merge_bounding_boxes(instances)

                # Apply padding to the combined rectangle
                combined_rect.x0 -= padding
                combined_rect.y0 -= padding
                combined_rect.x1 += padding
                combined_rect.y1 += padding

                # Draw a red rectangle around the combined box
                page.draw_rect(combined_rect, color=(1, 0, 0), width=2)
                words_highlighted += 1

    # Save the modified PDF
    pdf_document.save(output_path)
    pdf_document.close()

    return output_path