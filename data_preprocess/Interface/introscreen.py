import streamlit as st

st.markdown("""
    <h1 style='text-align: center;'>Lutfen adres tipini secin</h1>
""", unsafe_allow_html=True)

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



box_choice("Bulundugunuz Konum",
           "https://t3.ftcdn.net/jpg/09/62/53/46/360_F_962534654_tFyVQMaAKFGIzV7jOqK5LPwpqBcqgzvy.jpg",
           link="code.py")  

box_choice("Adres seciniz",
           "https://www.magnificenttravel.com/public/thumbs/860x450-thumbnail-Turkey-Map--1.jpg",
           link="adres")
