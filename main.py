import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


ASK_NAME, ASK_AGE = range(2)


async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        'Привет! Удобно Вам здесь получить информацию?',
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton('Поделиться контактом', request_contact=True)]],
            one_time_keyboard=True
        )
    )
    return ASK_NAME


async def contact_handler(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text('Спасибо! Как вас зовут?')
    return ASK_NAME

# Функция для обработки имени пользователя
async def name_handler(update: Update, context: CallbackContext) -> int:
    user_name = update.message.text
    context.user_data['name'] = user_name
    await update.message.reply_text(f'Приятно познакомиться, {user_name}! Сколько лет Вашему ребенку?')
    return ASK_AGE

# Функция для обработки возраста ребенка
async def age_handler(update: Update, context: CallbackContext) -> int:
    child_age = update.message.text
    await update.message.reply_text(f'Спасибо за информацию! В ближайшее время мы с Вами свяжемся!')
    return ConversationHandler.END

def main() -> None:
    # Вставьте сюда ваш токен
    application = Application.builder().token("").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.CONTACT, contact_handler), MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age_handler)],
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()