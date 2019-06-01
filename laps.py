import subprocess, sys
password = ''
# TODO do some exception handling here for system args
if len(sys.argv) > 1: computer = sys.argv[1]
else: exit()

p = subprocess.Popen(["powershell.exe", 
              "C:\\Users\laim\\Desktop\SLAPS\laps.ps1 {}".format(computer)], stdout=subprocess.PIPE)
(output, err) = p.communicate()
p_status = p.wait()
output = output.split()
if len(output) > 10: password = output[10].decode('UTF-8')

print("Command output : {}".format(password))
print("Command exit status/return code : {}".format(p_status))