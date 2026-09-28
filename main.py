import os
import telebot
from huggingface_hub import InferenceClient

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

if not TELEGRAM_TOKEN or not HF_TOKEN:
    raise ValueError("Не заданы ключи!")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

client = InferenceClient(
    model="microsoft/Phi-3.5-mini-instruct",
    token=HF_TOKEN
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот с ИИ. Напиши мне что-нибудь.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_text = message.text
    bot.send_chat_action(message.chat.id, 'typing')
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": user_text}],
            max_tokens=512,
            temperature=0.7
        )
        ai_answer = response.choices[0].message.content
        bot.reply_to(message, ai_answer)
    except Exception as e:
        # ВРЕМЕННО: показываем реальную ошибку прямо в Telegram
        bot.reply_to(message, f"ОШИБКА: {type(e).__name__}\n\n{str(e)[:500]}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()
