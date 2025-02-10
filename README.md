# *Eng For Netology*.  Telegram-бот который поможет учить английские слова. 

## Принцип работы бота.
Пользователь запускает бота командой "/start". Далее программа добавляет данного пользователя в базу данных и создает для него персональный словарь. Перед пользователем появляется слово (из общей базы данных и персонального словаря) и четыре варианта перевода. При правильном ответе, бот оповещает пользователя об успехе и переходит к следующему слову. При неправильном, предлагает выбрать другой вариант.

## Функционал бота.
1. 'Добавить слово+' : Позволяет добавить слово и его перевод в персональный словарь.
2. 'Удалить слово-' : Позволяет удалить слово из персонального словаря.
3. 'Дальше->' Позволяет перейти к следующему слову случайно выбранному из общего и персонального словаря.

## Особенности бота.
- Бот написан на языке программирования Python.
- Для создания бота необходим API токен Telegram.
- Для хранения данных используется БД PostgreSQL.
- Персональный словарь доступен только для конкретного пользователя. Другим пользователям слова из него попадаться не будут.
