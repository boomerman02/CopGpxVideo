
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2
import xml.etree.ElementTree as ET

# Función para parsear el archivo GPX y extraer las coordenadas
def parse_gpx(file):
    tree = ET.parse(file)
    root = tree.getroot()
    latitudes = []
    longitudes = []
    for trk in root.findall('{http://www.topografix.com/GPX/1/1}trk'):
        for trkseg in trk.findall('{http://www.topografix.com/GPX/1/1}trkseg'):
            for trkpt in trkseg.findall('{http://www.topografix.com/GPX/1/1}trkpt'):
                latitudes.append(float(trkpt.get('lat')))
                longitudes.append(float(trkpt.get('lon')))
    return latitudes, longitudes

# Función para visualizar la ruta como una imagen fija
def plot_route(latitudes, longitudes):
    plt.figure(figsize=(10, 6))
    plt.plot(longitudes, latitudes, marker='o')
    plt.title('Visualización de la Ruta')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.grid(True)
    plt.savefig('route.png')
    st.image('route.png', caption='Visualización de la Ruta')

# Función para generar el video de la moto recorriendo la ruta
def generate_video(latitudes, longitudes, motorcycle_image_path):
    # Cargar la imagen de la moto
    motorcycle_img = cv2.imread(motorcycle_image_path)
    
    # Crear un lienzo en blanco para los fotogramas del video
    height, width = 600, 800
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Definir el escritor de video
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter('route_video.avi', fourcc, 20.0, (width, height))
    
    # Generar fotogramas para el video
    for i in range(len(latitudes)):
        canvas.fill(255)  # Rellenar el lienzo con fondo blanco
        x = int((longitudes[i] - min(longitudes)) / (max(longitudes) - min(longitudes)) * width)
        y = int((latitudes[i] - min(latitudes)) / (max(latitudes) - min(latitudes)) * height)
        canvas[y:y+motorcycle_img.shape[0], x:x+motorcycle_img.shape[1]] = motorcycle_img
        
        video_writer.write(canvas)
    
    video_writer.release()
    st.video('route_video.avi')

# Diseño de la aplicación Streamlit
st.title("Visualización de Ruta GPX y Generación de Video")

# Cargador de archivos para el archivo GPX
gpx_file = st.file_uploader("Subir archivo GPX", type=["gpx"])

# Cargador de archivos para la imagen de la moto
motorcycle_image_file = st.file_uploader("Subir imagen de la moto", type=["png", "jpg", "jpeg"])

if gpx_file and motorcycle_image_file:
    latitudes, longitudes = parse_gpx(gpx_file)
    
    # Opción para visualizar la ruta como una imagen fija
    if st.button("Visualizar Ruta"):
        plot_route(latitudes, longitudes)
    
    # Opción para generar el video de la moto recorriendo la ruta
    if st.button("Generar Video"):
        generate_video(latitudes, longitudes, motorcycle_image_file.name)
