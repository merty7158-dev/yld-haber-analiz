import streamlit as st
import whisper
import tempfile
import os
from moviepy.editor import VideoFileClip

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(
    page_title="Medya Deşifre ve Metin Ayıklama Aracı", 
    page_icon="🎙️", 
    layout="wide"
)

# --- YAPAY ZEKA MODELİNİ YÜKLEME ---
# Performans için model belleğe alınır (cache)
@st.cache_resource
def load_whisper_model():
    # "base" modeli hızlıdır. Daha yüksek kesinlik için "small" veya "medium" yazılabilir.
    return whisper.load_model("base") 

model = load_whisper_model()

# --- ARAYÜZ TASARIMI ---
st.title("🎙️ Medya Deşifre Aracı")
st.markdown("""
Bu araç sayesinde video veya ses dosyalarındaki konuşmaları yüksek doğrulukla metne dökebilirsiniz. 
Özellikle **röportaj deşifreleri, haber bültenleri ve içerik altyazıları** hazırlamak için optimize edilmiştir.
""")
st.divider()

# --- DOSYA YÜKLEME ALANI ---
uploaded_file = st.file_uploader("İşlenecek Medya Dosyasını Yükleyin (MP4, MP3, WAV)", type=["mp4", "mp3", "wav"])

if uploaded_file is not None:
    # Dosya uzantısını tespit et
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    # Geçici dosya oluştur (İşlem bitince silinecek)
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
        
    audio_path = tmp_file_path
    
    with st.spinner('Medya analiz ediliyor...'):
        # Eğer yüklenen dosya video ise (MP4), önce sesi dışarı aktar
        if file_extension == "mp4":
            st.info("🎥 Video algılandı. Ses dosyası videodan ayrıştırılıyor...")
            try:
                video = VideoFileClip(tmp_file_path)
                audio_path = tmp_file_path.replace(".mp4", ".wav")
                video.audio.write_audiofile(audio_path, logger=None)
                video.close()
            except Exception as e:
                st.error(f"Sesi ayırırken bir hata oluştu: {e}")
                
        # Yapay zeka ile deşifre işlemi
        st.info("🧠 Konuşmalar metne dökülüyor, lütfen bekleyin (dosya boyutuna göre sürebilir)...")
        try:
            # Dili Türkçe olarak zorlamak başarı oranını artırır
            result = model.transcribe(audio_path, language="tr")
            extracted_text = result["text"]
            
            st.success("✅ Metin başarıyla ayıklandı!")
            
            # Sonucu göster
            st.text_area("Deşifre Edilen Metin", value=extracted_text, height=300)
            
            # İndirme butonu
            st.download_button(
                label="📝 Metni Belge Olarak İndir (.txt)",
                data=extracted_text,
                file_name="desifre_edilmis_metin.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Metin ayıklama sırasında bir hata oluştu: {e}")
            
    # --- TEMİZLİK ---
    # Sunucuda yer kaplamaması için geçici dosyaları sil
    try:
        os.remove(tmp_file_path)
        if file_extension == "mp4" and os.path.exists(audio_path):
            os.remove(audio_path)
    except:
        pass
