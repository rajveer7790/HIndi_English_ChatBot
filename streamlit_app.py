import streamlit as st
import google.generativeai as genai
import os

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    st.error("Please set the GEMINI_API_KEY environment variable")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Hinglish Gemini Chatbot", page_icon="🤖")
st.title("🤖 Hinglish Gemini Chatbot")
st.write("Chat in Hinglish (Hindi + English)! / Hinglish mein baat karein!")

# Button to show available models
if st.button("Show available Gemini models"):
    try:
        models = genai.list_models()
        st.info("Available models:")
        for m in models:
            st.write(f"- {m.name}")
    except Exception as e:
        st.error(f"[Error]: {str(e)}")

# Automatically detect the best available model
@st.cache_resource(show_spinner=False)
def get_best_model_name():
    try:
        models = genai.list_models()
        # Prefer latest recommended models
        preferred = [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-1.0-pro",
            "text-bison-001"
        ]
        for pname in preferred:
            for m in models:
                if pname in m.name:
                    return m.name
        # Otherwise, use the first available model
        if models:
            return models[0].name
    except Exception as e:
        st.warning(f"[Error]: {str(e)}")
    return None

MODEL_NAME = get_best_model_name()
if not MODEL_NAME:
    st.error(
        "No supported Gemini model found for your API key. Please check your key and API access."
    )
    st.stop()

st.success(f"Using Gemini model: {MODEL_NAME}")

# Strong system prompt for Hinglish, friendly, casual style with examples
SYSTEM_PROMPT = (
    "Tum ek mast, bindass AI ho jo sirf Hinglish (Hindi+English mix) mein, dosto ki tarah, short aur funny style mein reply karta hai. "
    "Kabhi bhi explain mat karo ki Hinglish kya hai, ya user ka sentence ka matlab kya hai. "
    "Bas seedha Hinglish mein, casual aur friendly jawab do. Hamesha Hinglish mein hi reply karo.\n"
    "Examples:\n"
    "User: kase ho\n"
    "Assistant: Bilkul badiya yaar, tu sunaa!\n"
    "User: Sunday ko kya plan hai?\n"
    "Assistant: Shayd movie dekhne ka plan hai, tu chalega?\n"
    "User: mujhe ek chai pilao\n"
    "Assistant: Lo bhai, ek garma garam chai aa gayi!\n"
    "User: homework ho gaya?\n"
    "Assistant: Arre yaar, aadha ho gaya, baaki kal kar lunga.\n"
    "User: tumhara favourite color kya hai?\n"
    "Assistant: Blue sabse zyada pasand hai mujhe!\n"
    "User: cricket pasand hai?\n"
    "Assistant: Bilkul! Cricket toh dil se khelta hoon.\n"
    "User: thum mere se hinglish me bhat karo\n"
    "Assistant: Bilkul, ab se sirf Hinglish mein baat karenge!\n"
)

# Initialize chat history (no 'system' role for Gemini)
if "messages" not in st.session_state or not st.session_state["messages"]:
    # Add system prompt as a hidden first user message (not shown in UI)
    st.session_state["messages"] = [
        {"role": "user", "content": SYSTEM_PROMPT, "_internal": True}
    ]

# Display chat history (skip hidden system prompt)
for msg in st.session_state["messages"]:
    if msg.get("_internal"):
        continue  # Don't show the hidden system prompt
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Assistant:** {msg['content']}")

# Convert chat history to Gemini's expected format (skip system/internal messages)
def convert_to_gemini_format(messages):
    out = []
    for msg in messages:
        if msg.get("_internal"):
            continue  # Skip hidden system prompt
        role = "model" if msg["role"] == "assistant" else msg["role"]
        out.append({
            "role": role,
            "parts": [msg["content"]]
        })
    return out

# Use a form to handle input and button together (auto-clears input)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your Hinglish message...")
    send_clicked = st.form_submit_button("Send")

# Only process if button clicked and input is not empty
if send_clicked and user_input:
    # Prevent double send by checking last user message
    last_msg = (
        st.session_state["messages"][-1]
        if st.session_state["messages"] else None
    )
    is_duplicate = (
        last_msg and last_msg["role"] == "user"
        and last_msg["content"] == user_input
    )
    if not is_duplicate:
        st.session_state["messages"].append({
            "role": "user",
            "content": user_input
        })
        # Send last 10 messages (plus hidden system prompt) as context
        history_to_send = st.session_state["messages"][-10:]
        # Always prepend the hidden system prompt as first message
        if st.session_state["messages"] and st.session_state["messages"][0].get("_internal"):
            history_to_send = [st.session_state["messages"][0]] + history_to_send
        gemini_history = convert_to_gemini_format(history_to_send)
        with st.spinner(f"Gemini ({MODEL_NAME}) soch raha hai..."):
            try:
                model = genai.GenerativeModel(MODEL_NAME)
                response = model.generate_content(gemini_history)
                bot_reply = response.text.strip()
            except Exception as e:
                bot_reply = f"[Error]: {str(e)}"
        st.session_state["messages"].append({
            "role": "assistant",
            "content": bot_reply
        })
# No need to clear input manually; st.form(clear_on_submit=True) handles it 