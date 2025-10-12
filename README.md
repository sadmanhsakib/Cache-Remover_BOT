# Auto-Junk-Remover
This is a single Python script that deletes specific folders. Upon deletion, the script also writes (creates, if the log file does not exist) a detailed description and data about the last deletion to the log.txt file. So far, it only works on the Windows operating system.
<h3>How does it work?</h3>
By default, it deletes five temp folders at different frequencies ranging from every day to every week. The script at first looks for a "log.txt" in its local directory. If there is no "log.txt" file, then it automatically creates one. Then, from that log file, it decides whether to delete certain folders in this run cycle. Then it counts the total size for every file that can be deleted and deletes the file. After that, the script logs the event in the "log.txt" file.

<h3>How to use?</h3>
0. Download & Install the dotenv module with the help of the terminal using this command: "pip install dotenv"<br> 
1. Clone the GitHub repository.<br>
2. Create a ".env" file in the same directory and open it. <br>
3. Write: PATH_EVERYDAY="". Add the paths inside the double inverted commas. Be sure to separate the paths with a comma(,) in between and ensure that there are no whitespaces. <br>
4. On the next line in the ".env" folder, write: PATH_EVERYWEEK="". Add the paths that you want to delete every week in here.<br>
5. Open the Task Scheduler. (If you are not using Windows, please follow the instructions for your operating system.)<br>
6. Create a new task for the script. (Trigger can be whatever the user wants. But it's recommended to run this script at least once every day.)<br>
