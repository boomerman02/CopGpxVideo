import streamlit as st
import gpxpy
import gpxpy.gpx
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import cv2

# Función para parsear el archivo GPX y extraer las coordenadas
def parse_gpx(file):
    gpx = gpxpy.parse(file)
    latitudes = []
    longitudes = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                latitudes.append(point.latitude)
                longitudes.append(point.longitude)
    return latitudes, longitudes

# Función para visualizar la ruta en un mapa
def plot_route(latitudes, longitudes, map_type='roadmap'):
    plt.figure(figsize=(10, 6))
    plt.plot(longitudes, latitudes, marker='o')
    plt.title('Visualización de la Ruta')
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')
    plt.grid(True)
    
    if map_type == 'satellite':
        plt.style.use('dark_background')
    
    plt.savefig('route.png')
    st.image('route.png', caption='Visualización de la Ruta')

# Función para crear una animación de una flecha siguiendo la ruta
def create_animation(latitudes, longitudes):
    # Crear un lienzo en blanco para los fotogramas de la animación
    height, width = 600, 800
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Cargar la imagen de la flecha
    arrow_img = Image.open('arrow.png').resize((50, 50))
    
    # Crear fotogramas para la animación
    frames = []
    for i in range(len(latitudes)):
        canvas.fill(255)  # Rellenar el lienzo con fondo blanco
        x = int((longitudes[i] - min(longitudes)) / (max(longitudes) - min(longitudes)) * width)
        y = int((latitudes[i] - min(latitudes)) / (max(latitudes) - min(latitudes)) * height)
        
        frame = Image.fromarray(canvas)
        frame.paste(arrow_img, (x, y), arrow_img)
        frames.append(frame)
    
    # Guardar la animación como GIF
    frames.save('route_animation.gif', save_all=True, append_images=frames[1:], duration=100, loop=0)
    st.image('route_animation.gif', caption='Animación de la Ruta')

# Función para generar un video de una flecha siguiendo la ruta
def generate_video(latitudes, longitudes):
    # Crear un lienzo en blanco para los fotogramas del video
    height, width = 600, 800
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Cargar la imagen de la flecha
    arrow_img = cv2.imread('arrow.png')
    
    # Definir el escritor de video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter('route_video.mp4', fourcc, 20.0, (width, height))
    
    # Generar fotogramas para el video
    for i in range(len(latitudes)):
        canvas.fill(255)  # Rellenar el lienzo con fondo blanco
        x = int((longitudes[i] - min(longitudes)) / (max(longitudes) - min(longitudes)) * width)
        y = int((latitudes[i] - min(latitudes)) / (max(latitudes) - min(latitudes)) * height)
        
        canvas[y:y+arrow_img.shape, x:x+arrow_img.shape] = arrow_img
        
        video_writer.write(canvas)
    
    video_writer.release()
    st.video('route_video.mp4')

# Diseño de la aplicación Streamlit
st.title("Visualización y Animación de Rutas GPX")

# Cargador de archivos para el archivo GPX
gpx_file = st.file_uploader("Subir archivo GPX", type=["gpx"])

if gpx_file:
    latitudes, longitudes = parse_gpx(gpx_file)
    
    # Opción para ver la ruta en un mapa
    if st.button("Ver Ruta"):
        map_type = st.selectbox("Seleccionar Tipo de Mapa", ["roadmap", "satellite"])
        plot_route(latitudes, longitudes, map_type)
    
    # Opción para crear una animación de una flecha siguiendo la ruta
    if st.button("Crear Animación"):
        create_animation(latitudes, longitudes)
    
    # Opción para generar un video de una flecha siguiendo la ruta
    if st.button("Generar Video"):
        generate_video(latitudes, longitudes)
