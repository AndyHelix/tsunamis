import sys
import os
import subprocess
import time

server_path = sys.argv[1]

print(server_path)

p = subprocess.Popen('python %s' % server_path, shell = False)
#stdoutput, erroutput=p.communicate()
#p = subprocess.Popen('python %s' % server_path, shell = False, stdout=subprocess.PIPE)

while 1:
    #print "new loop"
    old_mtime = os.stat(server_path).st_mtime
# sleep 3s
    time.sleep(0.5)
    new_mtime = os.stat(server_path).st_mtime
    if old_mtime != new_mtime:
# kill and run again
        p.terminate()
        print("Kill old process")
        p = subprocess.Popen('python %s' % server_path, shell = False, stdout=subprocess.PIPE)
        #p = subprocess.Popen('python %s' % server_path, shell = False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #stdoutput, erroutput=p.communicate()
        print('*'*20)
        print('*'*20)
        print("Run new process")
    else:
        #print ("no change")
        continue
        #break

#print p.communicate()
print "00000"
