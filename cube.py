import streamlit as st
import numpy as np
import pyvista as pv
from pyvista import themes
import io
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader


st.set_page_config(page_title="3D-knipvel", page_icon=":scissors:", layout="wide")
st.title("3D-knipvel")

# Slider voor de grootte van de vierkanten in cm
size_cm = st.slider("Grootte van de vierkanten (cm)", 1, 10, 5, 1)

# Maak een PyVista-blok
square = pv.Box([0, size_cm, 0, size_cm, 0, size_cm])

# Maak een PyVista-offscreen-renderer
plotter = pv.Plotter(off_screen=True)
plotter.set_background("white")
plotter.add_mesh(square, color="blue")

# Render het beeld en sla het op als een afbeelding
image = plotter.screenshot()
img = Image.fromarray(image)

# Sla de afbeelding op als een PDF
pdf_output = PdfFileWriter()
pdf_bytes = io.BytesIO()
img.save(pdf_bytes, format='PDF')
pdf_output.addPage(PdfFileReader(io.BytesIO(pdf_bytes.getvalue())).getPage(0))
pdf_data = pdf_output.getBytes()

# Download de PDF
b64 = base64.b64encode(pdf_data).decode()
href = f'<a href="data:application/pdf;base64,{b64}" download="3d_knipvel.pdf">Download de 3D-knipvel als PDF</a>'
st.markdown(href, unsafe_allow_html=True)

# Laat het beeld van de 3D-knipvel zien
st.image(image, use_column_width=True)
