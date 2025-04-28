import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key="AIzaSyAS9ReMCGSnUVS9cOwTXM5bXp7oY4WXsXM")

# Set page config
st.set_page_config(
    page_title="Norabot AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .chat-message {
            padding: 1rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            display: flex;
            max-width: 80%;
        }
        .user-message {
            background-color: #4a8cff;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 5px !important;
        }
        .bot-message {
            background-color: #ffffff;
            color: #333;
            margin-right: auto;
            border-bottom-left-radius: 5px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stTextInput>div>div>input {
            border-radius: 20px;
            padding: 10px 15px;
        }
        .stButton>button {
            border-radius: 20px;
            padding: 10px 25px;
            background-color: #4a8cff;
            color: white;
            border: none;
        }
        .stButton>button:hover {
            background-color: #3a7bef;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #5b86e5 0%, #36d1dc 100%);
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Static knowledge base for Kampus Merdeka          
kampus_merdeka_faq = {
    "Apa itu Kampus Merdeka?": "Kampus Merdeka adalah program dari Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi untuk memberikan kebebasan kepada mahasiswa dalam memilih mata kuliah dan kegiatan kampus yang relevan dengan minat dan karir mereka.",
    "Apa saja program yang ada di Kampus Merdeka?": "Beberapa program Kampus Merdeka antara lain Program Magang, Program Studi Independen, Program Pertukaran Mahasiswa, dan Program Proyek Independen.",
    "Bagaimana cara mendaftar program Kampus Merdeka?": "Untuk mendaftar, mahasiswa bisa mengunjungi situs resmi Kampus Merdeka atau mengikuti informasi yang diberikan oleh kampus terkait program yang tersedia.",
    "Siapa yang bisa mengikuti Kampus Merdeka?": "Program Kampus Merdeka terbuka untuk seluruh mahasiswa yang terdaftar di perguruan tinggi yang bekerja sama dengan program ini.",
    "Apa itu Norabot?": "Norabot adalah aplikasi chatbot informasi tentang Kampus Merdeka yang memberikan penjelasan tentang pelaksanaan, persyaratan, dan program yang ada di Kampus Merdeka. Norabot adalah teman informasi kamu untuk segala hal terkait Kampus Merdeka!",
    "Siapa yang menciptakan Norabot?": "Norabot diciptakan oleh Nora dari kelas 4IA10. Dengan ide kreatif dan semangat tim yang luar biasa, walaupun banyak rintangan dan drama, mereka berhasil menciptakan Norabot saat ini untuk membantu mahasiswa memahami lebih banyak tentang Kampus Merdeka."
}


# Sidebar
with st.sidebar:
    st.title("🤖 Norabot - Kampus Merdeka")
    st.markdown("""
    **Apa itu Norabot?**
                
    Norabot adalah aplikasi chatbot informasi tentang Kampus Merdeka yang memberikan penjelasan tentang pelaksanaan, persyaratan, dan program yang ada di Kampus Merdeka. Norabot adalah teman informasi kamu untuk segala hal terkait Kampus Merdeka!
    """)
    
    st.markdown("---")
    
    st.markdown("**Model Options**")
    # Update the model selection dropdown to allow dynamic model choice
    model_name = st.selectbox(
        "Pilih Model Gemini",
        ["models/gemini-1.5-flash", "models/gemini-1.5-pro"],
        index=0
    )
    
    temperature = st.slider("Kreativitas (Temperature)", 0.0, 1.0, 0.7)
    max_tokens = st.slider("Panjang Maksimum Jawaban", 100, 2000, 1000)
    
    st.markdown("---")
    st.markdown("Made with ❤️ using Norabot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to get Gemini response
def get_gemini_response(prompt, model_name):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )
    return response.text

# Function to get Kampus Merdeka response (from static knowledge base)
def get_kampus_merdeka_response(prompt):
    if prompt in kampus_merdeka_faq:
        return kampus_merdeka_faq[prompt]
    else:
        return get_gemini_response(prompt, model_name)

# Chat input with custom response logic
if prompt := st.chat_input("Apa yang ingin Anda tanyakan tentang Kampus Merdeka?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Menghasilkan jawaban..."):
            try:
                response = get_kampus_merdeka_response(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Terjadi error: {str(e)}")
