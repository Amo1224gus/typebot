
import asyncio
import json
import os
import requests
from telethon import events, TelegramClient

# РљРѕРЅСЃС‚Р°РЅС‚С‹
CONFIG_FILE = "config.json"
DEFAULT_TYPING_SPEED = 0.3
DEFAULT_CURSOR = "в–€"
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Amo1224gus/typebot/refs/heads/main/main.py"
SCRIPT_VERSION = "1.3"

# РџСЂРѕРІРµСЂСЏРµРј РЅР°Р»РёС‡РёРµ С„Р°Р№Р»Р° РєРѕРЅС„РёРіСѓСЂР°С†РёРё
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    API_ID = config.get("API_ID")
    API_HASH = config.get("API_HASH")
    PHONE_NUMBER = config.get("PHONE_NUMBER")
    typing_speed = config.get("typing_speed", DEFAULT_TYPING_SPEED)
    typing_cursor = config.get("typing_cursor", DEFAULT_CURSOR)
else:
    API_ID = int(input("Р’РІРµРґРёС‚Рµ РІР°С€ API ID: "))
    API_HASH = input("Р’РІРµРґРёС‚Рµ РІР°С€ API Hash: ")
    PHONE_NUMBER = input("Р’РІРµРґРёС‚Рµ РІР°С€ РЅРѕРјРµСЂ С‚РµР»РµС„РѕРЅР° (РІ С„РѕСЂРјР°С‚Рµ +375XXXXXXXXX, +7XXXXXXXXXX): ")
    typing_speed = DEFAULT_TYPING_SPEED
    typing_cursor = DEFAULT_CURSOR

    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "API_ID": API_ID,
            "API_HASH": API_HASH,
            "PHONE_NUMBER": PHONE_NUMBER,
            "typing_speed": typing_speed,
            "typing_cursor": typing_cursor
        }, f)

# РРЅРёС†РёР°Р»РёР·Р°С†РёСЏ РєР»РёРµРЅС‚Р°
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
        print(f"РћС€РёР±РєР° РїСЂРё РІС‹РїРѕР»РЅРµРЅРёРё Р°РЅРёРјР°С†РёРё РїРµС‡Р°С‚Р°РЅРёСЏ: {e}")
        await event.reply("<b>РџСЂРѕРёР·РѕС€Р»Р° РѕС€РёР±РєР° РІРѕ РІСЂРµРјСЏ РІС‹РїРѕР»РЅРµРЅРёСЏ РєРѕРјР°РЅРґС‹.</b>", parse_mode='html')

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
            json.dump(config, f)

        await event.reply(f"<b>РљСѓСЂСЃРѕСЂ РёР·РјРµРЅС‘РЅ РЅР°: {typing_cursor}</b>", parse_mode='html')
    except Exception as e:
        print(f"РћС€РёР±РєР° РїСЂРё РёР·РјРµРЅРµРЅРёРё РєСѓСЂСЃРѕСЂР°: {e}")
        await event.reply("<b>РџСЂРѕРёР·РѕС€Р»Р° РѕС€РёР±РєР° РїСЂРё РёР·РјРµРЅРµРЅРёРё РєСѓСЂСЃРѕСЂР°.</b>", parse_mode='html')

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
            json.dump(config, f)

        await event.reply("<b>РќР°СЃС‚СЂРѕР№РєРё СЃР±СЂРѕС€РµРЅС‹ РґРѕ Р·РЅР°С‡РµРЅРёР№ РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ.</b>", parse_mode='html')
    except Exception as e:
        print(f"РћС€РёР±РєР° РїСЂРё СЃР±СЂРѕСЃРµ РЅР°СЃС‚СЂРѕРµРє: {e}")
        await event.reply("<b>РџСЂРѕРёР·РѕС€Р»Р° РѕС€РёР±РєР° РїСЂРё СЃР±СЂРѕСЃРµ РЅР°СЃС‚СЂРѕРµРє.</b>", parse_mode='html')

async def main():
    print(f"Р—Р°РїСѓСЃРє main()\nР’РµСЂСЃРёСЏ СЃРєСЂРёРїС‚Р°: {SCRIPT_VERSION}")
    await client.start(phone=PHONE_NUMBER)
    print("РЎРєСЂРёРїС‚ СѓСЃРїРµС€РЅРѕ Р·Р°РїСѓС‰РµРЅ! Р”Р»СЏ РёСЃРїРѕР»СЊР·РѕРІР°РЅРёСЏ:")
    print("- /p (С‚РµРєСЃС‚) РґР»СЏ Р°РЅРёРјР°С†РёРё РїРµС‡Р°С‚Р°РЅРёСЏ.")
    print("- /cursor (СЃРёРјРІРѕР») РґР»СЏ РёР·РјРµРЅРµРЅРёСЏ РєСѓСЂСЃРѕСЂР°.")
    print("- /reset РґР»СЏ СЃР±СЂРѕСЃР° РЅР°СЃС‚СЂРѕРµРє.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
