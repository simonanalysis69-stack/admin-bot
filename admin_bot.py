import telebot, os, json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN=os.getenv("TOKEN")
ADMIN_ID=5739385019

bot=telebot.TeleBot(TOKEN)

PACKS=[500,1000,4000]

def file(p): return f"codes_{p}.txt"

def stock(p):
    try: return len([x for x in open(file(p)).read().splitlines() if x.strip()])
    except: return 0

orders=json.load(open("orders.json"))

def save(): json.dump(orders,open("orders.json","w"))

def take(p,q):
    with open(file(p)) as f:
        c=[x for x in f.read().splitlines() if x.strip()]
    if len(c)<q: return []
    out=c[:q]
    with open(file(p),"w") as f:
        f.write("\n".join(c[q:]))
    return out

@bot.message_handler(commands=["start"])
def start(m):
    if m.chat.id!=ADMIN_ID: return
    kb=InlineKeyboardMarkup()
    for p in PACKS:
        kb.add(InlineKeyboardButton(f"{p} stock: {stock(p)}",callback_data="none"))
    bot.send_message(m.chat.id,"Admin Stock Panel:",reply_markup=kb)

@bot.message_handler(commands=["orders"])
def orders_cmd(m):
    if m.chat.id!=ADMIN_ID: return
    for oid,o in orders.items():
        kb=InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("Verify",callback_data=f"v{oid}"))
        bot.send_message(m.chat.id,f"Order {oid} | {o['pack']} x {o['qty']}",reply_markup=kb)

@bot.callback_query_handler(func=lambda c:c.data.startswith("v"))
def verify(c):
    oid=c.data[1:]
    o=orders[oid]
    codes=take(o["pack"],o["qty"])
    if not codes:
        bot.send_message(c.message.chat.id,"No stock left")
        return
    bot.send_message(
        o["user"],
        "✅ Payment Verified!\n\nCodes:\n"+ "\n".join(codes)
    )
    del orders[oid]
    save()

bot.infinity_polling()
