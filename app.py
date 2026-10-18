import streamlit as st
import numpy as np
from scipy.io import wavfile
import os
import uuid
import subprocess
import imageio_ffmpeg

st.set_page_config(page_title="Conversor 8D Profesional", page_icon="🎧", layout="centered")

st.title("🎧 Conversor de Audio 8D Profesional")
st.write("Sube tu canción en cualquier formato (**MP3, WAV, M4A, FLAC, OGG**) y transfórmala con efecto espacial 3D, reverberación y paneo envolvente.")

# Obtener la ruta ejecutable de FFmpeg interno
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# --- Configuración de Parámetros Espaciales (Barra Lateral) ---
st.sidebar.header("⚙️ Personalización del Efecto 8D")
rotation_speed = st.sidebar.slider("Velocidad de rotación (Hz)", min_value=0.02, max_value=0.20, value=0.07, step=0.01)
reverb_level = st.sidebar.slider("Intensidad de Reverberación", min_value=0.0, max_value=0.8, value=0.4, step=0.05)

# Cargar archivo multimedia (Acepta MP3, WAV, M4A, FLAC, OGG)
uploaded_file = st.file_uploader(
    "Elige tu archivo de audio:", 
    type=["mp3", "wav", "m4a", "flac", "ogg"]
)

if uploaded_file is not None:
    st.success(f"¡Archivo '{uploaded_file.name}' seleccionado con éxito!")
    
    if st.button("🚀 Procesar y Convertir a 8D"):
        with st.spinner("Decodificando audio y aplicando efectos espaciales 8D... Por favor espera."):
            
            unique_id = str(uuid.uuid4())[:8]
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            temp_input_path = f"input_{unique_id}{ext}"
            temp_wav_path = f"converted_{unique_id}.wav"
            output_filename = "cancion_8d.wav"
            
            # 1. Guardar el archivo subido por el usuario
            with open(temp_input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # 2. Convertir el archivo de entrada a WAV estéreo a 44100Hz usando FFmpeg interno
                cmd = [
                    ffmpeg_exe, "-y", "-i", temp_input_path,
                    "-ac", "2", "-ar", "44100", temp_wav_path
                ]
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                
                # 3. Leer el WAV estandarizado
                sample_rate, data = wavfile.read(temp_wav_path)
                
                audio_data = data.astype(np.float32)
                num_samples = audio_data.shape[0]
                
                # --- ALGORITMO DSP 8D (Versión 3.0) ---
                
                # Reverberación
                delay_samples = int(sample_rate * 0.05)
                reverb_data = np.zeros_like(audio_data)
                if num_samples > delay_samples:
                    reverb_data[delay_samples:] = audio_data[:-delay_samples] * reverb_level
                audio_con_reverb = audio_data * (1 - reverb_level * 0.5) + reverb_data * (reverb_level * 0.75)
                
                # Paneo Circular
                time = np.arange(num_samples) / sample_rate
                theta = 2 * np.pi * rotation_speed * time
                gain_left = 0.5 * (1 + np.sin(theta))
                gain_right = 0.5 * (1 + np.cos(theta))
                
                left_channel = audio_con_reverb[:, 0] * gain_left
                right_channel = audio_con_reverb[:, 1] * gain_right
                
                # Efecto Haas
                haas_delay = int(sample_rate * 0.002)
                final_left = np.copy(left_channel)
                final_right = np.copy(right_channel)
                if num_samples > haas_delay:
                    final_left[haas_delay:] += right_channel[:-haas_delay] * 0.15
                    final_right[haas_delay:] += left_channel[:-haas_delay] * 0.15
                
                processed_data = np.stack((final_left, final_right), axis=-1)
                
                # Normalización (Evitar distorsión)
                max_val = np.max(np.abs(processed_data))
                if max_val > 0:
                    processed_data = (processed_data / max_val) * 32767
                processed_data = processed_data.astype(np.int16)
                
                # 4. Guardar archivo final
                wavfile.write(output_filename, sample_rate, processed_data)
                st.success("¡Proceso completado con éxito! 🎉")
                
                # Reproductor en línea y botón de descarga
                st.audio(output_filename)
                
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="📥 Descargar Canción 8D (.wav)",
                        data=file,
                        file_name="cancion_8d.wav",
                        mime="audio/wav"
                    )

            except Exception as e:
                st.error(f"Error durante el procesamiento del audio: {e}")
            
            finally:
                # Limpieza de archivos temporales de trabajo
                for p in [temp_input_path, temp_wav_path]:
                    if os.path.exists(p):
                        try:
                            os.remove(p)
                        except Exception:
                            pass