import urllib.request, json, time

TOKEN = "8975960218:AAH0eL_hqD5uCz1DwJvHcOzlGQzkGwBOieU"
URL = f"https://api.telegram.org/bot{TOKEN}/"

try:
    with open("badges.json", "r", encoding="utf-8") as f:
        badges = json.load(f)
except:
    badges = {}

try:
    resp = urllib.request.urlopen(URL + "getUpdates?timeout=5")
    data = json.loads(resp.read().decode())
    
    if data.get("ok"):
        last_update_id = 0
        for update in data["result"]:
            last_update_id = update["update_id"]
            msg = update.get("message", {})
            text = msg.get("text", "")
            user_id = str(msg.get("from", {}).get("id", ""))
            
            if text.startswith("/badges ") and user_id:
                emoji = text[8:].strip()
                if 1 <= len(emoji) <= 5:
                    badges[user_id] = emoji
                    reply = f"✅ Твой бейдж сохранен: {emoji}\nПодожди пару минут и перезапусти Telegram."
                    urllib.request.urlopen(f"{URL}sendMessage?chat_id={user_id}&text={reply}")
        
        if last_update_id > 0:
            urllib.request.urlopen(URL + f"getUpdates?offset={last_update_id + 1}")
            
        with open("badges.json", "w", encoding="utf-8") as f:
            json.dump(badges, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f"Error: {e}")
