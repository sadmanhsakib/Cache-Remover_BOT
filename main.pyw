import os
import math
import shutil
import datetime
from dotenv import load_dotenv

# loading the dotenv file for accessing it
load_dotenv(".env")

counter = 0
total_space = 0.0
shouldDeleteEveryday = True
shouldDeleteEveryweek = True
today = datetime.date.today().strftime("%Y-%m-%d")

# getting the data from the .env file
path_everyday = os.getenv("PATH_EVERYDAY").split(',')
path_everyweek = os.getenv("PATH_EVERYWEEK").split(',')

# creating empty dictionary for storing path and their storage
storage_everyday = {}
storage_everyweek = {}

# adding the path and storage on the dict
for path in path_everyday:
    storage_everyday.update({path: 0.0})
for path in path_everyweek:
    storage_everyweek.update({path: 0.0})


def main():
    global counter
    global total_space

    # Creates a log.txt file, if missing
    if not (os.path.exists("log.txt")):
        # creates a new log.txt file
        with open("log.txt", 'w') as file:
            # writing the starting lines
            file.write(f"Lifetime Run Counter: {counter}\n")
            file.write("Last Everyday Deletion: 2020-01-01\n")
            file.write("Last Weekly Deletion: 2020-01-01\n")
            file.write("Last Try: 2020-01-01\n")
            file.write(f"Total: {total_space} mB\n")
            file.write("Daily Deletion:\n")

            # writing the everyday lines
            for key in storage_everyday.keys():
                path_name = get_name(key)
                file.write(f"Last {path_name} space Freed: {storage_everyday[key]} mB\n")

            file.write("Weekly Deletion:\n")

            # writing the everyweek lines
            for key in storage_everyweek.keys():
                path_name = get_name(key)
                file.write(f"Last {path_name} space Freed: {storage_everyweek[key]} mB\n")
    log_file = "log.txt"

    with open(log_file, 'r') as file:
        lines = file.readlines()
        
        # getting the previous dates from the log file 
        counter = lines[0].replace("Lifetime Run Counter: ", "")
        previous_everyday_date = lines[1].replace("Last Everyday Deletion: ", "")
        previous_everyweek_date = lines[2].replace("Last Weekly Deletion: ", "")
        total_space = lines[4].replace("Total: ", "")

        total_space = total_space.replace(" mB", "")
        counter = int(counter)
        counter += 1
        total_space = float(total_space)

        # converting the weekly date to int to compare it with today
        previous_everyweek_addedvalue = int(previous_everyweek_date.replace("-", "")) + 7

    # Checking whether to Delete or not
    if (previous_everyday_date.strip() != today.strip()):
        shouldDeleteEveryday = True
    else:
         shouldDeleteEveryday= False
    if previous_everyweek_addedvalue <= int(today.replace("-", "")):
        shouldDeleteEveryweek = True
    else:
        shouldDeleteEveryweek = False

    if shouldDeleteEveryday:
        storage_counter = 0

        # for every dir, remove the contents
        for path in storage_everyday:
            delete_contents(path, storage_counter, isWeekly=False)
            storage_counter += 1

            # rounding the size upto 2 decimal points
            storage_everyday[path] = round(storage_everyday[path], 2)

            # adding the freed space to total_space
            total_space += storage_everyday[path]
        
        log_event(isWeekly=False)

    if shouldDeleteEveryweek:
        storage_counter = 0

        # for every dir, remove the contents
        for path in storage_everyweek:
            delete_contents(path, storage_counter, isWeekly=True)
            storage_counter += 1

            # rounding the size upto 2 decimal points
            storage_everyweek[path] = round(storage_everyweek[path], 2)

            # adding the freed space to total_space
            total_space += storage_everyweek[path]
        
        log_event(isWeekly=True)


def delete_contents(path, storage_counter, isWeekly):
    if os.path.exists(path):
        path_space_freed = 0.0
        
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
                    # converting to mB[get_size() function returns in bytes]
                    current_size /= math.pow(1024, 2)

                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    # adding the total size for each subfolder
                    current_size = get_dir_size(file_path)

                    # converting to mB
                    current_size /= math.pow(1024, 2)
                    
                    shutil.rmtree(file_path)
            except Exception:
                # In case file can't be deleted, set size to 0.0 for accurate calculation
                current_size = 0.0

             # adding the current file size to the total
            path_space_freed += current_size
        
        # updating the total space freed
        if isWeekly:
            match storage_counter:
                case 0:
                    storage_everyweek[path] = path_space_freed
                case 1:
                    storage_everyweek[path] = path_space_freed
                case 2:
                    storage_everyweek[path] = path_space_freed
        else:
            match storage_counter:
                case 0:
                    storage_everyday[path] = path_space_freed
                case 1:
                    storage_everyday[path] = path_space_freed


# calls for the function recursively until every file size is counted
def get_dir_size(path):
    dir_size = 0.0

    # os.walk() allways returns a three value tuple. 
    # that's why even when not using, I need to declare 3 variables in for loop
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            # creating a new file path for every file in the folder
            fp = os.path.join(dirpath, filename)

            # if the current file is a file, add it to the total size
            if os.path.isfile(fp):
                dir_size += os.path.getsize(fp)
            # recursively calling the function to get the size of the dir
            else:
                get_dir_size(fp)

    return dir_size


def get_name(path):
    last = path.rfind("\\")
    # 0 & last are the starting and ending index 
    index = path.rfind("\\", 0, last)

    # adjusting the name of the paths by taking the last 2 words
    name = path[index+1:]
    name = name.replace("\\", " ")

    return name


def log_event(isWeekly):
    global counter
    global total_space
    global path_name
    log_file = "log.txt"

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, 'r') as file:
        # storing the lines of the log in a list
        lines = file.readlines()

    # deleting the log file
    os.remove(log_file)

    # recreating the log file
    with open(log_file, 'w') as file:
        total_space = round(total_space, 2)

        # checking if the logging is for weekly or daily deletion
        if isWeekly:
            # making the changes on the initial lines
            lines[0] = lines[0].replace(lines[0], f"Lifetime Run Counter: {counter}\n")
            lines[2] = lines[2].replace(lines[2], f"Last Weekly Deletion: {today}\n")
            lines[3] = lines[3].replace(lines[3], f"Last Try: {now}\n")
            lines[4] = lines[4].replace(lines[4], f"Total: {total_space} mB\n")
            
            n = 0
            # getting the weekly data index
            for i in range(len(lines)):
                if lines[i] == "Weekly Deletion:\n":
                    n = i + 1
                    break

            # updating the weekly data
            for key in storage_everyweek:
                path_name = get_name(key)
                lines[n] = lines[n].replace(lines[n], f"Last {path_name} space Freed: {storage_everyweek[key]} mB\n")
                n += 1
        else:
            # making the changes on the initial lines
            lines[0] = lines[0].replace(lines[0], f"Lifetime Run Counter: {counter}\n")
            lines[1] = lines[1].replace(lines[1], f"Last Everyday Deletion: {today}\n")
            lines[3] = lines[3].replace(lines[3], f"Last Try: {now}\n")
            lines[4] = lines[4].replace(lines[4], f"Total: {total_space} mB\n")
            
            n = 0
            # getting the daily data index
            for i in range(len(lines)):
                if lines[i] == "Daily Deletion:\n":
                    n = i + 1
                    break

            # updating the daily data
            for key in storage_everyday:
                path_name = get_name(key)
                lines[n] = lines[n].replace(lines[n], f"Last {path_name} space Freed: {storage_everyday[key]} mB\n")
                n += 1
        
        file.writelines(lines)


main()