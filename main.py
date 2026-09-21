import os
import telebot
from huggingface_hub import InferenceClient

# --- Чтение ключей из переменных окружения ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

# Проверка, что ключи на месте
if not TELEGRAM_TOKEN or not HF_TOKEN:
    raise ValueError("Не заданы ключи! Проверь секреты в GitHub.")

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Инициализация клиента Hugging Face
# Заменили модель на Mistral, так как Llama может требовать одобрения доступа
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    token=HF_TOKEN
)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот с ИИ. Напиши мне что-нибудь, и я постараюсь ответить.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_text = message.text
    
    # Показываем пользователю, что бот "печатает"
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # Отправляем запрос к ИИ
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": user_text}
            ],
            max_tokens=512,
            temperature=0.7
        )
        
        # Извлекаем текст ответа
        ai_answer = response.choices[0].message.content
        
        # Отправляем ответ в Telegram
        bot.reply_to(message, ai_answer)
        
    except Exception as e:
        # Логируем ошибку в консоль, чтобы видеть её на хостинге
        print(f"Ошибка при запросе к ИИ: {e}")
        bot.reply_to(message, "Извини, произошла ошибка. Попробуй позже.")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен и слушает сообщения...")
    bot.infinity_polling()
