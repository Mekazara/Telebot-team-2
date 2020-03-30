import telebot
from telebot import *
import json

bot = telebot.TeleBot('1082851546:AAFgibZTTsO_i0U2x9M1k2NVPuv_Rh-n5XE')
list_of_district = ['Первомайский', 'Ленинский', 'Свердловский', 'Октябрьский']
address = ''
district = ''
name = ''
mask = ''

# greeting
@bot.message_handler(commands=['start'])
def send_hello(message):
    choice_button = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text='Пациент', callback_data="patient")
    btn2 = types.InlineKeyboardButton(text='Фармацевт', callback_data="pharmacist")
    choice_button.add(btn1, btn2)
    bot.send_message(message.chat.id, f'Добро пожаловать, {message.from_user.first_name}! '
                                      f'Кто вы?', reply_markup=choice_button)

# helper
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, f'Чтобы начать работу с ботом напишите /start, {message.from_user.first_name}!')

# start buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'patient':
        buttons_sick = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='Аптеки Бишкека', callback_data='chemistry')
        btn2 = types.InlineKeyboardButton(text='Поиск по адресу', callback_data='district')
        btn3 = types.InlineKeyboardButton(text='Выйти', callback_data='exit')
        buttons_sick.add(btn1, btn2, btn3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите категорию", reply_markup=buttons_sick)

    elif call.data == "pharmacist":
        button_district_choice = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Первомайский')
        btn2 = types.KeyboardButton('Ленинский')
        btn3 = types.KeyboardButton('Свердловский')
        btn4 = types.KeyboardButton('Октябрьский')
        btn5 = types.KeyboardButton('Назад')
        button_district_choice.add(btn1, btn2, btn3, btn4, btn5)
        message_ = bot.send_message(call.message.chat.id, text='Выберите район', reply_markup=button_district_choice)
        bot.register_next_step_handler(message_, get_from_superdata_pharm)

    elif call.data == 'chemistry' or call.data == 'exit' or call.data == 'district':
        if call.data == 'chemistry':
            button_district_for_patient = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
            btn_1 = types.KeyboardButton('Первомайский')
            btn_2 = types.KeyboardButton('Ленинский')
            btn_3 = types.KeyboardButton('Свердловский')
            btn_4 = types.KeyboardButton('Октябрьский')
            btn_5 = types.KeyboardButton('Назад')
            button_district_for_patient.add(btn_1, btn_2, btn_3, btn_4, btn_5)
            mess = bot.send_message(call.message.chat.id, text='Выберите район',
                                    reply_markup=button_district_for_patient)
            bot.register_next_step_handler(mess, get_from_superdata)
        elif call.data == 'exit':
            bot.send_message(call.message.chat.id, 'Досвидания')
        elif call.data == 'district':
            address_from_user = bot.send_message(call.message.chat.id, 'Напишите адрес аптеки')
            bot.register_next_step_handler(address_from_user, get_adrs)

# checking if it's not /start or /help and save chemistry name
@bot.message_handler(content_types=['text'])
def send_name_chemistry(message):
    if message.text != '/start' and message.text != '/help':
        global name
        name = message.text
        msg = bot.send_message(chat_id=message.chat.id, text='Напишите адрес аптеки')
        bot.register_next_step_handler(msg, get_address)
    elif message.text == '/start':
        bot.send_message(chat_id=message.chat.id, text='Похоже вы хотите начать с начала. Напишите /start')
    elif message.text == '/help':
        bot.send_message(chat_id=message.chat.id, text='Похоже вы нуждаетесь в помощи, тогда напишите /help')

# checking if it's not /start or /help and save address
@bot.message_handler(content_types=['text'])
def get_address(message):
    if message.text != '/start' and message.text != '/help':
        global address
        address = message.text
        msg2 = bot.send_message(chat_id=message.chat.id, text='Напишите количество масок в наличии')
        bot.register_next_step_handler(msg2, save_all_data)
    elif message.text == '/start':
        bot.send_message(chat_id=message.chat.id, text='Похоже вы хотите начать с начала. Напишите /start')
    elif message.text == '/help':
        bot.send_message(chat_id=message.chat.id, text='Похоже вы нуждаетесь в помощи, тогда напишите /help')

# save all data in json
@bot.message_handler(content_types=['text'])
def save_all_data(message):
    if message.text.isnumeric():
        global mask
        mask = int(message.text)
        # msg3 = bot.send_message(chat_id=message.chat.id, text='Данные приняты')
        # bot.register_next_step_handler(msg3, save_all_data)
        try:
            with open('data.json') as superfile:
                all_data = json.load(superfile)
                if type(all_data) is dict:
                    all_data = [all_data]
                    superdata = {'district': district,
                                 'name': name,
                                 'address': address,
                                 'mask': mask}
                    all_data.append(superdata)
                    with open('data.json', 'w') as new_file:
                        json.dump(all_data, new_file, ensure_ascii=False)
                        bot.send_message(chat_id=message.chat.id, text='Спасибо, все данные записаны. Всего доброго!')
                elif type(all_data) is list:
                    superdata = {'district': district,
                                 'name': name,
                                 'address': address,
                                 'mask': mask}
                    all_data.append(superdata)
                    with open('data.json', 'w') as new_file:
                        json.dump(all_data, new_file, ensure_ascii=False)
                        bot.send_message(chat_id=message.chat.id, text='Спасибо, все данные записаны. Всего доброго!')

        except:
            with open('data.json', 'a', encoding='utf-8') as superfile:
                superdata = {'district': district,
                             'name': name,
                             'address': address,
                             'mask': mask}
                json.dump(superdata, superfile, ensure_ascii=False)
                bot.send_message(chat_id=message.chat.id, text='Спасибо, все данные записаны. Всего доброго!')

    else:
        smth = bot.send_message(chat_id=message.chat.id, text='Напишите количество цифрами')
        bot.register_next_step_handler(smth, save_all_data)

# getting data for patient / only start going into data base and reading
@bot.message_handler(content_types=['text'])
def get_from_superdata(message):
    chosen_district = message.text
    if chosen_district in list_of_district:
        try:
            with open('data.json') as new_file:
                data = json.load(new_file)
                if type(data) is dict:
                    name_of_district = data['district']
                    chem_name = data['name']
                    adrs = data['address']
                    amount = data['mask']
                    if chosen_district == name_of_district:
                        bot.send_message(chat_id=message.chat.id,
                                         text=f'В районе {chosen_district} в аптеке "{chem_name}'
                                              f'по адресу {adrs} {amount} масок')
                    else:
                        bot.send_message(chat_id=message.chat.id,
                                         text=f'В районе {chosen_district} пока нет зарегистрированных аптек')
                elif type(data) is list:
                    list_ = []
                    for d in data:
                        name_of_district = d['district']
                        list_.append(name_of_district)
                        if chosen_district == name_of_district:
                            chem_name = d['name']
                            adrs = d['address']
                            amount = d['mask']
                            bot.send_message(chat_id=message.chat.id,
                                             text=f'В районе {chosen_district} в аптеке "{chem_name}" '
                                                  f'по адресу {adrs} {amount} масок')
                        else:
                            continue

                    if chosen_district in list_:
                        bot.send_message(chat_id=message.chat.id,
                                         text='Всего доброго!')
                    else:
                        bot.send_message(chat_id=message.chat.id,
                                         text=f'В районе {chosen_district} пока нет информации')
        except:
            bot.send_message(chat_id=message.chat.id, text='Извините, пока нет информации о наличии масок.'
                                                           'Попробуйте зайти позже!')

# getting data, sending msg to user if there is a chemistry with that adrs
@bot.message_handler(content_types=['text'])
def get_adrs(message):
    chosen_adrs = message.text
    try:
        with open('data.json') as info_file:
            data = json.load(info_file)
            if type(data) is dict:
                name_of_district = data['district']
                chem_name = data['name']
                adrs = data['address']
                amount = data['mask']
                if chosen_adrs == adrs:
                    bot.send_message(chat_id=message.chat.id,
                                     text=f'В районе {name_of_district} в аптеке "{chem_name}'
                                          f'по адресу {adrs} {amount} масок')
                else:
                    bot.send_message(chat_id=message.chat.id,
                                     text=f'В аптеке по адресу {chosen_adrs} пока нет зарегистрированных аптек')
            elif type(data) is list:
                list_new = []
                for d in data:
                    adrs = d['address']
                    list_new.append(adrs)
                    if chosen_adrs == adrs:
                        name_of_dist = d['district']
                        chem_name = d['name']
                        amount = d['mask']
                        bot.send_message(chat_id=message.chat.id,
                                         text=f'В районе {name_of_dist} в аптеке "{chem_name}" '
                                              f'по адресу {chosen_adrs} {amount} масок')
                    else:
                        continue
                if chosen_adrs in list_new:
                    bot.send_message(chat_id=message.chat.id,
                                     text='Всего доброго!')
                else:
                    bot.send_message(chat_id=message.chat.id,
                                     text=f'По адресу {chosen_adrs} пока нет информации')
    except:
        bot.send_message(chat_id=message.chat.id, text='Извините, пока нет информации о наличии масок.'
                                                       'Попробуйте зайти позже!')

# for pharmacist getting data
@bot.message_handler(content_types=['text'])
def get_from_superdata_pharm(message):
    chosen_district = message.text
    global district
    district = message.text
    if chosen_district in list_of_district:
        try:
            with open('data.json') as new_file:
                data = json.load(new_file)
                if type(data) is dict:
                    name_of_district = data['district']
                    chem_name = data['name']
                    if chosen_district == name_of_district:
                        kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                        btn1 = types.KeyboardButton('Обновить')
                        btn2 = types.KeyboardButton('Записать')
                        kb1.add(btn1, btn2)
                        msg_choose = bot.send_message(chat_id=message.chat.id,
                                         text=f'В районе {chosen_district} зарегистрирована "{chem_name}"  '
                                              f'Вы хотите обновить данные или записать новые?', reply_markup=kb1)
                        bot.register_next_step_handler(msg_choose, refresh_set)

                    else:
                        sug_msg = bot.send_message(chat_id=message.chat.id,
                                                   text='Напишите название вашей аптеки, чтобы записать новые данные')
                        bot.register_next_step_handler(sug_msg, send_name_chemistry)

                elif type(data) is list:
                    list_ = []
                    list2 =[]
                    for d in data:
                        name_of_district = d['district']
                        chem_name = d['name']
                        adrs = d['address']
                        list_.append(name_of_district)
                        list2.append(chem_name)
                        if chosen_district == name_of_district:
                            kb1 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                            btn1 = types.KeyboardButton('Обновить')
                            btn2 = types.KeyboardButton('Записать')
                            kb1.add(btn1, btn2)
                        else:
                            continue
                    if chosen_district not in list_:
                        bot.send_message(chat_id=message.chat.id,
                                         text=f'В районе {chosen_district} пока нет зарегистрированных аптек.'
                                              f'Напишите название аптеки, чтобы записать данные')
                    else:
                        for item in list_:
                            if chosen_district == item:
                                bot.send_message(chat_id=message.chat.id,
                                                 text=f'В районе {chosen_district} зарегистрирована "{chem_name}" '
                                                      f'по адресу {adrs}.')

                        msg_choose = bot.send_message(chat_id=message.chat.id,
                                                  text=f'Вы хотите обновить данные или записать новые?',
                                                  reply_markup=kb1)
                        bot.register_next_step_handler(msg_choose, refresh_set)
        except:
            mss = bot.send_message(chat_id=message.chat.id,
                                   text='Пока нет информаций. Напишите название аптеки, чтобы записать данные')
            bot.register_next_step_handler(mss, send_name_chemistry)

# if pharm wants to udate or write smth
@bot.message_handler(content_types=['text'])
def refresh_set(message):
    choice = message.text
    if choice == 'Обновить':
        try:
            with open('data.json') as f:
                data = json.load(f)
                if type(data) is dict:
                    adr = data['address']
                    name = data['name']
                    kb2 = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                    yes = types.KeyboardButton('Да')
                    no = types.KeyboardButton('Нет')
                    kb2.add(yes, no)
                    msg1 = bot.send_message(chat_id=message.chat.id, text=f'Совпадают ли адрес и название аптеки?\n'
                                                                   f'{adr} {name}', reply_markup=kb2)
                    bot.register_next_step_handler(msg1, yes_no_dict)

                elif type(data) is list:
                    for d in data:
                        chosen_dist = d['district']
                        if chosen_dist == district:
                            kb = types.ReplyKeyboardMarkup(True, True)
                            btn1 = types.KeyboardButton('Да')
                            btn2 = types.KeyboardButton('Нет')
                            kb.add(btn1, btn2)
                            mssg = bot.send_message(chat_id=message.chat.id,
                                                    text=f'Это ваша аптека?\n {d["name"]} {d["address"]}',
                                                    reply_markup=kb)
                            bot.register_next_step_handler(mssg, yes_no_list)

                        else:
                            continue

        except:
            bot.send_message(chat_id=message.chat.id, text='Something is wrong')

    elif choice == 'Записать':
        some_msg = bot.send_message(chat_id=message.chat.id, text='Напишите название аптеки')
        bot.register_next_step_handler(some_msg, send_name_chemistry)

# way to choose update or write a new one
@bot.message_handler(content_types=['text'])
def yes_no_list(message):
    yes_or_no = message.text
    if yes_or_no == 'Да':
        mtf = bot.send_message(chat_id=message.chat.id, text='Напишите количество масок')
        bot.register_next_step_handler(mtf, update)
    elif yes_or_no == 'Нет':
        ms = bot.send_message(chat_id=message.chat.id,
                              text='Напишите название аптеки, чтобы записать данные')
        bot.register_next_step_handler(ms, send_name_chemistry)

# way to choose update or write a new one
@bot.message_handler(content_types=['text'])
def yes_no_dict(message):
    if message.text == 'Да':
        mtf = bot.send_message(chat_id=message.chat.id, text='Напишите количество масок')
        bot.register_next_step_handler(mtf, update)

    elif message.text == 'Нет':
        ms = bot.send_message(chat_id=message.chat.id,
                         text='Напишите название аптеки, чтобы записать данные')
        bot.register_next_step_handler(ms, send_name_chemistry)

# if
@bot.message_handler(content_types=['text'])
def update(message):
    if message.text.isnumeric():
        global mask
        mask = int(message.text)
        try:
            with open('data.json') as f:
                data = json.load(f)
                if type(data) is dict:
                    data['district'] = district
                    data['name'] = name
                    data['address'] = address
                    with open('data.json', 'w') as sf:
                        superdata = {'district': district,
                                     'name': name,
                                     'address': address,
                                     'mask': mask}
                        json.dump(superdata, sf, ensure_ascii=False)
                        bot.send_message(chat_id=message.chat.id, text='Спасибо, все данные записаны. Всего доброго!')
                elif type(data) is list:
                    for d in data:
                        chosen_dist = d['district']
                        if district == chosen_dist:
                            nam = d['name']
                            adr = d['address']
                            with open('data.json', 'w') as sf:
                                superdata = {'district': district,
                                             'name': nam,
                                             'address': adr,
                                             'mask': mask}
                                json.dump(superdata, sf, ensure_ascii=False)
                                bot.send_message(chat_id=message.chat.id,
                                                 text='Спасибо, все данные записаны. Всего доброго!')
                        else:
                            continue


        except:
            print('smth is wrong')
    else:
        smth = bot.send_message(chat_id=message.chat.id, text='Напишите количество цифрами')
        bot.register_next_step_handler(smth, update)


if __name__ =='__main__':
    bot.polling()
