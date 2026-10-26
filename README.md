# Telegram bot — ЛР5 (Хмарні технології)

Simple Telegram bot hosted on an AWS EC2 instance (Amazon Linux 2023).
Author: Lypovetskyi Bohdan, PI-23-03.

## Commands
`/start`, `/help`, `/info`, `/server`, `/time`; any other text is echoed back.

## Run on EC2
```bash
sudo yum install -y git python3-pip
git clone https://github.com/lipoveeet/telegram-bot-lr5-lypovetskyi.git
cd telegram-bot-lr5-lypovetskyi
pip3 install -r requirements.txt
cp .env.example .env   # put the token from @BotFather into .env
nohup python3 bot.py > bot.log 2>&1 &
```
A status page is available on port **8081** (open it in the EC2 security group).
The token is kept only in `.env`, which is excluded by `.gitignore`.
