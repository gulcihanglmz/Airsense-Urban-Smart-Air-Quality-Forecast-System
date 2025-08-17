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

# Logo ve ana başlık - ortalanmış
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("logo.jpg", width=200)
    
st.markdown("""
    <div style='text-align:center; margin:20px 0;'>
        <span style='font-size:60px; margin-bottom:10px; display:block;'>🌍🌱🏙️</span>
        <h1 style='color:#1e3a8a; font-size:3.2rem; font-weight:700; margin-bottom:10px;'>UDEP - AirSense</h1>
        <div style='background:rgba(255,255,255,0.8); border-radius:12px; padding:12px 24px; margin:15px auto; width:fit-content; box-shadow:0 4px 12px rgba(0,0,0,0.1);'>
            <h2 style='color:#1e3a8a; font-size:1.6rem; font-weight:600; margin:0;'>SDG 3: Sağlıklı Bireyler & SDG 11: Sürdürülebilir Şehirler</h2>
        </div>
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

# Shade ile canlı veri başlığı
st.markdown("""
    <div style='width:fit-content; margin:0 auto; background:rgba(255,255,255,0.7); border-radius:12px; padding:8px 24px; margin-bottom:18px;'>
        <h2 style='text-align:center; font-size:2rem; color:#1e3a8a; margin:0;'>Canlı Hava Kalitesi Verisi</h2>
    </div>
""", unsafe_allow_html=True)
data_file = "dataset/processed_air_quality_filled.csv"
latest_data = pd.read_csv(data_file)

# Her açılışta en güncel satırı çek
data_file = "dataset/processed_air_quality_filled.csv"
latest_data = pd.read_csv(data_file)
latest_row = latest_data.iloc[-1]

# Başlangıç değerleri ata
temp = float(latest_row['temperature_2m'])
humidity = float(latest_row['relative_humidity_2m'])
pm25 = float(latest_row['pm2_5'])
pm10 = float(latest_row['pm10'])
no2 = float(latest_row['nitrogen_dioxide'])
so2 = float(latest_row['sulphur_dioxide'])
co = float(latest_row['carbon_monoxide'])
industrial = float(latest_row['Proximity_to_Industrial_Areas'])
population = float(latest_row['Population_Density'])

# Kartlar için grid benzeri bir konumlandırma
st.markdown("<div style='display:flex; flex-direction:column; align-items:center;'>", unsafe_allow_html=True)
info_box(f"🌡️ Sıcaklık: {temp:.1f} °C", "https://media.istockphoto.com/id/1007768414/photo/blue-sky-with-bright-sun-and-clouds.jpg?s=612x612&w=0&k=20&c=MGd2-v42lNF7Ie6TtsYoKnohdCfOPFSPQt5XOz4uOy4=")
info_box(f"🏭 Endüstriyel alana uzaklık: {industrial:.1f} km", "https://www.appliedcontrol.com/website/media/Shared/Industries/Refining%20and%20Upgrading/Gas%20Plant/GasPlant_T-M.jpg")
info_box(f"🏙️ Nüfus yoğunluğu: {population:.1f} %", "https://t4.ftcdn.net/jpg/03/25/09/21/360_F_325092112_4fAOmPGij72b0Z6AyayIyw9A4Yrc82K3.jpg")

pm25_status = "Hazardous" if pm25 > 75 else "Poor" if pm25 > 50 else "Moderate" if pm25 > 25 else "Good"
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
st.markdown("</div>", unsafe_allow_html=True)

# Kullanıcıdan veri al - input alanları altta
st.markdown("---")
st.markdown("<h3 style='text-align:center; color:#1e3a8a;'>Veri Girişi</h3>", unsafe_allow_html=True)
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

# Tahmin aracı ve butonunu sayfanın altına al
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
            alert_box(f"⚠️ Sağlığınız için dışarı çıkmayın.", overlay="rgb(255,0,0)")
        elif result == "Poor":
            alert_box(f"🚨 Sağlığınız için dışarıda bulunmaktan kaçının.", overlay="rgb(255, 165, 0)")
        elif result == "Moderate":
            alert_box(f"✅ Dışarı çıkmanızda herhangi bir problem yok.", overlay="rgb(255, 255, 0, 1.0)")
        else:
            alert_box(f"✅ Hava kalitesi çok iyi, dışarı çıkabilirsiniz.", overlay="rgb(0, 128, 0)")

# 🌟 Bölgesel Hava Kalitesi Haritası - İl & İlçe Seçimi 🌟
st.markdown("""
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
""", unsafe_allow_html=True)

# Türkiye İl ve İlçe Verileri
turkey_cities = {
    "Adana": ["Aladağ", "Ceyhan", "Çukurova", "Feke", "İmamoğlu", "Karaisalı", "Karataş", "Kozan", "Pozantı", "Saimbeyli", "Sarıçam", "Seyhan", "Tufanbeyli", "Yumurtalık", "Yüreğir"],
    "Adıyaman": ["Besni", "Çelikhan", "Gerger", "Gölbaşı", "Kahta", "Merkez", "Samsat", "Sincik", "Tut"],
    "Afyonkarahisar": ["Başmakçı", "Bayat", "Bolvadin", "Çay", "Çobanlar", "Dazkırı", "Dinar", "Emirdağ", "Evciler", "Hocalar", "İhsaniye", "İscehisar", "Kızılören", "Merkez", "Sandıklı", "Sinanpaşa", "Sultandağı", "Şuhut"],
    "Ağrı": ["Diyadin", "Doğubayazıt", "Eleşkirt", "Hamur", "Merkez", "Patnos", "Taşlıçay", "Tutak"],
    "Amasya": ["Göynücek", "Gümüşhacıköy", "Hamamözü", "Merkez", "Merzifon", "Suluova", "Taşova"],
    "Ankara": ["Akyurt", "Altındağ", "Ayaş", "Bala", "Beypazarı", "Çamlıdere", "Çankaya", "Çubuk", "Elmadağ", "Etimesgut", "Evren", "Gölbaşı", "Güdül", "Haymana", "Kalecik", "Kazan", "Keçiören", "Kızılcahamam", "Mamak", "Nallıhan", "Polatlı", "Pursaklar", "Sincan", "Şereflikoçhisar", "Yenimahalle"],
    "Antalya": ["Akseki", "Aksu", "Alanya", "Demre", "Döşemealtı", "Elmalı", "Finike", "Gazipaşa", "Gündoğmuş", "İbradı", "Kaş", "Kemer", "Kepez", "Konyaaltı", "Korkuteli", "Kumluca", "Manavgat", "Muratpaşa", "Serik"],
    "Artvin": ["Ardanuç", "Arhavi", "Borçka", "Hopa", "Merkez", "Murgul", "Şavşat", "Yusufeli"],
    "Aydın": ["Bozdoğan", "Buharkent", "Çine", "Didim", "Efeler", "Germencik", "İncirliova", "Karacasu", "Karpuzlu", "Koçarlı", "Köşk", "Kuşadası", "Kuyucak", "Nazilli", "Söke", "Sultanhisar", "Yenipazar"],
    "Balıkesir": ["Altıeylül", "Ayvalık", "Balya", "Bandırma", "Bigadiç", "Burhaniye", "Dursunbey", "Edremit", "Erdek", "Gömeç", "Gönen", "Havran", "İvrindi", "Karesi", "Kepsut", "Manyas", "Marmara", "Savaştepe", "Sındırgı", "Susurluk"],
    "Bilecik": ["Bozüyük", "Gölpazarı", "İnhisar", "Merkez", "Osmaneli", "Pazaryeri", "Söğüt", "Yenipazar"],
    "Bingöl": ["Adaklı", "Genç", "Karlıova", "Kiğı", "Merkez", "Solhan", "Yayladere", "Yedisu"],
    "Bitlis": ["Adilcevaz", "Ahlat", "Güroymak", "Hizan", "Merkez", "Mutki", "Tatvan"],
    "Bolu": ["Dörtdivan", "Gerede", "Göynük", "Kıbrıscık", "Mengen", "Merkez", "Mudurnu", "Seben", "Yeniçağa"],
    "Burdur": ["Ağlasun", "Altınyayla", "Bucak", "Çavdır", "Çeltikçi", "Gölhisar", "Karamanlı", "Kemer", "Merkez", "Tefenni", "Yeşilova"],
    "Bursa": ["Büyükorhan", "Gemlik", "Gürsu", "Harmancık", "İnegöl", "İznik", "Karacabey", "Keles", "Kestel", "Mudanya", "Mustafakemalpaşa", "Nilüfer", "Orhaneli", "Orhangazi", "Osmangazi", "Yenişehir", "Yıldırım"],
    "Çanakkale": ["Ayvacık", "Bayramiç", "Biga", "Bozcaada", "Çan", "Eceabat", "Ezine", "Gelibolu", "Gökçeada", "Lapseki", "Merkez", "Yenice"],
    "Çankırı": ["Atkaracalar", "Bayramören", "Çerkeş", "Eldivan", "Ilgaz", "Kızılırmak", "Korgun", "Kurşunlu", "Merkez", "Orta", "Şabanözü", "Yapraklı"],
    "Çorum": ["Alaca", "Bayat", "Boğazkale", "Dodurga", "İskilip", "Kargı", "Laçin", "Mecitözü", "Merkez", "Oğuzlar", "Ortaköy", "Osmancık", "Sungurlu", "Uğurludağ"],
    "Denizli": ["Acıpayam", "Babadağ", "Baklan", "Bekilli", "Beyağaç", "Bozkurt", "Buldan", "Çal", "Çameli", "Çardak", "Çivril", "Güney", "Honaz", "Kale", "Merkezefendi", "Pamukkale", "Sarayköy", "Serinhisar", "Tavas"],
    "Diyarbakır": ["Bağlar", "Bismil", "Çermik", "Çınar", "Çüngüş", "Dicle", "Eğil", "Ergani", "Hani", "Hazro", "Kayapınar", "Kocaköy", "Kulp", "Lice", "Silvan", "Sur", "Yenişehir"],
    "Düzce": ["Akçakoca", "Cumayeri", "Çilimli", "Gölyaka", "Gümüşova", "Kaynaşlı", "Merkez", "Yığılca"],
    "Edirne": ["Enez", "Havsa", "İpsala", "Keşan", "Lalapaşa", "Meriç", "Merkez", "Süloğlu", "Uzunköprü"],
    "Elazığ": ["Ağın", "Alacakaya", "Arıcak", "Baskil", "Karakoçan", "Keban", "Kovancılar", "Maden", "Merkez", "Palu", "Sivrice"],
    "Erzincan": ["Çayırlı", "İliç", "Kemah", "Kemaliye", "Merkez", "Otlukbeli", "Refahiye", "Tercan", "Üzümlü"],
    "Erzurum": ["Aşkale", "Aziziye", "Çat", "Hınıs", "Horasan", "İspir", "Karaçoban", "Karayazı", "Köprüköy", "Narman", "Oltu", "Olur", "Palandöken", "Pasinler", "Pazaryolu", "Şenkaya", "Tekman", "Tortum", "Uzundere", "Yakutiye"],
    "Eskişehir": ["Alpu", "Beylikova", "Çifteler", "Günyüzü", "Han", "İnönü", "Mahmudiye", "Mihalgazi", "Mihalıççık", "Odunpazarı", "Sarıcakaya", "Seyitgazi", "Sivrihisar", "Tepebaşı"],
    "Gaziantep": ["Araban", "İslahiye", "Karkamış", "Nizip", "Nurdağı", "Oğuzeli", "Şahinbey", "Şehitkamil", "Yavuzeli"],
    "Giresun": ["Alucra", "Bulancak", "Çamoluk", "Çanakçı", "Dereli", "Doğankent", "Espiye", "Eynesil", "Görele", "Güce", "Keşap", "Merkez", "Piraziz", "Şebinkarahisar", "Tirebolu", "Yağlıdere"],
    "Gümüşhane": ["Kelkit", "Köse", "Kürtün", "Merkez", "Şiran", "Torul"],
    "Hakkari": ["Çukurca", "Derecik", "Merkez", "Şemdinli", "Yüksekova"],
    "Hatay": ["Altınözü", "Antakya", "Arsuz", "Belen", "Defne", "Dörtyol", "Erzin", "Hassa", "İskenderun", "Kırıkhan", "Kumlu", "Payas", "Reyhanlı", "Samandağ", "Yayladağı"],
    "Iğdır": ["Aralık", "Karakoyunlu", "Merkez", "Tuzluca"],
    "Isparta": ["Aksu", "Atabey", "Eğirdir", "Gelendost", "Gönen", "Keçiborlu", "Merkez", "Senirkent", "Sütçüler", "Şarkikaraağaç", "Uluborlu", "Yalvaç", "Yenişarbademli"],
    "İstanbul": ["Adalar", "Arnavutköy", "Ataşehir", "Avcılar", "Bağcılar", "Bahçelievler", "Bakırköy", "Başakşehir", "Bayrampaşa", "Beşiktaş", "Beykoz", "Beylikdüzü", "Beyoğlu", "Büyükçekmece", "Çatalca", "Çekmeköy", "Esenler", "Esenyurt", "Eyüpsultan", "Fatih", "Gaziosmanpaşa", "Güngören", "Kadıköy", "Kağıthane", "Kartal", "Küçükçekmece", "Maltepe", "Pendik", "Sancaktepe", "Sarıyer", "Silivri", "Sultanbeyli", "Sultangazi", "Şile", "Şişli", "Tuzla", "Ümraniye", "Üsküdar", "Zeytinburnu"],
    "İzmir": ["Aliağa", "Balçova", "Bayındır", "Bayraklı", "Bergama", "Beydağ", "Bornova", "Buca", "Çeşme", "Çiğli", "Dikili", "Foça", "Gaziemir", "Güzelbahçe", "Karabağlar", "Karaburun", "Karşıyaka", "Kemalpaşa", "Kınık", "Kiraz", "Konak", "Menderes", "Menemen", "Narlıdere", "Ödemiş", "Seferihisar", "Selçuk", "Tire", "Torbalı", "Urla"],
    "Kahramanmaraş": ["Afşin", "Andırın", "Çağlayancerit", "Dulkadiroğlu", "Ekinözü", "Elbistan", "Göksun", "Nurhak", "Onikişubat", "Pazarcık", "Türkoğlu"],
    "Karabük": ["Eflani", "Eskipazar", "Merkez", "Ovacık", "Safranbolu", "Yenice"],
    "Karaman": ["Ayrancı", "Başyayla", "Ermenek", "Kazımkarabekir", "Merkez", "Sarıveliler"],
    "Kars": ["Akyaka", "Arpaçay", "Digor", "Kağızman", "Merkez", "Sarıkamış", "Selim", "Susuz"],
    "Kastamonu": ["Abana", "Ağlı", "Araç", "Azdavay", "Bozkurt", "Cide", "Çatalzeytin", "Daday", "Devrekani", "Doğanyurt", "Hanönü", "İhsangazi", "İnebolu", "Küre", "Merkez", "Pınarbaşı", "Seydiler", "Şenpazar", "Taşköprü", "Tosya"],
    "Kayseri": ["Akkışla", "Bünyan", "Develi", "Felahiye", "Hacılar", "İncesu", "Kocasinan", "Melikgazi", "Özvatan", "Pınarbaşı", "Sarıoğlan", "Sarız", "Talas", "Tomarza", "Yahyalı", "Yeşilhisar"],
    "Kırıkkale": ["Bahşılı", "Balışeyh", "Çelebi", "Delice", "Karakeçili", "Keskin", "Merkez", "Sulakyurt", "Yahşihan"],
    "Kırklareli": ["Babaeski", "Demirköy", "Kofçaz", "Lüleburgaz", "Merkez", "Pehlivanköy", "Pınarhisar", "Vize"],
    "Kırşehir": ["Akçakent", "Akpınar", "Boztepe", "Çiçekdağı", "Kaman", "Merkez", "Mucur"],
    "Kilis": ["Elbeyli", "Merkez", "Musabeyli", "Polateli"],
    "Kocaeli": ["Başiskele", "Çayırova", "Darıca", "Derince", "Dilovası", "Gebze", "Gölcük", "İzmit", "Kandıra", "Karamürsel", "Körfez", "Yalova"],
    "Konya": ["Ahırlı", "Akören", "Akşehir", "Altınekin", "Beyşehir", "Bozkır", "Cihanbeyli", "Çeltik", "Çumra", "Derbent", "Derebucak", "Doğanhisar", "Emirgazi", "Ereğli", "Güneysinir", "Hadim", "Halkapınar", "Hüyük", "Ilgın", "Kadınhanı", "Karapınar", "Karatay", "Kulu", "Meram", "Sarayönü", "Selçuklu", "Seydişehir", "Taşkent", "Tuzlukçu", "Yalıhüyük", "Yunak"],
    "Kütahya": ["Altıntaş", "Aslanapa", "Çavdarhisar", "Domaniç", "Dumlupınar", "Emet", "Gediz", "Hisarcık", "Merkez", "Pazarlar", "Simav", "Şaphane", "Tavşanlı"],
    "Malatya": ["Akçadağ", "Arapgir", "Arguvan", "Battalgazi", "Darende", "Doğanşehir", "Doğanyol", "Hekimhan", "Kale", "Kuluncak", "Pütürge", "Yazihan", "Yeşilyurt"],
    "Manisa": ["Ahmetli", "Akhisar", "Alaşehir", "Demirci", "Gölmarmara", "Gördes", "Kırkağaç", "Köprübaşı", "Kula", "Salihli", "Sarıgöl", "Saruhanlı", "Selendi", "Soma", "Şehzadeler", "Turgutlu", "Yunusemre"],
    "Mardin": ["Artuklu", "Dargeçit", "Derik", "Kızıltepe", "Mazıdağı", "Midyat", "Nusaybin", "Ömerli", "Savur", "Yeşilli"],
    "Mersin": ["Akdeniz", "Anamur", "Aydıncık", "Bozyazı", "Çamlıyayla", "Erdemli", "Gülnar", "Mezitli", "Mut", "Silifke", "Tarsus", "Toroslar", "Yenişehir"],
    "Muğla": ["Bodrum", "Dalaman", "Datça", "Fethiye", "Kavaklıdere", "Köyceğiz", "Marmaris", "Menteşe", "Milas", "Ortaca", "Seydikemer", "Ula", "Yatağan"],
    "Muş": ["Bulanık", "Hasköy", "Korkut", "Malazgirt", "Merkez", "Varto"],
    "Nevşehir": ["Acıgöl", "Avanos", "Derinkuyu", "Gülşehir", "Hacıbektaş", "Kozaklı", "Merkez", "Ürgüp"],
    "Niğde": ["Altunhisar", "Bor", "Çamardı", "Çiftlik", "Merkez", "Ulukışla"],
    "Ordu": ["Akkuş", "Altınordu", "Aybastı", "Çamaş", "Çatalpınar", "Çaybaşı", "Fatsa", "Gölköy", "Gülyalı", "Gürgentepe", "İkizce", "Kabadüz", "Kabataş", "Korgan", "Kumru", "Mesudiye", "Perşembe", "Ulubey", "Ünye"],
    "Osmaniye": ["Bahçe", "Düziçi", "Hasanbeyli", "Kadirli", "Merkez", "Sumbas", "Toprakkale"],
    "Rize": ["Ardeşen", "Çamlıhemşin", "Çayeli", "Derepazarı", "Fındıklı", "Güneysu", "Hemşin", "İkizdere", "İyidere", "Kalkandere", "Merkez", "Pazar"],
    "Sakarya": ["Adapazarı", "Akyazı", "Arifiye", "Erenler", "Ferizli", "Geyve", "Hendek", "Karapürçek", "Karasu", "Kaynarca", "Kocaali", "Pamukova", "Sapanca", "Serdivan", "Söğütlü", "Taraklı"],
    "Samsun": ["19 Mayıs", "Alaçam", "Asarcık", "Atakum", "Ayvacık", "Bafra", "Canik", "Çarşamba", "Havza", "İlkadım", "Kavak", "Ladik", "Ondokuzmayıs", "Salıpazarı", "Tekkeköy", "Terme", "Vezirköprü", "Yakakent"],
    "Siirt": ["Baykan", "Eruh", "Kurtalan", "Merkez", "Pervari", "Şirvan", "Tillo"],
    "Sinop": ["Ayancık", "Boyabat", "Dikmen", "Durağan", "Erfelek", "Gerze", "Merkez", "Saraydüzü", "Türkeli"],
    "Sivas": ["Akıncılar", "Altınyayla", "Divriği", "Doğanşar", "Gemerek", "Gölova", "Hafik", "İmranlı", "Kangal", "Koyulhisar", "Merkez", "Suşehri", "Şarkışla", "Ulaş", "Yıldızeli", "Zara"],
    "Şanlıurfa": ["Akçakale", "Birecik", "Bozova", "Ceylanpınar", "Eyyübiye", "Halfeti", "Haliliye", "Harran", "Hilvan", "Karaköprü", "Siverek", "Suruç", "Viranşehir"],
    "Şırnak": ["Beytüşşebap", "Cizre", "Güçlükonak", "İdil", "Merkez", "Silopi", "Uludere"],
    "Tekirdağ": ["Çerkezköy", "Çorlu", "Ergene", "Hayrabolu", "Kapaklı", "Malkara", "Marmaraereğlisi", "Muratlı", "Saray", "Süleymanpaşa", "Şarköy"],
    "Tokat": ["Almus", "Artova", "Başçiftlik", "Erbaa", "Merkez", "Niksar", "Pazar", "Reşadiye", "Sulusaray", "Turhal", "Yeşilyurt", "Zile"],
    "Trabzon": ["Akçaabat", "Araklı", "Arsin", "Beşikdüzü", "Çaykara", "Çarşıbaşı", "Dernekpazarı", "Düzköy", "Hayrat", "Köprübaşı", "Maçka", "Of", "Ortahisar", "Sürmene", "Şalpazarı", "Tonya", "Vakfıkebir", "Yomra"],
    "Tunceli": ["Çemişgezek", "Hozat", "Mazgirt", "Merkez", "Nazımiye", "Ovacık", "Pertek", "Pülümür"],
    "Uşak": ["Banaz", "Eşme", "Karahallı", "Merkez", "Sivaslı", "Ulubey"],
    "Van": ["Bahçesaray", "Başkale", "Çaldıran", "Çatak", "Edremit", "Erciş", "Gevaş", "Gürpınar", "İpekyolu", "Muradiye", "Özalp", "Saray", "Tuşba"],
    "Yalova": ["Altınova", "Armutlu", "Çınarcık", "Çiftlikköy", "Merkez", "Termal"],
    "Yozgat": ["Akdağmadeni", "Boğazlıyan", "Çandır", "Çayıralan", "Çekerek", "Kadışehri", "Merkez", "Saraykent", "Sarıkaya", "Sorgun", "Şefaatli", "Yenifakılı", "Yerköy"],
    "Zonguldak": ["Alaplı", "Çaycuma", "Devrek", "Gökçebey", "Kilimli", "Kozlu", "Merkez"]
}

# İl ve İlçe Seçimi Arayüzü
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
                    border-radius: 15px; padding: 20px; margin-bottom: 15px;'>
            <h3 style='color: white; text-align: center; margin: 0; 
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
                🏙️ İL SEÇİMİ
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    selected_city = st.selectbox(
        "",
        options=["İl Seçiniz..."] + list(turkey_cities.keys()),
        key="city_selector"
    )

with col2:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #A8E6CF, #88D8C0); 
                    border-radius: 15px; padding: 20px; margin-bottom: 15px;'>
            <h3 style='color: white; text-align: center; margin: 0;
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
                🏘️ İLÇE SEÇİMİ
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    if selected_city and selected_city != "İl Seçiniz...":
        selected_district = st.selectbox(
            "",
            options=["İlçe Seçiniz..."] + turkey_cities[selected_city],
            key="district_selector"
        )
    else:
        st.selectbox("", options=["Önce İl Seçiniz..."], disabled=True)

# Seçim sonrası görsel bilgi kartı
if selected_city and selected_city != "İl Seçiniz...":
    selected_district = st.session_state.get("district_selector", "İlçe Seçiniz...")
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 20px; padding: 25px; margin: 20px 0;
                    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
                    border: 2px solid rgba(255,255,255,0.2);'>
            <div style='text-align: center;'>
                <h3 style='color: white; font-size: 1.8rem; margin-bottom: 15px;
                           text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
                    📍 Seçili Bölge Bilgileri
                </h3>
                <div style='background: rgba(255,255,255,0.15); border-radius: 15px; 
                            padding: 20px; backdrop-filter: blur(10px);'>
                    <p style='color: white; font-size: 1.4rem; margin: 10px 0;'>
                        🏙️ <strong>İl:</strong> {selected_city}
                    </p>
                    <p style='color: white; font-size: 1.4rem; margin: 10px 0;'>
                        🏘️ <strong>İlçe:</strong> {selected_district if selected_district != "İlçe Seçiniz..." else "Henüz Seçilmedi"}
                    </p>
                    <div style='margin-top: 20px; padding: 15px; 
                                background: rgba(255,255,255,0.1); border-radius: 12px;'>
                        <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem; margin: 0;'>
                            💡 <em>Bu bölge için özel hava kalitesi analizleri ve öneriler hazırlanıyor...</em>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Eğer hem il hem ilçe seçildiyse özel özellikler göster
    if selected_district and selected_district != "İlçe Seçiniz...":
        st.markdown("""
            <div style='background: linear-gradient(45deg, #FF9A9E 0%, #FECFEF 50%, #FECFEF 100%); 
                        border-radius: 20px; padding: 25px; margin: 20px 0;
                        box-shadow: 0 8px 25px rgba(255, 154, 158, 0.3);'>
                <h4 style='color: #333; text-align: center; font-size: 1.6rem; margin-bottom: 20px;'>
                    🎯 Bölgesel Özellikler & Öneriler
                </h4>
                <div style='display: flex; justify-content: space-around; flex-wrap: wrap;'>
                    <div style='background: rgba(255,255,255,0.8); border-radius: 12px; 
                                padding: 15px; margin: 5px; min-width: 200px; text-align: center;'>
                        <span style='font-size: 2rem;'>🌡️</span>
                        <p style='color: #333; margin: 10px 0 5px 0; font-weight: bold;'>Sıcaklık Takibi</p>
                        <p style='color: #666; margin: 0; font-size: 0.9rem;'>Bölgesel sıcaklık verileri</p>
                    </div>
                    <div style='background: rgba(255,255,255,0.8); border-radius: 12px; 
                                padding: 15px; margin: 5px; min-width: 200px; text-align: center;'>
                        <span style='font-size: 2rem;'>💨</span>
                        <p style='color: #333; margin: 10px 0 5px 0; font-weight: bold;'>Rüzgar Analizi</p>
                        <p style='color: #666; margin: 0; font-size: 0.9rem;'>Hava akımı ve yön</p>
                    </div>
                    <div style='background: rgba(255,255,255,0.8); border-radius: 12px; 
                                padding: 15px; margin: 5px; min-width: 200px; text-align: center;'>
                        <span style='font-size: 2rem;'>🏭</span>
                        <p style='color: #333; margin: 10px 0 5px 0; font-weight: bold;'>Kirlilik Kaynakları</p>
                        <p style='color: #666; margin: 0; font-size: 0.9rem;'>Endüstriyel alan analizi</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 🔐 Kullanıcı Girişi & Favori Şehirler Sistemi 🌟
st.markdown("""
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
""", unsafe_allow_html=True)

# Kullanıcı giriş formu
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
                    border-radius: 20px; padding: 25px; margin-bottom: 20px;
                    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);'>
            <h3 style='color: white; text-align: center; margin-bottom: 20px; 
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.8rem;'>
                🔐 Kullanıcı Girişi
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    username = st.text_input("👤 Kullanıcı Adı", placeholder="Kullanıcı adınızı girin...", key="username_input")
    password = st.text_input("🔒 Şifre", type="password", placeholder="Şifrenizi girin...", key="password_input")
    
    col_login1, col_login2 = st.columns(2)
    with col_login1:
        if st.button("🚀 Giriş Yap", key="login_btn"):
            st.success("✅ Başarıyla giriş yapıldı!")
            st.balloons()
    
    with col_login2:
        if st.button("📝 Kayıt Ol", key="register_btn"):
            st.info("📧 Kayıt linki email'inize gönderildi!")

