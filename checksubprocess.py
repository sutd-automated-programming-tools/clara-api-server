import os, subprocess

file_path = '/examples/correct'
filenames = ['c1.py', 'c2.py']
cluster_path = os.getcwd() + '/clusters' + file_path
entryfnc = 'computeDeriv'
args = '[[[4.5]],[[1.0,3.0,5.5]]]'
path = ""
for filename in filenames:
    path += os.getcwd() + f"{file_path}/" + filename + " "
os.makedirs(cluster_path, exist_ok=True)
print(path)
command = f'clara cluster {path} --clusterdir {cluster_path} --entryfnc {entryfnc} --args {args} ' \
          f'--ignoreio 1'.split()
out = subprocess.run(command, capture_output=True)
if out.stdout == b'':
    print(out.stderr.decode())
else:
    print(out.stdout.decode())
