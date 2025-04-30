import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Replace 'ft-yourmodel' with your actual fine-tuned model name
model_name = "ft-yourmodel"

# List of new Hinglish prompts
prompts = [
    "Mujhe ek chai pilao.",
    "Aaj mausam kaisa hai?",
    "Kya tum kal aaoge?"
]

# Generate and print replies for each prompt
for prompt in prompts:
    # English: Send prompt to the model
    # Hindi: Prompt model ko bhejein
    resp = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0  # Default temperature for variety
    )
    print(f"User: {prompt}")
    print(f"Assistant: {resp.choices[0].message.content}\n") 