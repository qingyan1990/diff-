from parser import Parser
#from node import *
from json import loads
from subprocess import PIPE,Popen
#import diff

s1 =  Popen("ruby ast.rb /home/aiyanxu/study/diff++/test/test1.rb", shell=True, stdout=PIPE).stdout.read()
#s2 =  Popen("ruby ast.rb /home/aiyanxu/study/diff++/test/test2.rb", shell=True, stdout=PIPE).stdout.read()
h1 = loads(s1)
print h1
#h2 = loads(s2)
#content1 = open('/home/aiyanxu/study/diff++/test/test1.rb').read()
#content2 = open('/home/aiyanxu/study/diff++/test/test2.rb').read()

node1 = Parser().convert(h1)
print node1
#node2 = Parser().convert(h2)
#diff.diff_node(node1, node2)
