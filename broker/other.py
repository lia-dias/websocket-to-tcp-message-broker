import subprocess

returnal = subprocess.check_output('echo "134 167 225 225 210 198 131 130 182 194 135" | ./message_decoder', shell=True);

print(returnal);