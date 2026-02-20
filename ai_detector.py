from google import genai

client = genai.Client(api_key="PASTE_YOUR_API_KEY_HERE")

def analyze_message_ai(message):
    prompt = f"""
    You are a cybersecurity expert.
    Analyze this message and tell if it's a scam.
    Give:
    1. Risk score from 1-10
    2. Reasons why it's dangerous or safe
    Message: {message}
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    msg = input("Paste a message: ")
    print(analyze_message_ai(msg))
