import streamlit as st
from gemini import gemini, analyze_function, gemini_general
from ocr import ocr
from highlight import highlight_text_in_image
import PyPDF2

st.title("Legal AI Assistant")

uploaded_file = st.file_uploader(
    "Choose an image or PDF...", type=["png", "jpg", "jpeg", "pdf"]
)

if uploaded_file is not None:
    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    elif uploaded_file.type == "application/pdf":
        pass

    st.success("File successfully uploaded!")

    # perform OCR
    text = ocr(uploaded_file)
    
    while True:
        try:
            output = gemini(text, analyze_function)
            break
        except:
            pass

    st.write(output)

    if uploaded_file.type in ["image/png", "image/jpeg", "image/jpg"]:
        highlighted_image = highlight_text_in_image(uploaded_file, output["list"])
        st.image(highlighted_image, caption="Analyzed Image", use_column_width=True)

    summary = gemini_general(
        "Give a simple understandable summary in one paragraph: " + text
    )
    st.subheader("Summary")
    st.write(summary)

    st.subheader("Have a question? Ask me anything!")
    question = st.text_input("Question")
    if st.button("Ask"):
        answer = gemini_general(
            "Answer the question preciesly from the given context, question is: "
            + question
            + "Context: "
            + text
        )
        st.info(answer)
    else:
        st.write("Ask me anything!")
