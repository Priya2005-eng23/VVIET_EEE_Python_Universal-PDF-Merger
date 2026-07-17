import streamlit as st
from pypdf import PdfWriter, PdfReader
from PIL import Image
import img2pdf
import tempfile
import os

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Universal PDF & Image Merger",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Universal PDF & Image Merger")
st.write("Merge multiple PDF and image files into one PDF.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_files = st.file_uploader(
    "Choose PDF or Image Files",
    type=["pdf", "jpg", "jpeg", "png", "bmp"],
    accept_multiple_files=True
)

# -------------------------------
# Merge Button
# -------------------------------
if st.button("Merge Files"):

    if not uploaded_files:
        st.warning("Please upload at least one file.")
        st.stop()

    merger = PdfWriter()

    progress = st.progress(0)

    total_files = len(uploaded_files)

    for i, uploaded_file in enumerate(uploaded_files):

        extension = uploaded_file.name.split(".")[-1].lower()

        # ---------------------------
        # PDF Files
        # ---------------------------
        if extension == "pdf":

            reader = PdfReader(uploaded_file)

            for page in reader.pages:
                merger.add_page(page)

        # ---------------------------
        # Image Files
        # ---------------------------
        else:

            image = Image.open(uploaded_file)

            if image.mode != "RGB":
                image = image.convert("RGB")

            temp_img = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg"
            )

            image.save(temp_img.name)

            temp_pdf = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            )

            with open(temp_pdf.name, "wb") as pdf_file:
                pdf_file.write(img2pdf.convert(temp_img.name))

            reader = PdfReader(temp_pdf.name)

            for page in reader.pages:
                merger.add_page(page)

            os.remove(temp_img.name)
            os.remove(temp_pdf.name)

        progress.progress((i + 1) / total_files)

    output_pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    merger.write(output_pdf.name)
    merger.close()

    st.success("Files merged successfully!")

    with open(output_pdf.name, "rb") as pdf:

        st.download_button(
            label="⬇ Download Merged PDF",
            data=pdf,
            file_name="Merged_Document.pdf",
            mime="application/pdf"
        )

st.markdown("---")
st.caption("Developed with ❤️ using Streamlit")
