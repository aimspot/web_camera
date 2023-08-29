import os
import time
from datetime import datetime
import cv2

def get_names_folders():
    now = datetime.now()
    date_folder = now.strftime("%d_%m_%Y")
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

def main():
    date_folder, time_folder, minute_video, past_time = get_names_folders()
    create_directory(date_folder)
    create_directory(time_folder)

    cap = cv2.VideoCapture(0)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(5))
    output_file = f'{minute_video}.mp4'
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))


    while True:
        if not cap.isOpened():
            print("Не удалось открыть камеру.")
            exit()
        

        # now = datetime.now()
        # date_folder = now.strftime("%d_%m_%Y")
        # time_folder = f'{date_folder}/{now.strftime("%H")}'        

        # current_minute = int(time.strftime("%M"))
        # start_minute = (current_minute // 5) * 5
        # end_minute = start_minute + 4

        # start_time = f"{current_minute:02d}"
        # end_time = f"{end_minute:02d}"

        # minute_folder = f'{time_folder}/{start_time}_{end_time}'
        date_folder, time_folder, minute_video, end_time = get_names_folders()


        create_directory(date_folder)
        create_directory(time_folder)


        if past_time != end_time:
            past_time = end_time
            out.release()
            output_file = f'{minute_video}.mp4'
            out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

            #create_directory(minute_folder)
        
        ret, frame = cap.read()
        out.write(frame)

if __name__ == "__main__":
    main()

