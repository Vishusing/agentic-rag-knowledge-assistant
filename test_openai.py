
from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL

print("API key loaded:", bool(OPENAI_API_KEY))
print("Model:", OPENAI_MODEL)

client = OpenAI(api_key=OPENAI_API_KEY)

try:
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "user", "content": "Say hello"}
        ],
        max_tokens=50
    )

    print("SUCCESS!")
    print(response.choices[0].message.content)

except Exception as e:
    print("ERROR TYPE:", type(e).__name__)
    print("ERROR DETAILS:", str(e))
