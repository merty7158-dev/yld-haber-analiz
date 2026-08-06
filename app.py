import streamlit as st
from collections import Counter
import re

# Sayfayı geniş formatta kullanalım
st.set_page_config(layout="wide") 

st.title("YLD Haber - Gelişmiş Editör Masası")
st.write("Metin analizi, anahtar kelime çıkarımı ve otomatik prompter formatı.")

# Haber metnini almak için daha yüksek bir kutu
kullanici_metni = st.text_area("Haber metnini veya senaryoyu buraya yapıştırın:", height=200)

if st.button("Haber Metnini İşle"):
    
    if kullanici_metni:
        # --- 1. TEMEL HESAPLAMALAR ---
        kelimeler = kullanici_metni.split()
        kelime_sayisi = len(kelimeler)
        okuma_suresi = kelime_sayisi / 130
        
        # --- 2. VERİ TEMİZLEME VE ANAHTAR KELİME ANALİZİ ---
        # Noktalama işaretlerini sil ve tüm harfleri küçült (Veri temizleme adımı)
        temiz_metin = re.sub(r'[^\w\s]', '', kullanici_metni).lower()
        tum_kelimeler = temiz_metin.split()
        
        # Haberde anlam ifade etmeyen bağlaçları (stop words) filtrele
        stop_words = ["ve", "veya", "ile", "için", "bir", "bu", "da", "de", "gibi", "çok", "en", "daha", "kadar", "olan", "olarak"]
        anlamli_kelimeler = [k for k in tum_kelimeler if k not in stop_words and len(k) > 2]
        
        # Haberde en çok vurgulanan 5 kelimeyi bul
        en_sik_kelimeler = Counter(anlamli_kelimeler).most_common(5)
        
        # --- EKRANA YAZDIRMA (ARAYÜZ) ---
        st.success("Metin başarıyla işlendi ve yayına hazır!")
        
        st.subheader("📊 Temel Metrikler")
        col1, col2 = st.columns(2)
        col1.metric(label="Toplam Kelime", value=kelime_sayisi)
        col2.metric(label="Tahmini Seslendirme", value=f"{round(okuma_suresi, 2)} Dakika")
        
        st.subheader("🔍 Haberin Odak Noktası (Sık Geçen Kelimeler)")
        # En sık geçen kelimeleri liste halinde yazdır
        for kelime, sayi in en_sik_kelimeler:
            st.write(f"- **{kelime.capitalize()}**: {sayi} kez vurgulandı")
            
        st.subheader("📺 Prompter Formatı")
        st.caption("Spikerin rahat okuması için büyük harflere çevrildi.")
        # Prompter için metni tamamen büyük harfe çevir
        prompter_metni = kullanici_metni.upper()
        st.info(prompter_metni)
        
    else:
        st.warning("Lütfen analiz etmek için bir metin girin.")

# --- 3. CSV OLARAK İNDİRME BUTONU ---
        st.write("---")
        st.subheader("💾 Raporu İndir")
        
        # İndirilecek veriyi formatlıyoruz (Basit bir CSV yapısı)
        csv_verisi = "Kelime,Frekans\n"
        for kelime, sayi in en_sik_kelimeler:
            csv_verisi += f"{kelime},{sayi}\n"
            
        st.download_button(
            label="Anahtar Kelime Analizini İndir (CSV)",
            data=csv_verisi,
            file_name="yld_haber_analiz.csv",
            mime="text/csv"
        )
