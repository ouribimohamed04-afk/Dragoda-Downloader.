import telebot
import yt_dlp
import os

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحبا بيك فـ Dragoda Downloader! صيفط ليا أي رابط باش نحملو ليك. 🚀")

@bot.message_handler(func=lambda message: message.text.startswith('http'))
def handle_link(message):
    bot.reply_to(message, "⏳ جاري المعالجة...")
    try:
        ydl_opts = {'outtmpl': 'downloads/media.%(ext)s', 'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([message.text])
        for file in os.listdir('downloads/'):
            if file.startswith('media'):
                f_path = os.path.join('downloads/', file)
                with open(f_path, 'rb') as f:
                    if file.endswith(('.mp4', '.mov')): bot.send_video(message.chat.id, f)
                    else: bot.send_photo(message.chat.id, f)
                os.remove(f_path)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

bot.polling()
