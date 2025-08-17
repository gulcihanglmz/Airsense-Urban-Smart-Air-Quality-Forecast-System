import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

# SDG logoları ve renkleri
SDG3_LOGO = "https://sdgs.un.org/sites/default/files/goals/Goal-03.png"
SDG11_LOGO = "https://sdgs.un.org/sites/default/files/goals/Goal-11.png"
PRIMARY_COLOR = "#1e3a8a"

# Arayüz ayarları
st.set_page_config(page_title="UDEP - AirSense", page_icon="🌍", layout="centered")
st.markdown(f"""
    <div style='text-align:center; margin-top:30px;'>
        <span style='font-size:70px;'>🌍🌱🏙️</span>
        <h1 style='color:{PRIMARY_COLOR}; margin-bottom:0; font-size:3.2rem;'>UDEP - AirSense</h1>
        <h2 style='color:#1e3a8a; margin-top:0; font-size:2.1rem;'>SDG 3: Sağlıklı Bireyler & SDG 11: Sürdürülebilir Şehirler</h2>
    </div>
""", unsafe_allow_html=True)

# Giriş ekranı (introscreen.py'den)
def box_choice(text, bg_url, link="#", overlay="rgba(30,58,138,0.55)", text_opacity=0.95, width=260, height=140):
    st.markdown(f"""
    <a href="{link}" target="_self">
      <div style="
        border-radius:12px; padding:20px; width:{width}px; height:{height}px; 
        margin:12px auto; display:flex; align-items:center; justify-content:center;
        text-align:center; font:700 26px 'Arimo',sans-serif; color:#fff;
        background-image: linear-gradient({overlay},{overlay}), url('{bg_url}');
        background-size: cover; background-position: center;
        text-shadow: 2px 2px 6px rgba(0,0,0,.7);
      ">
        <span style="opacity:{text_opacity}">{text}</span>
      </div>
    </a>
    """, unsafe_allow_html=True)

# Modern veri kartı (code.py'den)
def info_box(text, bg_url, overlay="rgba(30,58,138,0.55)", text_opacity=0.95, width=260):
    st.markdown(f"""
    <div style="
      border-radius:12px; padding:20px; width:{width}px; margin:12px auto;
      text-align:center; font:700 26px 'Arimo',sans-serif; color:#fff;
      background-image: linear-gradient({overlay},{overlay}), url('{bg_url}');
      background-size: cover; background-position: center;
      text-shadow: 2px 2px 6px rgba(0,0,0,.7);
    ">
      <span style="opacity:{text_opacity}">{text}</span>
    </div>
    """, unsafe_allow_html=True)

def alert_box(text, overlay="rgb(30,58,138)", text_opacity=0.95, width=260):
    st.markdown(f"""
    <div style="
      border-radius:12px; padding:15px; width:{width}px; margin:12px auto;
      text-align:center; font:600 20px 'Arimo',sans-serif; color:#fff;
      background: {overlay};
      text-shadow: 1px 1px 4px rgb(0,0,0);
    ">
      <span style="opacity:{text_opacity}">{text}</span>
    </div>
    """, unsafe_allow_html=True)

# Canlı veri akışı simülasyonu
st.markdown("<h2 style='text-align:center; font-size:2rem; color:#1e3a8a; margin-bottom:18px;'>Canlı Hava Kalitesi Verisi</h2>", unsafe_allow_html=True)
data_file = "dataset/processed_air_quality_filled.csv"
latest_data = pd.read_csv(data_file)

# Son satırı "canlı veri" gibi göster
latest_row = latest_data.iloc[-1]

# Özellik kartları (fotoğraftaki gibi)
pm25_status = "Hazardous" if latest_row['pm2_5'] > 75 else "Poor" if latest_row['pm2_5'] > 50 else "Moderate" if latest_row['pm2_5'] > 25 else "Good"

# Doğru sütun isimleriyle kartlar
info_box(f"🌡️ Sıcaklık: {latest_row['temperature_2m']:.1f} °C", "https://media.istockphoto.com/id/1007768414/photo/blue-sky-with-bright-sun-and-clouds.jpg?s=612x612&w=0&k=20&c=MGd2-v42lNF7Ie6TtsYoKnohdCfOPFSPQt5XOz4uOy4=")
info_box(f"🏭 Endüstriyel alana uzaklık: {latest_row['Proximity_to_Industrial_Areas']:.1f} km", "https://www.appliedcontrol.com/website/media/Shared/Industries/Refining%20and%20Upgrading/Gas%20Plant/GasPlant_T-M.jpg")
info_box(f"🏙️ Nüfus yoğunluğu: {latest_row['Population_Density']:.1f} %", "https://t4.ftcdn.net/jpg/03/25/09/21/360_F_325092112_4fAOmPGij72b0Z6AyayIyw9A4Yrc82K3.jpg")

