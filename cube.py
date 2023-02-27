import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from io import BytesIO


st.set_page_config(page_title="3D-knipvel", page_icon=":scissors:", layout="wide")
st.title("3D-knipvel")

# Slider voor de grootte van de vierkanten in cm
size_cm = st.slider("Grootte van de vierkanten (cm)", 1, 10, 5, 1)

# Maak het matplotlib-blok
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
x, y, z = np.array([[0, 0, 0], [0, size_cm, 0], [size_cm, size_cm, 0], [size_cm, 0, 0], [0, 0, 0]]).T
ax.plot3D(x, y, z, 'gray')
ax.plot3D(x+size_cm, y, z, 'gray')
ax.plot3D(x, y+size_cm, z, 'gray')
ax.plot3D(x, y, z+size_cm, 'gray')
ax.plot3D(x, y+size_cm, z+size_cm, 'gray')
ax.plot3D(x+size_cm, y, z+size_cm, 'gray')
ax.plot3D(x+size_cm, y+size_cm, z, 'gray')
ax.plot3D(x+size_cm, y+size_cm, z+size_cm, 'gray')
ax.set_xlabel('X-as (cm)')
ax.set_ylabel('Y-as (cm)')
ax.set_zlabel('Z-as (cm)')

# Maak een PDF-bestand van het matplotlib-blok
pdf_output = PdfFileWriter()
pdf_bytes = BytesIO()
canvas_obj = canvas.Canvas(pdf_bytes)
fig.savefig(pdf_bytes, format='pdf')
canvas_obj.showPage()
canvas_obj.save()
pdf_output.addPage(PdfFileReader(BytesIO(pdf_bytes.getvalue())).getPage(0))
pdf_data = pdf_output.getBytes()

# Download de PDF
def download_file():
    with BytesIO() as data:
        data.write(pdf_data)
        data.seek(0)
        return data.read()

st.download_button(
    label="Download de 3D-knipvel als PDF",
    data=download_file(),
    file_name="PhotoCube.pdf",
    mime="application/pdf"
)

# Laat het beeld van de 3D-knipvel zien
st.pyplot(fig)
