
# 🌐 Chainlit Translator Bot

Welcome to the Translator Bot created by Humema Israr!  
Built using **Chainlit**, **Python**, and the **Gemini API**.

## ✨ Features
- Translate text into multiple languages (e.g., Urdu, Arabic, French)
- Interactive chat interface using Chainlit
- Session and language management
- Chat history saved to JSON

## 🚀 How to Run

```bash
git clone https://github.com/humemaisrar-github-account/chainlit-translator-bot.git
cd chainlit-translator-bot
pip install -r requirements.txt
cp .env.example .env
# Then add your GEMINI_API_KEY in the .env file
chainlit run trans-agent.py
