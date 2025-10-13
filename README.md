# Auto-Junk-Remover
This is a single Python script that deletes specific folders. Upon deletion, the script logs (creates, if the log file does not exist) detailed data about the deletions in a log.csv file.
<h3>How does it work?</h3>
The script at first looks for a "log.csv" in its local directory. If there is no "log.csv" file, then it automatically creates one. Then, from that log file, it decides whether to start deleting folders in this run cycle. Then, it counts the total size for every file that can be deleted and deletes the file. After that, the script logs the event in the "log.csv" file.

<h3>How to use?</h3>
0. Download & Install the dotenv module with the help of the terminal using this command: "pip install dotenv"<br> 
1. Clone the GitHub repository.<br>
2. Create a ".env" file in the same directory and open it. <br>
3. Inside the .env file, write: FOLDER_PATH=. Add the paths inside the double inverted commas. Be sure to separate the paths with a comma(,) in between and ensure that there are no whitespaces. <br>
4. Open the Task Scheduler. (If you are not using Windows, please follow the instructions for your operating system.)<br>
5. Create a new task for the script. (Trigger can be whatever the user wants. But it's recommended to run this script at least once every week.)<br>
