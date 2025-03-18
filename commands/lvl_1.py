import function, sqlite3, config

def snick(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      check = function.check_arguments(event, 3)
      if check[0] != 0:
         if check[1] == 'type_1':
            nick = ' '.join(text[1:])
         else:
            nick = ' '.join(text[2:])
         if function.comparison_access(peer_id, user_id, check[0], db):
            if not '[' in list(nick) and not ']' in list(nick) and len(nick) <= 32:
               function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} сменил(-а) ник {function.get_mention_nick(peer_id, check[0], db)}\nНовый ник: {nick}", msg_id)
               with db:
                  db.execute("UPDATE user_info SET nick = ? WHERE peer_id = ? AND user_id = ?", (nick, peer_id, check[0],))
            else:
               function.reply(peer_id, f"Ник не должен содержать ('[]') и состоять не более чем из 32 символов", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /snick <user> <nick>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def rnick(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if function.comparison_access(peer_id, user_id, check[0], db):
            if bool(len(db.execute("SELECT * FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchall())):
               if db.execute("SELECT * FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchone()[0] != "нету":
                  function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} удалил(-а) ник у {function.get_mention_nick(peer_id, check[0], db)}", msg_id)
                  with db:
                     db.execute("UPDATE user_info SET nick = ? WHERE peer_id = ? AND user_id = ?", ('нету', peer_id, check[0],))
               else:
                  function.reply(peer_id, f"У пользователя нету ника", msg_id)
            else:
               function.reply(peer_id, f"У пользователя нету ника", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /rnick <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def kick(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
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
            if not function.is_admin(peer_id, check[0]) and function.in_group(peer_id, check[0]):
               config.vk_api.messages.removeChatUser(chat_id=event.chat_id, member_id=check[0])
               function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} исключил(-а) из беседы {function.get_mention_nick(peer_id, check[0], db)}\nПричина: {reason}", msg_id)
               with db:
                  db.execute("DELETE FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],))
            else:
               function.reply(peer_id, f"Пользователь является администратором или не состоит в беседе", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /snick <user> <nick>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def get_user_access(peer_id, access, db: sqlite3.Connection):
   users = db.execute("SELECT * FROM user_info WHERE peer_id = ? AND access = ?", (peer_id, access,)).fetchall()
   msg = ""
   if users != []:
      for u in users:
         if u[3] != "нету":
            msg += f"\n[id{u[1]}|{u[3]}]"
         else:
            msg += f"\n[id{u[1]}|{u[2]}]"
   else:
      msg = "\nОтсутствуют"

   return msg


def staff(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      function.reply(peer_id, f"Владелец беседы:{get_user_access(peer_id, 5, db)}\n\nСтаршие администраторы:{get_user_access(peer_id, 4, db)}\n\nАдминистраторы:{get_user_access(peer_id, 3, db)}\n\nСтаршие модераторы:{get_user_access(peer_id, 2, db)}\n\nМодераторы:{get_user_access(peer_id, 1, db)}", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def nlist(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      users = db.execute("SELECT * FROM user_info WHERE peer_id = ? ORDER BY nick ASC", (peer_id,)).fetchall()
      count = 0
      msg = ""
      for u in users:
         if u[3] != "нету":
            count += 1
            msg += f"\n[{count}]. {u[3]} - [id{u[1]}|{u[2]}]"
      function.reply(peer_id, f"Список пользователей с никами [Всего: {count}]{msg}\n\nПользователи без ников «/nonick»", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def nonick(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      items = config.vk_api.messages.getConversationMembers(peer_id=peer_id)['profiles']
      msg = ""
      count = 0
      for i in items:
         if bool(len(db.execute("SELECT * FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, i['id'],)).fetchall())):
            if db.execute("SELECT nick FROM user_info WHERE peer_id = ? AND user_id = ?", (peer_id, i['id'],)).fetchone()[0] == "нету":
               count += 1
               msg += f"\n[{count}]. [id{i['id']}|{function.get_user_name(i['id'])}]"
         else:
            count += 1
            msg += f"\n[{count}]. [id{i['id']}|{function.get_user_name(i['id'])}]"
      function.reply(peer_id, f"Список пользователей без ников [Всего: {count}]{msg}\n\nПользователеи с никами «/nlist»", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def getban(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         global_ban = ""
         local_bans = ""
         bans = db.execute("SELECT * FROM ban_list WHERE user_id = ? AND type = ?", (check[0], 'local',)).fetchall()
         gban = db.execute("SELECT * FROM ban_list WHERE user_id = ? AND type = ?", (check[0], 'global',)).fetchone()
         if gban != None:
            global_ban = f"[id{gban[3]}|Модератор] | {gban[4]} | {gban[5]}"
         else:
            global_ban = "Отсутствует"
         if len(bans) > 0:
            count = 0
            for b in bans:
               count += 1
               title = config.vk_api.messages.getConversationsById(peer_ids=b[0])['items'][0]['chat_settings']['title']
               local_bans += f"\n[{count}]. {title} | [id{b[3]}|Модератор] | {b[4]} | {b[5]}"
         else:
            local_bans = "\nОтсутствуют"
         function.reply(peer_id, f"Информация о блокировках {function.get_mention_nick(peer_id, check[0], db)}\n\nИнформация о общей блокировки в беседах:\n{global_ban}\n\nПоследние 10 блокировок в беседах:{local_bans}", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /getban <user>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def clear(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      if 'reply_message' in event.obj['message']:
         if not function.is_admin(peer_id, event.obj['message']['reply_message']['from_id']) and function.comparison_access(peer_id, user_id, event.obj['message']['reply_message']['from_id'], db):
            function.delete(peer_id, event.obj['message']['reply_message']['conversation_message_id'])
            function.send(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} очистил(-а) сообщение")
         else:
            function.reply(peer_id, f"Нельзя очистить сообщение от данного пользователя", msg_id)
      else:
         function.reply(peer_id, f"Команду /clear нужно использовать ответным сообщение", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def warn(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      check = function.check_arguments(event, 3)
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
          if user_id != check[0]:
            if not function.is_admin(peer_id, check[0]) and function.in_group(peer_id, check[0]):
               with db:
                  db.execute("INSERT INTO warn_list ('peer_id', 'user_id', 'moder_id', 'reason', 'giveDate') VALUES (?,?,?,?,?)", (peer_id, check[0], user_id, reason, function.get_moscow_date(),))
               warns = db.execute("SELECT * FROM warn_list WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchall()
               function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} выдал(-а) предупреждение {function.get_mention_nick(peer_id, check[0], db)}\nПричина: {reason}\nАктивных предупреждений: {len(warns)}", msg_id)
               if len(warns) >= 3:
                  config.vk_api.messages.removeChatUser(chat_id=event.chat_id, member_id=check[0])
                  function.send(peer_id, f"[club229655124|Помощник Степан | ГОСС] исключил из беседы {function.get_mention_nick(peer_id, check[0], db)}\nПричина: 3/3 Предупреждений")
                  with db:
                     db.execute("DELETE FROM warn_list WHERE user_id = ? AND peer_id = ?", (check[0], peer_id,))
            else:
               function.reply(peer_id, f"Пользователь является администратором или не состоит в беседе", msg_id)
          else:
             function.reply(peer_id, f"Нельзя выдать предупреждение самому себе", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /warn <user> <reason>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def unwarn(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         if function.comparison_access(peer_id, user_id, check[0], db):
            if check[0] != user_id:
               if not function.is_admin(peer_id, check[0]) and function.in_group(peer_id, check[0]):
                  warns = db.execute("SELECT * FROM warn_list WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchall()
                  if len(warns) > 0:
                     function.reply(peer_id, f"{function.get_mention_nick(peer_id, user_id, db)} снял(-а) предупреждение {function.get_mention_nick(peer_id, check[0], db)}\nАктивных предупреждений: {len(warns)-1}", msg_id)
                     warn_id = warns[len(warns)-1][5]
                     with db:
                        db.execute("DELETE FROM warn_list WHERE user_id = ? AND peer_id = ? AND warn_id = ?", (check[0], peer_id, warn_id,))
                  else:
                     function.reply(peer_id, f"У пользователя отсутствуют активные предупреждения", msg_id)
               else:
                  function.reply(peer_id, f"Пользователь является администратором или не состоит в беседе", msg_id)
            else:
               function.reply(peer_id, f"Нельзя снять предупреждение самому себе", msg_id)
         else:
            function.reply(peer_id, f"У пользователя уровень прав выше вашего", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /warn <user> <reason>", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def warnlist(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      warns = db.execute("SELECT * FROM warn_list WHERE peer_id = ?", (peer_id,)).fetchall()
      msg = ""
      count = 0
      for w in warns:
         count += 1
         msg += f"\n[{count}]. [id{w[1]}|{function.get_user_name(w[1])}] | Активных предупреждений: {len(warns)}"

      function.reply(peer_id, f"Список пользователей с варном [Всего: {count}]{msg}", msg_id)
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)

def getwarn(event, db: sqlite3.Connection):
   peer_id = event.obj['message']['peer_id']
   user_id = event.obj['message']['from_id']
   text = event.obj['message']['text'].split()
   msg_id = event.obj['message']['conversation_message_id']
   if function.check_access(peer_id, user_id, 1, db):
      check = function.check_arguments(event, 2)
      if check[0] != 0:
         warns = db.execute("SELECT * FROM warn_list WHERE peer_id = ? AND user_id = ?", (peer_id, check[0],)).fetchall()
         msg = ""
         count = 0
         for w in warns:
            count += 1
            msg += f"\n[{count}]. [id{w[2]}|Модератор] | {w[3]} | {w[4]}"

         function.reply(peer_id, f"Список предупреждений пользователя {function.get_mention_nick(peer_id, check[0], db)} [Всего: {count}]{msg}", msg_id)
      else:
         function.reply(peer_id, f"Используйте: /getwarn <user>")
   else:
      function.reply(peer_id, f'Недостаточно прав!', msg_id)