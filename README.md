# ✨ AI Prompt Enhancer

A research-backed web app that transforms rough prompts into optimised 
versions tailored for specific AI models — powered by Groq and a RAG 
pipeline over published NLP research papers.

**Live demo:** https://prompt-enhancer-rohan.streamlit.app

---

## What it does

Paste any rough prompt, select your target AI model, and get back three 
enhanced versions — each applying that model's published best practices, 
grounded in findings from 6 peer-reviewed NLP research papers.

**Supported models:** Claude · ChatGPT · Gemini · DeepSeek · Grok

---

## Example

| | Score |
|---|---|
| Original: `help me solve a complex math problem` | 12/40 |
| Enhanced (DeepSeek, detailed variant) | 27/40 |

**Improvement: +15 points across clarity, specificity and context**

---

## How it works

1. **User pastes a rough prompt** and selects a target AI model
2. **RAG retrieval** — the prompt is embedded and matched against
   chunks from 6 research papers using FAISS vector search
3. **Research context** — top 3 relevant findings are retrieved
   and injected into the enhancement instruction
4. **Model-specific guidelines** — Groq LLM enhances the prompt
   using both the model's published best practices and research context
5. **Three variants returned** — concise, detailed, with examples
6. **Before/after scoring** — four dimensions scored 0-10 each

---

## Research foundation

This app uses a RAG pipeline to retrieve relevant findings from
6 published NLP research papers at inference time:

| Paper | Authors | Key finding |
|-------|---------|-------------|
| Chain-of-Thought Prompting | Wei et al., Google (2022) | Step-by-step reasoning improves complex tasks |
| Zero-Shot Reasoners | Kojima et al. (2022) | "Think step by step" boosts accuracy |
| Self-Consistency | Wang et al., Google (2022) | Multiple reasoning paths improve reliability |
| Tree of Thoughts | Yao et al., Princeton (2023) | Explore reasoning branches for hard problems |
| ReAct | Yao et al., Princeton (2022) | Combine reasoning with action steps |
| Least-to-Most Prompting | Zhou et al., Google (2022) | Break complex problems into sub-problems |

---

## Prompt scoring dimensions

Each prompt is scored before and after enhancement across four dimensions:

| Dimension | Question |
|-----------|----------|
| Clarity | Is the task unambiguous and easy to understand? |
| Specificity | Does it specify exactly what is needed? |
| Context | Does it provide sufficient background information? |
| Actionability | Can the model act on this immediately? |

---

## Tech stack

Python · Groq API · LLaMA 3.3 70B · FAISS · sentence-transformers ·
PyMuPDF · Streamlit · GitHub

---

## Project structure
prompt-enhancer/
├── app.py                    # Streamlit web app
├── setup_rag.py              # Downloads papers and builds index on startup
├── requirements.txt          # Dependencies
├── src/
│   ├── enhancer.py           # Core enhancement engine with RAG support
│   ├── guidelines.py         # Model-specific prompting guidelines
│   ├── ingest.py             # PDF ingestion and FAISS index builder
│   ├── retriever.py          # Vector search and context retrieval
│   └── startup.py            # Index availability check
└── data/
├── papers/               # Downloaded research PDFs (runtime only)
└── faiss_index/          # Built FAISS index (runtime only)

---

## Run locally
```bash
git clone https://github.com/rohansairongala/prompt-enhancer.git
cd prompt-enhancer
pip install -r requirements.txt
streamlit run app.py
```

On first run the app downloads the research papers and builds
the FAISS index automatically. Subsequent runs load instantly.

---

## What I learned

- Building a RAG pipeline from scratch — ingestion, chunking, embedding, retrieval
- FAISS vector search for semantic similarity matching
- Encoding domain knowledge into LLM system prompts
- Model-specific prompt engineering for 5 different AI models
- Connecting academic research findings to practical application
- Deploying a multi-component AI app to Streamlit Cloud
