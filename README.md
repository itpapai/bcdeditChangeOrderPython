Installation:
on drive C there should be a folder “py_win_log” where the user’s choice will be stored in the file win_update_status.txt;
for OS on drive C, you need to configure the script to run with the "--install" switch when logging in (using Task Scheduler). ;
         I did it this way, created a bat file which contains: <full path to python.exe> <full path to task_1.py> --install (as example: C:\Users\Alex\Anaconda2\python.exe L:\task_1 .py --install);
         indicated that it is necessary to run this file once when logging in;
on the remaining disks you need to run the script (from the command line) or create a bat nickname;
The script must be run from a user with Administrator rights;
