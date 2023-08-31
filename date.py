import os
import time
from datetime import datetime, timedelta
import cv2
import argparse 
from loguru import logger
import shutil 

cameras_url = ['rtsp://admin:1q2w3e4r@192.168.20.100/Streaming/Channels/101', 'rtsp://admin:1q2w3e4r@192.168.20.98/Streaming/Channels/101'] 

def opt(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('--camera', type=int, default=1, help='№ camera [1, 2]') 
    return parser.parse_args()


def delete_old_folders(base_path):
    days_threshold = 8
    today = datetime.now()
    for folder_name in os.listdir(base_path):
        try:
            folder_date = datetime.strptime(folder_name, "%d_%m_%Y")
            if (today - folder_date) > timedelta(days=days_threshold):
                folder_path = os.path.join(base_path, folder_name)
                if os.path.isdir(folder_path):
                    shutil.rmtree(folder_path)
                    print(f"Deleting folder: {folder_path}")
        except ValueError:
            pass


def get_names_folders(path_root_folder): 
    now = datetime.now() 
    date_folder = f'{path_root_folder}/{now.strftime("%d_%m_%Y")}' 
    time_folder = f'{date_folder}/{now.strftime("%H")}'         
 
    current_minute = int(time.strftime("%M")) 
    start_minute = (current_minute // 5) * 5 
    end_minute = start_minute + 4 
 
    start_time = f"{current_minute:02d}" 
    end_time = f"{end_minute:02d}" 
 
    minute_folder = f'{time_folder}/{start_time}_{end_time}' 
 
    return date_folder, time_folder, minute_folder, end_time


def create_directory(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass


def main(opt):
    path_root_folder = f'camera №{opt.camera}' 
    date_folder, time_folder, minute_video, past_time = get_names_folders(path_root_folder)
    create_directory(date_folder)
    create_directory(time_folder)

    cap = cv2.VideoCapture(cameras_url[opt.camera - 1])

    frame_width = 1920#int(cap.get(3))
    frame_height = 1080#int(cap.get(4))
    fps = 25
    output_file = f'{minute_video}.mp4'
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))


    while True:
        if not cap.isOpened():
            print("Не удалось открыть камеру.")
            cap = cv2.VideoCapture(cameras_url[opt.camera - 1])
            
        
        date_folder, time_folder, minute_video, end_time = get_names_folders(path_root_folder)


        create_directory(date_folder)
        create_directory(time_folder)
        delete_old_folders(path_root_folder)


        if past_time != end_time:
            past_time = end_time
            out.release()
            output_file = f'{minute_video}.mp4'
            out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

        try:
            ret, frame = cap.read() 
            if not ret: 
                cap.release() 
                continue
            else:
                out.write(frame)
        except: 
            cap.release() 

if __name__ == "__main__":
    opt = opt() 
    main(opt)