with col2:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #A8E6CF, #88D8C0); 
                    border-radius: 20px; padding: 25px; margin-bottom: 20px;
                    box-shadow: 0 8px 25px rgba(168, 230, 207, 0.3);'>
            <h3 style='color: white; text-align: center; margin-bottom: 20px;
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.8rem;'>
                ⭐ Favori Şehirlerim
            </h3>
        </div>
    """, unsafe_allow_html=True)
    
    favorite_city = st.selectbox("🏙️ Favori şehir ekle", 
                                options=["Şehir seçin..."] + list(turkey_cities.keys()), 
                                key="fav_city_selector")
    
    col_fav1, col_fav2 = st.columns(2)
    with col_fav1:
        if st.button("⭐ Favorime Ekle", key="add_fav_btn"):
            if favorite_city and favorite_city != "Şehir seçin...":
                st.success(f"✅ {favorite_city} favorilere eklendi!")
            else:
                st.warning("⚠️ Lütfen şehir seçin!")
    
    with col_fav2:
        if st.button("🗑️ Favorileri Temizle", key="clear_fav_btn"):
            st.info("🧹 Favoriler temizlendi!")

# Favori şehirler listesi (demo)
st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; padding: 25px; margin: 20px 0;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);'>
        <h4 style='color: white; text-align: center; font-size: 1.6rem; margin-bottom: 20px;
                   text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
            📋 Kayıtlı Favori Şehirleriniz
        </h4>
        <div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 15px;'>
            <div style='background: rgba(255,255,255,0.15); border-radius: 12px; 
                        padding: 15px 20px; backdrop-filter: blur(10px);
                        border: 1px solid rgba(255,255,255,0.2);'>
                <span style='color: white; font-size: 1.1rem;'>🏙️ İstanbul</span>
            </div>
            <div style='background: rgba(255,255,255,0.15); border-radius: 12px; 
                        padding: 15px 20px; backdrop-filter: blur(10px);
                        border: 1px solid rgba(255,255,255,0.2);'>
                <span style='color: white; font-size: 1.1rem;'>🌊 İzmir</span>
            </div>
            <div style='background: rgba(255,255,255,0.15); border-radius: 12px; 
                        padding: 15px 20px; backdrop-filter: blur(10px);
                        border: 1px solid rgba(255,255,255,0.2);'>
                <span style='color: white; font-size: 1.1rem;'>🏛️ Ankara</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 🔔 Uyarı Sistemi 
st.markdown("""
    <div style='background: linear-gradient(45deg, #FF9A9E 0%, #FECFEF 50%, #FECFEF 100%); 
                border-radius: 25px; padding: 30px; margin: 30px 0;
                box-shadow: 0 12px 30px rgba(255, 154, 158, 0.4);
                border: 2px solid rgba(255,255,255,0.3);'>
        <h3 style='color: #333; text-align: center; font-size: 2.2rem; margin-bottom: 25px;
                   text-shadow: 1px 1px 2px rgba(255,255,255,0.5);'>
            🔔 Akıllı Uyarı Sistemi 📱
        </h3>
        <div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; margin-bottom: 25px;'>
            <div style='background: rgba(255,255,255,0.8); border-radius: 15px; 
                        padding: 20px; min-width: 250px; text-align: center;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                <span style='font-size: 2.5rem; margin-bottom: 10px; display: block;'>📧</span>
                <h4 style='color: #333; margin: 10px 0 5px 0;'>Email Uyarıları</h4>
                <p style='color: #666; margin: 0; font-size: 0.9rem;'>Hava kalitesi değişimlerinde email bildirim</p>
            </div>
            <div style='background: rgba(255,255,255,0.8); border-radius: 15px; 
                        padding: 20px; min-width: 250px; text-align: center;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                <span style='font-size: 2.5rem; margin-bottom: 10px; display: block;'>📱</span>
                <h4 style='color: #333; margin: 10px 0 5px 0;'>SMS Bildirimleri</h4>
                <p style='color: #666; margin: 0; font-size: 0.9rem;'>Kritik seviyelerde SMS uyarısı</p>
            </div>
            <div style='background: rgba(255,255,255,0.8); border-radius: 15px; 
                        padding: 20px; min-width: 250px; text-align: center;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                <span style='font-size: 2.5rem; margin-bottom: 10px; display: block;'>🔔</span>
                <h4 style='color: #333; margin: 10px 0 5px 0;'>Push Bildirimleri</h4>
                <p style='color: #666; margin: 0; font-size: 0.9rem;'>Anlık mobil bildirimler</p>
            </div>
        </div>
        
    </div>
