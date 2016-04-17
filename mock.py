from rubyparser import Parser
from json import loads
from subprocess import PIPE,Popen
import diff

s1 =  Popen("ruby ast.rb test/test1.rb", shell=True, stdout=PIPE).stdout.read()
s2 =  Popen("ruby ast.rb test/test2.rb", shell=True, stdout=PIPE).stdout.read()
h1 = loads(s1)
h2 = loads(s2)
content1 = open('/home/aiyanxu/study/diff++/test/test1.rb').read()
content2 = open('/home/aiyanxu/study/diff++/test/test2.rb').read()

node1 = Parser().convert(h1)
node2 = Parser().convert(h2)
changes, cost = diff.diff_node(node1, node2)
print changes
diff.generate_html('tmp.html', diff.Texts(content1, content2,changes))
