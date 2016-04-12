import json
from subprocess import PIPE,Popen

s =  Popen("ruby ast.rb /home/aiyanxu/study/diff++/test/test1.rb", shell=True, stdout=PIPE).stdout.read()
h = json.loads(s)
print h.get('type')
