import streamlit as st
import os
import base64
import fitz  # PyMuPDF
from functools import lru_cache

# إعدادات الصفحة
st.set_page_config(page_title="Maharah Design | لوحة التحكم", layout="wide")

# =========================
# 🔐 نظام الباسورد (Glass Style)
# =========================
def check_password():
    def password_entered():
        if st.session_state["password"] == "1234":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("""
        <style>
        .stApp {
            background-image: url("https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1200px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg");
            background-size: cover; background-attachment: fixed;
        }
        .login-box {
            background: rgba(255, 255, 255, 0.1); padding: 50px; border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.2); text-align: center;
            max-width: 420px; margin: 120px auto; backdrop-filter: blur(25px);
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        }
        </style>
        """, unsafe_allow_html=True)
        st.markdown('<div class="login-box"><h2 style="color:white; font-family:sans-serif;">MAHARAH DESIGN</h2><p style="color:#00d2ff">ادخل كلمة المرور يا باشا</p></div>', unsafe_allow_html=True)
        st.text_input("Password", type="password", on_change=password_entered, key="password", label_visibility="collapsed")
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("❌ الباسورد غلط يا يوسف")
        return False
    return st.session_state["password_correct"]

if not check_password():
    st.stop()

# =========================
# 📁 إعداد المجلدات والكاش
# =========================
pdf_folder = "pdf_files"
os.makedirs(pdf_folder, exist_ok=True)

if "custom_names" not in st.session_state:
    st.session_state.custom_names = {}

@lru_cache(maxsize=128)
def get_pdf_thumbnail_cached(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap(matrix=fitz.Matrix(0.4, 0.4)) # جودة متوسطة للسرعة
        return base64.b64encode(pix.tobytes("png")).decode()
    except: return None

def get_base64_image(path):
    try:
        with open(path, "rb") as f: return base64.b64encode(f.read()).decode()
    except: return None

# =========================
# 🎨 CSS التصميم الزجاجي المتطور
# =========================
st.markdown("""
<style>
    /* التعتيم الخلفي للسايت */
    .stApp::before { content:""; position:fixed; inset:0; background:rgba(0,0,0,0.45); z-index:-1; }
    
    /* تنسيق الكروت */
    .movie-card {
        background: rgba(255, 255, 255, 0.08); 
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 25px; 
        height: 380px; 
        display: flex; 
        flex-direction: column; 
        backdrop-filter: blur(15px);
        transition: 0.4s ease;
        overflow: hidden;
        margin-bottom: 10px;
    }
    .movie-card:hover { transform: scale(1.03); border-color: #00d2ff; box-shadow: 0 10px 30px rgba(0,210,255,0.2); }
    
    /* الصورة المصغرة */
    .pdf-thumbnail { height: 300px; width: 100%; object-fit: cover; border-radius: 25px 25px 0 0; }
    
    /* اسم الملف */
    .file-info { padding: 12px; text-align: center; }
    .file-name { color: #f0f0f0; font-size: 14px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

    /* أزرار Streamlit المخصصة */
    div.stButton > button {
        border-radius: 20px !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover { background: #00d2ff !important; color: black !important; border-color: #00d2ff !important; }
    
    /* السايد بار */
    [data-testid="stSidebar"] { background: rgba(0, 0, 0, 0.6) !important; backdrop-filter: blur(20px); border-right: 1px solid rgba(255,255,255,0.1); }
    
    /* شريط البحث */
    .stTextInput input { border-radius: 20px !important; background: rgba(255,255,255,0.1) !important; color: white !important; border: 1px solid rgba(255,255,255,0.2) !important; }
</style>
""", unsafe_allow_html=True)

# =========================
# 🧭 السايدبار (الأدوات)
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:white;'>🛠️ DASHBOARD</h2>", unsafe_allow_html=True)
    
    uploaded = st.file_uploader("Upload New Assets", type=["pdf"], accept_multiple_files=True)
    if uploaded:
        for file in uploaded:
            with open(os.path.join(pdf_folder, file.name), "wb") as f: f.write(file.getbuffer())
        st.success("Files Added!")
        st.rerun()

    files_all = sorted([f for f in os.listdir(pdf_folder) if f.endswith(".pdf")])

    with st.expander("📝 Edit File Names"):
        if files_all:
            target = st.selectbox("Select File", files_all)
            new_title = st.text_input("Display Name", st.session_state.custom_names.get(target, target.replace(".pdf","")))
            if st.button("Rename ✅"):
                st.session_state.custom_names[target] = new_title
                st.rerun()

    with st.expander("🗑 Delete Assets"):
        if files_all:
            to_del = st.selectbox("Select to remove", files_all, key="del_box")
            if st.button("Delete Permanently ⚠️"):
                os.remove(os.path.join(pdf_folder, to_del))
                st.rerun()

    st.markdown("---")
    if st.button("🔴 Logout Session"):
        del st.session_state["password_correct"]
        st.rerun()

# =========================
# 🧩 الهيدر الاحترافي
# =========================
logo_b64 = get_base64_image(os.path.join(pdf_folder, "LOGO MAHARA.png"))
head_col1, head_col2 = st.columns([1, 4])

with head_col1:
    if logo_b64: st.markdown(f'<img src="data:image/png;base64,{logo_b64}" width="120" style="filter:drop-shadow(0 0 10px #00d2ff)">', unsafe_allow_html=True)

with head_col2:
    st.markdown("<h1 style='margin-bottom:0; color:white;'>MAHARAH <span style='color:#00d2ff;'>DESIGN</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#9fbcd6; margin-top:0;'>Premium Assets Control Center</p>", unsafe_allow_html=True)

# =========================
# 🔎 البحث الفلتر
# =========================
search_query = st.text_input("🔍 Search Assets...", placeholder="Search by name...")
filtered_files = [f for f in files_all if search_query.lower() in f.lower()]

# =========================
# 🧱 شبكة العرض (Glass Grid)
# =========================
if filtered_files:
    # تقسيم العرض لـ 5 أعمدة زي الصورة
    rows = [filtered_files[i:i + 5] for i in range(0, len(filtered_files), 5)]
    
    for row in rows:
        cols = st.columns(5)
        for i, f in enumerate(row):
            path = os.path.join(pdf_folder, f)
            thumb = get_pdf_thumbnail_cached(path)
            display_title = st.session_state.custom_names.get(f, f.replace(".pdf","").upper())

            with cols[i]:
                # الكارت الزجاجي
                st.markdown(f'''
                    <div class="movie-card">
                        {'<img src="data:image/png;base64,'+thumb+'" class="pdf-thumbnail">' if thumb else '<div style="height:300px; display:flex; align-items:center; justify-content:center; color:white;">📄 NO PREVIEW</div>'}
                        <div class="file-info">
                            <div class="file-name">{display_title}</div>
                        </div>
                    </div>
                ''', unsafe_allow_html=True)
                
                # أزرار التحكم تحت الكارت مباشرة
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(f"👁 VIEW", key=f"v_{f}"):
                        show_pdf_popup(path)
                with btn_col2:
                    with open(path, "rb") as pdf_file:
                        st.download_button(f"📥 GET", pdf_file, file_name=f, key=f"d_{f}")
else:
    st.info("لا يوجد ملفات مطابقة للبحث.")
