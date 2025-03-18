import config, json, sqlite3, re, requests
from datetime import datetime, timezone, timedelta

def send(peer_id, text):
    config.vk_api.messages.send(peer_id=peer_id, message=text, random_id=0)

def reply(peer_id, text, msg_id):
    config.vk_api.messages.send(peer_id=peer_id, message=text, forward=json.dumps({
       'peer_id': peer_id,
       'conversation_message_ids': msg_id,
       'is_reply': 1
    }), random_id=0)

def delete(peer_id, msg_id):
    config.session_vk.method('messages.delete', {"peer_id": peer_id, "cmids": msg_id, "delete_for_all": 1, 'random_id': 0})

def get_user_name(user_id):
    user = config.session_vk.method("users.get", {"user_ids": user_id})[0] 
    return f"{user['first_name']} {user['last_name']}"

def get_mention_nick(peer_id, user_id, db: sqlite3.Connection):
    if bool(len(db.execute("SELECT * FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, user_id,)).fetchall())):
        if db.execute("SELECT nick FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, user_id,)).fetchone()[0] != "нету":
            return f'[id{user_id}|{db.execute("SELECT nick FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, user_id,)).fetchone()[0]}]'
        else:
            return f'[id{user_id}|{get_user_name(user_id)}]'
    else:
        return f'[id{user_id}|{get_user_name(user_id)}]'

def get_access(peer_id, user_id, db: sqlite3.Connection):
    if bool(len(db.execute("SELECT * FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, user_id,)).fetchall())):
        return int(db.execute("SELECT access FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, user_id,)).fetchone()[0])
    else:
        with db:
            db.execute("INSERT INTO user_info ('peer_id', 'user_id', 'user_name') VALUES (?,?,?)", (peer_id, user_id, get_user_name(user_id),))
        return 0
    
def get_id(text: str):
    user_id = 0
    if text.count('vk.com/') != 1:
        if re.findall(r'id(\d+)|', text)[1] != '':
            user_id = int(re.findall(r'id(\d+)|', text)[1])
        else:
            try:
                user_id = int(text)
            except:
                pass
    else:
        if text.split('vk.com/')[1].count('id') == 1:
            user_id = int(''.join(re.findall(r'id(\d+)', text.split('vk.com/')[1])))
        else:
            user = config.session_vk.method("users.get", {"user_ids": text.split('vk.com/')[1]})[0]
            user_id = user['id']
    
    if config.session_vk.method("users.get", {"user_ids": user_id}) != []:
        return user_id
    else:
        return 0
    
def in_group(peer_id, user_id):
    items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['items']
    for i in items:
        if i['member_id'] == user_id:
            return True
        
    return False
    
def is_admin(peer_id, user_id):
    items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['items']
    for i in items:
        if i['member_id'] == user_id:
            if 'is_admin' in i:
                return i['is_admin']
        
    return False
    
def is_onwer(peer_id, user_id):
    items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['items']
    for i in items:
        if i['member_id'] == user_id:
            if 'is_owner' in i:
                return i['is_owner']
        
    return False
    
def check_access(peer_id, user_id, access, db: sqlite3.Connection):
    return get_access(peer_id, user_id, db) >= access

def comparison_access(peer_id, user_id, member_id, db: sqlite3.Connection):
    return get_access(peer_id, user_id, db) >= get_access(peer_id, member_id, db)

def check_arguments(event, args_count):
    text = event.obj['message']['text'].split()
    if event.obj['message']['fwd_messages'] != []:
        return [int(event.obj['message']['fwd_messages'][0]['from_id']), 'type_1']
    elif 'reply_message' in event.obj['message']:
        return [int(event.obj['message']['reply_message']['from_id']), 'type_1']
    elif len(text) >= args_count:
        return [get_id(text[1]), 'type_2']
    return [0, 0]

def get_moscow_date():
    moscow = timezone(timedelta(hours=3), "Moscow")
    a = datetime.now(moscow)
    return a.strftime("%H:%M:%S %d.%m.%Y")

def get_name_access(access):
    if access == 5:
        return "Владелец"
    if access == 4:
        return "Старший администратор"
    if access == 3:
        return "Администратор"
    if access == 2:
        return "Старший модератор"
    if access == 1:
        return "Модератор"
    if access == 0:
        return "Участник"
    
def get_regDate(user_id):
    url = 'https://vk.com/foaf.php?id='+str(user_id)
    headers = {"Accept-Language": "ru-RU,ru;q=0.75"}
    response = requests.get(url, headers=headers)
    text = response.text
    num = text.find('<ya:created')
    text = text[(num+21):(num+46)]
    dt = datetime.strptime(text[:19], '%Y-%m-%dT%H:%M:%S')
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'апреля', 'сентября', 'октября', 'ноября', 'декабря']
    return f'{dt.day} {months[dt.month-1]} {dt.year}'

def is_online(user_id):
    return config.session_vk.method("users.get", {"user_ids": user_id, "fields": 'online', "name_case": "gen"})[0]['online'] > 0
    