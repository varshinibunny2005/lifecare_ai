import streamlit as st
import os
import requests
from dotenv import load_dotenv
from PIL import Image
import io

# ─────────────────────────────────────────
# Load Groq API Key
# ─────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
def analyze_with_groq(prompt: str) -> str:
    """Send prompt to Groq API and return response."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful medical assistant. Provide structured, clear medical analysis."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

# ─────────────────────────────────────────
# Page config
# ─────────────────────────────────────────
st.set_page_config(
    page_title="LifeCare AI",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────
# CSS Styling
# ─────────────────────────────────────────
st.markdown("""
<style>
section[data-testid="stSidebar"], div[data-testid="stSidebarNav"] { display: none !important; }

.block-container { padding-top: 1rem; padding-bottom: 1rem; }
.title { text-align: center; font-size: 48px; font-weight: bold; color: #1B4F72; }
.desc { text-align: center; font-size: 18px; color: #444; margin: 8px auto; line-height: 1.6; max-width: 700px; }
.disclaimer { margin-top: 12px; background-color: #fff3cd; padding: 10px; border-radius: 8px; border: 1px solid #ffc107; color: #856404; text-align: center; font-size: 14px; }
.spacer { margin-top: 25px; }

div.stButton > button {
    background: linear-gradient(90deg, #007BFF, #00C6FF);
    color: white;
    font-size: 16px;
    padding: 5px 19px;
    border-radius: 10px;
    border: none;
    height: 45px;
    transition: 0.3s;
}
div.stButton > button:hover { transform: scale(1.05); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# Session state defaults
# ─────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ─────────────────────────────────────────
# Page 1 — Home
# ─────────────────────────────────────────
if st.session_state.page == "home":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo.png", width=330)

    st.markdown("""
    <div class="desc">
        LifeCare AI is an intelligent medical assistant powered by advanced language models.<br>
        It analyzes user symptoms and provides meaningful insights in real time.<br>
        Built to enhance accessibility with AI-driven support and user-friendly interaction.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="disclaimer">
    ⚠️ This application is for informational purposes only and is not a substitute for professional medical advice.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.page = "details"
            st.rerun()

# ─────────────────────────────────────────
# Page 2 — Personal Details
# ─────────────────────────────────────────
elif st.session_state.page == "details":
    st.markdown("<h1 style='text-align: center;'>🩺 LifeCare AI</h1>", unsafe_allow_html=True)
    st.subheader("User Verification")

    name   = st.text_input("Enter your full name")
    age    = st.number_input("Enter your age", min_value=0)
    gender = st.radio("Select Gender", ["Male", "Female", "Other"])

    st.write("")
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        if st.button("Next", use_container_width=True):
            if name.strip() != "" and age > 0:
                st.session_state.name   = name
                st.session_state.age    = age
                st.session_state.gender = gender
                st.session_state.page   = "symptoms"
                st.rerun()
            else:
                st.warning("Please fill valid details")

# ─────────────────────────────────────────
# Page 3 — Symptoms
# ─────────────────────────────────────────
elif st.session_state.page == "symptoms":
    st.markdown("<h1 style='text-align: center;'>🩺 LifeCare AI</h1>", unsafe_allow_html=True)

    st.success(
        f"✅ {st.session_state.name} verified! "
        f"Age: {st.session_state.age}, Gender: {st.session_state.gender}"
    )
    st.subheader("Enter Symptoms")

    symptoms = st.text_area("Describe your symptoms")

    uploaded_file = st.file_uploader(
        "Upload your image or report",
        type=["png", "jpg", "pdf"]
    )

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        if uploaded_file.type in ["image/png", "image/jpeg"]:
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                st.image(uploaded_file, caption="Preview", width=100)
            with col2:
                st.markdown(f"**{uploaded_file.name}**")
                st.caption(f"{round(uploaded_file.size / 1024, 1)} KB")
        elif uploaded_file.type == "application/pdf":
            import fitz
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            page = doc[0]
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat)
            img = Image.open(io.BytesIO(pix.tobytes("png")))

            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(img, caption=f"Page 1 of {len(doc)}", width=160)
            with col2:
                st.markdown(f"**📄 {uploaded_file.name}**")
                st.caption(f"{round(uploaded_file.size / 1024, 1)} KB  •  {len(doc)} page(s)")

    st.write("")
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        analyze_clicked = st.button("Analyze", use_container_width=True)

    if analyze_clicked:
        if symptoms.strip() == "":
            st.warning("Please enter symptoms first!")
        else:
            with st.spinner("Analyzing with AI... 🤖"):
                prompt = f"""
                You are a helpful medical assistant.
                User details:
                Name: {st.session_state.name}
                Age: {st.session_state.age}
                Gender: {st.session_state.gender}

                Symptoms:
                {symptoms}

                Provide a structured analysis:
                - Summary of symptoms
                - Possible causes
                - Recommended next steps
                """
                try:
                    ai_output = analyze_with_groq(prompt)
                    st.session_state.ai_result = ai_output
                except Exception as e:
                    st.error(f"Error analyzing: {e}")

    if "ai_result" in st.session_state and st.session_state.ai_result:
        st.markdown("---")
        st.markdown("## 🤖 AI Analysis Result")
        st.markdown(st.session_state.ai_result)
