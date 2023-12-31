import telebot
from telebot import types
from data import get_all_folders_in_directory, find_folders_in_current_directory, get_all_files_in_directory, split_video, count_pep_unit_folders
import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


folders_date = list()
folders_hour = list()
files_path = list()

users_request = dict()

target_folder_camera = ["camera №1", "camera №2"]
target_callback_camera = ['camera1_pressed', 'camera2_pressed']

target_callback_date = ['date1_pressed', 'date2_pressed', 'date3_pressed', 'date4_pressed', 'date5_pressed', 'date6_pressed', 'date7_pressed', 'date8_pressed']

target_callback_hour = ['hour1_pressed', 'hour2_pressed', 'hour3_pressed', 'hour4_pressed', 'hour5_pressed', 'hour6_pressed', 'hour7_pressed',
                        'hour8_pressed', 'hour9_pressed', 'hour10_pressed', 'hour11_pressed', 'hour12_pressed', 'hour13_pressed', 'hour14_pressed',
                        'hour15_pressed', 'hour16_pressed', 'hour17_pressed', 'hour18_pressed', 'hour19_pressed', 'hour20_pressed', 'hour21_pressed','hour22_pressed', 'hour23_pressed', 'hour24_pressed']

target_callback_video = ['video1_pressed', 'video2_pressed', 'video3_pressed', 'video4_pressed', 'video5_pressed', 'video6_pressed', 'video7_pressed', 'video8_pressed', 'video9_pressed', 'video10_pressed', 'video11_pressed', 'video12_pressed']

#bot = telebot.TeleBot('YOUT TOKEN')

users = []


cameras_disconect = ['DISCONECT camera №1.txt','DISCONECT camera №2.txt', 'Camera №1 is ready.txt', 'Camera №2 is ready.txt']

def send_notification(filename):
    for chat_id in users:
        bot.send_message(chat_id, f"{filename.split('.')[0]}")
        os.remove(filename)


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        for file_path in cameras_disconect:
            if event.src_path.endswith(file_path):
                send_notification(os.path.basename(event.src_path))


event_handler = FileHandler()

observer = Observer()
path_error = os.getcwd()
observer.schedule(event_handler, path=path_error) #path='/' path='.'
observer.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    if user_id not in users:
        users.append(user_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Video Recordings")  # Текст кнопки
    markup.add(item)

    bot.send_message(message.chat.id, "Welcome", reply_markup=markup)



@bot.message_handler(func=lambda message: message.text == "Video Recordings")
def handle_button_click(message):
    user_id = message.chat.id
    if user_id not in users:
        users.append(user_id)
    create_buttons_folders(message)



def create_buttons_folders(message):
    buttons = []
    for i in range(len(target_folder_camera)):
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(target_folder_camera[i], callback_data=target_callback_camera[i])
        buttons.append(button)
    for button in buttons:
        markup.row(button)
    bot.send_message(message.chat.id, "Choose a camera:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    global folders_date
    global folders_hour
    global files_path
    delete_files()
    user_id = call.message.chat.id
    if user_id not in users:
        users.append(user_id)
    if call.data == 'camera1_pressed':
        try:
            folder_path = find_folders_in_current_directory([target_folder_camera[0]])[0]
            folders_date = get_all_folders_in_directory(folder_path)
            create_buttons_date(folders_date, call)
        except:
            bot.send_message(call.message.chat.id, "Currently there are no suitable directories or the camera is not running")

    elif call.data == 'camera2_pressed':
        try:
            folder_path = find_folders_in_current_directory([target_folder_camera[1]])[0]
            folders_date = get_all_folders_in_directory(folder_path)
            create_buttons_date(folders_date, call)
        except:
            bot.send_message(call.message.chat.id, "Currently there are no suitable directories or the camera is not running")

    for i, command in enumerate(target_callback_date):
        if command == call.data:
            try:
                folders_hour = get_all_folders_in_directory(folders_date[i])
                # print(folders_hour)
                create_buttons_hour(folders_hour, call)
            except:
                bot.send_message(call.message.chat.id, "Currently there are no suitable directories")


    for i, command in enumerate(target_callback_hour):
        if command == call.data:
            files_path = get_all_files_in_directory(folders_hour[i])
            create_buttons_video(files_path, call)
    
    for i, video in enumerate(target_callback_video):
        if video == call.data:
            send_mp4(call, files_path[i])



def send_mp4(call, mp4_path):
    chat_id = call.message.chat.id
    output_path = f'output_parts_{chat_id}'
    count = count_pep_unit_folders(output_path)
    output_path = f'{output_path}_{count}'
    bot.send_message(chat_id, f'Wait for a few minutes you will be sent a video clip: {mp4_path.split("/")[-1]}')
    try:
        video_paths = split_video(mp4_path, output_path)
        for i, video in enumerate(video_paths):
            if os.path.exists(video):
                with open(video, 'rb') as part_video:
                    bot.send_message(chat_id, f'Video clip day {mp4_path.split("/")[-3]}, hours {mp4_path.split("/")[-2]}, minutes {mp4_path.split("/")[-1]} _part{i}')
                    bot.send_video(chat_id, part_video)
            else:
                bot.send_message(chat_id, "MP4 file not found.")
        shutil.rmtree(output_path)
    except:
        bot.send_message(chat_id, "Try later, video in process recording.")



def create_buttons_date(folders_date, call):
    buttons = []
    for i in range(len(folders_date)):
        date = folders_date[i].split('/')[-1]
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(date, callback_data=target_callback_date[i])
        buttons.append(button)
    for button in buttons:
        markup.row(button)
    bot.send_message(call.message.chat.id, "Date:", reply_markup=markup)


def create_buttons_hour(folders_hour, call):
    buttons = []
    for i in range(len(folders_hour)):
        hour = folders_hour[i].split('/')[-1]
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(hour, callback_data=target_callback_hour[i])
        buttons.append(button)
    for button in buttons:
        markup.row(button)
    bot.send_message(call.message.chat.id, "Hours:", reply_markup=markup)


def create_buttons_video(files_path, call):
    buttons = []
    for i in range(len(files_path)):
        path = files_path[i].split('/')[-1]
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(path, callback_data=target_callback_video[i])
        buttons.append(button)
    for button in buttons:
        markup.row(button)
    bot.send_message(call.message.chat.id, "Minutes:", reply_markup=markup)

def delete_files():
    files_to_delete = ["DISCONECT camera №1.txt", "DISCONECT camera №2.txt", "Camera №1 is ready.txt", "Camera №2 is ready.txt"]
    cur_path = os.getcwd()
    
    # Перебираем файлы и папки в папке folder_path
    for root, dirs, files in os.walk(cur_path):
        for file in files:
            if file in files_to_delete:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                #print(f"Delete file: {file_path}")

def delete_folders():
    cur_path = os.getcwd()
    for root, dirs, files in os.walk(cur_path):
         for directory in dirs:
            if directory.startswith("output_parts_"):
                dir_path = os.path.join(root, directory)
                os.rmdir(dir_path)
        

if __name__ == "__main__":
    delete_files()
    delete_folders()
    bot.polling(none_stop=True)