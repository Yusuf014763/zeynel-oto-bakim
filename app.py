import streamlit as st
import pandas as pd

SHEET_URL = "https://docs.google.com/spreadsheets/d/1FiSSkuSlJNGn1xV5TKbM79ffAnA3cyGgK08ZycTgNyU/export?format=csv"

@st.cache_data(ttl=60)
def get_data():
    return pd.read_csv(SHEET_URL)

st.title("🚗 Zeynel Oto Bakım Takip")

df = get_data()
df.columns = df.columns.str.strip() 
df['Plaka_Temiz'] = df['Plaka'].astype(str).str.replace(" ", "").str.upper()

plaka_input = st.text_input("Plakanızı girin (Örn: 01ZS047)").upper().replace(" ", "")

if plaka_input:
    car = df[df['Plaka_Temiz'] == plaka_input]
    
    if not car.empty:
        st.success(f"✅ Araç bulundu: {car.iloc[0]['Plaka']}")
        
        # Tarih ve KM verilerini al
        giris_km = int(car.iloc[0]['Giris_KM'])
        giris_tarihi = car.iloc[0]['Giris_Tarihi']
        
        # Bilgileri göster
        st.write(f"📅 **Son Bakım Tarihi:** {giris_tarihi}")
        st.write(f"📊 **Servis Giriş KM:** {giris_km} KM")
        
        simdiki_km = st.number_input("Aracınızın şu anki kilometresini girin:", min_value=giris_km, value=giris_km)
        
        if st.button("Bakım Durumunu Gör"):
            hedef_km = giris_km + 10000
            kalan_km = hedef_km - simdiki_km
            
            if kalan_km > 0:
                st.info(f"✅ Bakımınıza kalan mesafe: {kalan_km} KM")
            else:
                st.error(f"⚠️ Bakım sürenizi {abs(kalan_km)} KM geçtiniz! Lütfen Zeynel Oto'ya uğrayın.")
                st.warning("📞 Randevu için: 0XXX XXX XX XX") # Buraya kendi numaranı yazabilirsin
    else:
        st.error("❌ Plaka bulunamadı!")
