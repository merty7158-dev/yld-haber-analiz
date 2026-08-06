import streamlit as st
from collections import Counter
import re

st.set_page_config(layout="wide") 

st.title("YLD Haber - Gelişmiş Editör Masası")
st.write("Metin analizi, otomatik özetleme ve prompter formatı.")

kullanici_metni = st.text_area("Haber metnini veya senaryoyu buraya yapıştırın:", height=200)

if st.button("Haber Metnini İşle"):
    
    if kullanici_metni:
        # --- 1. TEMEL HESAPLAMALAR ---
        kelimeler = kullanici_metni.split()
        kelime_sayisi = len(kelimeler)
        okuma_suresi = kelime_sayisi / 130
        
        # --- 2. VERİ TEMİZLEME VE ANAHTAR KELİME ANALİZİ ---
        temiz_metin = re.sub(r'[^\w\s]', '', kullanici_metni).lower()
        tum_kelimeler = temiz_metin.split()
        
        stop_words = ["ve", "veya", "ile", "için", "bir", "bu", "da", "de", "gibi", "çok", "en", "daha", "kadar", "olan", "olarak", "ise", "göre"]
        anlamli_kelimeler = [k for k in tum_kelimeler if k not in stop_words and len(k) > 2]
        en_sik_kelimeler = Counter(anlamli_kelimeler).most_common(5)
        
        # Sadece kelime isimlerini bir listeye alalım
        anahtar_kelime_listesi = [kelime[0] for kelime in en_sik_kelimeler]

        # --- 3. OTOMATİK ÖZETLEME VE VURGU MOTORU ---
        # Metni noktalara göre cümlelere bölüyoruz
        cumleler = [c.strip() for c in re.split(r'[.!?]', kullanici_metni) if len(c.strip()) > 10]
        
        # Her cümleye anahtar kelime barındırma sayısına göre puan veriyoruz
        cumle_skorlari = {}
        for cumle in cumleler:
            skor = sum(1 for kelime in anahtar_kelime_listesi if kelime in cumle.lower())
            cumle_skorlari[cumle] = skor
            
        # En yüksek puanı alan (en önemli) 2 cümleyi özet olarak seçiyoruz
        en_iyi_cumleler = sorted(cumle_skorlari, key=cumle_skorlari.get, reverse=True)[:2]
        
        
        # --- EKRANA YAZDIRMA (ARAYÜZ) ---
        st.success("Yapay Zeka Destekli Analiz Tamamlandı!")
        
        # Üst Panel: Özet ve Vurgular
        st.subheader("📝 Otomatik Haber Özeti")
        if len(en_iyi_cumleler) > 0:
            ozet_metin = " ... ".join(en_iyi_cumleler) + "."
            st.info(ozet_metin)
        else:
            st.info("Metin özet çıkarmak için çok kısa.")

        st.subheader("🎯 Vurgulanacak Anahtar Kelimeler")
        # Kelimeleri yan yana şık butonlar/etiketler gibi göstermek için
        etiketler = " | ".join([f"🔥 {kelime.capitalize()}" for kelime in anahtar_kelime_listesi])
        st.markdown(f"**{etiketler}**")

        st.divider() # Araya şık bir çizgi çeker

        # Alt Panel: Detaylar
        st.subheader("📊 Temel Metrikler")
        col1, col2 = st.columns(2)
        col1.metric(label="Toplam Kelime", value=kelime_sayisi)
        col2.metric(label="Tahmini Seslendirme", value=f"{round(okuma_suresi, 2)} Dakika")
            
        st.subheader("📺 Prompter Formatı")
        st.caption("Spikerin rahat okuması için büyük harflere çevrildi.")
        st.code(kullanici_metni.upper(), language="text")
        
        # --- CSV İNDİRME BUTONU ---
        st.write("---")
        csv_verisi = "Kelime,Frekans\n"
        for kelime, sayi in en_sik_kelimeler:
            csv_verisi += f"{kelime},{sayi}\n"
            
        st.download_button(
            label="Raporu İndir (CSV)",
            data=csv_verisi,
            file_name="yld_haber_analiz.csv",
            mime="text/csv"
        )
        
    else:
        st.warning("Lütfen analiz etmek için bir metin girin.")
