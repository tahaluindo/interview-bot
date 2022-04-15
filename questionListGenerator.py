import os
from bs4 import BeautifulSoup as Soup
import csv
questions=[]
os.chdir("aiml")
root=list(os.listdir())
path=os.getcwd()
newpath=path
dtype={"TECHNICAL":0,"NON_TECHNICAL":0}
qtype=[]
def readFiles(directory,path):
	#print(directory)
	for d in directory:
		if len(d.split("."))==1:
			os.chdir(d)
			readFiles(list(os.listdir()),os.getcwd())
			os.chdir(path)
		else:
			typ=os.getcwd().split("/")[-1]
			ttype=""
			if "Technical" in os.getcwd():
				ttype="TECHNICAL"
			else:
				ttype="NON_TECHNICAL"
			text=""
			with open(d,'r',encoding = 'utf-8') as f:
				text+=f.read()
			soup = Soup(text)
			for e in soup.findAll('li'):
				element=str(e)
				element=element.split("<li>")[1]
				element=element.split("</li>")[0]
				if element=="":
					continue
				else:
					info=(d.split(".")[0],typ)
					questions.append((element,info,ttype))
					dtype[ttype]=dtype[ttype]+1



print(path)
readFiles(root,newpath)
print(len(questions))
alreadyPresent=list()

with open('{}/technical.csv'.format(os.getcwd()),'w') as f:
	f.write("{},{},{},{}\n".format("Question","Question Type","Sub Category","Category"))
	for q in questions:
		info=q[1]
		typ=q[2]
		if typ=="TECHNICAL":
			if q[0] not in alreadyPresent:

				f.write("{},{},{},{}\n".format(q[0],typ,info[0],info[1]))
				#print("{},{},{},{}\n".format(q[0],typ,info[0],info[1]))
				alreadyPresent.append(q[0])

with open('{}/non_technical.csv'.format(os.getcwd()),'w') as f:
	f.write("{},{},{},{}\n".format("Question","Question Type","Sub Category","Category"))
	for q in questions:
		info=q[1]
		typ=q[2]
		if typ!="TECHNICAL":
			if q[0] not in alreadyPresent:

				f.write("{},{},{},{}\n".format(q[0],typ,info[0],info[1]))
				#print("{},{},{},{}\n".format(q[0],typ,info[0],info[1]))
				alreadyPresent.append(q[0])

for k,v in dtype.items():
	print("{} - {}".format(k,v))
