import subprocess

filename='c1.py'
path='/home/ismam/Desktop/work/clara-api-server/clusters/sub_code/year/category/Qn/c1.py'
entryfnc='computeDeriv'
args='[[[4.5]],[[1.0,3.0,5.5]]]'
command = f'python bin/clara feedback {path} incorrect/incorrect.py --entryfnc {entryfnc}' \
          f' --args {args} --ignoreio 1 --feedtype python'
print(command)
command = command.split()
out = subprocess.run(command, capture_output=True)
print(out.stderr.decode())
print(out.stdout.decode())
