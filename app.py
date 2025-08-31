import streamlit as st
import model as nlp  # Import your backend logic
import base64

# Function to encode local image to base64
def get_base64_of_image(image_path):
    """Encodes a local image file to a base64 string."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Background image '{image_path}' not found. Please make sure it's in the same folder as app.py.")
        return None

# Get base64 string of your background image
bg_image_base64 = get_base64_of_image("tbbt.jpg")

# Custom CSS with background image + improvements
custom_css = f"""
<style>
    @keyframes fadeInUp {{
        0% {{ opacity: 0; transform: translateY(20px); }}
        100% {{ opacity: 1; transform: translateY(0); }}
    }}
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image_base64 if bg_image_base64 else ''}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .main .block-container {{
        max-width: 900px;
        padding: 1rem 2rem;
    }}
    
    /* Remove whitespace between elements */
    .main .block-container > div {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* Remove default Streamlit spacing */
    .element-container {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    
    /* Remove gap between your title and content */
    .main .block-container {{
        gap: 0 !important;
    }}
    
    /* Force elements to stick together */
    div[data-testid="stMarkdownContainer"] {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    h1 {{
        font-family: 'Garamond', serif;
        font-weight: 600;
        color: #f0f0f0;
        text-align: center;
        animation: fadeInUp 0.5s ease-out forwards;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
        margin-bottom: 0 !important; /* Remove space under title */
    }}
    .stButton > button {{
        background-image: linear-gradient(45deg, #007aff, #00A8E8);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 12px 35px;
        font-size: 1.2rem;
        transition: all 0.3s;
        display: block;
        margin: 0 auto;
    }}
    .stButton > button:hover {{
        opacity: 0.9;
        box-shadow: 0 0 15px rgba(0, 122, 255, 0.5);
    }}
    .stTextInput > div > div > input {{
        background-color: rgba(255, 255, 255, 0.6);
        border: 1px solid #ccc;
        border-radius: 8px;
        color: #111;
        font-size: 1.6rem !important;
        text-align: center;
    }}
    .episode-info {{
        font-size: 1.8rem !important;
        color: #007aff;
        text-align: center;
        margin-top: 0.2rem;
        margin-bottom: 0.8rem;
        font-weight: 700;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }}
    hr {{
        border: none;
        height: 2px;
        background: linear-gradient(to right, #007aff, #00A8E8);
        margin: 10px auto 20px auto;
        width: 100%;
    }}
    
    /* Increase font size for tabs and output content */
    .stTabs [data-baseweb="tab-list"] {{
        font-size: 1.8rem !important;
    }}
    
    .stTabs [data-baseweb="tab-panel"] {{
        font-size: 1.8rem !important;
    }}
    
    /* Target the subheaders in tabs */
    .stTabs h3 {{
        font-size: 1.8rem !important;
    }}
    
    /* Target the generated text output */
    .stTabs p, .stTabs div[data-testid="stMarkdownContainer"] {{
        font-size: 1.8rem !important;
        line-height: 1.4 !important;
    }}
    
    /* Target the bold n-gram labels specifically */
    .stTabs strong {{
        font-size: 1.8rem !important;
    }}
    
    /* Caption text (perplexity description) */
    .stTabs .stCaption {{
        font-size: 1.3rem !important;
    }}
</style>
"""

# Define the built-in corpus files
CORPUS_FILES = (
    "TheBigBangTheory.Season01 1.Episode02",
    "TheBigBangTheory.Season01 1.Episode03",
    "TheBigBangTheory.Season01 3.Episode01",
)

@st.cache_data
def load_inbuilt_corpus():
    """Loads the built-in corpus files and preprocesses them."""
    all_text = ""
    for file_path in CORPUS_FILES:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                all_text += f.read() + " "
        except FileNotFoundError:
            st.error(f"Error: The file '{file_path}' was not found.")
            return None
    return nlp.preprocess_text(all_text)

# --- Streamlit App UI ---
st.set_page_config(layout="centered")
st.markdown(custom_css, unsafe_allow_html=True) 

# --- Title ---
st.markdown("<h1>The Big Bang Theory Dialogue Generator</h1>", unsafe_allow_html=True)

# --- Content Box ---
st.markdown('<div class="content-box">', unsafe_allow_html=True)

# --- Season Info ---
st.markdown('<p class="episode-info">Season 1 Episode 1-3</p>', unsafe_allow_html=True)

# --- Separator ---
st.markdown("<hr>", unsafe_allow_html=True)

# --- Model Config Section ---
st.markdown(
    "<div style='text-align: center;'><h3>Model Configuration</h3></div>",
    unsafe_allow_html=True,
)

# --- Sliders ---
col1, col2 = st.columns([1, 1], gap="large")
with col1:
    max_n = st.slider("Select Max N-Gram Order", 2, 7, 5)
with col2:
    sentence_len = st.slider("Select Sentence Length", 5, 30, 12)

# --- Text Input ---
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
start_phrase = st.text_input("Enter Starting Words", value="sheldon said")
st.markdown("</div>", unsafe_allow_html=True)

# --- Generate Button (Centered by CSS) ---
generate_button = st.button("Generate")

st.markdown('</div>', unsafe_allow_html=True)

# --- Model Output ---
tokens = load_inbuilt_corpus()
if tokens and generate_button:
    st.markdown("---") 
    start_words = tuple(start_phrase.lower().split()) if start_phrase else ("sheldon", "said")
    vocab = set(tokens)
    
    tab1, tab2 = st.tabs(["Generated Sentences", "Model Analysis"])

    with tab1:
        st.subheader("Model Output")
        for n_val in range(2, max_n + 1):
            model = nlp.build_ngram_model(tokens, n_val)
            generated = nlp.generate_sentence(model, n_val, start_words, sentence_len, vocab)
            st.write(f"**{n_val}-gram:** {generated}")

    with tab2:
        st.subheader("Perplexity Scores")
        st.caption("Lower perplexity generally indicates a better model.")
        for n_val in range(2, max_n + 1):
            model = nlp.build_ngram_model(tokens, n_val)
            perplexity = nlp.calculate_perplexity(model, n_val, tokens, vocab)
            st.write(f"**{n_val}-gram Perplexity:** `{perplexity:.2f}`")