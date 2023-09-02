import os


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

# # Имена папок, которые вы хотите найти
# target_folder_names = ["camera №1", "camera №2"]

# # Получение путей к папкам
# folder_paths = find_folders_in_current_directory(target_folder_names)

# # Вывод путей к найденным папкам
# for folder_path in folder_paths:
#     print(folder_path)