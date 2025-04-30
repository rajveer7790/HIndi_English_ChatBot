# Hinglish Chatbot with Gemini AI

A Streamlit-based chat application that allows users to chat in Hinglish (Hindi + English) using Google's Gemini AI.

## Features

- Natural Hinglish conversation
- Powered by Google's Gemini AI
- Simple and intuitive interface
- Real-time chat experience

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/rajveer7790/Hinglish-Chatbot.git
   cd Hinglish-Chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Gemini API key as an environment variable:
   - Windows (PowerShell):
     ```powershell
     $env:GEMINI_API_KEY="your-api-key-here"
     ```
   - Linux/Mac:
     ```bash
     export GEMINI_API_KEY="your-api-key-here"
     ```

4. Run the application:
   ```bash
   streamlit run streamlit_app.py
   ```

## Project Structure

- `streamlit_app.py` - Main application file
- `requirements.txt` - Project dependencies
- `README.md` - This documentation file

## How to Use

1. Start the application using the command above
2. Open your web browser and navigate to the provided local URL
3. Start chatting in Hinglish!
4. The bot will respond in a friendly, casual Hinglish style

## Dependencies

- streamlit
- google-generativeai
- python-dotenv

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for the powerful language model
- Streamlit for the amazing web framework 