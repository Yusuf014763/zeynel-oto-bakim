import streamlit as st
import pandas as pd
from datetime import datetime

# Senin Google Sheets tablonun linki
SHEET_URL = "https://docs.google.com/spreadsheets/d/1FiSSkuSlJNGn1xV5TKbM79ffAnA3cyGgK08ZycTgNyU/export?format=csv"

@st.cache_data
def get_data():
    return pd.read_csv(SHEET_URL)

st.title("🚗 Zeynel Oto Bakım Takip")
st.write("Aracınızın bakım durumunu öğrenmek için plakanızı girin.")

# Kullanıcı girişi
plaka_input = st.text_input("Plakanızı girin (Örn: 01 ABC 123)").upper().replace(" ", "")

if st.button("Sorgula"):
    df = get_data()
    
    # Veritabanındaki plakaları temizleyip karşılaştırıyoruz
    df['Plaka_Temiz'] = df['Plaka'].astype(str).str.replace(" ", "").str.upper()
    car = df[df['Plaka_Temiz'] == plaka_input]
    
    if not car.empty:
        # Bilgileri al
        giris_km = int(car.iloc[0]['Giris_KM'])
        
        st.success(f"✅ Araç bulundu: {car.iloc[0]['Plaka']}")
        
        # Kullanıcıdan güncel KM'yi al
        simdiki_km = st.number_input("Aracınızın şu anki kilometresini girin:", min_value=giris_km)
        
        if st.button("Bakım Durumunu Gör"):
            # Bakım hesaplama (10.000 KM periyot)
            hedef_km = giris_km + 10000
            kalan_km = hedef_km - simdiki_km
            
            # Sonuçları göster
            if kalan_km > 0:
                st.info(f"📅 Bakımınıza kalan mesafe: {kalan_km} KM")
            else:
                st.error(f"⚠️ Bakım sürenizi {abs(kalan_km)} KM geçtiniz! Lütfen Zeynel Oto'ya uğrayın.")
    else:
        st.error("❌ Plaka bulunamadı! Lütfen plakanızı kontrol edin veya dükkanla iletişime geçin.")
