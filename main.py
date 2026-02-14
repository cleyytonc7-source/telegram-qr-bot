import os
import qrcode
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ QR Bot online.\n\n"
        "Use:\n"
        "/qr <texto ou link> → gera QR Code\n\n"
        "Exemplo:\n"
        "/qr https://instagram.com/wutratores"
    )

async def qr_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Use assim: /qr <texto ou link>")
        return

    texto = " ".join(context.args)
    img = qrcode.make(texto)
    path = "/tmp/qr.png"
    img.save(path)

    await update.message.reply_photo(photo=open(path, "rb"), caption=f"QR gerado para:\n{texto}")

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /qr <texto ou link>")

def main():
    if not TOKEN:
        raise RuntimeError("Defina a variável BOT_TOKEN com seu token do BotFather.")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("qr", qr_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback))

    app.run_polling()

if __name__ == "__main__":
    main()