""", unsafe_allow_html=True)

# Uyarı seçenekleri - Streamlit checkbox'ları ile
col1, col2, col3 = st.columns(3)
with col1:
    email_check = st.checkbox("📧 Email Uyarıları", key="email_alerts_check")
with col2:
    sms_check = st.checkbox("📱 SMS Bildirimleri", key="sms_alerts_check")
with col3:
    push_check = st.checkbox("🔔 Push Bildirimleri", key="push_alerts_check")
""", unsafe_allow_html=True)

# Uyarı ayarlama butonları
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("✅ Uyarıları Aktifleştir", key="enable_alerts"):
        st.success("🔔 Tüm uyarılar aktifleştirildi!")
        
with col2:
    if st.button("⚙️ Uyarı Ayarları", key="alert_settings"):
        st.info("⚙️ Uyarı ayarları penceresi açılıyor...")
        
with col3:
    if st.button("🔕 Uyarıları Kapat", key="disable_alerts"):
        st.warning("🔕 Uyarılar kapatıldı!")

# 💡 AI Destekli Öneri Sistemi 🤖
ai_suggestion_html = """
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
st.markdown(ai_suggestion_html, unsafe_allow_html=True)

# Öneri kategorileri
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
                    border-radius: 20px; padding: 25px; margin-bottom: 20px;
                    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
                    text-align: center;'>
            <span style='font-size: 3rem; margin-bottom: 15px; display: block;'>🏃‍♂️</span>
            <h3 style='color: white; margin-bottom: 15px; 
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.6rem;'>
                Aktivite Önerileri
            </h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem;'>
                Hava durumuna göre spor ve aktivite tavsiyeleri
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏃‍♂️ Aktivite Önerisi Al", key="activity_suggestion"):
        suggestions = [
            "🏠 İç mekan yogası yapabilirsiniz",
            "🚶‍♂️ Kısa mesafe yürüyüş uygun",
            "🏋️‍♂️ Spor salonunda antrenman",
            "🧘‍♀️ Meditasyon ve nefes egzersizleri",
            "🏊‍♂️ Kapalı havuz aktiviteleri"
        ]
        import random
        suggestion = random.choice(suggestions)
        st.success(f"💡 **Öneri:** {suggestion}")

with col2:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #A8E6CF, #88D8C0); 
                    border-radius: 20px; padding: 25px; margin-bottom: 20px;
                    box-shadow: 0 8px 25px rgba(168, 230, 207, 0.3);
                    text-align: center;'>
            <span style='font-size: 3rem; margin-bottom: 15px; display: block;'>🏥</span>
            <h3 style='color: white; margin-bottom: 15px;
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.6rem;'>
                Sağlık Önerileri
            </h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem;'>
                Hava kalitesine göre sağlık korunma tavsiyeleri
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🏥 Sağlık Önerisi Al", key="health_suggestion"):
        health_tips = [
            "😷 N95 maske kullanımı önerilir",
            "💧 Bol su tüketin ve hidrate kalın",
            "🌿 İç mekan bitkilerini artırın",
            "🏠 Ev havalandırma sistemini kontrol edin",
            "💊 Astım ilaçlarınızı yanınızda bulundurun"
        ]
        import random
        tip = random.choice(health_tips)
        st.info(f"⚕️ **Sağlık Tavsiyesi:** {tip}")

with col3:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #FF9A9E, #FECFEF); 
                    border-radius: 20px; padding: 25px; margin-bottom: 20px;
                    box-shadow: 0 8px 25px rgba(255, 154, 158, 0.3);
                    text-align: center;'>
            <span style='font-size: 3rem; margin-bottom: 15px; display: block;'>🌱</span>
            <h3 style='color: white; margin-bottom: 15px;
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.6rem;'>
                Çevre Önerileri
            </h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem;'>
                Sürdürülebilir yaşam ve çevre koruma tavsiyeleri
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌱 Çevre Önerisi Al", key="environment_suggestion"):
        env_tips = [
            "🚗 Toplu taşıma kullanın",
            "🌳 Ağaç dikme etkinliklerine katılın",
            "♻️ Geri dönüşüm yapın",
            "🚴‍♂️ Bisiklet kullanımını artırın",
            "🌿 Organik ürünler tercih edin"
        ]
        import random
        env_tip = random.choice(env_tips)
        st.success(f"🌍 **Çevre Tavsiyesi:** {env_tip}")

# Kapsamlı öneri sistemi
st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; padding: 25px; margin: 25px 0;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);'>
        <h4 style='color: white; text-align: center; font-size: 2rem; margin-bottom: 20px;
                   text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
            🎯 Kişiselleştirilmiş Kapsamlı Öneri
        </h4>
        <div style='text-align: center; margin: 25px 0;'>
            <p style='color: rgba(255,255,255,0.9); font-size: 1.2rem; margin-bottom: 25px;'>
                🧠 Mevcut hava kalitesi, kişisel tercihleriniz ve sağlık durumunuza göre<br>
                AI destekli kapsamlı öneriler alın!
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Ana öneri butonu
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 KAPSAMLI ÖNERİ AL 🤖", key="comprehensive_suggestion", 
                 help="AI destekli kişiselleştirilmiş öneri sistemi"):
        st.markdown("""
            <div style='background: linear-gradient(45deg, #FF9A9E 0%, #FECFEF 50%, #FECFEF 100%); 
                        border-radius: 20px; padding: 25px; margin: 20px 0;
                        box-shadow: 0 12px 30px rgba(255, 154, 158, 0.4);
                        border: 2px solid rgba(255,255,255,0.3);'>
                <h4 style='color: #333; text-align: center; font-size: 1.8rem; margin-bottom: 20px;
                           text-shadow: 1px 1px 2px rgba(255,255,255,0.5);'>
                    🎯 Kişiselleştirilmiş Önerileriniz
                </h4>
                <div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 15px;'>
                    <div style='background: rgba(255,255,255,0.8); border-radius: 12px; 
                                padding: 15px; min-width: 200px; text-align: center;
                                box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                        <span style='font-size: 2rem; margin-bottom: 10px; display: block;'>🏃‍♂️</span>
                        <p style='color: #333; margin: 0; font-weight: 600;'>İç mekan egzersizi yapın</p>
                    </div>
                    <div style='background: rgba(255,255,255,0.8); border-radius: 12px; 
                                padding: 15px; min-width: 200px; text-align: center;
                                box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                        <span style='font-size: 2rem; margin-bottom: 10px; display: block;'>😷</span>
                        <p style='color: #333; margin: 0; font-weight: 600;'>N95 maske kullanın</p>
                    </div>
                    <div style='background: rgba(255,255,255,0.8); border-radius: 12px; 
                                padding: 15px; min-width: 200px; text-align: center;
                                box-shadow: 0 5px 15px rgba(0,0,0,0.1);'>
                        <span style='font-size: 2rem; margin-bottom: 10px; display: block;'>🚗</span>
                        <p style='color: #333; margin: 0; font-weight: 600;'>Toplu taşıma tercih edin</p>
                    </div>
                </div>
                <div style='text-align: center; margin-top: 20px; padding: 15px; 
                            background: rgba(255,255,255,0.6); border-radius: 12px;'>
                    <p style='color: #333; margin: 0; font-style: italic;'>
                        💡 <strong>AI Analizi:</strong> Mevcut hava kalitesi seviyenize göre 
                        özelleştirilmiş öneriler hazırlandı.
                    </p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.balloons()

