'''
Created on May 31, 2015

@ author: Dhaneesh

'''

import os
import platform
import getpass
cwd = os.getcwd().replace("\\", "/")
dir_list = []
l = os.walk(cwd)
for i in l:
    dr, *sdr = i
    for j in sdr:
        for x in j:
            if not os.path.isfile(dr+"/"+x):
                dir_list.append((dr+"/"+x).replace("\\", "/"))
m = "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/config.py"
if platform.system() == 'Windows':
    ls = ["C:/Python34/"]
    s = "C:/Users/"+getpass.getuser()+"/Google Drive/"
    if os.path.exists(s):
        ls.append(s+"WebApp")
    for i in ls:
        if not os.path.exists(i):
            os.makedirs(i)
    t = open(ls[0]+"config.py", "w")
else:
    t = open(m, "w")
s = "import sys\nsys.path.append('"+cwd+"')\n"
for i in dir_list:
    s = s+"sys.path.append('"+i+"')\n"
s = s + "FRAME_PATH ='"+cwd+"'\n"

t.write(s)
t.close()

# l = [cwd+"/webappcmd_v2.pyc", cwd+"/webappcmd_v2.py"]
# sl = [cwd+"/scheduler.pyc", cwd+"/scheduler.py"]

# for i in l:
#     if os.path.exists(i):
#         l_p = i
        
# for j in sl:
#     if os.path.exists(i):
#         sl_p = j


# if platform.system() == "Windows":
#     f = open(cwd+"/webappcmd_v2.bat", "w")
#     f.write("@echo off\nC:/Python34/python "+l_p)
#     f.close()
#     f = open(cwd+"/schedular.bat", "w")
#     f.write("@echo off\nC:/Python34/python "+sl_p)
#     f.close()    
#     f = open(cwd+"/schedular_v2.bat", "w")
#     f.write("@echo off\nC:/Python34/python schecular_v2.py")
#     f.close()
# else:
#     f = open(cwd+"/webappcmd_v2.sh", "w")
#     f.write("cd `dirname $BASH_SOURCE`\nclear;\npython3.4 "+l_p)
#     f.close()
#     f = open(cwd+"/schedular.sh", "w")
#     f.write("cd `dirname $BASH_SOURCE`\nclear;\npython3.4 "+sl_p)
#     f.close()