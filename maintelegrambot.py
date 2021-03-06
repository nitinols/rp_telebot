import telebot
import time
from threading import Thread
import keyboa
from keyboa import Keyboa
import RPi.GPIO as GPIO


# telebot setup
bot = telebot.TeleBot('1827375393:AAEyVqBwJ59JiWUTscbw775UbY4Zy1d-XRY')

BOT_READI = 1

gpio_list = [6, 12, 13]

backlight_options = ['Вариант 1', 'Вариант 2', 'Вариант 3']
kb_backlight = Keyboa(items=backlight_options, copy_text_to_callback=True).keyboard
# end setup


def GPIO_Rasberry(gp06, gp12, gp13, id_user_chat):  # setup and change gpi voluem
    global BOT_READI
    GPIO.setmode(GPIO.BCM)
    BOT_READI = 0
    GPIO.setup(gpio_list, GPIO.OUT)
    GPIO.output(gpio_list, GPIO.LOW)
    if gp06:
        GPIO.output(6, GPIO.HIGH)
    elif gp12:
        GPIO.output(12, GPIO.HIGH)
    elif gp13:
        GPIO.output(13, GPIO.HIGH)
    bot.send_message(id_user_chat, 'Подсветка моста изменена')
    time.sleep(300)
    bot.send_message(id_user_chat, 'Можете выбрать подсветку моста снова')
    BOT_READI = 1
    GPIO.output(gpio_list, GPIO.LOW)



@bot.message_handler(commands=['start'])
def start_message(message):
    #bot.send_message(message.chat.id, 'Привет! Выбери цвет и режим подсветки моста')
    bot.send_message(
        message.chat.id, reply_markup=kb_backlight,
        text="Привет! Выбери цвет и режим подсветки моста:")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if BOT_READI:
        if call.data == 'Вариант 1':
                    bot.send_message(call.message.chat.id, 'подсветка изменяется на Вариант 1')
                    th = Thread(target=GPIO_Rasberry, args=(1, 0, 0, call.message.chat.id))
                    th.start()
        elif call.data == 'Вариант 2':
                    bot.send_message(call.message.chat.id, 'подсветка изменяется на Вариант 2')
                    th = Thread(target=GPIO_Rasberry, args=(0, 1, 0, call.message.chat.id))
                    th.start()

        elif call.data == 'Вариант 3':
                    bot.send_message(call.message.chat.id, 'подсветка изменяется на Вариант 3')
                    th = Thread(target=GPIO_Rasberry, args=(0, 0, 1, call.message.chat.id))
                    th.start()
    else:
        bot.send_message(call.message.chat.id, 'Подождите, вы не можете менять подсветку так часто')


@bot.message_handler(commands=['help'])
def start_messager(message):
    pass



bot.polling()