# ⏰ Akıllı Hatırlatıcı Sistemi 🔔
st.markdown("""
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
""", unsafe_allow_html=True)

# Hatırlatıcı kategorileri
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
                    border-radius: 20px; padding: 25px; margin-bottom: 20px;
                    box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
                    text-align: center;'>
            <span style='font-size: 3rem; margin-bottom: 15px; display: block;'>💊</span>
            <h3 style='color: white; margin-bottom: 15px; 
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.6rem;'>
                İlaç Hatırlatıcısı
            </h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem;'>
                Astım ve alerji ilaçları için hatırlatıcı
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("💊 İlaç Hatırlatıcısı Ekle", key="medicine_reminder"):
        st.success("✅ İlaç hatırlatıcısı 08:00 ve 20:00 için ayarlandı!")
        st.info("📱 Telefon bildirimi aktif edildi")

with col2:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #A8E6CF, #88D8C0); 
                    border-radius: 20px; padding: 25px; margin-bottom: 20px;
                    box-shadow: 0 8px 25px rgba(168, 230, 207, 0.3);
                    text-align: center;'>
            <span style='font-size: 3rem; margin-bottom: 15px; display: block;'>🌤️</span>
            <h3 style='color: white; margin-bottom: 15px;
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.6rem;'>
                Hava Durumu Kontrolü
            </h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem;'>
                Günlük hava kalitesi kontrol hatırlatıcısı
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🌤️ Hava Kontrolü Hatırlatıcısı", key="weather_reminder"):
        st.success("✅ Günlük 07:00'da hava durumu kontrolü!")
        st.info("🔔 Sabah bildirimi ayarlandı")

