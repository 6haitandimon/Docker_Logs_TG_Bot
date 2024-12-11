# Telegram Bot for Docker Logs

Этот проект представляет собой Telegram бота, который может отправлять логи из контейнеров Docker, запущенных с помощью Docker Compose, и предоставляет интерфейс для выбора контейнеров и получения их логов.

## Установка

### 1. Клонируйте репозиторий

Сначала клонируйте этот репозиторий на ваш локальный компьютер:

```bash
git clone https://github.com/your-username/Logs_bot.git
cd Logs_bot
```
### 2. Установите зависимости
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate  # Для Windows

pip install -r requirements.txt
```
## Укажите Token
В файле main.py:
Замените your-telegram-bot-token на настоящий токен вашего бота, который можно получить у BotFather


## По желанию
Можно так же создать демон для автоматическгого запуска и перезапуска бота в случае ошибок.
Если вы хотите, чтобы бот запускался автоматически при старте системы, создайте systemd unit-файл:
```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/project/main.py
WorkingDirectory=/path/to/your/project
Restart=always
RestartSec=5
StandardOutput=append:/var/log/telegram-bot.log
StandardError=append:/var/log/telegram-bot.log
User=your-username
Group=your-group

[Install]
WantedBy=multi-user.target
```

Команды для запуска демона:

```bash
sudo systemctl daemon-reload
sudo systemctl start telegram-bot.service
sudo systemctl enable telegram-bot.service
```