import function, sqlite3, config

def addsenmoder(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 3, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if function.comparison_access(peer_id, user_id, check[0], db):
            if check[0] != user_id:
                function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} выдал(-а) права старшего модератора {function.get_mention_nick(peer_id, check[0], db)}", msg_id)
                with db:
                   db.execute("UPDATE user_info SET access = ? WHERE peer_id = ? AND user_id = ?", (2, peer_id, check[0],))
            else:
               function.reply(peer_id, f"Нельзя изменить уровень прав самому себе", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /addsenmoder <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def ssnick(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 3, db):
      check = function.check_arguments(event, 3)
      if check[0] != 0:
         server = db.execute("SELECT pull_id FROM server_info WHERE peer_id = ?", (peer_id,)).fetchone()
         if check[1] == 'type_1':
            nick = ' '.join(text[1:])
         else:
            nick = ' '.join(text[2:])
         if server[0] == 0:
            function.reply(peer_id, f"Привязка к сетке бесед отсутствует", msg_id)
            return
         if function.comparison_access(peer_id, user_id, check[0], db):
            if not '[' in list(nick) and not ']' in list(nick) and len(nick) <= 32:
               servers = db.execute("SELECT * FROM server_info WHERE pull_id = ?", (server[0],)).fetchall()
               for s in servers:
                  peer_id = s[0]
                  function.send(peer_id, f'{function.get_mention_nick(peer_id, user_id, db)} сменил(-а) ник в сетке бесед <<{server[0]}>> {function.get_mention_nick(peer_id, check[0], db)}\nНовый ник: {nick}')
                  with db:
                     db.execute("UPDATE user_info SET nick = ? WHERE peer_id = ? AND user_id = ?", (nick, peer_id, check[0],))
            else:
               function.reply(peer_id, f"Ник не должен содержать ('[]') и состоять не более чем из 32 символов", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /ssnick <user> <nick>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def srnick(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 3, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         server = db.execute("SELECT pull_id FROM server_info WHERE peer_id = ?", (peer_id,)).fetchone()
         if check[1] == 'type_1':
            nick = ' '.join(text[1:])
         else:
            nick = ' '.join(text[2:])
         if server[0] == 0:
            function.reply(peer_id, f"Привязка к сетке бесед отсутствует", msg_id)
            return
         if function.comparison_access(peer_id, user_id, check[0], db):
            servers = db.execute("SELECT * FROM server_info WHERE pull_id = ?", (server[0],)).fetchall()
            for s in servers:
               peer_id = s[0]
               if bool(len(db.execute("SELECT * FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchall())):
                  if db.execute("SELECT * FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchone()[0] != "нету":
                     function.send(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} удалил(-а) ник в сетке бесед <<{server[0]}>> у {function.get_mention_nick(peer_id, check[0], db)}")
                     with db:
                        db.execute("UPDATE user_info SET nick = ? WHERE peer_id = ? AND user_id = ?", ('нету', peer_id, check[0],))
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /srnick <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)