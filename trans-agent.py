
import os
import json
import re
from dotenv import load_dotenv
import chainlit as cl
from litellm import completion

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

# 🔹 On chat start
@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    cl.user_session.set("language_selected", False)

    await cl.Message(
        author="🌍 Translator Bot",
        content=(
            "**Welcome to the Translator Agent by Humema Israr!** 🌐\n\n"
            "Please type the language you want to translate **into** (e.g., Urdu, Arabic, French):\n\n"
            
        )
    ).send()

# 🔹 On message
@cl.on_message
async def on_message(message: cl.Message):
    chat_history = cl.user_session.get("chat_history") or []
    language_selected = cl.user_session.get("language_selected", False)
    msg_text = message.content.strip()

    # Handle language change
    if msg_text.lower() == "/change":
        cl.user_session.set("language_selected", False)
        await cl.Message(
            content="🔁 Language reset.\n\nPlease type the new language you want to translate into:"
        ).send()
        return

    text_to_translate = msg_text
    target_language = cl.user_session.get("target_language")

    # Step 1: Try to extract language from the input like "translate into Urdu"
    if not language_selected:
        pattern = re.compile(r"translate into (\w+)", re.IGNORECASE)
        match = pattern.search(msg_text)
        if match:
            language = match.group(1)
            text_to_translate = pattern.sub("", msg_text).strip(" .:")
            cl.user_session.set("target_language", language)
            cl.user_session.set("language_selected", True)
            target_language = language
        else:
            # No "translate into" found, assume user typed only the language
            cl.user_session.set("target_language", msg_text)
            cl.user_session.set("language_selected", True)
            await cl.Message(
                content=f"✅ Language selected: **{msg_text}**\n\nNow enter the text you want to translate."
            ).send()
            return

    if not target_language:
        await cl.Message(
            content="⚠️ Please select a target language first by typing: Urdu, French, etc."
        ).send()
        return

    user_input = f"Translate this into {target_language}: {text_to_translate}"
    chat_history.append({"role": "user", "content": user_input})

    msg = cl.Message(content="🔄 Translating, please wait...")
    await msg.send()

    try:
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=gemini_api_key,
            messages=chat_history
        )

        translated_text = response.choices[0].message.content.strip()
        msg.content = f"🌐 **Translated to {target_language}:**\n\n{translated_text}"
        await msg.update()

        chat_history.append({"role": "assistant", "content": translated_text})
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        msg.content = f"❌ Error: {str(e)}"
        await msg.update()

# 🔹 On chat end
@cl.on_chat_end
async def on_chat_end():
    chat_history = cl.user_session.get("chat_history") or []
    with open("translation_chat_history.json", "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=2, ensure_ascii=False)
    print("✅ Chat history saved.")
