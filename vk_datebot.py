import config
from button import sender
import main
from config import count
from config import offset

for event in main.bot.longpoll.listen():
    if event.type == main.VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        if request == 'начать поиск':
            main.creating_database()
            main.bot.write_msg(user_id, f'Привет, {main.bot.user_info(user_id, field = 1)}')
            main.bot.send_sticker(user_id)
            candidate_information = main.bot.find_user(user_id, count, offset)
            while candidate_information is None:
                offset += 100
                candidate_information = main.bot.find_user(user_id, count, offset)
            else:
                main.bot.write_msg(event.user_id, f'Нашёл для тебя пару, что бы продолжить нажми "Далее..."')
                main.bot.find_persons(user_id,  candidate_information)
        elif request == 'далее...':
            main.creating_database()
            for i in main.line:
                candidate_information = main.bot.find_user(user_id, count, offset)
                while candidate_information is None:
                    offset += 100
                    candidate_information = main.bot.find_user(user_id, count, offset)
                else:
                    main.bot.find_persons(user_id, candidate_information)
                break
        elif request == 'очистить данные':
            main.drop_table()
            main.bot.write_msg(user_id, f'Данные удалены')
        elif request == 'профиль':
            main.bot.write_msg(user_id, f'Карточка пользователя:')
            if main.bot.user_info(user_id, field=3) == 1:
                main.bot.write_msg(user_id, f'Пол для поиска - женский')
            elif main.bot.user_info(user_id, field=3) == 2:
                main.bot.write_msg(user_id, f'Пол для поиска - мужской')
            main.bot.write_msg(user_id, f'Город для поиска - {main.bot.user_info(user_id, field=2)[0]}')
            main.bot.write_msg(user_id, f'Возраст для поиска - {main.bot.user_info(user_id, field=4)}')
        elif request == 'привет':
            main.bot.write_msg(user_id, f'Привет, {main.bot.user_info(user_id, field=1)}')
        else:
            main.bot.write_msg(event.user_id, 'Собщение не распознано, используй кнопки управления. Если кнопок нет, обнови страницу')
