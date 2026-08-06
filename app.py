import streamlit as st

# 1. Arayüzün başlığı ve açıklaması
st.title("YLD Haber - İçerik Analiz Aracı")
st.write("Haber metninizi veya senaryonuzu aşağıya yapıştırın, okuma süresini anında hesaplayalım.")

# 2. Kullanıcıdan veri almak için geniş bir metin kutusu (Input)
kullanici_metni = st.text_area("Metni buraya girin:")

# 3. İşlemi başlatacak aksiyon butonu
if st.button("Analiz Et"):
    
    # Butona basıldığında arka planda çalışacak motorumuz (Bir önceki adımdaki kod)
    if kullanici_metni: # Eğer kutu boş değilse
        kelimeler = kullanici_metni.split()
        kelime_sayisi = len(kelimeler)
        okuma_suresi = kelime_sayisi / 130
        
        # 4. Sonuçları ekranda şık paneller halinde gösterme (Output)
        st.success("Analiz başarıyla tamamlandı!")
        
        # Ekranı iki sütuna bölüp verileri yan yana gösterelim
        col1, col2 = st.columns(2)
        col1.metric(label="Toplam Kelime", value=kelime_sayisi)
        col2.metric(label="Tahmini Seslendirme (Dakika)", value=round(okuma_suresi, 2))
    else:
        st.warning("Lütfen analiz etmek için bir metin girin.")
