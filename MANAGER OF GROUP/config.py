from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api import VkApi

session_vk = VkApi(token="vk1.a.EfNLHGOP1abrcu0hwYC1ZRKTwLyxL5C_1hoQ8pVvZE3AUQGLxRITe0HY6cZluqwYo7k4ple2qbWyXRucJRuKStlj02dw8zrYoLtxuV3x1vrL5kmaD8tjgy_ibUbjB51LGPF88Bk7Ci_5PK-fd6m3dEqP-YPNvTTlyCTpqsIV6YSOJay0OjZIxzjD9M5pFapY85mBxhZUSvs8SOynK8vmPQ")
vk_api = session_vk.get_api()
longpoll = VkBotLongPoll(session_vk, 229655124)