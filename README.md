### HomeAssistBot
### !!!БОТ НАХОДИТСЯ В СОСТОЯНИИ АЛЬФА-ВЕРСИИ!!!


Телеграмм бот созданный на основе библиотек aiogram (версии 3.0.7b) и homeassistant-api, для управления некоторыми сущностями, из данного списка: 
__'binary_sensor', 'sensor', 'button', 'light', 'switch'__. Бот использует асинхронное взаимодействие с СУБД PostgreSQL.
На данном этапе разработки общение с Home Assist происходит в синхронном варианте. 

Для установки бота необходим python3 не ниже версии 3.10, все остальные зависимости есть в файле requirements.txt.

Порядок установки бота на Linux-сервер, на примере Ubuntu-сервера:
Перед установкой бота убедитесь, что python у вас версии не ниже 3.10. На момент написания инструкции крайне рекомендуется версия 3.10.12.
Проверить версию python можно командой:

````bash
python3.10 -V
````

1. Установить СУБД PostgreSQL:
```bash
sudo apt -y install postgresql
```

2. Перейдите на пользователя postgres
```bash
sudo -i -u postgres
```
3. Создайте пользователя, который будет управлять СУБД. На этом моменте запомните пользователя.
````bash
createuser --interactive
````
4. Создайте Базу Данных для этого пользователя и перейдите на этого пользователя. После чего зайдите в СУБД под этим пользователем.
````bash
createdb <user>
sudo su - <user>
psql
````
5. Проверьте соединение
````bash
\conninfo
````
Вывод должен быть примерно таким:
````bash
You are connected to database "<user_name>" as user "<user_name>" via socket in "/var/run/postgresql" at port "5432".
````
6. При необходимости установите пароль для этого пользователя. Запомните этот пароль.
````bash
\password
````

7. С СУБД закончено, нужно установить бота. Установите, если нету, Git
```bash
sudo apt install git
git --version
```

8. Перейдите в домашний каталог, склонируйте этот репозиторий и перейдите в папку проекта:
```bash
cd ~
git clone https://github.com/ChronoDi/HomeAssistBot.git
cd HomeAssistBot/
````

9. Все настройки для бота должны храниться в файле .env, пример его заполнения есть в файле .env.dict. Создайте файл .env и откройте его с помощью редактора:
```bash
cp .env.dict .env
nano .env
```
**Все значения файла указываются без пробелов, списки пользователей без пробелов через запятую.**  
````nano
#Bot
BOT_TOKEN= Токен бота полученный от https://t.me/BotFather
ADMINS= Список администраторов, которые будут иметь возможность собирать комнаты
USERS= Список пользователей, которые смогут использовать готовые комнаты

#Redis
USE_REDIS=True Необходимость использовать Redis
REDIS_HOST=localhost адрес серварера Redis

#HomeAssist
HA_URL=http://localhost:8123/api адрес до Home Assistans API
HA_TOKEN= Токен для подключения к Home Assistant API

#Database
DB_HOST=localhost Адрес до psql сервера
DB_PORT=5432 порт psql
DB_USER= Пользователь, которого вы создали в шаге 4.
DB_PASSWORD= Пароль, который вы создали в шаге 6.
DB_NAME= База данных, которую вы создали в шаге 4.
````
10. Если будете использовать Redis, то его нужно установить:
```bash
sudo apt install redis
```

11. Убедитесь что вы все еще находитесь в папке с проектом и установите виртуального окружения для python, создайте его для проекта и активируйте:
```bash
sudo apt install python3.10-venv
python3.10 -m venv venv
source venv/bin/activate
```

12. Проверьте установлен ли pip:
```bash
pip3.10 -V
```
Если нет, то установите его:
```bash
sudo apt install python3-pip
```
13. Загрузите все необходимые зависимости в виртуальное окружение и проверьте установку:
```bash
pip install -r requirements.txt
pip list
```

14. Необходимо создать таблицы в СУБД по тем шаблонам, которые заданы в боте

````bash
alembic upgrade head
````

Проверить что таблицы создались можно зайдя в СУБД
````bash
psql
\d
````

Вывод должен быть таким:
````psql
List of relations
 Schema |      Name       |   Type   | Owner
--------+-----------------+----------+--------
 public | alembic_version | table    | <user_name>
 public | entities        | table    | <user_name>
 public | entities_id_seq | sequence | <user_name>
 public | groups          | table    | <user_name>
 public | rooms           | table    | <user_name>
 public | rooms_id_seq    | sequence | <user_name>
````

15. Перейдите в папку /etc/systemd/system/ и создайте там файл HomeAssistBot.service
```bash
cd /etc/systemd/system/
sudo nano HomeAssistBot.service
```

16. Запишите в него следующее:
```nano
[Unit]
Description=HomeAssistBot
After=syslog.target
After=network.target

[Service]
Type=simple
User=<ваше имя пользователя>
WorkingDirectory=/home/<ваше имя пользователя>/HomeAssistBot
ExecStart=/home/<ваше имя пользователя>/HomeAssistBot/venv/bin/python3.10 /home/<ваше имя пользователя>/HomeAssistBot/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

17. Перезагрузите systemd, активируйте созданный сервис и запустите его.

```bash
sudo systemctl daemon-reload
sudo systemctl enable HomeAssistBot.service
sudo systemctl start HomeAssistBot.service
```
18. Если нужно остановить скрипт:
```bash
sudo systemctl stop HomeAssistBot.service
```

19. Посмотреть статус сервиса бота:
```bash
sudo systemctl status HomeAssistBot.service
```






