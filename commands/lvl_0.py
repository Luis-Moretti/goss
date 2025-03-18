import function, sqlite3

def help(event, db: sqlite3.Connection):
    peer_id = event.obj['message']['peer_id']
    user_id = event.obj['message']['from_id']
    msg_id = event.obj['message']['conversation_message_id']
    access = function.get_access(peer_id, user_id, db)
    msg = "Список доступных команд:\n/stats - Посмотреть статистика пользователя\n/getid - Узнать оригинальную ссылку пользователя\n/info - Информация о боте"
    if access >= 1:
        msg += "\n\nКоманды модератора:\n/snick - Установить ник пользователю\n/rnick - Удалить ник у пользователя\n/kick - Исключить пользователя с беседы\n/nlist - Список пользователей с никами\n/nonick - Список пользователей без ников\n/staff - Список участников с правами\n/warn - Выдать предупреждение пользователю\n/unwarn - Убрать предупреждение у пользователя\n/warnlist - Список пользователей с варнами\n/getwarn - Получить все предупреждения пользователя\n/getban - Информация о блокировках пользователя\n/clear - Удалить сообщение от пользователя"
    if access >= 2:
        msg += "\n\nКоманды старшего модератора:\n/ban - Заблокировать пользователя\n/unban - Разблокировать пользователя\n/banlist - Список заблокированных пользователей\n/zov - Вызвать всех участников\n/online - Вызвать участников онлайн\n/olist - Список участников онлайн\n/addmoder - Выдать права модератора пользователю\n/removerole - Забрать все права у пользователя"
    if access >= 3:
        msg += "\n\nКоманды администратора:\n/ssnick - Установить ник пользователю в сетке бесед\n/srnick - Удалить ник у пользователя в сетке бесед\n/skick - Исключить пользователя в сетке бесед\n/addsenmoder - Выдать права старшего модератора пользователю"
    if access >= 4:
        msg += "\n\nКоманды старшего администратора:\n/izov - Вызвать всех учатников в беседах инфо\n/fzov - Вызвать всех учатников в беседах флуд\n/gzov - Вызвать всех участников во всех беседах\n/sban - Заблокировать пользователя в сетке бесед\n/sunban - Разблокировать пользователя в сетке бесед\n/gban - Глобально заблокировать пользователя\n/gunban - Глобально разблокировать пользователя\n/addadmin - Выдать права администратора пользователю\n/sremoverole - Забрать все права у пользователя в сетке бесед\n/srole - Выдать права в сетке бесед"
    if access == 5: 
        msg += "\n\nКоманды владельца беседы:\n/pullinfo - Информация о сетке бесед\n/setpull - Сменить сетку бесед\n/urkick - Исключить всех участников без прав\n/addsenadmin - Выдать права старшего администратора пользователю\n/type - Изменить тип беседы\n/setowner - Передать владельца беседы пользователю"
    
    function.reply(peer_id, msg, msg_id)

def id(event):
    peer_id = event.obj['message']['peer_id']
    user_id = event.obj['message']['from_id']
    msg_id = event.obj['message']['conversation_message_id']
    id = function.check_arguments(event, 2)[0]
    if id == 0:
        id = user_id
    function.reply(peer_id, f"Оригинальная ссылка [id{id}|пользователя]:\nhttps://vk.com/id{id}", msg_id)

def info(event, db: sqlite3.Connection):
    peer_id = event.obj['message']['peer_id']
    user_id = event.obj['message']['from_id']
    msg_id = event.obj['message']['conversation_message_id']
    servers = db.execute("SELECT * FROM server_info").fetchall()
    users = db.execute("SELECT * FROM user_info").fetchall()
    developers = db.execute("SELECT * FROM developer_info")
    msg = ""
    count = 0
    for d in developers:
        count += 1
        msg += f"\n[{count}]. [id{d[0]}|{function.get_user_name(d[0])}] | Должность: {d[1]}"
    function.reply(peer_id, f"Информация о боте\nЯзык: Python\nВерсия бота: 1.0\nПоследнее обновление:\n11.03.2025\n\nКол-во бесед: {len(servers)}\nКол-во пользователей: {len(users)}\n\nСостав команды:{msg}", msg_id)

def stats(event, db: sqlite3.Connection):
    peer_id = event.obj['message']['peer_id']
    user_id = event.obj['message']['from_id']
    text = event.obj['message']['text'].split()
    msg_id = event.obj['message']['conversation_message_id']
    id = function.check_arguments(event, 2)[0]
    if id == 0:
        id = user_id
    bans = len(db.execute("SELECT * FROM ban_list WHERE user_id = ? AND type = ?", (id, 'local',)).fetchall())
    gban = db.execute("SELECT * FROM ban_list WHERE user_id = ? AND type = ?", (id, 'global',)).fetchone()
    if gban != None:
        gban = "Есть"
    else:
        gban = "Отсутствует"
    warns = len(db.execute("SELECT * FROM warn_list WHERE user_id = ? AND peer_id = ?", (id, peer_id,)).fetchall())
    user = db.execute("SELECT * FROM user_info WHERE user_id = ? AND peer_id = ?", (id, peer_id,)).fetchone()
    function.reply(peer_id, f"Информация о пользователе {function.get_mention_nick(peer_id, id, db)}\n\nУровень прав: {function.get_name_access(user[4])}\nНик: {user[3]}\n\nОбщая блокировка в беседах: {gban}\nБлокировок в беседах: {bans}\nАктивных предупреждений: {warns}\n\nДата регистрации: {function.get_regDate(id)}\nОтправлено сообщений: {user[5]}\nПоследнее сообщение: {user[6]}", msg_id)