# Исправленный код с правильной кодировкой и исправлением начального символа 

import asyncio

import json

import os

import requests

from telethon import events, TelegramClient



# Константы

CONFIG_FILE = "config.json"

DEFAULT_TYPING_SPEED = 0.3

DEFAULT_CURSOR = "\u2588"  # Курсор по умолчанию

GITHUB_RAW_URL = "https://raw.githubusercontent.com/mishkago/userbot/refs/heads/main/main.py"

SCRIPT_VERSION = "1.3"



# Проверяем наличие файла конфигурации

if os.path.exists(CONFIG_FILE):

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:

        config = json.load(f)

    API_ID = config.get("API_ID")

    API_HASH = config.get("API_HASH")

    PHONE_NUMBER = config.get("PHONE_NUMBER")

    typing_speed = config.get("typing_speed", DEFAULT_TYPING_SPEED)

    typing_cursor = config.get("typing_cursor", DEFAULT_CURSOR)

else:

    API_ID = int(input("Введите ваш API ID: "))

    API_HASH = input("Введите ваш API Hash: ")

    PHONE_NUMBER = input("Введите ваш номер телефона (в формате +375XXXXXXXXX, +7XXXXXXXXXX): ")

    typing_speed = DEFAULT_TYPING_SPEED

    typing_cursor = DEFAULT_CURSOR



    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:

        json.dump({

            "API_ID": API_ID,

            "API_HASH": API_HASH,

            "PHONE_NUMBER": PHONE_NUMBER,

            "typing_speed": typing_speed,

            "typing_cursor": typing_cursor

        }, f, ensure_ascii=False)



# Инициализация клиента

client = TelegramClient('sessions', API_ID, API_HASH, system_version='4.16.30-vxCUSTOM')



@client.on(events.NewMessage(pattern=r'/p (.+)'))

async def animated_typing(event):

    global typing_speed, typing_cursor

    try:

        if not event.out:

            return



        text = event.pattern_match.group(1)

        typed_text = ""



        for char in text:

            typed_text += char

            await event.edit(typed_text + typing_cursor)

            await asyncio.sleep(typing_speed)



        await event.edit(typed_text)

    except Exception as e:

        print(f"Ошибка при выполнении анимации печатания: {e}")

        await event.reply("<b>Произошла ошибка во время выполнения команды.</b>", parse_mode='html')



@client.on(events.NewMessage(pattern=r'/cursor (.+)'))

async def set_cursor(event):

    global typing_cursor

    try:

        if not event.out:

            return



        new_cursor = event.pattern_match.group(1)

        typing_cursor = new_cursor



        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:

            config = json.load(f)

        config["typing_cursor"] = typing_cursor

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:

            json.dump(config, f, ensure_ascii=False)



        await event.reply(f"<b>Курсор изменён на: {typing_cursor}</b>", parse_mode='html')

    except Exception as e:

        print(f"Ошибка при изменении курсора: {e}")

        await event.reply("<b>Произошла ошибка при изменении курсора.</b>", parse_mode='html')



@client.on(events.NewMessage(pattern=r'/reset'))

async def reset_settings(event):

    global typing_speed, typing_cursor

    try:

        if not event.out:

            return



        typing_speed = DEFAULT_TYPING_SPEED

        typing_cursor = DEFAULT_CURSOR



        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:

            config = json.load(f)

        config["typing_speed"] = typing_speed

        config["typing_cursor"] = typing_cursor

        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:

            json.dump(config, f, ensure_ascii=False)



        await event.reply("<b>Настройки сброшены до значений по умолчанию.</b>", parse_mode='html')

    except Exception as e:

        print(f"Ошибка при сбросе настроек: {e}")

        await event.reply("<b>Произошла ошибка при сбросе настроек.</b>", parse_mode='html')



async def main():

    print(f"Запуск main()\\nВерсия скрипта: {SCRIPT_VERSION}")

    await client.start(phone=PHONE_NUMBER)

    print("Скрипт успешно запущен! Для использования:")

    print("- /p (текст) для анимации печатания.")

    print("- /cursor (символ) для изменения курсора.")

    print("- /reset для сброса настроек.")

    await client.run_until_disconnected()



if __name__ == "__main__":

    asyncio.run(main())
