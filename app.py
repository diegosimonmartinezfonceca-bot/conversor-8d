import streamlit as st
import numpy as np
from scipy.io import wavfile
import os
import uuid
import subprocess
import imageio_ffmpeg

# Configuración de página con título, ícono y layout
st.set_page_config(
    page_title="Conversor Audio 8D | CEDHU",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para mejorar el diseño visual
st.markdown("""
    <style>
    /* Estilo del fondo principal y tipografía */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        color: #f8fafc;
    }
    
    /* Tarjeta contenedora de la cabecera */
    .header-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        color: #a78bfa;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 8px;
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        line-height: 1.5;
    }

    /* Estilo de la tarjeta institucional del proyecto */
    .info-card {
        background: linear-gradient(135deg, rgba(88, 28, 135, 0.4) 0%, rgba(30, 58, 138, 0.4) 100%);
        border-left: 5px solid #8b5cf6;
        border-radius: 12px;
        padding: 18px 22px;
        margin-top: 15px;
        margin-bottom: 25px;
    }

    .project-title {
        color: #c084fc;
        font-size: 0.95rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .project-desc {
        color: #e2e8f0;
        font-size: 0.9rem;
        line-height: 1.4;
    }

    .author-badge {
        display: inline-block;
        background: #6d28d9;
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-top: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Executable de FFmpeg interno
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# --- BARRA LATERAL (Sidebar) ---
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/headphones.png", width=70)
    st.title("🎛️ Controles DSP 8D")
    st.caption("Ajusta la espacialización acústica para la meditación y estimulación sonora.")
    
    st.markdown("---")
    
    rotation_speed = st.slider(
        "🔄 Velocidad de Rotación (Hz)", 
        min_value=0.02, 
        max_value=0.20, 
        value=0.07, 
        step=0.01,
        help="Controla qué tan rápido gira el audio alrededor de la cabeza."
    )
    
    reverb_level = st.slider(
        "🌌 Intensidad de Reverberación", 
        min_value=0.0, 
        max_value=0.8, 
        value=0.4, 
        step=0.05,
        help="Aumenta la sensación de espacio físico y profundidad tridimensional."
    )
    
    st.markdown("---")
    st.info("💡 **Consejo:** Utiliza auriculares estéreo para percibir correctamente el efecto binaural y binaural 8D.")

# --- CUERPO PRINCIPAL ---

# Cabecera Principal
st.markdown("""
    <div class="header-card">
        <div class="main-title">🎧 Conversor de Audio 8D & Espacialización Sonica</div>
        <div class="sub-title">Herramienta de procesamiento digital de señales (DSP) para la transformación de audio inmersivo con balanceo binaural y profundización espacial.</div>
    </div>
""", unsafe_allow_html=True)

# Sección Informativa del Proyecto e Investigación
st.markdown("""
    <div class="info-card">
        <div class="project-title">🔬 Proyecto de Investigación Institucional</div>
        <div class="project-desc">
            <b>IMPLEMENTACIÓN DE ESTRATEGIAS DE MEDITACIÓN POR MEDIO DE MÚSICA BINAURAL PARA LA REDUCCIÓN DEL ESTRÉS ACADÉMICO ENTRE EDUCANDOS DE UNDÉCIMO GRADO</b>
        </div>
        <div style="margin-top: 8px;">
            <span class="author-badge">Diseñado por: Diego Simon Martinez Fonseca</span>
            <span style="color: #cbd5e1; font-size: 0.85rem; margin-left: 10px;">Centro de Desarrollo Humano (CEDHU)</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Área de carga de archivos
st.subheader("📁 Carga de Archivo de Audio")
uploaded_file = st.file_uploader(
    "Selecciona una pista sonora (MP3, WAV, M4A, FLAC, OGG):", 
    type=["mp3", "wav", "m4a", "flac", "ogg"]
)

if uploaded_file is not None:
    st.success(f"🎵 **Archivo cargado:** {uploaded_file.name}")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        process_btn = st.button("🚀 Procesar Audio a 8D", use_container_width=True)
    
    if process_btn:
        with st.spinner("⚡ Decodificando frecuencias y generando espacio tridimensional 8D..."):
            
            unique_id = str(uuid.uuid4())[:8]
            ext = os.path.splitext(uploaded_file.name)[1].lower()
            temp_input_path = f"input_{unique_id}{ext}"
            temp_wav_path = f"converted_{unique_id}.wav"
            output_filename = "cancion_8d.wav"
            
            # Guardar entrada
            with open(temp_input_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            try:
                # Convertir a WAV estándar
                cmd = [
                    ffmpeg_exe, "-y", "-i", temp_input_path,
                    "-ac", "2", "-ar", "44100", temp_wav_path
                ]
                subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                
                # Leer WAV
                sample_rate, data = wavfile.read(temp_wav_path)
                audio_data = data.astype(np.float32)
                num_samples = audio_data.shape[0]
                
                # --- PROCESAMIENTO DSP 8D ---
                
                # Reverberación de Profundidad
                delay_samples = int(sample_rate * 0.05)
                reverb_data = np.zeros_like(audio_data)
                if num_samples > delay_samples:
                    reverb_data[delay_samples:] = audio_data[:-delay_samples] * reverb_level
                audio_con_reverb = audio_data * (1 - reverb_level * 0.5) + reverb_data * (reverb_level * 0.75)
                
                # Paneo Circular Senoidal
                time = np.arange(num_samples) / sample_rate
                theta = 2 * np.pi * rotation_speed * time
                gain_left = 0.5 * (1 + np.sin(theta))
                gain_right = 0.5 * (1 + np.cos(theta))
                
                left_channel = audio_con_reverb[:, 0] * gain_left
                right_channel = audio_con_reverb[:, 1] * gain_right
                
                # Efecto Haas Psychoacoustics
                haas_delay = int(sample_rate * 0.002)
                final_left = np.copy(left_channel)
                final_right = np.copy(right_channel)
                if num_samples > haas_delay:
                    final_left[haas_delay:] += right_channel[:-haas_delay] * 0.15
                    final_right[haas_delay:] += left_channel[:-haas_delay] * 0.15
                
                processed_data = np.stack((final_left, final_right), axis=-1)
                
                # Normalización Estricta
                max_val = np.max(np.abs(processed_data))
                if max_val > 0:
                    processed_data = (processed_data / max_val) * 32767
                processed_data = processed_data.astype(np.int16)
                
                # Guardar resultado
                wavfile.write(output_filename, sample_rate, processed_data)
                
                st.balloons() # Animación festiva al completar
                st.success("🎉 **¡Transformación 8D Completada con Éxito!**")
                
                # Reproductor y botón de descarga interactivo
                st.subheader("🎧 Resultado Tridimensional")
                st.audio(output_filename)
                
                with open(output_filename, "rb") as file:
                    st.download_button(
                        label="📥 Descargar Pista 8D Procesada (.wav)",
                        data=file,
                        file_name="cancion_8d_meditacion.wav",
                        mime="audio/wav",
                        use_container_width=True
                    )

            except Exception as e:
                st.error(f"❌ Error durante la conversión del audio: {e}")
            
            finally:
                for p in [temp_input_path, temp_wav_path]:
                    if os.path.exists(p):
                        try:
                            os.remove(p)
                        except Exception:
                            pass
