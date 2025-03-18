import function, sqlite3, config

def type_group(event, db: sqlite3.Connection):
    peer_id = event.obj['message']['peer_id']
    user_id = event.obj['message']['from_id']
    text = event.obj['message']['text'].split()
    msg_id = event.obj['message']['conversation_message_id']
    if function.check_access(peer_id, user_id, 5, db):
        type = db.execute("SELECT type FROM server_info WHERE peer_id = ?", (peer_id,)).fetchone()[0]
        if len(text) == 2:
            if text[1] != type:
                if text[1] == 'default':
                    with db:
                        db.execute("UPDATE server_info SET type = ? WHERE peer_id = ?", ('default', peer_id,))
                    items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['items']
                    for i in items:
                        config.vk_api.messages.changeConversationMemberRestrictions(peer_id=peer_id, member_ids=i['member_id'], action='rw')
                    function.reply(peer_id, f'{function.get_mention_nick(peer_id, user_id, db)} изменил тип беседы на "default"', msg_id)
                elif text[1] == 'info':
                    with db:
                        db.execute("UPDATE server_info SET type = ? WHERE peer_id = ?", ('info', peer_id,))
                    function.reply(peer_id, f'{function.get_mention_nick(peer_id, user_id, db)} изменил тип беседы на "info"', msg_id)
                elif text[1] == 'flood':
                    with db:
                        db.execute("UPDATE server_info SET type = ? WHERE peer_id = ?", ('flood', peer_id,))
                    function.reply(peer_id, f'{function.get_mention_nick(peer_id, user_id, db)} изменил тип беседы на "flood"', msg_id)
                else:
                    function.reply(peer_id, f"Информация о типе беседы:\nУстановленный тип: {type}\n\nДоступные типы: \n1. default - по умолчанию (Все могут писать)\n2. info - беседа с информацией (Только с правами могут писать)", msg_id)
            else:
                function.reply(peer_id, f'Тип "{type}" уже установлен для данной беседы', msg_id)
        else:
            function.reply(peer_id, f"Информация о типе беседы:\nУстановленный тип: {type}\n\nДоступные типы: \n1. default - по умолчанию (Все могут писать)\n2. info - беседа с информацией (Только с правами могут писать)\n3. flood - беседы флуда (Задержка на отправку сообщений)\n\nДля изменения: /type <type>", msg_id)
    else:
        function.reply(peer_id, f"Недостаточно прав!", msg_id)

def addsenadmin(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 5, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if function.comparison_access(peer_id, user_id, check[0], db):
            if check[0] != user_id:
                function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} выдал(-а) права старшего администратора {function.get_mention_nick(peer_id, check[0], db)}", msg_id)
                with db:
                   db.execute("UPDATE user_info SET access = ? WHERE peer_id = ? AND user_id = ?", (4, peer_id, check[0],))
            else:
               function.reply(peer_id, f"Нельзя изменить уровень прав самому себе", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /addsenadmin <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def setpull(event, db: sqlite3.Connection):
    peer_id = event.obj['message']['peer_id']
    user_id = event.obj['message']['from_id']
    text = event.obj['message']['text'].split()
    msg_id = event.obj['message']['conversation_message_id']
    if function.check_access(peer_id, user_id, 5, db):
        if len(text) == 2:
            try:
                text[1] = int(text[1])
                if text[1] == "0":
                    with db:
                        db.execute("UPDATE server_info SET pull_id = ? WHERE peer_id = ?", (0, peer_id,))
                    function.reply(peer_id, f'{function.get_mention_nick(peer_id, user_id, db)} отвязал(-а) беседу от сетки бесед', msg_id)
                else:
                    with db:
                        db.execute("UPDATE server_info SET pull_id = ? WHERE peer_id = ?", (text[1], peer_id,))
                    function.reply(peer_id, f'{function.get_mention_nick(peer_id, user_id, db)} привязал(-а) беседу к сетке бесед <<{text[1]}>>. Для отвязки: /setpull 0', msg_id)
            except ValueError:
                function.reply(peer_id, f"Используйте: /setpull <ID>", msg_id)
        else:
            function.reply(peer_id, f"Используйте: /setpull <ID>", msg_id)
    else:
        function.reply(peer_id, f'Недостаточно прав!', msg_id)

def pullinfo(event, db: sqlite3.Connection):
    peer_id = event.obj['message']['peer_id']
    user_id = event.obj['message']['from_id']
    text = event.obj['message']['text'].split()
    msg_id = event.obj['message']['conversation_message_id']
    if function.check_access(peer_id, user_id, 5, db):
        server = db.execute("SELECT pull_id FROM server_info WHERE peer_id = ?", (peer_id,)).fetchone()
        if server[0] != 0:
            count_server = db.execute("SELECT * FROM server_info WHERE pull_id = ?", (server[0],)).fetchall()
            function.reply(peer_id, f"Информация о сетке бесед:\nID: {server[0]} | Бесед: {len(count_server)}", msg_id)
        else:
            function.reply(peer_id, f"Информация о сетке бесед:\nПривязка отсутвует", msg_id)
    else:
        function.reply(peer_id, f'Недостаточно прав!', msg_id)