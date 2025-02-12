import streamlit as st
from model import predict_outfit
import time

# Page Configuration
st.set_page_config(
    page_title="Fashion AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
    }
    
    /* Header */
    .header {
        background: linear-gradient(45deg, #161729, #004e92) !important;
        margin: -6rem -4rem 2rem -4rem;
        padding: 8rem 4rem 4rem 4rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 50px rgba(59,130,246,0.3); }
        100% { box-shadow: 0 0 100px rgba(59,130,246,0.5); }
    }
    
    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at center, transparent 0%, rgba(0,0,0,0.3) 100%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.3; }
        50% { opacity: 0.7; }
        100% { opacity: 0.3; }
    }
    
    .header h1 {
        font-size: 4.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(0,0,0,0.3);
        animation: slideDown 1s ease-out, glowText 3s ease-in-out infinite alternate;
    }
    
    @keyframes glowText {
        0% { text-shadow: 0 0 20px rgba(255,255,255,0.3); }
        100% { text-shadow: 0 0 40px rgba(255,255,255,0.5); }
    }
    
    .header p {
        font-size: 1.5rem;
        color: rgba(255,255,255,0.9);
        animation: fadeIn 1s ease-out 0.5s both;
    }
    
    /* Input Section */
    .input-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid rgba(59,130,246,0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        margin: 2rem auto;
        max-width: 1000px;
        animation: slideUp 1s ease-out;
        text-align: center;
    }
    
    /* Input Fields */
    .stTextInput  {
        background: rgba(15, 23, 42, 0.8) !important;
        border: 2px solid rgba(59,130,246,0.2) !important;
        border-radius: 12px !important;
        padding: 1.8rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput input {
        color: #60a5fa !important;
        # margin-bottom : 100px;  
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.5px !important;
    }
    
    .stTextInput > label {
        color: #93c5fd !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    
    .stTextInput > div > div:focus-within {
        background: rgba(15, 23, 42, 0.9) !important;
        border-color: #3b82f6 !important;
        box-shadow: 0 0 20px rgba(59,130,246,0.3) !important;
        transform: translateY(-2px);
    }
    
    /* Button */
    .stButton > button {
        background: linear-gradient(45deg, #161729, #004e92) !important;
        color: white !important;
        padding: 1rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 0 30px rgba(59,130,246,0.3) !important;
        width: 100% !important;
        margin-top: 1rem !important;
        
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 30px rgba(99,102,241,0.3);
    }
            
    
    /* Results */
    .results-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2.5rem;
        border: 1px solid rgba(59,130,246,0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        margin: 2rem auto;
        max-width: 1000px;
        animation: fadeIn 0.5s ease-out;
        text-align: center;
            height: 10%;
        # font-size: 1.2rem;
    }
    
    .result-card {
        background: rgba(15, 23, 42, 0.8);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid rgba(59,130,246,0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(59,130,246,0.1), transparent);
        transform: translateX(-100%);
        transition: transform 0.5s;
    }
    
    .result-card:hover::before {
        transform: translateX(100%);
    }
    
    .result-card:hover {
        border-color: #3b82f6;
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 0 30px rgba(59,130,246,0.3);
    }
    
    .result-title {
        color: #93c5fd;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        letter-spacing: 0.5px;
    }
    
    .result-value {
        color: #60a5fa;
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    /* Style Tips */
    .tips-container {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        padding: 2.5rem;
        border-radius: 20px;
        border: 1px solid rgba(59,130,246,0.2);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        margin: 2rem auto;
        max-width: 1000px;
        animation: slideUp 0.5s ease-out;
    }
    
    .tips-title {
        color: #93c5fd;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 1px;
    }
    
    .tip-item {
        background: rgba(15, 23, 42, 0.8);
        padding: 1.5rem;
        margin-bottom: 1rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: slideRight 0.5s ease-out;
        color: #60a5fa;
        font-size: 1.1rem;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    .tip-item:hover {
        transform: translateX(10px);
        background: rgba(15, 23, 42, 0.9);
        box-shadow: 0 0 30px rgba(59,130,246,0.2);
    }
    
    /* Animations */
    @keyframes slideDown {
        from {
            transform: translateY(-100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes slideUp {
        from {
            transform: translateY(100px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideRight {
        from {
            transform: translateX(-50px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #1d4ed8) !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

# Rest of your code remains the same
# Header
st.markdown("""
    <div class="header">
        <h1>Fashion AI</h1>
        <p>Discover Your Perfect Style Combination</p>
    </div>
""", unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-container">Let AI help you create the perfect outfit combination!</div>', unsafe_allow_html=True)
col1, space, col2 = st.columns([1, 0.1, 1])

with col1:
    blazer_input = st.text_input("Blazer Color", value="navy",
                                help="Enter your preferred blazer color")

with col2:
    pant_input = st.text_input("Pant Color", value="gray",
                              help="Enter your preferred pant color")

predict_button = st.button("Generate Perfect Match")
st.markdown('</div>', unsafe_allow_html=True)

if predict_button:
    try:
        # Loading Animation
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)
        progress.empty()
        
        # Get Predictions
        shirt, tie, shoe = predict_outfit(blazer_input, pant_input)
        
        # Display Results
        st.markdown('<div class="results-container">Your Curated Ensemble</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">Shirt</div>
                    <div class="result-value">{shirt.title()}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">Tie</div>
                    <div class="result-value">{tie.title()}</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown(f"""
                <div class="result-card">
                    <div class="result-title">Shoes</div>
                    <div class="result-value">{shoe.title()}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Style Tips
        st.markdown("""
            <div class="tips-container">
                <div class="tips-title">Expert Style Tips</div>
                <div class="tip-item">Match leather accessories (belt, shoes, watch strap) for a cohesive look</div>
                <div class="tip-item">Choose a tie that's slightly darker than your shirt for optimal contrast</div>
                <div class="tip-item">Consider seasonal colors and fabric weights for the perfect ensemble</div>
                <div class="tip-item">Balance patterns - if one piece is bold, keep others subtle</div>
            </div>
        """, unsafe_allow_html=True)
        
    except ValueError as e:
        st.error(str(e))
