# -----------------------
# أول حاجة: الاستيراد
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from server import keep_alive
keep_alive()
import os
import yt_dlp
# -----------------------

BOT_TOKEN = "8252000774:AAGmJsqlkxAz-GXSCwcg6NguvOr2vdHo6r8"

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ydl_opts = {
    'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
    'format': 'best',
    'quiet': True,
    'merge_output_format': 'mp4'
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ابعتلي أي لينك فيديو أو صورة من:\n"
        "TikTok\nInstagram\nFacebook\nYouTube\nTwitter/X\n\n"
        "و أنا أحملهولك مباشرة 🔥"
    )

async def downloader(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("⏳ جاري التحميل...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        if filename.endswith((".mp4", ".mkv", ".webm")):
            await update.message.reply_video(video=open(filename, 'rb'))
        else:
            await update.message.reply_document(document=open(filename, 'rb'))

        os.remove(filename)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ حصل خطأ: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), downloader))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
