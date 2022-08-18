
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


api_id = 13429252
api_hash = "33d94e2daae5c7777f0d9b59a72ab0a6"
bot_token = "5540973513:AAGoNjBtP5w8IADXLGhuzz3n1zdmYkWkJVk"
channel = -1001633495002

bot = Client("Zero", api_id, api_hash, bot_token=bot_token, plugins=dict(root="plugins"))




scores = {}  # {uid: {"name": NAME, "score": 0}}


@bot.on_message(filters.chat("AS222002") & ~filters.command("start") & ~filters.command("results"))
async def Q(_, msg: Message):
    data = msg.text.split("\n")
    qe = data[0]
    buttons = []
    for line in data[1:]:
        if line.startswith("."):
            tr = "a"
            line = line[1:]
        else:
            tr = "b"
        buttons.append([InlineKeyboardButton(line, tr)])
    reply_markup_ = InlineKeyboardMarkup(buttons)
    await bot.send_message(channel, qe, reply_markup=reply_markup_)


@bot.on_message(filters.command("start"))
async def start(_, msg: Message):
    await msg.reply_text("السلام عليكم ورحمة الله وبركاته\n لنبدأ الاختبار")


@bot.on_message(filters.command("results"))
async def results(_, msg: Message):
    text = "results:\n"
    for user in scores.values():
        text += f"{user['name']}: {user['score']}\n"
    await msg.reply_text(text)


@bot.on_callback_query()
async def callback(_, cb: CallbackQuery):
    data = cb.data
    uid = cb.from_user.id
    if uid not in scores:
        name = cb.from_user.first_name
        scores[uid] = {"name": name, "score": 0}
    if data == "a":
        scores[uid]["score"] += 1
        await cb.answer(f'حسنت تم إضافة نقطة إلى رصيدك - {scores[uid]["score"]}', show_alert=True)
    else:
        await cb.answer(f'للأسف إجابة خاطئة - {scores[uid]["score"]}', show_alert=True)
    
    keyboard = cb.message.reply_markup.inline_keyboard
    buttons = []
    for row in keyboard:
        row = []
        for button in row:
        	if button.data == "a":
        		row.append(InlineKeyboardButton('✅' + button.text, button.data))
        	else:
        		row.append(InlineKeyboardButton('❌' + button.text, button.data))
        	buttons.append(row)
    reply_markup = InlineKeyboardMarkup(buttons)
    await cb.message.edit_reply_markup(reply_markup=reply_markup)

bot.run()











    


