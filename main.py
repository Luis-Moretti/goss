import config, function, threading, sqlite3, time
from vk_api.bot_longpoll import VkBotEventType
from commands import lvl_0, lvl_1, lvl_2, lvl_3, lvl_4, lvl_5

def type_info():
    db = sqlite3.connect('database.db')
    while True:
        servers = db.execute("SELECT * FROM server_info WHERE type = ?", ('info',)).fetchall()
        for s in servers:
            items = config.vk_api.messages.getConversationMembers(peer_id=s[0])['profiles']
            for i in items:
                if function.get_access(s[0], i['id'], db) == 0:
                    config.vk_api.messages.changeConversationMemberRestrictions(peer_id=s[0], member_ids=i['id'], action='ro')
                else:
                    config.vk_api.messages.changeConversationMemberRestrictions(peer_id=s[0], member_ids=i['id'], action='rw')
        time.sleep(5)

def main():
    db = sqlite3.connect('database.db')
    for event in config.longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat:
                peer_id = event.obj['message']['peer_id']
                text = event.obj['message']['text'].split()
                msg_id = event.obj['message']['conversation_message_id']
                user_id = event.obj['message']['from_id']
                if 'action' in event.obj['message']:
                    if event.obj['message']['action']['type'] == 'chat_invite_user':
                        if event.obj['message']['action']['member_id'] == -229655124:
                            function.send(peer_id, "Для активации бота используйте команду /start")
                if bool(len(db.execute("SELECT * FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, user_id,)).fetchall())) and bool(len(db.execute("SELECT * FROM server_info WHERE peer_id = ?", (peer_id,)).fetchall())):
                    with db:
                        db.execute("UPDATE user_info SET msg_count = msg_count + ? WHERE user_id = ? AND peer_id = ?", (1, user_id, peer_id,))
                        db.execute("UPDATE user_info SET lastMessageDate = ? WHERE user_id = ? AND peer_id = ?", (function.get_moscow_date(), user_id, peer_id,))
                else:
                    with db:
                        db.execute("INSERT INTO user_info ('peer_id', 'user_id', 'user_name', 'msg_count', 'lastMessageDate') VALUES (?,?,?,?,?)", (peer_id, user_id, function.get_user_name(user_id), 1, function.get_moscow_date()))
                if bool(len(db.execute("SELECT * FROM server_info WHERE peer_id = ?", (peer_id,)).fetchall())):
                 if text != [] and text[0][0] in ['+', '/', '!']:
                    if text[0][1:] in ['start', 'начать', 'старт']:
                        try:
                            if function.is_admin(peer_id, user_id):
                                with db:
                                    db.execute("INSERT INTO server_info ('peer_id') VALUES (?)", (peer_id,))
                                    db.execute("INSERT INTO user_info ('peer_id', 'user_id', 'user_name', 'access') VALUES (?,?,?,?)", (peer_id, user_id, function.get_user_name(user_id), 5,))
                                function.reply(peer_id, "Связь с ботом уставнолена. Для просмотра команд - /help. Для настройки типа беседы - /type", msg_id)
                            else:
                                function.reply(peer_id, "Актвировать бота может только создатель беседы", msg_id)
                        except:
                            function.reply(peer_id, "У бота нету звёздочки (администратора) в беседе", msg_id)
                    # === LVL 0 ===
                    if text[0][1:] in ['help', 'хэлп']:
                        lvl_0.help(event, db)
                    if text[0][1:] in ['инфо', 'info']:
                        lvl_0.info(event, db)
                    if text[0][1:] in ['id', 'getid', 'ид']:
                        lvl_0.id(event)
                    if text[0][1:] in ['stats', 'стата']:
                        lvl_0.stats(event, db)
                
                    # === LVL 1 ===
                    if text[0][1:] in ['snick', 'setnick', 'сник']:
                        lvl_1.snick(event, db)
                    if text[0][1:] in ['rnick', 'removenick', 'рник']:
                        lvl_1.rnick(event, db)
                    if text[0][1:] in ['kick', 'кик']:
                        lvl_1.kick(event, db)
                    if text[0][1:] in ['staff', 'стафф']:
                        lvl_1.staff(event, db)
                    if text[0][1:] in ['nlist', 'nicklist', 'ники']:
                        lvl_1.nlist(event, db)
                    if text[0][1:] in ['nonick', 'безников']:
                        lvl_1.nonick(event, db)
                    if text[0][1:] in ['getban', 'чекбан', 'гетбан']:
                        lvl_1.getban(event, db)
                    if text[0][1:] in ['clear', 'очистить']:
                        lvl_1.clear(event, db)
                    if text[0][1:] in ['warn', 'варн']:
                        lvl_1.warn(event, db)
                    if text[0][1:] in ['unwarn', 'унварн']:
                        lvl_1.unwarn(event, db)
                    if text[0][1:] in ['warnlist', 'варнлист']:
                        lvl_1.warnlist(event, db)
                    if text[0][1:] in ['getwarn', 'чекварн', 'гетварн']:
                        lvl_1.getwarn(event, db)

                    # === LVL 2 ===
                    if text[0][1:] in ['addmoder', 'moder']:
                        lvl_2.addmoder(event, db)
                    if text[0][1:] in ['removerole', 'rrole']:
                        lvl_2.removerole(event, db)
                    if text[0][1:] in ['ban', 'бан']:
                        lvl_2.ban(event, db)
                    if text[0][1:] in ['unban', 'разбан']:
                        lvl_2.unban(event, db)
                    if text[0][1:] in ['zov', 'зов']:
                        lvl_2.zov(event, db)
                    if text[0][1:] in ['online', 'онлайн']:
                        lvl_2.online(event, db)
                    if text[0][1:] in ['olist', 'onlinelist', 'онлайнлист']:
                        lvl_2.olist(event, db)

                    # === LVL 3 ===
                    if text[0][1:] in ['addsenmoder', 'senmoder']:
                        lvl_3.addsenmoder(event, db)
                    if text[0][1:] in ['ssnick', 'ссник']:
                        lvl_3.ssnick(event, db)
                    if text[0][1:] in ['srnick', 'срник']:
                        lvl_3.srnick(event, db)

                    # === LVL 4 ===
                    if text[0][1:] in ['addadmin', 'admin']:
                        lvl_4.addadmin(event, db)
                    if text[0][1:] in ['infozov', 'izov', 'инфозов']:
                        lvl_4.izov(event, db)
                    if text[0][1:] in ['floodzov', 'fzov', 'флудзов']:
                        lvl_4.fzov(event, db)
                    if text[0][1:] in ['globalzov', 'gzov', 'гзов']:
                        lvl_4.gzov(event, db)
                    if text[0][1:] in ['gban', 'гбан']:
                        lvl_4.gban(event, db)
                    if text[0][1:] in ['gunban', 'гразбан']:
                        lvl_4.gunban(event, db)

                    # === LVL 5 ===
                    if text[0][1:] in ['type', 'тип']:
                        lvl_5.type_group(event, db)
                    if text[0][1:] in ['addsenadmin', 'senadmin']:
                        lvl_5.addsenadmin(event, db)
                    if text[0][1:] in ['setpull', 'ксетка']:
                        lvl_5.setpull(event, db)
                    if text[0][1:] in ['pullinfo', 'сетка']:
                        lvl_5.pullinfo(event, db)

if __name__ == '__main__':
    main_th = threading.Thread(target=main)
    info_th = threading.Thread(target=type_info)
    info_th.start()
    main_th.start()