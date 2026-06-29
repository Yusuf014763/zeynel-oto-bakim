import streamlit as st
import pandas as pd
from datetime import datetime

SHEET_URL = "https://docs.google.com/spreadsheets/d/1FiSSkuSlJNGn1xV5TKbM79ffAnA3cyGgK08ZycTgNyU/export?format=csv"

@st.cache_data(ttl=60)
def get_data():
    return pd.read_csv(SHEET_URL)

st.title("🚗 Zeynel Oto Bakım Takip")

df = get_data()
df.columns = df.columns.str.strip() 
df['Plaka_Temiz'] = df['Plaka'].astype(str).str.replace(" ", "").str.upper()

plaka_input = st.text_input("Plakanızı girin (Örn: 01ABC123)").upper().replace(" ", "")

if plaka_input:
    car = df[df['Plaka_Temiz'] == plaka_input]
    
    if not car.empty:
        st.success(f"✅ Araç bulundu: {car.iloc[0]['Plaka']}")
        
        giris_km = int(car.iloc[0]['Giris_KM'])
        giris_tarihi_str = str(car.iloc[0]['Giris_Tarihi'])
        
        # Tarih hesaplama
        giris_tarihi = datetime.strptime(giris_tarihi_str, "%d.%m.%Y")
        bugun = datetime.now()
        fark_gun = (bugun - giris_tarihi).days
        
        st.write(f"📅 **Son Bakım Tarihi:** {giris_tarihi_str} ({fark_gun} gün önce)")
        st.write(f"📊 **Servis Giriş KM:** {giris_km} KM")
        
        simdiki_km = st.number_input("Aracınızın şu anki kilometresini girin:", min_value=giris_km, value=giris_km)
        
        if st.button("Bakım Durumunu Gör"):
            # KM Hesabı
            kalan_km = (giris_km + 10000) - simdiki_km
            
            # Zaman Hesabı (365 gün sınırı)
            kalan_gun = 365 - fark_gun
            
            # Sonuçları göster
            if kalan_km > 0 and kalan_gun > 0:
                st.info(f"✅ Bakımınıza **{kalan_km} KM** ve **{kalan_gun} gün** var.")
            else:
                st.error("⚠️ Bakım süreniz dolmuş! Lütfen Zeynel Oto'ya uğrayın.")
                if kalan_km <= 0: st.write(f"• KM sınırı geçildi: {abs(kalan_km)} KM fazla.")
                if kalan_gun <= 0: st.write(f"• Yıllık bakım süresi doldu: {abs(kalan_gun)} gün geçti.")
    else:
        st.error("❌ Plaka bulunamadı!")
