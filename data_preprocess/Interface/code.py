
import streamlit as st
import pandas as pd

sicaklik=28.5

User_Dictionary = {
    "First_User": {
        "sicaklik": 28.5,           # °C
        "sanayi_uzaklik": 3.2,      # km
        "nufus_orani": 50,          # oran
        "pm10": 72,
    },

    "Second_User":  {
        "sicaklik": 15.5,           # °C
        "sanayi_uzaklik": 1.2,      # km
        "nufus_orani": 80,          # oran
        "pm10": 10,
    },
    "Third_User": {
        "sicaklik": 30.5,           # °C
        "sanayi_uzaklik": 7.2,      # km
        "nufus_orani": 10,          # oran
        "pm10": 45,
    },
}

st.set_page_config(page_title="Air Sense", page_icon="🌤️")

import streamlit as st


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


# Kullanım
sicaklik = 28.5
mesafe_km = 3.2
nufus_orani = 50
air_quality = "Hazardous"

info_box(f"🌡️ Sıcaklık: {sicaklik:.1f} °C",
         "https://media.istockphoto.com/id/1007768414/photo/blue-sky-with-bright-sun-and-clouds.jpg?s=612x612&w=0&k=20&c=MGd2-v42lNF7Ie6TtsYoKnohdCfOPFSPQt5XOz4uOy4=")

info_box(f"🏭 Endüstriyel alana uzaklık: {mesafe_km:.1f} km",
         "https://www.appliedcontrol.com/website/media/Shared/Industries/Refining%20and%20Upgrading/Gas%20Plant/GasPlant_T-M.jpg")

info_box(f"🌃 Nüfus yoğunluğu: {nufus_orani:.1f} %",
         "https://t4.ftcdn.net/jpg/03/25/09/21/360_F_325092112_4fAOmPGij72b0Z6AyayIyw9A4Yrc82K3.jpg")


#PM oranina gore uyari verecek kisim:

if air_quality == "Hazardous":
    info_box(f"😷 PM2.5: {air_quality} ",
             "https://images.wsj.net/im-843566?width=700&height=466")
    alert_box(f"⚠️ Sagliginiz icin disari cikmayin.",overlay="rgb(255,0,0)")
elif air_quality == "Poor":
    info_box(f"🤧 PM2.5: {air_quality} %",
             "https://media.istockphoto.com/id/472067517/photo/denver-colorado-vehicle-tail-pipe-auto-exhaust-at-busy-intersection.jpg?s=612x612&w=0&k=20&c=DgWbm9SsuXk6FxpoFtkqzuvm06vtss9u-2fzxy9Xmp4=")
    alert_box(f"🚨 Sagliginiz icin disarida bulunmaktan kacinin.",overlay="rgb(255, 165, 0,")
elif air_quality == "Moderate":
    info_box(f"👌 PM2.5: {air_quality} %",
             "https://www.airdri.com/wp-content/uploads/2023/08/clean-air-blog-pic.jpg")
    alert_box(f"✅ Disari cikmanizda herhangi bir problem yaratmamaktadir.",overlay="rgb(255, 255, 0, 1.0)")

else:
    info_box(f"😌 PM2.5: {air_quality} %",
             "https://plus.unsplash.com/premium_photo-1675177698286-8c3edc5de261?fm=jpg&q=60&w=3000&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y2xlYW4lMjBhaXJ8ZW58MHx8MHx8fDA%3D")
    alert_box(f"✅ Hava kalitesi cok iyi, disari cikabilirsiniz.",overlay="rgb(0, 128, 0)")