pm25_status = "Hazardous" if latest_row['pm2_5'] > 75 else "Poor" if latest_row['pm2_5'] > 50 else "Moderate" if latest_row['pm2_5'] > 25 else "Good"

if pm25_status == "Hazardous":
    info_box(f"😷 PM2.5: Hazardous", "https://images.wsj.net/im-843566?width=700&height=466")
    alert_box(f"⚠️ Sağlığınız için dışarı çıkmayın.", overlay="rgb(255,0,0)")
elif pm25_status == "Poor":
    info_box(f"🤧 PM2.5: Poor", "https://media.istockphoto.com/id/472067517/photo/denver-colorado-vehicle-tail-pipe-auto-exhaust-at-busy-intersection.jpg?s=612x612&w=0&k=20&c=DgWbm9SsuXk6FxpoFtkqzuvm06vtss9u-2fzxy9Xmp4=")
    alert_box(f"🚨 Sağlığınız için dışarıda bulunmaktan kaçının.", overlay="rgb(255, 165, 0)")
elif pm25_status == "Moderate":
    info_box(f"👌 PM2.5: Moderate", "https://www.airdri.com/wp-content/uploads/2023/08/clean-air-blog-pic.jpg")
    alert_box(f"✅ Dışarı çıkmanızda herhangi bir problem yok.", overlay="rgb(255, 255, 0, 1.0)")
else:
    info_box(f"😌 PM2.5: Good", "https://plus.unsplash.com/premium_photo-1675177698286-8c3edc5de261?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y2xlYW4lMjBhaXJ8ZW58MHx8MHx8fDA%3D")
    alert_box(f"✅ Hava kalitesi çok iyi, dışarı çıkabilirsiniz.", overlay="rgb(0, 128, 0)")

st.markdown("---")
st.subheader("Tahmin Aracı")

# Kullanıcıdan veri al
col1, col2 = st.columns(2)
with col1:
    temp = st.number_input("Sıcaklık (°C)", value=float(latest_row['temperature_2m']))
    humidity = st.number_input("Nem (%)", value=float(latest_row['relative_humidity_2m']))
    pm25 = st.number_input("PM2.5 (µg/m³)", value=float(latest_row['pm2_5']))
    pm10 = st.number_input("PM10 (µg/m³)", value=float(latest_row['pm10']))
    no2 = st.number_input("NO2 (µg/m³)", value=float(latest_row['nitrogen_dioxide']))
with col2:
    so2 = st.number_input("SO2 (µg/m³)", value=float(latest_row['sulphur_dioxide']))
    co = st.number_input("CO (µg/m³)", value=float(latest_row['carbon_monoxide']))
    industrial = st.number_input("Sanayi Uzaklığı (km)", value=float(latest_row['Proximity_to_Industrial_Areas']))

# Modeli yükle
with open("dataset/logreg_model.pkl", "rb") as f:
    model = pickle.load(f)

# Özellikleri uygun sırada birleştir
features = np.array([[temp, humidity, pm25, pm10, no2, so2, co, industrial]])

# Tahmin
if st.button("Tahmin Et"):
    # Modelin eğitildiği scaler ile ölçekleme yapılmalı (örnek: StandardScaler ile)
    # Burada demo amaçlı direkt tahmin
    prediction = model.predict(features)
    air_quality_map = {0: "Hazardous", 1: "Poor", 2: "Moderate", 3: "Good"}
    result = air_quality_map.get(int(prediction[0]), "Unknown")
    st.markdown(f"<h2 style='text-align:center;color:{PRIMARY_COLOR};'>Tahmin: {result}</h2>", unsafe_allow_html=True)
    if result == "Hazardous":
        alert_box(f"⚠️ Sağlığınız için dışarı çıkmayın.", overlay="rgb(255,0,0)")
    elif result == "Poor":
        alert_box(f"🚨 Sağlığınız için dışarıda bulunmaktan kaçının.", overlay="rgb(255, 165, 0)")
    elif result == "Moderate":
        alert_box(f"✅ Dışarı çıkmanızda herhangi bir problem yok.", overlay="rgb(255, 255, 0, 1.0)")
    else:
        alert_box(f"✅ Hava kalitesi çok iyi, dışarı çıkabilirsiniz.", overlay="rgb(0, 128, 0)")



# Etkileyici footer ve gradient arka plan
st.markdown("""
    <style>
        body, .stApp {
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80');
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
        }
        .stApp {
            opacity: 0.98;
        }
        .footer {
            text-align:center;
            color:#1e3a8a;
            font-size:2.2rem;
            font-weight:700;
            margin-top:40px;
            letter-spacing:1px;
        }
    </style>
    <div class='footer'>
        🚀 UDEP - Samsung Innovation Program | SDG 3 & SDG 11 🌱
    </div>
""", unsafe_allow_html=True)
