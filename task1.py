# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 10:29:15 2017

@author: Alex Bardov
"""
import sys, os, subprocess, platform, psutil
import uuid

os_id = {'C' : "{3c535be8-20a8-11e3-8ba3-9ee49890ad48_C}", 'D' : "{3c535be8-20a8-11e3-8ba3-9ee49890ad48_D}", 'E' : "{3c535be8-20a8-11e3-8ba3-9ee49890ad48_E}", 'F' : "{3c535be8-20a8-11e3-8ba3-9ee49890ad48_F"}
win_update_status = "C:\\py_win_log\\win_update_status.txt"
os_list = {'7':"Windows 7", '8':"Windows 8", '10':"Windows 10"}

def get_windows_to_install(prompt):
     while True:
         try:
             value = str(raw_input(prompt))
         except ValueError:
             print("Sorry, I didn't understand that.")
             continue
         #print  "os_list.has_key(value)=="+os_list.has_key(value)  
         if os_list.has_key(value)==False:
             print("Sorry, please enter correct Windows")
             continue
         else:
             break
     return value

def get_disk_for_install(prompt):
     while True:
         try:
             value = str(raw_input(prompt)).upper()
         except ValueError:
             print("Sorry, I didn't understand that.")
             continue    
         if (value.upper() in ("C")) or (os_id.has_key(value.upper())==False):
             print("Sorry, please enter correct disk")
             continue
         else:
             break
     return value
	 
def get_record_for_installation_and_reboot_to_C(disk_for_windows,winnumber):
	if os.stat(win_update_status).st_size > 0:
		print 'Another instance of "ghost.exe" is in progress please start program later'
		sys.exit(1)
	else:
		print ("bcdedit /bootsequence %s /addfirst" %(os_id.get("C")))
		result = subprocess.call("bcdedit /bootsequence %s /addfirst" %(os_id.get("C")))
		#validate operation status
        if result==1:
            print "error"
        elif result==0:
			to_file = disk_for_windows+"\n" +str(winnumber)
			file = open(win_update_status,"w")
			file.write(to_file)
			file.close() 
			subprocess.call(["shutdown", "/r"])

def confirm_Windows_reimagin(prompt):
     while True:
         data = str(raw_input(prompt))
         if data.lower() in ['no']:
             sys.exit(0)
         elif data.lower()  not in ['yes']:
             print("Sorry, please enter correct ansver")
             continue                  
         else:
             break
     return data


leng = len(sys.argv)
if len(sys.argv)>1:
	if sys.argv[1] == "--install" and os.getenv("SystemDrive")=='C:':
		if os.stat(win_update_status).st_size > 0: 
			file = open(win_update_status,"r")
			lines = file.readlines()
			disk_to_update = lines[0].rstrip()
			win_to_instal = lines[1].rstrip()
			print ("Disk: %s install OS: %s" %(disk_to_update, os_list[win_to_instal]))
			file.close()
			result = subprocess.call(u"ping 192.168.1.1 -n 1")
			if result<0 :
				print "error"
			elif result>0:
				print ("bcdedit /bootsequence %s /addfirst" %(os_id.get(disk_to_update)))
				result = subprocess.call("bcdedit /bootsequence %s /addfirst" %(os_id.get(disk_to_update)))
				file = open(win_update_status,"w")
				file.write('')
				file.close()
				print "shutdown.exe /r"
				subprocess.call(["shutdown", "/r"])
	elif sys.argv[1] not in ['--install']:
		print "to satrt installation use --install argument"
elif len(sys.argv)==1:
		disk_for_windows = get_disk_for_install("Please enter one of the follwoing disks D E F for installing windows\n Your choice:")	
		winnumber = get_windows_to_install("Please enter the Windows number that you want to installing to disk: "+disk_for_windows+" on this PC:" +"\n 7 for win7\n 8 for win8\n 10 for win10\n Your choice: ")
		confirm_status = confirm_Windows_reimagin("The drive "+disk_for_windows+" will be reimaged by the Windows "+str(winnumber)+"\n YES - If you agree;\n No - for exit\n Your choice:")
		get_record_for_installation_and_reboot_to_C(disk_for_windows,winnumber)
