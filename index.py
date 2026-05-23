import os
import yt_dlp
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters
)


BOT_TOKEN = os.getenv("8842212414:AAGzm_cbm5-oDwenDfea5gplo2Hbp1ZS2lw") 


async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:

        await update.message.reply_text(
            "Відправ YouTube посилання"
        )

        return

    await update.message.reply_text(
        "Завантажую аудіо..."
    )

    output_file = "%(title)s.%(ext)s"

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'quiet': True,
    'noplaylist': True,
    'retries': 10,
    'fragment_retries': 10,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

    try:

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            title = info.get("title", "audio")

            filename = f"{title}.mp3"

        for file in os.listdir():

            if file.endswith(".mp3"):

                filename = file

                break

        await update.message.reply_audio(
            audio=open(filename, "rb")
        )

        os.remove(filename)

    except Exception as e:

        await update.message.reply_text(
            f"Помилка: {e}"
        )


app = (
    ApplicationBuilder()
    .token(BOT_TOKEN)
    .connect_timeout(30)
    .read_timeout(30)
    .write_timeout(30)
    .pool_timeout(30)
    .build()
)

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        download_audio
    )
)

print("Bot started...")

app.run_polling()
