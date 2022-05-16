import os
import errno
import subprocess
import platform
import re
import signal
import glob

scriptpath = (os.path.dirname(os.path.abspath(__file__)) + "\\")
system = platform.uname().system

#script that checks if a process is running based on PID.
#script is from psutil
def pid_exists(pid):
    """Check whether pid exists in the current process table.
    UNIX only.
    """
    if pid < 0:
        return False
    if pid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        raise ValueError('invalid PID 0')
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise 
    else:
        return True

#uses pid_exists or windows equivalent to figure out if process is running based on PID
def search_pid(pid, system):
    if re.search('Linux', system, re.IGNORECASE):
        if pid_exists(pid) == True:
            return True
        else:
            return False
    elif re.search('Windows', system, re.IGNORECASE):
        out = subprocess.check_output(["tasklist","/fi",f"PID eq {pid}"]).strip()
        # b'INFO: No tasks are running which match the specified criteria.'
        if re.search(b'No tasks', out, re.IGNORECASE):
            return False
        else:
            return True
    else:
        raise RuntimeError(f"unsupported system={system}")

#kills process based on PID
def botkiller(pid):
    UsrInput = input('Would you like to kill processID {}?\nWARNING: this will kill any process that has the processID of {}.\nYes or No: '.format(pid,pid))
    if UsrInput == "Yes":
        print("Killing PID: {}".format(pid))
        os.kill(pid, signal.SIGTERM)
        return True
    elif UsrInput == "No":
        print("Keeping PID: {} alive, for now.".format(pid))
        return False

#Searching for .env
if os.path.exists(scriptpath + '.env'):
    print ("File: .env Found.")
else:
    print ("File: .env Not Found, Making...")
    f = open(scriptpath + '.env','w')
    Disctoken = input("Discord Bot Token: ")
    f.write('# .env\nDISCORD_TOKEN={}'.format(Disctoken))
    f.close

#Searching if PublicGagBot is running
try:
    p = open(scriptpath + ".pid",'r')
    readlines = p.readlines()
    for line in readlines:
        if "BotPID=" in line:
            try:
                pid = int(line.replace('BotPID=',''))
            except:
                raise ValueError('PID found can not exist. It either has Letters or doesn\'t exist')
    if search_pid(pid, system) == True:
        print('PublicGagBotClient is being seen as running!')
        #Asking if you want to kill Bot. pew pew pew
        Killed = botkiller(pid)
        if Killed == False:
            raise RuntimeError('Can\'t run another instance of the bot if one is already running.')
    else:
        print('PublicGabBotClient is not being seen as running.')
except FileNotFoundError:
    print('PID file not found, the bot will make one when it runs.')
    
#Searching for Newest PublicGagBotClient Script
filesfound = glob.glob(scriptpath +'PublicGagBotClient-*.py')
filesfound.sort(reverse=True)

#Asking if you want to run Newest script
print ('Found Newest Bot File to be: {}\nHow would you like to run this file?'.format(filesfound[0].replace(scriptpath,'')))
runfile = input('No = Do Not Run\nICT = In current terminal\nIB = In Background\n')
if runfile == "No":
    print('Not Running File.')
if runfile == 'ICT':
    print('Running In Current Terminal.')
    if re.search('Linux', system, re.IGNORECASE):
        os.chdir(scriptpath)
        os.system('python3 {}'.format(filesfound[0]))
    elif re.search('Windows', system, re.IGNORECASE):
        os.chdir(scriptpath)
        os.system('python {}'.format(filesfound[0]))
    else:
        raise RuntimeError(f"unsupported system={system}")
if runfile == 'IB':
    print('Running File In Background')
    if re.search('Linux', system, re.IGNORECASE):
        subprocess.Popen('nohup python3 {} &'.format(filesfound[0]),cwd=scriptpath)
    elif re.search('Windows', system, re.IGNORECASE):
        subprocess.Popen('python {} &'.format(filesfound[0]),cwd=scriptpath)
    else:
        raise RuntimeError(f"unsupported system={system}")