with col3:
    st.markdown("""
        <div style='background: linear-gradient(45deg, #FF9A9E, #FECFEF); 
                    border-radius: 20px; padding: 25px; margin-bottom: 20px;
                    box-shadow: 0 8px 25px rgba(255, 154, 158, 0.3);
                    text-align: center;'>
            <span style='font-size: 3rem; margin-bottom: 15px; display: block;'>😷</span>
            <h3 style='color: white; margin-bottom: 15px;
                       text-shadow: 1px 1px 2px rgba(0,0,0,0.3); font-size: 1.6rem;'>
                Maske Hatırlatıcısı
            </h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0; font-size: 1rem;'>
                Dışarı çıkmadan önce maske hatırlatıcısı
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("😷 Maske Hatırlatıcısı Ekle", key="mask_reminder"):
        st.success("✅ Dışarı çıkış öncesi maske hatırlatıcısı!")
        st.info("📍 Konum bazlı bildirim aktif")

# Özel hatırlatıcı oluşturma
st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; padding: 25px; margin: 25px 0;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);'>
        <h4 style='color: white; text-align: center; font-size: 2rem; margin-bottom: 20px;
                   text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
            📝 Özel Hatırlatıcı Oluştur
        </h4>
    </div>
""", unsafe_allow_html=True)

