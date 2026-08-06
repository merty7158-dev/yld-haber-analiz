import streamlit as st
from collections import Counter
import re

st.set_page_config(layout="wide") 

# --- YAN MENÜ (SIDEBAR) AYARLARI ---
st.sidebar.title("⚙️ Ayarlar")
okuma_hizi = st.sidebar.slider("Spiker Okuma Hızı (Kelime/Dk)", min_value=100, max_value=180, value=130, step=10)
st.sidebar.caption("Standart okuma hızı 130 kelime/dakikadır. Metnin coşkusuna veya spikerin tarzına göre değiştirebilirsiniz.")

# --- ANA EKRAN ---
st.title("YLD Haber - Gelişmiş Editör Masası")
st.write("Metin analizi, özetleme, ton ölçümü, hashtag üretimi ve prompter formatı tek ekranda.")

kullanici_metni = st.text_area("Haber metnini veya senaryoyu buraya yapıştırın:", height=200)

if st.button("Haber Metnini İşle"):
    if kullanici_metni:
        # 1. TEMEL HESAPLAMALAR
        kelimeler = kullanici_metni.split()
        kelime_sayisi = len(kelimeler)
        okuma_suresi = kelime_sayisi / okuma_hizi
        
        # 2. VERİ TEMİZLEME VE ANAHTAR KELİMELER
        temiz_metin = re.sub(r'[^\w\s]', '', kullanici_metni).lower()
        tum_kelimeler = temiz_metin.split()
        stop_words = ["ve", "veya", "ile", "için", "bir", "bu", "da", "de", "gibi", "çok", "en", "daha", "kadar", "olan", "olarak", "ise", "göre", "sonra", "önce"]
        anlamli_kelimeler = [k for k in tum_kelimeler if k not in stop_words and len(k) > 2]
        en_sik_kelimeler = Counter(anlamli_kelimeler).most_common(5)
        anahtar_kelime_listesi = [kelime[0] for kelime in en_sik_kelimeler]
        
        # 3. ÖZETLEME VE NEFES KONTROLÜ (CÜMLE ANALİZİ)
        cumleler = [c.strip() for c in re.split(r'[.!?]', kullanici_metni) if len(c.strip()) > 10]
        
        cumle_skorlari = {}
        uzun_cumleler = [] # Nefes kontrolü için riskli cümleler listesi
        
        for cumle in cumleler:
            # Özet için skorlama
            skor = sum(1 for kelime in anahtar_kelime_listesi if kelime in cumle.lower())
            cumle_skorlari[cumle] = skor
            
            # Nefes kontrolü: Cümle 20 kelimeden uzunsa listeye ekle
            if len(cumle.split()) > 20:
                uzun_cumleler.append(cumle)
            
        en_iyi_cumleler = sorted(cumle_skorlari, key=cumle_skorlari.get, reverse=True)[:2]
        
        # 4. DUYGU VE TON ANALİZİ
        olumlu_havuz = ["başarı", "müjde", "harika", "yeni", "gelişim", "artış", "çözüm", "destek", "olumlu", "devrim", "kazanç", "keşif"]
        olumsuz_havuz = ["kriz", "kaza", "sorun", "düşüş", "uyarı", "tehlike", "ölüm", "zarar", "olumsuz", "iptal", "felaket", "skandal"]
        
        olumlu_skor = sum(1 for k in anlamli_kelimeler if k in olumlu_havuz)
        olumsuz_skor = sum(1 for k in anlamli_kelimeler if k in olumsuz_havuz)
        
        ton_durumu = "⚖️ Tarafsız (Bilgi Odaklı)"
        if olumlu_skor > olumsuz_skor:
            ton_durumu = "🟢 Olumlu (Müjdeli/Başarı)"
        elif olumsuz_skor > olumlu_skor:
            ton_durumu = "🔴 Olumsuz (Kriz/Uyarı)"

        # --- EKRANA YAZDIRMA (ARAYÜZ) ---
        st.success("Tüm Analizler Başarıyla Tamamlandı!")
        
        # Üst Panel: Temel Metrikler (3 Sütun)
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Toplam Kelime", value=kelime_sayisi)
        col2.metric(label="Tahmini Seslendirme", value=f"{round(okuma_suresi, 2)} Dk")
        col3.metric(label="Haberin Tonu", value=ton_durumu)
        
        st.divider()
        
        # Orta Panel: İki Sütunlu Yapı (Sol: Editör Masası, Sağ: Sosyal Medya)
        sol_sutun, sag_sutun = st.columns([2, 1])
        
        with sol_sutun:
            st.subheader("📝 Otomatik Haber Özeti")
            if len(en_iyi_cumleler) > 0:
                st.info(" ... ".join(en_iyi_cumleler) + ".")
            
            # NEFES KONTROLÜ UYARISI
            if len(uzun_cumleler) > 0:
                st.warning(f"⚠️ Spiker Uyarısı: Metinde {len(uzun_cumleler)} adet çok uzun cümle var. Spiker nefes almakta zorlanabilir veya ritmi kaçırabilir.")
                with st.expander("Uzun Cümleleri Göster (Bölmeniz Tavsiye Edilir)"):
                    for uc in uzun_cumleler:
                        st.write(f"- {uc}")
            else:
                st.success("✅ Cümle uzunlukları spiker okuması için ideal seviyede.")
        
        with sag_sutun:
            st.subheader("🎯 Anahtar Kelimeler")
            for k, s in en_sik_kelimeler:
                st.write(f"- **{k.capitalize()}** ({s} kez)")
                
            st.subheader("#️⃣ Sosyal Medya Etiketleri")
            st.caption("Kopyalayıp Instagram/YouTube açıklamasına yapıştırın.")
            hashtags = " ".join([f"#{k}" for k in anahtar_kelime_listesi])
            st.code(hashtags, language="text")
            
        st.divider()
        
        # Alt Panel: Prompter
        st.subheader("📺 Prompter Formatı")
        st.code(kullanici_metni.upper(), language="text")
        
    else:
        st.warning("Lütfen analiz etmek için bir metin girin.")
