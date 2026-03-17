
import streamlit as st
import sys
import os
from groq import Groq

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from setup_rag import setup
setup()

from guidelines import MODEL_GUIDELINES, VARIANT_INSTRUCTIONS
from enhancer import enhance_all_variants, score_prompt, compare_scores

st.set_page_config(
    page_title="AI Prompt Enhancer",
    page_icon="✨",
    layout="wide"
)

INDEX_DIR = os.path.join(os.path.dirname(__file__), "data", "faiss_index")

def get_client():
    if "GROQ_API_KEY" in st.secrets:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    api_key = st.session_state.get("api_key", "")
    if api_key:
        return Groq(api_key=api_key)
    return None

def rag_available():
    return os.path.exists(os.path.join(INDEX_DIR, "papers.index"))

st.title("✨ AI Prompt Enhancer")
st.markdown("Transform a rough prompt into an optimised version — backed by published AI research papers.")
st.markdown("---")

with st.sidebar:
    st.header("About")
    rag_status = "✅ Active" if rag_available() else "⚠️ Not available"
    st.markdown(f"**Research RAG:** {rag_status}")
    st.markdown("""
**Papers used:**
- Chain-of-Thought Prompting
- Zero-Shot Reasoners
- Self-Consistency
- Tree of Thoughts
- ReAct
- Least-to-Most Prompting

**Supported models:**
Claude · ChatGPT · Gemini · DeepSeek · Grok
    """)
    if "GROQ_API_KEY" not in st.secrets:
        st.markdown("---")
        st.header("API Key")
        api_key_input = st.text_input(
            "Groq API Key",
            type="password",
            placeholder="gsk_..."
        )
        if api_key_input:
            st.session_state["api_key"] = api_key_input
        st.markdown("Get a free key at [console.groq.com](https://console.groq.com)")
    st.markdown("---")
    st.markdown("Built with Groq · LLaMA 3.3 · FAISS · Streamlit")

col1, col2 = st.columns([1, 1])

with col1:
    user_prompt = st.text_area(
        "Your prompt",
        placeholder="e.g. help me solve a complex math problem",
        height=150
    )
    target_model = st.selectbox(
        "Target AI model",
        options=list(MODEL_GUIDELINES.keys())
    )
    model_info = MODEL_GUIDELINES[target_model]["description"]
    st.caption(f"📋 {model_info}")
    enhance_btn = st.button(
        "✨ Enhance my prompt",
        type="primary",
        use_container_width=True
    )

with col2:
    st.markdown("**How it works**")
    st.markdown("""
1. Your prompt is embedded and matched against research paper chunks
2. The top 3 most relevant research findings are retrieved
3. Those findings are injected into the enhancement instruction
4. The LLM enhances your prompt using both model guidelines and research context
5. Three variants are returned — concise, detailed, with examples
    """)

if enhance_btn:
    client = get_client()
    if not client:
        st.error("API key not found. Please add your Groq API key in the sidebar.")
    elif not user_prompt.strip():
        st.warning("Please enter a prompt to enhance.")
    else:
        index_dir = INDEX_DIR if rag_available() else None

        with st.spinner("Retrieving research context and enhancing your prompt..."):
            before_scores = score_prompt(client, user_prompt)
            variants      = enhance_all_variants(
                client, user_prompt, target_model, index_dir
            )
            best_variant  = variants["detailed"]
            after_scores  = score_prompt(client, best_variant)
            comparison    = compare_scores(before_scores, after_scores)

        st.markdown("---")
        st.subheader("📊 Quality improvement")

        metric_cols = st.columns(4)
        dims = list(comparison.keys())
        for i, dim in enumerate(dims):
            data  = comparison[dim]
            delta = f"+{data['improvement']}" if data['improvement'] > 0 else str(data['improvement'])
            metric_cols[i].metric(
                label=dim.capitalize(),
                value=f"{data['after']}/10",
                delta=delta
            )

        total_before = sum(before_scores.values())
        total_after  = sum(after_scores.values())
        improvement  = total_after - total_before
        st.info(f"Overall: {total_before}/40 → {total_after}/40  (+{improvement} points)")

        if rag_available():
            st.caption("✅ Enhancement informed by research papers")
        else:
            st.caption("⚠️ Running without RAG — index not found")

        st.markdown("---")
        st.subheader("✨ Enhanced versions")

        tab1, tab2, tab3 = st.tabs(["Concise", "Detailed", "With examples"])

        with tab1:
            st.markdown("**Best for:** Quick tasks, simple instructions")
            st.text_area("", value=variants["concise"], height=200, key="concise")

        with tab2:
            st.markdown("**Best for:** Complex tasks, detailed requirements")
            st.text_area("", value=variants["detailed"], height=200, key="detailed")

        with tab3:
            st.markdown("**Best for:** Structured output, format-specific tasks")
            st.text_area("", value=variants["with_examples"], height=200, key="examples")

        st.markdown("---")
        with st.expander("🔍 View original prompt"):
            st.text(user_prompt)
            st.caption(f"Original quality score: {total_before}/40")
