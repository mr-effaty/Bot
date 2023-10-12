import logging
from time import sleep
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from rps import RPS
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

ingame = lgdone = botworking = False
winner_point = 0
round_number = 1
empty_keyboard = [[]]
rps_keyboard = [['سنگ','کاغذ','قیچی']]


def start(bot: Bot, update: Update):
    global botworking
    botworking = True
    update.message.reply_text('به بازی سنگ کاغذ قیچی خوش اومدی! 🤗\nچند دست می خوای با هم بازی کنیم؟ 🤔')

def cancel(bot: Bot, update: Update):
    global ingame, lgdone, winner_point, round_count, round_number, botworking
    ingame = lgdone = botworking = False
    winner_point = 0
    round_number = 1
    update.message.reply_text('بازی متوقف شد.\nاگه خواستی دوباره بازی کنی کافیه بنویسی /start\nمن همینجا منتظرم. 😉',reply_markup= ReplyKeyboardMarkup(empty_keyboard,one_time_keyboard=True))

def round_input(bot: Bot, update: Update, isdigit):
    if isdigit:
        global round_count, ingame
        round_count = int(update.message.text)
        update.message.reply_text(f'اوکی پس {round_count} دست با هم بازی می کنیم.\nهرجا خسته شدی بنویس /cancel تا همونجا بازی رو متوقف کنیم \nبریم؟', reply_markup = ReplyKeyboardMarkup(keyboard=[['بزن بریم!']],one_time_keyboard=True))
        ingame = True
    else:
        update.message.reply_text('رفیق یه *عدد* بنویس خواهشا! صفر و منفی هم نباشه .')

def game_luncher(bot: Bot, update: Update):
    global round_number, round_count, ingame, lgdone, botworking, winner_point
    if round_count != 0:
        update.message.reply_text(f'دست {round_number}',reply_markup= ReplyKeyboardMarkup(empty_keyboard,one_time_keyboard=True))
        sleep(0.3)
        update.message.reply_text('سنگ',reply_markup= ReplyKeyboardMarkup(empty_keyboard,one_time_keyboard=True))
        sleep(0.3)
        update.message.reply_text('کاغذ',reply_markup= ReplyKeyboardMarkup(empty_keyboard,one_time_keyboard=True))
        sleep(0.3)
        update.message.reply_text('قیچی...',reply_markup= ReplyKeyboardMarkup(rps_keyboard,one_time_keyboard=True))
        round_count -= 1
        round_number += 1
    else:
        round_number -= 1
        if winner_point > 0:
            update.message.reply_text(f'بعد از {round_number} دست *تو برنده کل بازی شدی!* 🎉')
        elif winner_point < 0:
            update.message.reply_text(f'بعد از {round_number} دست *من برنده کل بازی شدم!* 🤗')
        else:
            update.message.reply_text(f'بعد از {round_number} دست *ما مساوی شدیم!* 😎')
        update.message.reply_text('بازی دیگه تموم شد. اما اگه می خوای بازم بازی کنی کافیه بنویسی /start \nمن همینجا منتظرم. 😉',reply_markup=ReplyKeyboardMarkup(empty_keyboard,one_time_keyboard=True))
        ingame = lgdone = botworking = False
        winner_point = 0
        round_number = 1

def game_judge(bot: Bot, update: Update):
    global winner_point
    game = RPS(update.message.text)
    update.message.reply_text(f'من {game.bot_choice} رو انتخاب کردم پس {game.winer_string}')
    winner_point += game.win_status

def conversation_handler(bot: Bot, update: Update):
    global ingame, round_count, round_number, lg_done
    if not ingame and botworking:
        try:
            if int(update.message.text) > 0:
                round_input(bot, update, True)
            else:
                round_input(bot, update, False)
        except:
            round_input(bot, update, False)
    elif ingame and update.message.text == 'بزن بریم!':
        lg_done = True
        game_luncher(bot, update)
    elif ingame and lg_done and (update.message.text == 'سنگ' or update.message.text == 'کاغذ' or update.message.text == 'قیچی'):
        game_judge(bot, update)
        game_luncher(bot, update)



def main():
    updater = Updater(token="88669327:9DYGLT5zJiv8xzQPNEK6NayXgffGtJY4rKdNxUL7",base_url="https://tapi.bale.ai/")
    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('cancel',cancel))
    dp.add_handler(MessageHandler(Filters.text,conversation_handler))

    updater.start_polling(poll_interval=1)
    updater.idle()

if __name__ == '__main__':
    main()