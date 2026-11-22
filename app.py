import base64
import time
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="NİLAY", page_icon="💖", layout="wide")

BASE = Path(__file__).parent  # resimler app.py ile aynı klasörde olmalı

# ---------- Stil ----------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffe4ec;
    }
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp span, .stApp label {
        color: #c2185b !important;
    }
    .stApp button p {
        color: #c2185b !important;
    }
    .intro {
        display:flex; justify-content:center; align-items:center;
        height:70vh; font-size:7rem; font-weight:800; letter-spacing:1.5rem;
        color:#c2185b !important; text-shadow:0 0 25px rgba(194,24,91,.4);
    }
    .cursor { animation: blink .7s infinite; }
    @keyframes blink { 50% { opacity:0; } }
    .baslik { text-align:center; font-size:3rem; font-weight:800; color:#c2185b !important; }
    .kart-baslik { text-align:center; font-weight:700; font-size:1.1rem; margin:.4rem 0; color:#c2185b !important; }
    .resim-kutu { position:relative; }
    .resim-kutu img { width:100%; border-radius:12px; display:block; }
    .stApp .resim-kutu span {
        position:absolute; left:0; right:0; bottom:0; padding:12px;
        text-align:center; font-weight:800; color:white !important; font-size:1.2rem;
        background:linear-gradient(transparent, rgba(0,0,0,.8));
        border-radius:0 0 12px 12px;
    }
    .madde { font-size:1.6rem; padding:.5rem 0; color:#c2185b !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Yardımcılar ----------
def resim_bul(ad):
    """Resmi bulur; jpeg/jpg/png uzantı farklarını da dener."""
    p = BASE / ad
    if p.exists():
        return p
    stem = Path(ad).stem
    for ext in (".jpeg", ".jpg", ".JPG", ".JPEG", ".png"):
        q = BASE / (stem + ext)
        if q.exists():
            return q
    return None


def resim_goster(ad):
    p = resim_bul(ad)
    if p:
        st.image(str(p), use_container_width=True)
    else:
        st.warning(f"'{ad}' bulunamadı")


def yazili_resim(ad, yazi):
    p = resim_bul(ad)
    if not p:
        st.warning(f"'{ad}' bulunamadı")
        return
    data = base64.b64encode(p.read_bytes()).decode()
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    st.markdown(
        f'<div class="resim-kutu"><img src="data:{mime};base64,{data}"><span>{yazi}</span></div>',
        unsafe_allow_html=True,
    )


def sayfa_git(ad):
    st.session_state.sayfa = ad


def resim_ac_kapa(anahtar):
    k = f"goster_{anahtar}"
    st.session_state[k] = not st.session_state.get(k, False)


# ---------- Durum ----------
if "sayfa" not in st.session_state:
    st.session_state.sayfa = "ana"
if "intro_bitti" not in st.session_state:
    st.session_state.intro_bitti = False

# ---------- İntro ----------
if not st.session_state.intro_bitti:
    alan = st.empty()
    yazi = ""
    for harf in "NİLAY":
        yazi += harf
        alan.markdown(
            f'<div class="intro">{yazi}<span class="cursor">|</span></div>',
            unsafe_allow_html=True,
        )
        time.sleep(0.6)  # 5 harf x 0.6 sn = 3 sn
    time.sleep(0.4)
    alan.empty()
    st.session_state.intro_bitti = True
    st.rerun()

# ---------- Kategoriler ----------
KATEGORILER = [
    ("tanitim", "UYGULAMA TANITIMI", "uygulama tanıtımı.jpeg"),
    ("fedakarlik", "NİLAYIN FEDAKARLIKLARI", "nilayın fedakarlıkları.jpeg"),
    ("kavga", "BİRBİRİMİZİ DE YERİZ SAN SEBASTİAN DA", "kavgalarımız.jpeg"),
    ("ask", "NİLAY'IN AŞKLARI", "nilayın aşkları.jpeg"),
    ("staj", "NİLAYIN STAJI", "nilayın stajı.jpeg"),
]


def ana_sayfa():
    st.markdown('<div class="baslik">💖 NİLAY 💖</div>', unsafe_allow_html=True)
    st.write("")
    for satir in (KATEGORILER[:3], KATEGORILER[3:]):
        sutunlar = st.columns(3)
        for sutun, (anahtar, baslik, resim) in zip(sutunlar, satir):
            with sutun:
                with st.container(border=True):
                    resim_goster(resim)
                    st.markdown(f'<div class="kart-baslik">{baslik}</div>', unsafe_allow_html=True)
                    st.button(
                        "Aç",
                        key=f"btn_{anahtar}",
                        use_container_width=True,
                        on_click=sayfa_git,
                        args=(anahtar,),
                    )


def geri_butonu():
    st.button("⬅ Geri", on_click=sayfa_git, args=("ana",))


def tanitim():
    geri_butonu()
    st.header("UYGULAMA TANITIMI")
    c1, c2, c3 = st.columns(3)
    with c1:
        yazili_resim("uygulamanın kurucusu.jpeg", "UYGULAMANIN KURUCUSU")
    with c2:
        yazili_resim("uygulamanın sahibi.jpeg", "UYGULAMANIN SAHİBİ")
    with c3:
        yazili_resim("manevi motivasyoncu.jpeg", "MANEVİ MOTİVASYONCU")


def resimli_maddeler(baslik, liste):
    """Her maddenin yanında 'Tıkla' butonu olur, basınca resim açılır/kapanır.
    liste: (madde metni, resim dosyası, benzersiz anahtar)"""
    geri_butonu()
    st.header(baslik)
    for metin, resim, anahtar in liste:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f'<div class="madde">{metin}</div>', unsafe_allow_html=True)
        with c2:
            st.button("Tıkla", key=f"btn_{anahtar}", on_click=resim_ac_kapa, args=(anahtar,))
        if st.session_state.get(f"goster_{anahtar}", False):
            p = resim_bul(resim)
            if p:
                st.image(str(p), width=400)
            else:
                st.warning(f"'{resim}' bulunamadı")


def fedakarlik():
    resimli_maddeler(
        "NİLAYIN FEDAKARLIKLARI",
        [
            ("1-) Nisa'ya 2 flört yaptı.", "rulo.jpeg", "rulo"),
            ("2-) Ceydaya caminin önünde manifest yaptı.", "cami.jpeg", "cami"),
        ],
    )


def kavga():
    resimli_maddeler(
        "BİRBİRİMİZİ DE YERİZ SAN SEBASTİAN DA",
        [
            ("1-) Nilay Ankaraya gelmedi", "ankara.jpeg", "ankara"),
            ("2-) Nilay sandiviçi beğenmedi.", "sandiviç.jpeg", "sandivic"),
        ],
    )


def ask():
    geri_butonu()
    st.header("NİLAY'IN AŞKLARI")
    liste = [
        ("1-) AHMET: Kübra kaptı.", "https://youtu.be/xHICL1-Ps34?si=X8o00xMGrt3yoC2u"),
        ("2-) YUSUF: En büyük aşkı.", "https://youtu.be/cdMmUasRqro?si=i1EAwtbVDKrc4RWU"),
        ("3-) MUHSİN: İlan-ı aşk yaptı.", "https://youtu.be/GcU6hWpPvCU?si=Msdt02QGFWDOpLf6"),
        ("4-) MEHMET: Kahtalı.", "https://youtu.be/xelzK5nq-8w?si=dBFA3Z890t4wEWfo"),
        ("5-) BAYRAM: Kendini Kurtlar Vadisi Polat sanan çocuk.", "https://youtube.com/shorts/81N2CZ0Acnc?si=ieCzbJaQqxA0zems"),
        ("6-) EYÜP CAN: Küçük çocuk.", "https://youtu.be/CBUdZIut0OA?si=qIqudrWERPnfWmfU"),
        ("7-) FERHAN: Nişanlandı.", "https://youtu.be/TuLmRVugdFo?si=v_XwOSnbJR9ix9vD"),
    ]
    for metin, link in liste:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f'<div class="madde">{metin}</div>', unsafe_allow_html=True)
        with c2:
            st.link_button("İzle ▶", link)


def staj():
    geri_butonu()
    st.header("NİLAYIN STAJI")
    link = "https://youtube.com/shorts/QFERKyx1Lcc?si=GB-ap-txy3i0N9iS"
    st.markdown(f"🔗 [{link}]({link})")
    st.link_button("Videoyu aç ▶", link)


# ---------- Yönlendirme ----------
sayfa = st.session_state.sayfa
if sayfa == "ana":
    ana_sayfa()
elif sayfa == "tanitim":
    tanitim()
elif sayfa == "fedakarlik":
    fedakarlik()
elif sayfa == "kavga":
    kavga()
elif sayfa == "ask":
    ask()
elif sayfa == "staj":
    staj()
