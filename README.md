# Cache-RemoverBOT
This is a single Python script that deletes specific folders. Upon deletion, the script also writes (creates, if the log file does not exist) a detailed description and data about the last deletion to the log.txt file. So far, it only works on the Windows operating system.
<h3>How does it work?</h3>
By default, it deletes five temp folders at different frequencies ranging from every day to every week. The script at first looks for a "log.txt" in its local directory. If there is no "log.txt" file, then it automatically creates one. Then, from that log file, it decides whether to delete certain folders in this run cycle. Then it counts the total size for every file that can be deleted and deletes the file. After that, the script logs the event in the "log.txt" file.

<h3>How to use?</h3>
1. Download the GitHub repository.<br>
2. Unzip the repository.<br>
3. Replace line 14 of the main.pyw file, with the paths that you want to use.<br>
4. Save and close the script.<br>
5. Open the Task Scheduler.<br>
6. Create a new task for the script. (Trigger can be whatever the user wants. But it's recommended to run this script at least once every day.)<br>
