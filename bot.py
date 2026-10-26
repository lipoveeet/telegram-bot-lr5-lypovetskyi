"""Telegram bot for Cloud Technologies lab 5 (hosted on AWS EC2).
Author: Lypovetskyi Bohdan, PI-23-03.

The bot token is read from the BOT_TOKEN environment variable (.env file),
it is never stored in the repository.
A small HTTP status page runs on port 8081.
"""
import os
import platform
import threading
from datetime import datetime, timezone

import telebot
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise SystemExit("BOT_TOKEN is not set (create .env, see .env.example)")

bot = telebot.TeleBot(TOKEN)
web = Flask(__name__)
STARTED = datetime.now(timezone.utc)
stats = {"messages": 0}


@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(m, f"Привіт, {m.from_user.first_name}! Я бот ЛР5 з хмарних технологій.\n"
                    "Я працюю на сервері AWS EC2. Команди: /help")


@bot.message_handler(commands=["help"])
def help_cmd(m):
    bot.reply_to(m, "/start - привітання\n/help - список команд\n/info - про автора\n"
                    "/server - інформація про сервер\n/time - час на сервері\n"
                    "Будь-який інший текст я повторю.")


@bot.message_handler(commands=["info"])
def info(m):
    bot.reply_to(m, "Лабораторна робота №5, Хмарні технології.\n"
                    "Виконав: Липовецький Богдан, ПІ-23-03.")


@bot.message_handler(commands=["server"])
def server(m):
    up = datetime.now(timezone.utc) - STARTED
    bot.reply_to(m, f"Хост: {platform.node()}\nОС: {platform.platform()}\n"
                    f"Python: {platform.python_version()}\nБот працює: {str(up).split('.')[0]}")


@bot.message_handler(commands=["time"])
def time_cmd(m):
    bot.reply_to(m, "Час на сервері (UTC): " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))


@bot.message_handler(func=lambda m: True)
def echo(m):
    stats["messages"] += 1
    bot.reply_to(m, "Ви написали: " + (m.text or ""))


@web.route("/")
def status():
    me = bot.get_me()
    return jsonify(bot=f"@{me.username}", status="running", host=platform.node(),
                   started_utc=STARTED.isoformat(timespec="seconds"), echo_messages=stats["messages"])


if __name__ == "__main__":
    threading.Thread(target=lambda: web.run(host="0.0.0.0", port=8081), daemon=True).start()
    print("Bot @%s started, status page on port 8081" % bot.get_me().username, flush=True)
    bot.infinity_polling(skip_pending=True)
