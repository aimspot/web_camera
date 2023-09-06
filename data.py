import os
from moviepy.editor import VideoFileClip


def get_all_folders_in_directory(current_directory):
    folders = []
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if os.path.isdir(item_path):
            folders.append(item_path)
    sorted_folders = sorted(folders)
    return sorted_folders


def find_folders_in_current_directory(folder_names):
    current_directory = os.getcwd()
    folder_paths = []
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        if os.path.isdir(item_path) and item in folder_names:
            folder_paths.append(item_path)
    return folder_paths


def get_all_files_in_directory(directory_path):
    file_paths = []
    for root, directories, files in os.walk(directory_path):
        files.sort()
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


def split_video(input_video_path, output_dir, max_size_mb=49):
    path_split_video = list()
    video = VideoFileClip(input_video_path)
    total_bytes = os.path.getsize(input_video_path)
    part_size_bytes = max_size_mb * 1024 * 1024
    num_parts = total_bytes // part_size_bytes + 1
    os.makedirs(output_dir, exist_ok=True)
    for i in range(num_parts):
        start_time = i * video.duration / num_parts
        end_time = (i + 1) * video.duration / num_parts
        subclip = video.subclip(start_time, end_time)
        subclip.write_videofile(os.path.join(output_dir, f'part_{i + 1}.mp4'))
        path_split_video.append(os.path.join(output_dir, f'part_{i + 1}.mp4'))
    return path_split_video


def count_pep_unit_folders(out_path):
    count = 0
    cur_path = os.getcwd()

    directory_contents = os.listdir(cur_path)

    for item in directory_contents:
        item_path = os.path.join(cur_path, item)
        
        if os.path.isdir(item_path) and item.startswith(out_path):
            count += 1
    return count

# if __name__ == "__main__":
#     input_video_path = "/Users/misha/Desktop/GitHub/web_camera/camera №1/03_09_2023/14/05-09.mp4"
#     output_dir = "output_parts"
#     # max_size_mb = 49
#     split_video(input_video_path, output_dir)