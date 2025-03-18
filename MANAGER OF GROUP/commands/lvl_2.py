import function, sqlite3, config

def addmoder(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 2, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if function.comparison_access(peer_id, user_id, check[0], db):
            if check[0] != user_id:
                function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} выдал(-а) права модератора {function.get_mention_nick(peer_id, check[0], db)}", msg_id)
                with db:
                   db.execute("UPDATE user_info SET access = ? WHERE peer_id = ? AND user_id = ?", (1, peer_id, check[0],))
            else:
               function.reply(peer_id, f"Нельзя изменить уровень прав самому себе", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /addmoder <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def removerole(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 2, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if function.comparison_access(peer_id, user_id, check[0], db):
            if check[0] != user_id:
                function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} забрал(-а) все права {function.get_mention_nick(peer_id, check[0], db)}", msg_id)
                with db:
                   db.execute("UPDATE user_info SET access = ? WHERE peer_id = ? AND user_id = ?", (0, peer_id, check[0],))
            else:
               function.reply(peer_id, f"Нельзя забрать все права у самого себя", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /removerole <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def ban(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 2, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if check[1] == 'type_1':
            reason = text[1:]
         else:
            reason = text[2:]
         if reason == []:
            reason = "Не указана"
         else:
            reason = ' '.join(reason)
         if function.comparison_access(peer_id, user_id, check[0], db):
            if check[0] != user_id:
               if not bool(len(db.execute("SELECT * FROM ban_list WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchall())):
                  if not function.is_admin(peer_id, check[0]):
                     if function.in_group(peer_id, check[0]):
                        config.vk_api.messages.removeChatUser(chat_id=event.chat_id, member_id=check[0])
                     with db:
                        db.execute("INSERT INTO ban_list ('peer_id', 'user_id', 'type', 'moder_id', 'reason', 'giveDate') VALUES (?,?,?,?,?,?)", (peer_id, check[0], 'local', user_id, reason, function.get_moscow_date(),))
                     function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} заблокировал(-а) {function.get_mention_nick(peer_id, check[0], db)}\nПричина: {reason}", msg_id)
               else:
                  function.reply(peer_id, f"Пользователь уже находится в бане", msg_id)
            else:
               function.reply(peer_id, f"Нельзя забанить самого себя", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /ban <user> <reason>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def unban(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 2, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if bool(len(db.execute("SELECT * FROM ban_list WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchall())):
            if check[0] != user_id:
               if not function.is_admin(peer_id, check[0]):
                  function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} разблокировал(-а) {function.get_mention_nick(peer_id, check[0], db)}", msg_id)
                  with db:
                     db.execute("DELETE FROM ban_list WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],))
            else:
               function.reply(peer_id, f"Нельзя забанить самого себя", msg_id)
         else:
            function.reply(peer_id, f"Пользователь не находится в бане", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /unban <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def zov(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      if len(text) >= 2:
         members = ""
         items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['profiles']
         for i in items:
            members += f"[id{i['id']}|🖤]"
         function.send(peer_id, f"📢 Вы были вызваны [id{user_id}|администратором] беседы\n\n{members}\n\n❗ Причина: {' '.join(text[1:])}")
      else:
         function.reply(peer_id, f"Используйте: /zov <reason|text>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def online(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      if len(text) >= 2:
         members = ""
         items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['profiles']
         for i in items:
            if function.is_online(i['id']):
               members += f"[id{i['id']}|🖤]"
         function.send(peer_id, f"📢 Кто онлайн? Вы были вызваны [id{user_id}|администратором] беседы\n\n{members}\n\n❗ Причина: {' '.join(text[1:])}")
      else:
         function.reply(peer_id, f"Используйте: /online <reason|text>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def olist(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      members = ""
      count = 0
      items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['profiles']
      for i in items:
         if 'online_info' in i:
            count += 1
            if i['online_info']['is_mobile']:
               members += f"\n[{count}]. [id{i['id']}|{i['first_name']} {i['last_name']}] - 📱"
            else:
               members += f"\n[{count}]. [id{i['id']}|{i['first_name']} {i['last_name']}] - 💻"
      function.send(peer_id, f"Список пользователей онлайн [Всего: {count}]:{members}")
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)