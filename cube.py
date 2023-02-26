import streamlit as st
from PIL import Image
import PyPDF2

def resize_image(image, target_size):
    # Convert cm to inches
    target_size_inches = target_size / 2.54
    # Calculate the new size in pixels
    new_size = tuple(int(x * target_size_inches) for x in image.size)
    # Resize the image
    return image.resize(new_size)

def generate_pdf(uploaded_files, target_size):
    pdf = PyPDF2.PdfFileWriter()
    page = pdf.PageObject.createBlankPage(None, 595, 842)
    x, y = 0, 0

    for file in uploaded_files:
        image = Image.open(file)
        resized_image = resize_image(image, target_size)
        page_left, page_top, page_right, page_bottom = page.mediaBox
        width, height = resized_image.size
        if x + width > page_right:
            y += height
            x = 0
        if y + height > page_bottom:
            pdf.addPage(page)
            page = PyPDF2.pdf.PageObject.createBlankPage(None, 595, 842)
            x, y = 0, 0
        page.mergeTranslatedPage(resized_image.convert("RGB"), x, page_bottom - y - height)
        x += width
    pdf.addPage(page)

    output_filename = "output.pdf"
    with open(output_filename, "wb") as out_file:
        pdf.write(out_file)

    return output_filename

uploaded_files = st.file_uploader("Upload 6 images", accept_multiple_files=True, type=['png', 'jpg'])
target_size = st.slider("Target size in cm", 1, 10, 5)

if st.button("Generate PDF"):
    output_filename = generate_pdf(uploaded_files, target_size)
    pdf = PyPDF2.PdfFileReader(output_filename)
    for i in range(pdf.getNumPages()):
        page = pdf.getPage(i)
        st.image(page, use_column_width=True)
