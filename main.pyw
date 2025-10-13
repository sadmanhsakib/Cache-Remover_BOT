import os
import math
import shutil
import datetime
from dotenv import load_dotenv

# loading the .env file for accessing it
load_dotenv(".env")

counter = 0
previous_deletion = ""
total_space = 0.0
today = datetime.datetime.now().date().strftime("%Y-%m-%d")

# getting the data from the .env file
path_list = os.getenv("FOLDER_PATH").split(',')

storage = {}

# adding the path and storage on the dict
for path in path_list:
    storage.update({path: 0.0})
    
log_file = ""


def main():
    global counter
    global previous_deletion
    global total_space
    global log_file

    # check for log file
    if not (os.path.exists("log.csv")):
        # creates a new log file
        with open("log.csv", 'w') as file:
            # writing the header
            header = "Lifetime-Counter,Deletion-Date,Total"
            
            for key in storage:
                path_name = get_name(key)
                header += f",{path_name}"
            
            file.write(f"{header}\n")
            
    log_file = "log.csv"
    
    with open(log_file, 'r') as file:
        lines = file.readlines()
        
        # checking if the program was ever run before
        if len(lines) == 1:
            # for the first run
            counter = 1
            shouldDelete = True
        else:
            last_line = lines[-1]
            parts = last_line.split(',')
            
            # getting the previous data from the log file 
            counter = int(parts[0])
            counter += 1
            previous_deletion = parts[1]
            
            # deciding whether to delete or not
            if previous_deletion != today:
                shouldDelete = True
            else:
                shouldDelete = False

    if shouldDelete:
        previous_deletion = today
        
        # for every dir, remove the contents
        for path in storage:
            space_freed = delete_contents(path)
            storage[path] = space_freed
            
            # adding the freed space to total_space
            total_space += space_freed
        log_event()


def delete_contents(path):
    if os.path.exists(path):
        space_freed = 0.0
        
        # returns the list of filenames in that dir
        files = os.listdir(path)

        for file in files:
            current_size = 0.0

            # creates the path for that specific file
            file_path = os.path.join(path, file)

            try:
                # os.remove only deletes single files and shutil.rmtree only deletes entire directories
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    # getting the size of the file that is about to be
                    current_size = os.path.getsize(file_path)

                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    # adding the total size for each subfolder
                    current_size = get_dir_size(file_path)

                    shutil.rmtree(file_path)
            except Exception:
                # if file can't be deleted, set size to 0.0 for accurate calculation
                current_size = 0.0

             # adding the current file size to the total
            space_freed += current_size
        
        # converting to mB
        space_freed /= math.pow(1024, 2)
        space_freed = round(space_freed, 2)
        return space_freed


# calls for the function recursively until every file size is counted
def get_dir_size(path):
    dir_size = 0.0

    # os.walk() always returns a three value tuple. 
    # that's why even when not using, I need to declare 3 variables in for loop
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # creating a new file path for every file in the folder
            fp = os.path.join(dirpath, filename)

            # if the current file is a file, add it to the total size
            if os.path.isfile(fp):
                dir_size += os.path.getsize(fp)
    return dir_size


def get_name(path):
    last = path.rfind("\\")
    # 0 & last are the starting and ending index 
    index = path.rfind("\\", 0, last)

    # adjusting the name of the paths by taking the last 2 words
    name = path[index+1:]
    name = name.replace("\\", "-")

    return name


def log_event():
    global counter
    global previous_deletion
    global total_space
    global log_file

    # storing the values of the dictionary in one variable for easier writing
    storage_values = ""
    for key in storage:
        storage_values += f",{storage[key]}"

    # adding the changes to the log file
    with open(log_file, 'a') as file:
        file.write(f"{counter},{previous_deletion},{total_space}{storage_values}\n")


main()