import os
import math
import shutil
import datetime
from dotenv import load_dotenv

load_dotenv(".env")

counter = 0
total_space = 0.0
shouldDeleteEveryday = True
shouldDeleteEveryweek = True
today = datetime.date.today().strftime("%Y-%m-%d")
paths = os.getenv("PATHS").split(',')

# storing the path and their storage freed in a dict
# first 2 are for daily and the rest are for weekly
storage_everyday = {
    paths[0]: 0.0,
    paths[1]: 0.0
}
storage_everyweek = {
    paths[2]: 0.0,
    paths[3]: 0.0,
    paths[4]: 0.0
}

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
        file.write(f"Last temp space Freed: {storage_everyday[paths[0]]} mB\n")
        file.write(f"Last %temp% space Freed: {storage_everyday[paths[1]]} mB\n")
        file.write(f"Last prefetch space Freed: {storage_everyweek[paths[2]]} mB\n")
        file.write(f"Last Software Distribution space Freed: {storage_everyweek[paths[3]]} mB\n")
        file.write(f"Last AMD space Freed: {storage_everyweek[paths[4]]} mB")

log_file = "log.txt"


def Main():
    global counter
    global total_space

    with open(log_file, 'r') as file:
        lines = file.readlines()
        
        # getting the previous dates from the log file 
        counter = lines[0].replace("Lifetime Run Counter: ", "")
        previous_everyday_date = lines[1].replace("Last Everyday Deletion: ", "")
        previous_everyweek_date = lines[2].replace("Last Weekly Deletion: ", "")
        total_space = lines[4].replace("Total: ", "")
        total_space = total_space.replace(" mB", "")

        # converting the weekly date to int to compare it with today
        counter = int(counter)
        counter += 1
        previous_everyweek_addedvalue = int(previous_everyweek_date.replace("-", "")) + 7
        total_space = float(total_space)

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
            DeleteContents(path, storage_counter, isWeekly=False)
            storage_counter += 1

        # rounding the size upto 2 decimal points
        storage_everyday[paths[0]] = round(storage_everyday[paths[0]], 2)
        storage_everyday[paths[1]] = round(storage_everyday[paths[1]], 2)

        # adding the freed space to total_space
        total_space += storage_everyday[paths[0]] + storage_everyday[paths[1]]
        LogEvent(False)

    if shouldDeleteEveryweek:
        storage_counter = 0

        # for every dir, remove the contents
        for path in storage_everyweek:
            DeleteContents(path, storage_counter, isWeekly=True)
            storage_counter += 1

        # rounding the size upto 2 decimal points
        storage_everyweek[paths[2]] = round(storage_everyweek[paths[2]], 2)
        storage_everyweek[paths[3]] = round(storage_everyweek[paths[3]], 2)
        storage_everyweek[paths[4]] = round(storage_everyweek[paths[4]], 2)

        # after deletion, adding each folder size freed to the total_space
        total_space += storage_everyweek[paths[2]] + storage_everyweek[paths[3]] + storage_everyweek[paths[4]]
        LogEvent(True)


def DeleteContents(path, storage_counter, isWeekly):
    if os.path.exists(path):
        total_size = 0.0
        
        # returns the list of filenames in that dir
        files = os.listdir(path)

        for file in files:
            # creates the path for that specific file
            file_path = os.path.join(path, file)

            try:
                # os.remove only deletes single files and shutil.rmtree only deletes entire directories
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    # getting the size of the file that is about to be
                    total_size += os.path.getsize(file_path)
                    # converting to mB[get_size() function returns in bytes]
                    total_size /= math.pow(1024, 2)

                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    # os.walk() allways returns a three value tuple. 
                    # that's why even when not using, I need to declare 3 variables in for loop
                    for dirpath, dirnames, filenames in os.walk(path):
                        for filename in filenames:
                            # creating a new file path for every file in the folder
                            fp = os.path.join(dirpath, filename)
                            # getting the total filesize of that dir
                            total_size += os.path.getsize(fp)

                    # converting to mB
                    total_size /= math.pow(1024, 2)
                    shutil.rmtree(file_path)
            except Exception:
                # In case file can't be deleted, set size to 0.0 for accurate calculation
                total_size = 0.0

        # adding the current file size to the total based on their deletion frequency
        if isWeekly:
            match storage_counter:
                case 0:
                    storage_everyweek[path] = total_size
                case 1:
                    storage_everyweek[path] = total_size
                case 2:
                    storage_everyweek[path] = total_size
        else:
            match storage_counter:
                case 0:
                    storage_everyday[path] = total_size
                case 1:
                    storage_everyday[path] = total_size


def LogEvent(isWeekly):
    global counter
    global total_space

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
            # making the necessary changes foreach line of the log file
            lines[0] = lines[0].replace(lines[0], f"Lifetime Run Counter: {counter}\n")
            lines[2] = lines[2].replace(lines[2], f"Last Weekly Deletion: {today}\n")
            lines[3] = lines[3].replace(lines[3], f"Last Try: {now}\n")
            lines[4] = lines[4].replace(lines[4], f"Total: {total_space} mB\n")
            lines[7] = lines[7].replace(lines[7], f"Last prefetch space Freed: {storage_everyweek[paths[2]]} mB\n")
            lines[8] = lines[8].replace(lines[8], f"Last Software Distribution space Freed: {storage_everyweek[paths[3]]} mB\n")
            lines[9] = lines[9].replace(lines[9], f"Last AMD space Freed: {storage_everyweek[paths[4]]} mB")

            file.writelines(lines)
        else:
            # making the necessary changes foreach line of the log file
            lines[0] = lines[0].replace(lines[0], f"Lifetime Run Counter: {counter}\n")
            lines[1] = lines[1].replace(lines[1], f"Last Everyday Deletion: {today}\n")
            lines[3] = lines[3].replace(lines[3], f"Last Try: {now}\n")
            lines[4] = lines[4].replace(lines[4], f"Total: {total_space} mB\n")
            lines[5] = lines[5].replace(lines[5], f"Last temp space Freed: {storage_everyday[paths[0]]} mB\n")
            lines[6] = lines[6].replace(lines[6], f"Last %temp% space Freed: {storage_everyday[paths[1]]} mB\n")

            file.writelines(lines)

Main()