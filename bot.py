from telebot import *
from The_main import auth
from EVS import *
from Auto_scale import *
from ECS import *
from ECC import *

bot = telebot.TeleBot('6120139999:AAFVQUjBN2XaSNI6HHGgk974Z-PyBPFNVG4')
global current_project
current_project = '5961ba0e13994cc3bf416d1ce74d5dea'


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    auth_button = types.KeyboardButton(text='Авторизоваться')
    keyboard.add(auth_button)
    bot.send_message(message.chat.id,
                     'Добро пожаловать в телеграмм-бот Cloud! Пожалуйста, авторизируйтесь, чтобы начать работу:',
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, domain_name_ask)


@bot.message_handler(content_types=['text'])
def domain_name_ask(message):
    auth_list = []
    bot.send_message(message.chat.id, "Введите логин главного пользователя:")
    bot.register_next_step_handler(message, name_ask, auth_list)


def name_ask(message, auth_list):
    bot.send_message(message.chat.id, "Введите логин IAM пользователя:")
    auth_list.append(message.text)
    bot.register_next_step_handler(message, password_ask, auth_list)


def password_ask(message, auth_list):
    bot.send_message(message.chat.id, "Введите пароль IAM пользователя:")
    auth_list.append(message.text)
    bot.register_next_step_handler(message, auth_api, auth_list)


def auth_api(message, auth_list):
    auth_list.append(message.text)
    authh = auth(auth_list[0], auth_list[1], auth_list[2])
    if (authh.status_code == 201):
        bot.send_message(message.chat.id, "Авторизация прошла успешно!")
        services(message)
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так, повторите авторизацию")


def services(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
    EVS_button = types.KeyboardButton(text='EVS')
    ECS_button = types.KeyboardButton(text='ECS')
    AS_button = types.KeyboardButton(text='AS')
    CCE_button = types.KeyboardButton(text='ECC')
    keyboard.add(EVS_button, ECS_button, AS_button, CCE_button)
    bot.send_message(message.chat.id, 'Выберите нужный сервис:', reply_markup=keyboard)
    bot.register_next_step_handler(message, choose_service)


def choose_service(message):
    if message.text == 'AS':
        names_as = []
        info = querying_as_groups(current_project, The_main.TOKEN)
        bot.send_message(message.chat.id, '{info}'.format(info=info))
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
        for i in range(info['total_number']):
            name = info['scaling_groups'][i]['scaling_group_name']
            names_as.append(name)
            keyboard.add(types.KeyboardButton(text='{name}'.format(name=name)))
        keyboard.add(types.KeyboardButton(text='Создать новую группу'))
        bot.send_message(message.chat.id, 'Выберите нужную группу или создайте новую:', reply_markup=keyboard)
        bot.register_next_step_handler(message, as_service, names_as)

    if message.text == 'ECC':
        names_ecc = []
        info = listing_clusters_of_project_api(current_project, The_main.TOKEN)
        bot.send_message(message.chat.id, '{info}'.format(info=info))
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
        for i in range(len(info['items'])):
            name = info['items'][i]['metadata']['name']
            names_ecc.append(name)
            keyboard.add(types.KeyboardButton(text='{name}'.format(name=name)))
        keyboard.add(types.KeyboardButton(text='Создать новый кластер'))
        bot.send_message(message.chat.id, 'Выберите нужный кластер или создайте новый:', reply_markup=keyboard)
        bot.register_next_step_handler(message, ecc_service, names_ecc)

    if message.text == 'ECS':
        names_ecs = []
        info = ecs_servers_list(current_project, The_main.TOKEN).json()
        bot.send_message(message.chat.id, '{info}'.format(info=info))
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
        for i in range(len(info['servers'])):
            name = info['servers'][i]['name']
            names_ecs.append(name)
            keyboard.add(types.KeyboardButton(text='{name}'.format(name=name)))
        keyboard.add(types.KeyboardButton(text='Создать новый сервер'))
        bot.send_message(message.chat.id, 'Выберите нужный сервер или создайте новый:', reply_markup=keyboard)
        bot.register_next_step_handler(message, ecs_service, names_ecs)

    if message.text == 'EVS':
        evsNames = []
        info = listing_volumes_of_project_api(current_project, token()).json()
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
        for i in range(len(info['volumes'])):
            name = info['volumes'][i]['name']
            evsNames.append(name)
            keyboard.add(types.KeyboardButton(text='{name}'.format(name=name)))
        keyboard.add(types.KeyboardButton(text='Создать новый диск'))
        bot.send_message(message.chat.id, '{a}'.format(a=len(info)), reply_markup=keyboard)
        bot.send_message(message.chat.id, 'Выберите нужный диск или создайте новый:', reply_markup=keyboard)
        bot.register_next_step_handler(message, evsService, evsNames)


def as_service(message, names_as):
    if message.text in names_as:
        name = message.text
        id_as = as_id_by_name(current_project, name, The_main.TOKEN)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
        keyboard.add(types.KeyboardButton(text='Изменить данную группу'))
        keyboard.add(types.KeyboardButton(text='Удалить данную группу'))
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)
        bot.register_next_step_handler(message, as_service_ud, name)


