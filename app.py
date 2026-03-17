
import streamlit as st
import sys
import os
from groq import Groq

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from guidelines import MODEL_GUIDELINES, VARIANT_INSTRUCTIONS
from enhancer import enhance_all_variants, score_prompt, compare_scores

st.set_page_config(
    page_title="AI Prompt Enhancer",
    page_icon="✨",
    layout="wide"
)

def get_client():
    if "GROQ_API_KEY" in st.secrets:
        return Groq(api_key=st.secrets["GROQ_API_KEY"])
    api_key = st.session_state.get("api_key", "")
    if api_key:
        return Groq(api_key=api_key)
    return None

st.title("✨ AI Prompt Enhancer")
st.markdown("Transform a rough prompt into an optimised version tailored for your target AI model.")
st.markdown("---")

with st.sidebar:
    st.header("About")
    st.markdown("""
Paste any rough prompt, select your target AI model,
and get three optimised versions with before/after quality scores.

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
    st.header("How it works")
    st.markdown("""
1. Paste your rough prompt
2. Select your target AI model
3. Click Enhance
4. Get 3 optimised versions
5. See before/after quality scores
    """)
    st.markdown("---")
    st.markdown("Built with Groq · LLaMA 3.3 · Streamlit")

col1, col2 = st.columns([1, 1])

with col1:
    user_prompt = st.text_area(
        "Your prompt",
        placeholder="e.g. write me a python function",
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

if enhance_btn:
    client = get_client()
    if not client:
        st.error("API key not found. Please add your Groq API key in the sidebar.")
    elif not user_prompt.strip():
        st.warning("Please enter a prompt to enhance.")
    else:
        with st.spinner("Analysing and enhancing your prompt..."):
            before_scores = score_prompt(client, user_prompt)
            variants      = enhance_all_variants(client, user_prompt, target_model)
            best_variant  = variants["detailed"]
            after_scores  = score_prompt(client, best_variant)
            comparison    = compare_scores(before_scores, after_scores)

        st.markdown("---")
        st.subheader("📊 Quality improvement")

        metric_cols = st.columns(4)
        dims = list(comparison.keys())
        for i, dim in enumerate(dims):
            data = comparison[dim]
            delta = f"+{data['improvement']}" if data['improvement'] > 0 else str(data['improvement'])
            metric_cols[i].metric(
                label=dim.capitalize(),
                value=f"{data['after']}/10",
                delta=delta
            )

        total_before = sum(before_scores.values())
        total_after  = sum(after_scores.values())
        improvement  = total_after - total_before
        st.info(f"Overall: {total_before}/40 → {total_after}/40  (+{improvement} points improvement)")

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
