import telebot
from huggingface_hub import InferenceClient

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

if not TELEGRAM_TOKEN or not HF_TOKEN:
    raise ValueError("Не заданы ключи!")

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Инициализация клиента Hugging Face
client = InferenceClient(
    model="meta-llama/Llama-3.2-3B-Instruct",
    token=HF_TOKEN
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот с ИИ. Напиши мне что-нибудь, и я постараюсь ответить.")

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
        print(f"Ошибка при запросе к ИИ: {e}")
        bot.reply_to(message, "Извини, произошла ошибка. Попробуй позже.")

if __name__ == "__main__":
    print("Бот запущен и слушает сообщения...")
    bot.infinity_polling()
