from subprocess import PIPE,Popen

print Popen("ruby tempory.rb", shell=True, stdout=PIPE).stdout.read()
