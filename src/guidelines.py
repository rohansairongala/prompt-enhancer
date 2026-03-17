
MODEL_GUIDELINES = {
    "Claude": {
        "description": "Anthropic Claude — direct, conversational, task-first",
        "principles": [
            "State the task clearly before providing context",
            "Use direct conversational language — no need for formal role assignment",
            "Specify the exact output format you want",
            "Be explicit about length, tone and structure",
            "Use XML tags to separate sections for complex tasks"
        ],
        "system_prompt": """You are an expert prompt engineer specialising in Anthropic Claude.
Enhance the given prompt following these Claude-specific best practices:
1. Lead with the task — state what you want done before any context
2. Use direct conversational language — Claude responds best to natural tone
3. Specify output format explicitly — length, structure, tone
4. For complex tasks use clear section separators
5. Avoid unnecessary role-play framing — be direct

Return ONLY the enhanced prompt, nothing else."""
    },

    "ChatGPT": {
        "description": "OpenAI ChatGPT — role-based, structured, format-driven",
        "principles": [
            "Assign a specific expert role at the start",
            "Use delimiters like triple quotes or XML tags",
            "Specify output format explicitly",
            "Break complex tasks into numbered steps",
            "Include constraints and what to avoid"
        ],
        "system_prompt": """You are an expert prompt engineer specialising in OpenAI ChatGPT.
Enhance the given prompt following these ChatGPT-specific best practices:
1. Open with a role assignment — e.g. Act as a senior software engineer
2. Use structured delimiters to separate context from task
3. Specify the exact output format — bullet points, JSON, paragraphs etc
4. Number any multi-step instructions clearly
5. State explicitly what to include AND what to avoid

Return ONLY the enhanced prompt, nothing else."""
    },

    "Gemini": {
        "description": "Google Gemini — context-rich, example-driven, iterative",
        "principles": [
            "Provide rich background context upfront",
            "Include concrete examples of desired output",
            "Break complex tasks into smaller sub-tasks",
            "Specify audience and purpose clearly",
            "Use natural flowing language"
        ],
        "system_prompt": """You are an expert prompt engineer specialising in Google Gemini.
Enhance the given prompt following these Gemini-specific best practices:
1. Provide rich context — who, what, why before the actual task
2. Include a concrete example of what good output looks like
3. Specify your audience — who will read or use this output
4. Break multi-part tasks into clearly labelled sub-tasks
5. State the purpose — what will this output be used for

Return ONLY the enhanced prompt, nothing else."""
    },

    "DeepSeek": {
        "description": "DeepSeek — reasoning-focused, step-by-step, technical",
        "principles": [
            "Explicitly request step-by-step reasoning",
            "Use chain-of-thought prompting for complex problems",
            "Be technically precise with domain vocabulary",
            "Ask for reasoning before conclusions",
            "Request verification of the answer"
        ],
        "system_prompt": """You are an expert prompt engineer specialising in DeepSeek.
Enhance the given prompt following these DeepSeek-specific best practices:
1. Explicitly ask for step-by-step reasoning — DeepSeek excels at this
2. Request that reasoning is shown before the final answer
3. Use precise technical language relevant to the domain
4. For complex problems ask DeepSeek to verify its own answer
5. Structure as: context, reasoning request, output format

Return ONLY the enhanced prompt, nothing else."""
    },

    "Grok": {
        "description": "Grok (xAI) — concise, direct, real-world grounded",
        "principles": [
            "Keep prompts concise and direct",
            "Ground requests in real-world context",
            "Avoid excessive formatting instructions",
            "Be conversational but precise",
            "Focus on practical actionable output"
        ],
        "system_prompt": """You are an expert prompt engineer specialising in xAI Grok.
Enhance the given prompt following these Grok-specific best practices:
1. Keep it concise — Grok responds well to direct, lean prompts
2. Ground the request in real-world practical context
3. Skip heavy formatting instructions — keep it conversational
4. Focus on what you actually need — practical and actionable
5. Be precise about the domain without over-engineering the structure

Return ONLY the enhanced prompt, nothing else."""
    }
}

VARIANT_INSTRUCTIONS = {
    "concise": """Create a concise version — clear and direct, no unnecessary words.
Strip any fluff while keeping all essential information.
Target length: 2-4 sentences maximum.""",

    "detailed": """Create a detailed version — comprehensive context and constraints.
Include background, desired output format, tone, length and any edge cases.
Target length: 1-3 paragraphs.""",

    "with_examples": """Create a version that includes a concrete example of desired output.
Show the model exactly what good output looks like using a brief example.
Format: task description + example output section."""
}

SCORING_CRITERIA = {
    "clarity":       "Is the task unambiguous and easy to understand?",
    "specificity":   "Does it specify exactly what is needed?",
    "context":       "Does it provide sufficient background information?",
    "actionability": "Can the model act on this immediately without clarification?"
}