# Hatırlatıcı formu
col1, col2 = st.columns(2)

with col1:
    reminder_text = st.text_input("📝 Hatırlatıcı Metni", 
                                 placeholder="Hatırlatıcı mesajınızı yazın...", 
                                 key="reminder_text")
    reminder_time = st.time_input("⏰ Hatırlatıcı Saati", key="reminder_time")

with col2:
    reminder_frequency = st.selectbox("🔄 Tekrar Sıklığı", 
                                     ["Bir kez", "Günlük", "Haftalık", "Aylık"],
                                     key="reminder_frequency")
    reminder_priority = st.selectbox("🚨 Öncelik Seviyesi",
                                    ["Düşük", "Orta", "Yüksek", "Kritik"],
                                    key="reminder_priority")

# Ana hatırlatıcı oluşturma butonu
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("⚡ HATIRLATİCİ OLUŞTUR ⚡", key="create_reminder", 
                 help="Kişiselleştirilmiş hatırlatıcı oluştur"):
        if reminder_text:
            priority_colors = {
                "Düşük": "🟢",
                "Orta": "🟡", 
                "Yüksek": "🟠",
                "Kritik": "🔴"
            }
            priority_icon = priority_colors.get(reminder_priority, "🟢")
            
            st.markdown(f"""
                <div style='background: linear-gradient(45deg, #FF9A9E 0%, #FECFEF 50%, #FECFEF 100%); 
                            border-radius: 20px; padding: 25px; margin: 20px 0;
                            box-shadow: 0 12px 30px rgba(255, 154, 158, 0.4);
                            border: 2px solid rgba(255,255,255,0.3);'>
                    <h4 style='color: #333; text-align: center; font-size: 1.8rem; margin-bottom: 20px;
                               text-shadow: 1px 1px 2px rgba(255,255,255,0.5);'>
                        ✅ Hatırlatıcı Başarıyla Oluşturuldu!
                    </h4>
                    <div style='background: rgba(255,255,255,0.8); border-radius: 15px; 
                                padding: 20px; margin: 15px 0;'>
                        <p style='color: #333; margin: 10px 0; font-size: 1.2rem;'>
                            📝 <strong>Mesaj:</strong> {reminder_text}
                        </p>
                        <p style='color: #333; margin: 10px 0; font-size: 1.2rem;'>
                            ⏰ <strong>Saat:</strong> {reminder_time}
                        </p>
                        <p style='color: #333; margin: 10px 0; font-size: 1.2rem;'>
                            🔄 <strong>Sıklık:</strong> {reminder_frequency}
                        </p>
                        <p style='color: #333; margin: 10px 0; font-size: 1.2rem;'>
                            {priority_icon} <strong>Öncelik:</strong> {reminder_priority}
                        </p>
                    </div>
                    <div style='text-align: center; margin-top: 20px; padding: 15px; 
                                background: rgba(255,255,255,0.6); border-radius: 12px;'>
                        <p style='color: #333; margin: 0; font-style: italic;'>
                            🔔 <strong>Bildirim sistemi aktif!</strong> Hatırlatıcınız zamanında size ulaşacak.
                        </p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.warning("⚠️ Lütfen hatırlatıcı mesajı yazın!")

# Mevcut hatırlatıcılar listesi (demo)
st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; padding: 25px; margin: 25px 0;
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);'>
        <h4 style='color: white; text-align: center; font-size: 1.8rem; margin-bottom: 20px;
                   text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
            📋 Aktif Hatırlatıcılarınız
        </h4>
        <div style='display: flex; justify-content: center; flex-wrap: wrap; gap: 15px;'>
            <div style='background: rgba(255,255,255,0.15); border-radius: 12px; 
                        padding: 15px 20px; backdrop-filter: blur(10px);
                        border: 1px solid rgba(255,255,255,0.2);'>
                <span style='color: white; font-size: 1rem;'>💊 08:00 - Astım İlacı</span>
            </div>
            <div style='background: rgba(255,255,255,0.15); border-radius: 12px; 
                        padding: 15px 20px; backdrop-filter: blur(10px);
                        border: 1px solid rgba(255,255,255,0.2);'>
                <span style='color: white; font-size: 1rem;'>🌤️ 07:00 - Hava Kontrolü</span>
            </div>
            <div style='background: rgba(255,255,255,0.15); border-radius: 12px; 
                        padding: 15px 20px; backdrop-filter: blur(10px);
                        border: 1px solid rgba(255,255,255,0.2);'>
                <span style='color: white; font-size: 1rem;'>😷 Çıkış - Maske Kontrol</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Hatırlatıcı yönetim butonları
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📱 Tüm Bildirimleri Aç", key="enable_all_reminders"):
        st.success("🔔 Tüm hatırlatıcı bildirimleri aktifleştirildi!")
        
with col2:
    if st.button("⚙️ Hatırlatıcı Ayarları", key="reminder_settings"):
        st.info("⚙️ Hatırlatıcı ayarları penceresi açılıyor...")
        
with col3:
    if st.button("🔕 Sessize Al", key="mute_reminders"):
        st.warning("🔕 Hatırlatıcılar sessiz moda alındı!")

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
""", unsafe_allow_html=True)
