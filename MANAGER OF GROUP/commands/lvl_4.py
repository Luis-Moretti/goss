import function, sqlite3, config

def addadmin(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 4, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if function.comparison_access(peer_id, user_id, check[0], db):
            if check[0] != user_id:
                function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} выдал(-а) права администратора {function.get_mention_nick(peer_id, check[0], db)}", msg_id)
                with db:
                   db.execute("UPDATE user_info SET access = ? WHERE peer_id = ? AND user_id = ?", (3, peer_id, check[0],))
            else:
               function.reply(peer_id, f"Нельзя изменить уровень прав самому себе", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /addadmin <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def izov(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 4, db):
      if len(text) >= 2:
         servers = db.execute("SELECT * FROM server_info WHERE type = ?", ('info',)).fetchall()
         for s in servers:
            peer_id = s[0]
            items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['profiles']
            members = ""
            for i in items:
               members += f"[id{i['id']}|🖤]"
            function.send(peer_id, f"📢 Вы были вызваны [id{user_id}|администратором] беседы\n\n{members}\n\n❗ Причина: {' '.join(text[1:])}")
      else:
         function.reply(peer_id, f"Используйте: /izov <reason|text>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def fzov(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 4, db):
      if len(text) >= 2:
         servers = db.execute("SELECT * FROM server_info WHERE type = ?", ('flood',)).fetchall()
         for s in servers:
            peer_id = s[0]
            items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['profiles']
            members = ""
            for i in items:
               members += f"[id{i['id']}|🖤]"
            function.send(peer_id, f"📢 Вы были вызваны [id{user_id}|администратором] беседы\n\n{members}\n\n❗ Причина: {' '.join(text[1:])}")
      else:
         function.reply(peer_id, f"Используйте: /fzov <reason|text>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def gban(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 4, db):
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
               if not bool(len(db.execute("SELECT * FROM ban_list WHERE user_id = ? AND type = ?", (check[0], 'global',)).fetchall())):
                  servers = db.execute("SELECT * FROM server_info",).fetchall()
                  for s in servers:
                     peer_id = s[0]
                     if not function.is_admin(peer_id, check[0]):
                        if function.in_group(peer_id, check[0]):
                           config.vk_api.messages.removeChatUser(chat_id=(peer_id-2000000000), member_id=check[0])
                        function.send(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} заблокировал(-а) во всех беседах {function.get_mention_nick(peer_id, check[0], db)}\nПричина: {reason}")
                  with db:
                     db.execute("INSERT INTO ban_list ('peer_id', 'user_id', 'type', 'moder_id', 'reason', 'giveDate') VALUES (?,?,?,?,?,?)", (0, check[0], 'global', user_id, reason, function.get_moscow_date(),))
               else:
                  function.reply(peer_id, f"Пользователь уже находится в глобальном бане", msg_id)
            else:
               function.reply(peer_id, f"Нельзя забанить самого себя", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /gban <user> <reason>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def gunban(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 4, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if bool(len(db.execute("SELECT * FROM ban_list WHERE user_id = ? AND type = ?", (check[0], 'global',)).fetchall())):
            if check[0] != user_id:
               servers = db.execute("SELECT * FROM server_info",).fetchall()
               for s in servers:
                  peer_id = s[0]
                  if not function.is_admin(peer_id, check[0]):
                     function.send(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} разблокировал(-а) во всех беседах {function.get_mention_nick(peer_id, check[0], db)}")
               with db:
                  db.execute("DELETE FROM ban_list WHERE user_id = ? AND type = ?", (check[0], 'global',))
            else:
               function.reply(peer_id, f"Нельзя забанить самого себя", msg_id)
         else:
            function.reply(peer_id, f"Пользователь не находится в бане", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /gunban <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def gzov(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 4, db):
      if len(text) >= 2:
         servers = db.execute("SELECT * FROM server_info").fetchall()
         for s in servers:
            peer_id = s[0]
            items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['profiles']
            members = ""
            for i in items:
               members += f"[id{i['id']}|🖤]"
            function.send(peer_id, f"📢 Вы были вызваны [id{user_id}|администратором] беседы\n\n{members}\n\n❗ Причина: {' '.join(text[1:])}")
      else:
         function.reply(peer_id, f"Используйте: /gzov <reason|text>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)