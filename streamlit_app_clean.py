import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time
import random

# SDG logoları ve renkleri
SDG3_LOGO = "https://sdgs.un.org/sites/default/files/goals/Goal-03.png"
SDG11_LOGO = "https://sdgs.un.org/sites/default/files/goals/Goal-11.png"
PRIMARY_COLOR = "#1e3a8a"

# HTML Templates (ayrı değişkenler olarak)
MAIN_HEADER_HTML = """
    <div style='text-align:center; margin:20px 0;'>
        <span style='font-size:60px; margin-bottom:10px; display:block;'>🌍🌱🏙️</span>
        <h1 style='color:#1e3a8a; font-size:3.2rem; font-weight:700; margin-bottom:10px;'>UDEP - AirSense</h1>
        <div style='background:rgba(255,255,255,0.8); border-radius:12px; padding:12px 24px; margin:15px auto; width:fit-content; box-shadow:0 4px 12px rgba(0,0,0,0.1);'>
            <h2 style='color:#1e3a8a; font-size:1.6rem; font-weight:600; margin:0;'>SDG 3: Sağlıklı Bireyler & SDG 11: Sürdürülebilir Şehirler</h2>
        </div>
    </div>
"""

REGIONAL_HEADER_HTML = """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; padding: 25px; margin: 30px 0; 
                box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);'>
        <h2 style='color: white; text-align: center; font-size: 2.5rem; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-bottom: 20px;'>
            🗺️ Bölgesel Hava Kalitesi Keşfi 🔍
        </h2>
        <p style='color: rgba(255,255,255,0.9); text-align: center; font-size: 1.2rem; margin: 0;'>
            📍 İlinizi ve ilçenizi seçerek bölgesel hava kalitesi verilerini keşfedin!
        </p>
    </div>
"""

USER_LOGIN_HTML = """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 25px; padding: 30px; margin: 40px 0; 
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
                border: 3px solid rgba(255,255,255,0.2);'>
        <h2 style='color: white; text-align: center; font-size: 2.8rem; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-bottom: 25px;'>
            👤 Kullanıcı Merkezi 🎯
        </h2>
        <p style='color: rgba(255,255,255,0.9); text-align: center; font-size: 1.3rem; margin-bottom: 30px;'>
            🔒 Giriş yapın ve favori şehirlerinizi kaydedin!
        </p>
    </div>
"""

SUGGESTION_HEADER_HTML = """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 25px; padding: 30px; margin: 40px 0; 
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
                border: 3px solid rgba(255,255,255,0.2);'>
        <h2 style='color: white; text-align: center; font-size: 2.8rem; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-bottom: 25px;'>
            🤖 Akıllı Öneri Merkezi 💡
        </h2>
        <p style='color: rgba(255,255,255,0.9); text-align: center; font-size: 1.3rem; margin-bottom: 30px;'>
            🧠 AI destekli kişiselleştirilmiş öneriler alın!
        </p>
    </div>
"""

REMINDER_HEADER_HTML = """
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 25px; padding: 30px; margin: 40px 0; 
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
                border: 3px solid rgba(255,255,255,0.2);'>
        <h2 style='color: white; text-align: center; font-size: 2.8rem; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3); margin-bottom: 25px;'>
            ⏰ Akıllı Hatırlatıcı Merkezi 🔔
        </h2>
        <p style='color: rgba(255,255,255,0.9); text-align: center; font-size: 1.3rem; margin-bottom: 30px;'>
            📅 Kişiselleştirilmiş hatırlatıcılar oluşturun ve yönetin!
        </p>
    </div>
"""

FOOTER_HTML = """
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
        .footer-shade {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 40px;
        }
        .footer {
            background: rgba(255,255,255,0.75);
            border-radius: 18px;
            padding: 18px 32px;
            text-align:center;
            color:#1e3a8a;
            font-size:2.2rem;
            font-weight:700;
            letter-spacing:1px;
            box-shadow: 0 4px 24px rgba(30,58,138,0.18);
            width: fit-content;
        }
    </style>
    <div class='footer-shade'>
        <div class='footer'>
            🚀 UDEP - Samsung Innovation Program |<br>SDG 3 & SDG 11 🌱
        </div>
    </div>
"""

# Arayüz ayarları
st.set_page_config(page_title="UDEP - AirSense", page_icon="🌍", layout="centered")

# Logo ve ana başlık - ortalanmış
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=200)
    
st.markdown(MAIN_HEADER_HTML, unsafe_allow_html=True)

# Fonksiyonlar
def box_choice(text, bg_url, link="#", overlay="rgba(30,58,138,0.55)", text_opacity=0.95, width=260, height=140):
    box_html = f"""
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
    """
    st.markdown(box_html, unsafe_allow_html=True)

