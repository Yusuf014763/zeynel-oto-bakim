import streamlit as st
import pandas as pd
from datetime import datetime

# Secrets'tan güvenli link çekimi
SHEET_URL = st.secrets["SHEET_URL"]

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
            kalan_km = (giris_km + 10000) - simdiki_km
            kalan_gun = 365 - fark_gun
            
            # Müşteriye durumu net gösteren profesyonel mantık
            if kalan_km > 0 and kalan_gun > 0:
                st.info(f"✅ Aracınızın bakımı için her şey yolunda! **{kalan_km} KM** ve **{kalan_gun} gün** daha süreniz var.")
            
            elif kalan_km <= 0 and kalan_gun > 0:
                st.error("⚠️ Bakım kilometre sınırınız dolmuştur!")
                st.warning(f"• **KM Aşımı:** Limit aşılmış, {abs(kalan_km)} KM fazlanız var.")
                st.info("📍 **Lütfen bakım için Zeynel Oto'ya uğrayın.**")
            
            elif kalan_km > 0 and kalan_gun <= 0:
                st.error("⚠️ Yıllık bakım süreniz dolmuştur!")
                st.warning(f"• **Zaman Aşımı:** Bakım süresi {abs(kalan_gun)} gün önce dolmuş.")
                st.info("📍 **Lütfen bakım için Zeynel Oto'ya uğrayın.**")
            
            else:
                st.error("⚠️ Hem bakım süreniz hem de kilometre sınırınız dolmuştur!")
                st.warning(f"• **KM Aşımı:** {abs(kalan_km)} KM fazlanız var.")
                st.warning(f"• **Zaman Aşımı:** Bakım süresi {abs(kalan_gun)} gün önce dolmuş.")
                st.info("📍 **Lütfen bakım için Zeynel Oto'ya uğrayın.**")
                
    else:
        st.error("❌ Plaka bulunamadı!")
