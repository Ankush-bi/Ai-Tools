
import os
import openai

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Simple classifier using patterns + optional LLM fallback

def classify_link_with_llm(url: str) -> str:
    """
    Returns one of: 'youtube', 'image', 'direct_video', 'social', 'unknown'
    Uses simple pattern matching first. If OpenAI key is set, uses a tiny prompt to confirm.
    """
    u = url.lower()
    # Quick pattern checks
    if 'youtube.com' in u or 'youtu.be' in u:
        return 'youtube'
    if u.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
        return 'image'
    if u.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        return 'direct_video'
    # common social platforms
    if any(p in u for p in ['instagram.com', 'tiktok.com', 'twitter.com', 'x.com', 'facebook.com']):
        return 'social'

    # Fallback to LLM if key available
    if OPENAI_API_KEY:
        try:
            prompt = f"Classify this URL into one of: youtube, image, direct_video, social, unknown. URL: {url}\nReply with single word only."
            resp = openai.ChatCompletion.create(
                model='gpt-4o',
                messages=[{'role': 'user', 'content': prompt}],
                max_tokens=5
            )
            text = resp.choices[0].message['content'].strip().lower()
            # sanitize
            for choice in ['youtube', 'image', 'direct_video', 'social', 'unknown']:
                if choice in text:
                    return choice
        except Exception:
            pass

    return 'unknown'