def info_box(text, bg_url, overlay="rgba(30,58,138,0.55)", text_opacity=0.95, width=260):
    info_html = f"""
    <div style="
      border-radius:12px; padding:20px; width:{width}px; margin:12px auto;
      display:flex; align-items:center; justify-content:center;
      text-align:center; font:700 20px 'Arimo',sans-serif; color:#fff;
      background-image: linear-gradient({overlay},{overlay}), url('{bg_url}');
      background-size: cover; background-position: center;
      text-shadow: 2px 2px 6px rgba(0,0,0,.7);
    ">
      <span style="opacity:{text_opacity}">{text}</span>
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)

def alert_box(text, overlay="rgba(30,58,138,0.55)", text_opacity=0.95, width=300):
    alert_html = f"""
    <div style="
      border-radius:12px; padding:20px; width:{width}px; margin:12px auto;
      display:flex; align-items:center; justify-content:center;
      text-align:center; font:700 18px 'Arimo',sans-serif; color:#fff;
      background: {overlay};
      text-shadow: 2px 2px 6px rgba(0,0,0,.7);
    ">
      <span style="opacity:{text_opacity}">{text}</span>
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)

# Ana kartlar
st.markdown('<div style="background:rgba(255,255,255,0.7); border-radius:12px; padding:8px 24px; margin:10px auto; width:fit-content;"><h3 style="color:#1e3a8a; margin:0; text-align:center;">📊 Canlı Hava Kalitesi Verisi</h3></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    info_box("Sıcaklık: 23°C", "https://images.unsplash.com/photo-1504608524841-42fe6f032b4b", overlay="rgba(255, 140, 0, 0.7)")
with col2:
    info_box("Nem: %65", "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0", overlay="rgba(30, 144, 255, 0.7)")
with col3:
    info_box("Rüzgar: 12 km/h", "https://images.unsplash.com/photo-1506905925346-21bda4d32df4", overlay="rgba(34, 139, 34, 0.7)")

col1, col2, col3 = st.columns(3)
with col1:
    info_box("PM2.5: 45 µg/m³", "https://images.unsplash.com/photo-1581833971358-2c8b550f87b3", overlay="rgba(255, 69, 0, 0.7)")
with col2:
    info_box("PM10: 60 µg/m³", "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05", overlay="rgba(220, 20, 60, 0.7)")
with col3:
    info_box("Ozon: 120 µg/m³", "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", overlay="rgba(75, 0, 130, 0.7)")

# Veri giriş formu
st.markdown('<div style="background:rgba(255,255,255,0.7); border-radius:12px; padding:8px 24px; margin:30px auto 10px; width:fit-content;"><h3 style="color:#1e3a8a; margin:0; text-align:center;">📝 Veri Giriş Merkezi</h3></div>', unsafe_allow_html=True)

# Varsayılan değerler
temp, humidity, pm25, pm10, no2, so2, co, industrial = 25.0, 60.0, 35.0, 50.0, 40.0, 30.0, 1.2, 5.0

col1, col2 = st.columns(2)
with col1:
    temp = st.number_input("Sıcaklık (°C)", value=temp, key="input_temp")
    humidity = st.number_input("Nem (%)", value=humidity, key="input_humidity")
    pm25 = st.number_input("PM2.5 (µg/m³)", value=pm25, key="input_pm25")
    pm10 = st.number_input("PM10 (µg/m³)", value=pm10, key="input_pm10")
    no2 = st.number_input("NO2 (µg/m³)", value=no2, key="input_no2")

with col2:
    so2 = st.number_input("SO2 (µg/m³)", value=so2, key="input_so2")
    co = st.number_input("CO (µg/m³)", value=co, key="input_co")
    industrial = st.number_input("Sanayi Uzaklığı (km)", value=industrial, key="input_industrial")

st.markdown("---")
st.subheader("Tahmin Aracı")

# Tahmin aracı
with st.container():
    with open("dataset/logreg_model.pkl", "rb") as f:
        model = pickle.load(f)
    features = np.array([[temp, humidity, pm25, pm10, no2, so2, co, industrial]])
    if st.button("Tahmin Et"):
        prediction = model.predict(features)
        air_quality_map = {0: "Hazardous", 1: "Poor", 2: "Moderate", 3: "Good"}
        result = air_quality_map.get(int(prediction[0]), "Unknown")
        st.markdown(f"<h2 style='text-align:center;color:{PRIMARY_COLOR};'>Tahmin: {result}</h2>", unsafe_allow_html=True)
        if result == "Hazardous":
            alert_box("⚠️ Sağlığınız için dışarı çıkmayın.", overlay="rgb(255,0,0)")
        elif result == "Poor":
            alert_box("🚨 Sağlığınız için dışarıda bulunmaktan kaçının.", overlay="rgb(255, 165, 0)")
        elif result == "Moderate":
            alert_box("✅ Dışarı çıkmanızda herhangi bir problem yok.", overlay="rgb(255, 255, 0, 1.0)")
        else:
            alert_box("✅ Hava kalitesi çok iyi, dışarı çıkabilirsiniz.", overlay="rgb(0, 128, 0)")

# Bölgesel sistem
st.markdown(REGIONAL_HEADER_HTML, unsafe_allow_html=True)

# Türkiye şehirleri (kısaltılmış liste)
turkey_cities = {
    "İstanbul": ["Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler"],
    "Ankara": ["Akyurt", "Altındağ", "Ayaş", "Bala", "Beypazarı", "Çamlıdere"],
    "İzmir": ["Aliağa", "Balçova", "Bayındır", "Bayraklı", "Bergama", "Beydağ"],
    "Bursa": ["Büyükorhan", "Gemlik", "Gürsu", "Harmancık", "İnegöl", "İznik"],
    "Antalya": ["Akseki", "Aksu", "Alanya", "Demre", "Döşemealtı", "Elmalı"]
}

col1, col2 = st.columns(2)
with col1:
    selected_city = st.selectbox("🏙️ İl Seçiniz", options=["İl Seçiniz..."] + list(turkey_cities.keys()))
with col2:
    if selected_city and selected_city != "İl Seçiniz...":
        selected_district = st.selectbox("🏘️ İlçe Seçiniz", options=["İlçe Seçiniz..."] + turkey_cities[selected_city])
    else:
        st.selectbox("🏘️ İlçe Seçiniz", options=["Önce İl Seçiniz..."], disabled=True)

# Kullanıcı sistemi
st.markdown(USER_LOGIN_HTML, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    username = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adınızı girin...")
    password = st.text_input("🔒 Şifre", type="password", placeholder="Şifrenizi girin...")
    if st.button("🚀 Giriş Yap"):
        st.success("✅ Başarıyla giriş yapıldı!")
        st.balloons()

with col2:
    favorite_city = st.selectbox("⭐ Favori şehir ekle", options=["Şehir seçin..."] + list(turkey_cities.keys()))
    if st.button("⭐ Favorime Ekle"):
        if favorite_city and favorite_city != "Şehir seçin...":
            st.success(f"✅ {favorite_city} favorilere eklendi!")
        else:
            st.warning("⚠️ Lütfen şehir seçin!")

# Uyarı sistemi
alert_system_html = """
    <div style='background: linear-gradient(45deg, #FF9A9E 0%, #FECFEF 50%, #FECFEF 100%); 
                border-radius: 25px; padding: 30px; margin: 30px 0;
                box-shadow: 0 12px 30px rgba(255, 154, 158, 0.4);'>
        <h3 style='color: #333; text-align: center; font-size: 2.2rem; margin-bottom: 25px;'>
            🔔 Akıllı Uyarı Sistemi 📱
        </h3>
    </div>
"""
st.markdown(alert_system_html, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    email_check = st.checkbox("📧 Email Uyarıları")
with col2:
    sms_check = st.checkbox("📱 SMS Bildirimleri")
with col3:
    push_check = st.checkbox("🔔 Push Bildirimleri")

# Öneri sistemi
st.markdown(SUGGESTION_HEADER_HTML, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🏃‍♂️ Aktivite Önerisi Al"):
        suggestions = ["🏠 İç mekan yogası yapabilirsiniz", "🚶‍♂️ Kısa mesafe yürüyüş uygun", "🏋️‍♂️ Spor salonunda antrenman"]
        suggestion = random.choice(suggestions)
        st.success(f"💡 **Öneri:** {suggestion}")

with col2:
    if st.button("🏥 Sağlık Önerisi Al"):
        health_tips = ["😷 N95 maske kullanımı önerilir", "💧 Bol su tüketin", "🌿 İç mekan bitkilerini artırın"]
        tip = random.choice(health_tips)
        st.info(f"⚕️ **Sağlık Tavsiyesi:** {tip}")

with col3:
    if st.button("🌱 Çevre Önerisi Al"):
        env_tips = ["🚗 Toplu taşıma kullanın", "🌳 Ağaç dikme etkinliklerine katılın", "♻️ Geri dönüşüm yapın"]
        env_tip = random.choice(env_tips)
        st.success(f"🌍 **Çevre Tavsiyesi:** {env_tip}")

# Hatırlatıcı sistemi
st.markdown(REMINDER_HEADER_HTML, unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    reminder_text = st.text_input("📝 Hatırlatıcı Metni", placeholder="Hatırlatıcı mesajınızı yazın...")
    reminder_time = st.time_input("⏰ Hatırlatıcı Saati")
with col2:
    reminder_frequency = st.selectbox("🔄 Tekrar Sıklığı", ["Bir kez", "Günlük", "Haftalık", "Aylık"])
    reminder_priority = st.selectbox("🚨 Öncelik Seviyesi", ["Düşük", "Orta", "Yüksek", "Kritik"])

if st.button("⚡ HATIRLATİCİ OLUŞTUR ⚡"):
    if reminder_text:
        st.success(f"✅ Hatırlatıcı '{reminder_text}' başarıyla oluşturuldu!")
        st.balloons()
    else:
        st.warning("⚠️ Lütfen hatırlatıcı mesajı yazın!")

# Footer
st.markdown(FOOTER_HTML, unsafe_allow_html=True)
