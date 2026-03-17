
import sys
import os
sys.path.append(os.path.dirname(__file__))

from groq import Groq
from guidelines import MODEL_GUIDELINES, VARIANT_INSTRUCTIONS, SCORING_CRITERIA
from retriever import load_index, retrieve, format_context

_index = None
_meta  = None

def get_index(index_dir: str):
    global _index, _meta
    if _index is None:
        _index, _meta = load_index(index_dir)
    return _index, _meta

def create_client(api_key: str) -> Groq:
    return Groq(api_key=api_key)

def enhance_prompt(
    client: Groq,
    user_prompt: str,
    target_model: str,
    variant: str,
    index_dir: str = None
) -> str:
    if target_model not in MODEL_GUIDELINES:
        raise ValueError(f"Unknown model: {target_model}")
    if variant not in VARIANT_INSTRUCTIONS:
        raise ValueError(f"Unknown variant: {variant}")

    guidelines   = MODEL_GUIDELINES[target_model]["system_prompt"]
    variant_inst = VARIANT_INSTRUCTIONS[variant]

    research_context = ""
    if index_dir and os.path.exists(index_dir):
        try:
            index, meta      = get_index(index_dir)
            results          = retrieve(user_prompt, index, meta, top_k=3)
            research_context = "\n\n" + format_context(results)
        except Exception:
            research_context = ""

    full_system = f"{guidelines}\n\nVariant instruction: {variant_inst}{research_context}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": full_system},
            {"role": "user",   "content": f"Enhance this prompt: {user_prompt}"}
        ],
        max_tokens=600,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def enhance_all_variants(
    client: Groq,
    user_prompt: str,
    target_model: str,
    index_dir: str = None
) -> dict:
    results = {}
    for variant in VARIANT_INSTRUCTIONS:
        results[variant] = enhance_prompt(
            client, user_prompt, target_model, variant, index_dir
        )
    return results

def score_prompt(client: Groq, prompt_text: str) -> dict:
    scoring_system = """You are a prompt quality evaluator.
Score the given prompt on these four dimensions, each from 0 to 10:
- clarity: Is the task unambiguous and easy to understand?
- specificity: Does it specify exactly what is needed?
- context: Does it provide sufficient background information?
- actionability: Can an AI act on this immediately without clarification?

Respond in this exact format with nothing else:
clarity: <score>
specificity: <score>
context: <score>
actionability: <score>"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": scoring_system},
            {"role": "user",   "content": f"Score this prompt: {prompt_text}"}
        ],
        max_tokens=60,
        temperature=0.1
    )

    raw    = response.choices[0].message.content.strip()
    scores = {}

    for line in raw.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            if key in SCORING_CRITERIA:
                try:
                    scores[key] = min(10, max(0, int(val.strip())))
                except ValueError:
                    scores[key] = 5

    for dim in SCORING_CRITERIA:
        if dim not in scores:
            scores[dim] = 5

    return scores

def compare_scores(before: dict, after: dict) -> dict:
    return {
        dim: {
            "before":      before[dim],
            "after":       after[dim],
            "improvement": after[dim] - before[dim]
        }
        for dim in before
    }
