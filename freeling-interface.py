import subprocess

filename = raw_input('Please enter the name of the file you want to analyze (remember that if the file is not in the same folder as this program, you should provide the full path to the input file. Enter a file name: ')
p = subprocess.Popen('analyze -f en.cfg <'+filename+' >output.txt', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout.readlines():
    print line,
retval = p.wait()