def ecs_service(message, names_ecs):
    if message.text in names_ecs:
        name = message.text
        id_ecs = ecs_servers_id_by_name(current_project, The_main.TOKEN, name)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
        keyboard.add(types.KeyboardButton(text='Изменить данный сервер'))
        keyboard.add(types.KeyboardButton(text='Удалить данный сервер'))
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)


def evsService(message, evsNames):
    if message.text in evsNames:
        name = message.text
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
        keyboard.add(types.KeyboardButton(text='Изменить данный диск'))
        keyboard.add(types.KeyboardButton(text='Удалить данный диск'))
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)
        bot.register_next_step_handler(message, evsServiceUD, name)
    elif message.text == "Создать новый диск":
        createDiskParaameters = []
        bot.send_message(message.chat.id, "Введите название нового диска:")
        bot.register_next_step_handler(message, newDiskSize, createDiskParaameters)


def ecc_service(message, names_ecs):
    if message.text in names_ecs:
        name = message.text
        id_ecc = ecс_id_by_name(current_project, The_main.TOKEN, name)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False, one_time_keyboard=True)
        keyboard.add(types.KeyboardButton(text='Изменить данный кластер'))
        keyboard.add(types.KeyboardButton(text='Удалить данный кластер'))
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=keyboard)


def newDiskSize(message, createDiskParaameters):
    createDiskParaameters.append(message.text)
    bot.send_message(message.chat.id, "Введите количество выделенной памяти:")
    bot.register_next_step_handler(message, newDiskAZ, createDiskParaameters)


def newDiskAZ(message, createDiskParaameters):
    createDiskParaameters.append(message.text)
    bot.send_message(message.chat.id, "Введите название зоны доступа:")
    bot.register_next_step_handler(message, diskQuantity, createDiskParaameters)


def diskQuantity(message, createDiskParaameters):
    createDiskParaameters.append(message.text)
    bot.send_message(message.chat.id, "Введите количество создаваемых дисков:")
    bot.register_next_step_handler(message, addDescription, createDiskParaameters)


def addDescription(message, createDiskParaameters):
    createDiskParaameters.append(message.text)
    bot.send_message(message.chat.id, "Вы можете добавить описание:")
    bot.register_next_step_handler(message, newDiskVolumeType, createDiskParaameters)


def as_service_ud(message, id_as):
    if message.text == 'Удалить данную группу':
        delete = delete_as_group(current_project, id_as, The_main.TOKEN).status_code
        if delete == 204:
            bot.send_message(message.chat.id, 'Группа успешно удалена!')
        else:
            bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз')


def newDiskVolumeType(message, createDiskParaameters):
    createDiskParaameters.append(message.text)
    bot.send_message(message.chat.id, "Вы можете добавить тип диска:")
    bot.register_next_step_handler(message, createDisk, createDiskParaameters)


def createDisk(message, createDiskParaameters):
    createDiskParaameters.append(message.text)
    newDisk = createEVSDisk(current_project, token(), createDiskParaameters[0], createDiskParaameters[1],
                            createDiskParaameters[2], createDiskParaameters[3], createDiskParaameters[4],
                            createDiskParaameters[5])
    if (newDisk.status_code > 199 and newDisk.status_code < 300):
        bot.send_message(message.chat.id, "Авторизация прошла успешно!")
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так, повторите авторизацию")


def evsServiceUD(message, name):
    if message.text == 'Удалить данный диск':
        delete = deleteEVSDisk(current_project, name, token()).status_code
        bot.send_message(message.chat.id, '{delete}'.format(delete=delete))
        if delete > 199 and delete < 300:
            bot.send_message(message.chat.id, 'Диск успешно удален!')
        else:
            bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз')
    elif message.text == 'Изменить данный диск':
        updateDiskParameters = []
        bot.send_message(message.chat.id, "Введите новое название данного диска:")
        bot.register_next_step_handler(message, updateDescription, updateDiskParameters, name)

def updateDescription(message, updateDiskParameters, name):
    updateDiskParameters.append(message.text)
    bot.send_message(message.chat.id, "Введите новое описание данного диска:")
    bot.register_next_step_handler(message, updateDisk, updateDiskParameters, name)


def updateDisk(message, updateDiskParameters, name):
    # bot.send_message(message.chat.id, "{a}".format(a = updateDiskParameters[0]))
    updateDiskParameters.append(message.text)
    # bot.send_message(message.chat.id, "{a}".format(a = updateDiskParameters[0]))
    updatedDisk = updateInfo(current_project, name, token(), updateDiskParameters[0], updateDiskParameters[1])
    if (updatedDisk.status_code > 199 and updatedDisk.status_code < 300):
        bot.send_message(message.chat.id, "Обновление прошло успешно!")
    else:
        bot.send_message(message.chat.id, "Что-то пошло не так, повторите авторизацию")


bot.polling(none_stop=True)
