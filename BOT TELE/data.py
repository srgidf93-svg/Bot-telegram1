import pandas as pd
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Charger Excel
df = pd.read_excel("data.xlsx")
df = df.astype(str)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()

    # Recherche dans toutes les colonnes
    results = df[df.apply(
        lambda row: row.str.lower().str.contains(query).any(),
        axis=1
    )]

    if not results.empty:
        row = results.iloc[0]

        # Réponse avec entêtes en gras
        response = "\n".join(
            f"🔹 <b>{col} :</b> {row[col]}"
            for col in df.columns
        )
    else:
        response = "Aucun résultat"

    # IMPORTANT : activer HTML
    await update.message.reply_text(response, parse_mode="HTML")

# Bot Telegram
app = ApplicationBuilder().token("8706109528:AAHgoj3NHnWUvPhggsXz7_MSh4DtwXzmnpw").build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()