import os
import time
from datetime import datetime
import cv2
import argparse 
from loguru import logger 

cameras_url = ['rtsp://admin:1q2w3e4r@192.168.20.100/Streaming/Channels/101', 'rtsp://admin:1q2w3e4r@192.168.20.98/Streaming/Channels/101'] 

def opt(): 
    parser = argparse.ArgumentParser() 
    parser.add_argument('--camera', type=int, default=1, help='№ camera [1, 2]') 
    return parser.parse_args() 


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

    #rtsp://admin:1q2w3e4r@192.168.20.98/Streaming/Channels/101
    #rtsp://admin:1q2w3e4r@192.168.20.100/Streaming/Channels/101
    #cap = cv2.VideoCapture('rtsp://admin:1q2w3e4r@192.168.20.98/Streaming/Channels/101')#98

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


        if past_time != end_time:
            past_time = end_time
            out.release()
            output_file = f'{minute_video}.mp4'
            out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

        try:
            #time.sleep(0.001)
            ret, frame = cap.read() 
            if not ret: 
                cap.release() 
                continue
            else:
                # cv2.imshow(path_root_folder, frame)
                out.write(frame)
        except: 
            cap.release() 

        # ret, frame = cap.read()
        
        # out.write(frame)

if __name__ == "__main__":
    opt = opt() 
    main(opt)