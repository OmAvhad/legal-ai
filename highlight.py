import cv2
import numpy as np
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Om Avhad\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)
import re
import os


def preprocess_image(image):
    """Convert the image to grayscale, denoise it, and apply thresholding."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray)
    thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return thresh


def normalize_text(text):
    """Normalize text by converting to lowercase and removing extra spaces."""
    return re.sub(r"\s+", " ", text.lower().strip())


def highlight_text_in_image(upload_file, text_list, padding=5):
    """Highlight specific phrases in the image with a red border and padding."""

    try:
        # Load the image with Pillow (PIL)
        pil_image = Image.open(upload_file)

        # Convert the Pillow image to an OpenCV format (NumPy array)
        image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # Check if image was properly decoded
        if image is None:
            raise ValueError("Could not decode image file.")

    except Exception as e:
        raise ValueError(f"Error decoding image: {e}")

    if image is None:
        raise ValueError("The uploaded file could not be read as an image.")

    print(f"Image shape: {image.shape}")

    # Preprocess the image for better OCR results
    preprocessed = preprocess_image(image)

    # Perform OCR with Tesseract
    custom_config = r"--oem 3 --psm 6"
    data = pytesseract.image_to_data(
        preprocessed, output_type=pytesseract.Output.DICT, config=custom_config
    )

    words_highlighted = 0

    # Join all detected words into a normalized full text
    detected_text = " ".join([word for word in data["text"] if word.strip()])
    normalized_full_text = normalize_text(detected_text)
    print(f"Detected Text:\n{normalized_full_text}")

    # Iterate over the input phrases to find exact matches
    for idx, input_text in enumerate(text_list):
        normalized_input = normalize_text(input_text)
        print(f"\nSearching for phrase: '{normalized_input}'")

        if normalized_input in normalized_full_text:
            print(f"Phrase found: '{input_text}'")

            # Find the starting index of the phrase in the detected text
            start_index = normalized_full_text.find(normalized_input)

            # Track the total length of characters scanned
            current_char_index = 0
            found_start = False
            phrase_boxes = []

            # Iterate over each word detected by Tesseract
            for i, word in enumerate(data["text"]):
                if not word.strip():
                    continue  # Skip empty words

                word_length = len(normalize_text(word))

                # Check if the word is part of the matched phrase
                if (
                    current_char_index >= start_index
                    and current_char_index < start_index + len(normalized_input)
                ):
                    x, y, w, h = (
                        data["left"][i],
                        data["top"][i],
                        data["width"][i],
                        data["height"][i],
                    )
                    phrase_boxes.append((x, y, w, h))
                    found_start = True

                current_char_index += word_length + 1  # +1 accounts for spaces

            if found_start:
                # Calculate the padded rectangle coordinates
                x_min = min([box[0] for box in phrase_boxes]) - padding
                y_min = min([box[1] for box in phrase_boxes]) - padding
                x_max = max([box[0] + box[2] for box in phrase_boxes]) + padding
                y_max = max([box[1] + box[3] for box in phrase_boxes]) + padding

                # Ensure the coordinates are within the image boundaries
                x_min = max(0, x_min)
                y_min = max(0, y_min)
                x_max = min(image.shape[1], x_max)
                y_max = min(image.shape[0], y_max)

                # Draw a red rectangle with thickness = 2
                cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
                words_highlighted += 1
                print(f"Highlighted phrase '{input_text}' with border")

    print(f"\nTotal phrases highlighted: {words_highlighted}")

    return image


# # Example usage
# image_path = "image.png"
# text_to_highlight = [
#     # "2. you are eligible for a stipend of inr 35,000 per month during the term which shall be paid subject to completion of the project/ deliverables assigned to you during your intemship to the satisfaction of the company.",
#     "All intellectual property including but not limited to copyrights, design rights, trade marks, patents in or to any literary or artistic works, innovations on processes, methodologies, applications developed by you during the course of your internship will constitute absolute property of the Company and you agree to treat such intellectual property as confidential and proprietary and use such information solely for the benefit of the Company and shall not ay claim on any such intellectual property. All such rights shall be irrevocably assigned to the Company and if required by the Company, you shall enter into and execute an intellectual property\assignment agreement with the Company stating that the ownership of such intellectual property rights\nbelong solely and exclusively to the Company."
# ]

# try:
#     highlighted_image = highlight_text_in_image(
#         image_path, text_to_highlight, padding=10
#     )
#     if highlighted_image is not None:
#         # Save and display the highlighted image
#         cv2.imwrite("highlighted_image.jpg", highlighted_image)
#         cv2.imshow("Highlighted Image", highlighted_image)
#         cv2.waitKey(0)
#         cv2.destroyAllWindows()
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
