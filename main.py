import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_docker_containers():
    try:
        containers = os.popen("docker ps --format '{{.Names}}'").read().strip().split("\n")
        return containers if containers[0] else []
    except Exception as e:
        return []

# Получение логов контейнера
def get_docker_logs(container_name):
    try:
        logs = os.popen(f"docker logs {container_name} --tail 50").read()
        return logs
    except Exception as e:
        return f"Ошибка: {str(e)}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь команду /containers, чтобы выбрать контейнер и посмотреть его логи."
    )


async def containers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    container_list = get_docker_containers()
    
    if not container_list:
        await update.message.reply_text("Контейнеры не найдены!")
        return

    # Создаем кнопки для контейнеров
    keyboard = [
        [InlineKeyboardButton(container, callback_data=f"logs:{container}")]
        for container in container_list
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Выберите контейнер для просмотра логов:", reply_markup=reply_markup
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data.startswith("logs:"):
        container_name = data.split(":")[1]
        logs = get_docker_logs(container_name)

        await query.edit_message_text(
            f"Логи контейнера `{container_name}`:\n\n{logs[-4000:]}"
        )

if __name__ == "__main__":
    TOKEN = "TOKEN"

    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("containers", containers))
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    application.run_polling()
