list=[]
with open("output.txt","r") as f:
	a=f.read()
list=a.split("\n")
for l in list:
	print("<li>{}</li>".format(l))
