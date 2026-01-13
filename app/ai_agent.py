import os
import requests
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# ENV CONFIG


HF_API_KEY = os.getenv("HF_API_KEY")


HF_MODEL = "distilgpt2"


HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

HF_HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json"
}

# HUGGING FACE INFERENCE


def generate_with_hf(prompt: str) -> Optional[str]:
    """
    Call Hugging Face free inference API.
    Returns generated text if successful, otherwise None.
    """

    if not HF_API_KEY:
        print("HF_API_KEY not set")
        return None

    try:
        response = requests.post(
            HF_API_URL,
            headers=HF_HEADERS,
            json={"inputs": prompt},
            timeout=30
        )

        if response.status_code != 200:
            # Common: 503 (model loading / busy)
            print("HF inference error:", response.status_code, response.text)
            return None

        data = response.json()

        # Expected response format:
        # [{'generated_text': '...'}]
        if isinstance(data, list) and len(data) > 0:
            if isinstance(data[0], dict) and "generated_text" in data[0]:
                return data[0]["generated_text"]

        return None

    except Exception as e:
        print("HF exception:", e)
        return None


# =========================
# ORCHESTRATOR 
# =========================

def generate_recipe(prompt: str) -> str:
    """
    Orchestrator:
    1. Try Hugging Face
    2. If unavailable → deterministic fallback
    """

    # 1 Try Hugging Face
    hf_result = generate_with_hf(prompt)
    if hf_result:
        return hf_result

    # 2️ Guaranteed fallback (query-aware)
    keyword = prompt.split()[0].title() if prompt else "Simple"

    return (
        f"Recipe Name: {keyword} Home-Style Recipe\n"
        f"Ingredients: Main ingredient, oil, spices, vegetables\n"
        f"Steps:\n"
        f"1. Prepare all ingredients\n"
        f"2. Heat oil and add spices\n"
        f"3. Add main ingredient and cook thoroughly\n"
        f"4. Add vegetables and simmer\n"
        f"5. Serve hot\n"
        f"Cuisine: Indian\n"
        f"Preparation Time: 30–40 minutes\n"
        f"(Fallback response due to AI service unavailability)"
    )
