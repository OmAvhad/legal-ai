import streamlit as st
from gemini import gemini, analyze_function, gemini_general
from ocr import ocr
from highlight import highlight_text_in_image
from highlight_pdf import highlight_text_in_pdf
import PyPDF2
from translation import translate_text, language_titles
import os

st.title("Legal AI Assistant")

uploaded_file = st.file_uploader(
    "Choose an image or PDF...", type=["png", "jpg", "jpeg", "pdf"]
)

if uploaded_file is not None:
    # Display the original file
    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    elif uploaded_file.type == "application/pdf":
        # Display the original PDF
        with st.expander("View Original PDF"):
            pdf_display = PyPDF2.PdfReader(uploaded_file)
            page_count = len(pdf_display.pages)
            st.write(f"Number of pages: {page_count}")
            for i in range(page_count):
                page = pdf_display.pages[i]
                st.write(f"Page {i+1}")
                st.write(page.extract_text())

    st.success("File successfully uploaded!")

    # Perform OCR
    text = ocr(uploaded_file)

    # Call Gemini API
    while True:
        try:
            output = gemini(text, analyze_function)
            break
        except:
            pass

    st.write(output)

    # Extract the highlighted text
    highlighted_text = "\n".join(output.get("list", []))

    # Language Translation for Highlighted Text
    st.subheader("Translate Highlighted Text")
    languages_highlighted = st.multiselect(
        "Select languages to translate the highlighted text", 
        options=list(language_titles.keys()), 
        format_func=lambda x: language_titles[x], 
        key="highlighted_text_languages"
    )

    if st.button("Translate Highlighted Text"):
        translations = translate_text(highlighted_text, languages_highlighted)
        for lang, translated_text in translations.items():
            st.write(f"**{language_titles[lang]} ({lang})**: {translated_text}")

    # Display highlighted content based on file type
    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        highlighted_image = highlight_text_in_image(uploaded_file, output["list"])
        st.image(highlighted_image, caption="Analyzed Image", use_column_width=True)
    elif uploaded_file.type == "application/pdf":
        # Reset file pointer
        uploaded_file.seek(0)
        
        # Generate highlighted PDF
        highlighted_pdf_path = highlight_text_in_pdf(uploaded_file, output["list"])
        
        # Display the highlighted PDF
        with open(highlighted_pdf_path, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            st.download_button(
                label="Download Highlighted PDF",
                data=pdf_bytes,
                file_name="highlighted_document.pdf",
                mime="application/pdf"
            )
        
        # Clean up temporary file
        os.remove(highlighted_pdf_path)

    # Get Summary from Gemini
    summary = gemini_general(
        "Give a simple understandable summary in one paragraph: " + text
    )
    st.subheader("Summary")
    st.write(summary)

    # Language Translation for Summary
    st.subheader("Translate Summary")
    languages_summary = st.multiselect(
        "Select languages to translate the summary", 
        options=list(language_titles.keys()), 
        format_func=lambda x: language_titles[x], 
        key="summary_languages"
    )

    if st.button("Translate Summary"):
        translations = translate_text(summary, languages_summary)
        for lang, translated_text in translations.items():
            st.write(f"**{language_titles[lang]} ({lang})**: {translated_text}")

    # Question-Answer Section
    st.subheader("Have a question? Ask me anything!")
    question = st.text_input("Question")
    
    if st.button("Ask"):
        answer = gemini_general(
            f"Answer the question precisely from the given context. "
            f"Question: {question} Context: {text}"
        )
        st.info(answer)
    else:
        st.write("Ask me anything!")