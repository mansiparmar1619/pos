import streamlit as st
import pandas as pd
import stanza

st.set_page_config(page_title="POS Tagger Pro", layout="centered")

# Load model
@st.cache_resource
def load_pipeline(lang):
    return stanza.Pipeline(lang=lang, processors='tokenize,pos', verbose=False)

# 🎨 CSS (Clean + Professional)
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #2b5876, #4e4376);
}

/* Card container */
.block-container {
    background-color: white;
    padding: 2rem;
    border-radius: 15px;
    max-width: 750px;
    margin-top: 40px;
}

/* Title */
h1 {
    text-align: center;
    color: #1f2937;
}

/* Inputs */
textarea, div[data-baseweb="select"] {
    background-color: #f3f4f6 !important;
    color: black !important;
    border-radius: 10px !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-weight: bold;
    font-size: 16px;
}

/* Tag styling */
.tag {
    padding: 6px 12px;
    margin: 5px;
    border-radius: 20px;
    display: inline-block;
    font-size: 14px;
    font-weight: 500;
}

</style>
""", unsafe_allow_html=True)

# 🧠 Title
st.title("🧠 POS Tagger Pro")
st.markdown("<p style='text-align:center;'>Indian Languages NLP Tool</p>", unsafe_allow_html=True)

# Inputs
lang = st.selectbox("🌐 Select Language", ["hi", "mr", "ta"])
text = st.text_area("✍️ Enter Text", "भारत में भाषा विविधता है।", height=150)

# Run button
if st.button("🚀 Run Tagger"):
    with st.spinner("Processing..."):
        nlp = load_pipeline(lang)
        doc = nlp(text)

        data = []
        for sent in doc.sentences:
            for w in sent.words:
                data.append({"Word": w.text, "POS Tag": w.upos})

        df = pd.DataFrame(data)

    # ✅ SAFE TABLE (NO ERROR)
    st.subheader("📊 Output Table")
    st.dataframe(df)

    # 🎨 Color Mapping
    TAG_COLORS = {
        'NOUN': '#fde68a',
        'VERB': '#86efac',
        'ADJ': '#93c5fd',
        'ADV': '#f9a8d4',
        'PRON': '#67e8f9',
        'NUM': '#fcd34d',
        'DET': '#fef08a',
        'ADP': '#bbf7d0',
        'CONJ': '#ddd6fe',
        'PART': '#fdba74',
        'INTJ': '#e5e7eb',
        'X': '#cbd5f5',
        'PUNCT': '#f1f5f9'
    }

    # 🎨 Visual Output
    st.subheader("🎨 Tagged Output")

    html = ""
    for _, row in df.iterrows():
        tag = row["POS Tag"] if row["POS Tag"] else "X"
        color = TAG_COLORS.get(tag, "#cbd5f5")

        html += f"""
        <span class='tag' style='background:{color}; color:black'>
            {row["Word"]} / {tag}
        </span>
        """

    st.markdown(html, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("⚡ Built with Streamlit + Stanza")