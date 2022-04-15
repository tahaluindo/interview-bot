import os
category=input("\nEnter Category")
current_directory=os.getcwd()
path="{}/aiml/{}".format(current_directory,category)
print(current_directory)

if not os.path.exists(path):
	os.makedirs(path)

pattern=input("\nEnter Pattern").upper()
srai=input("\nEnter SRAI").upper()
addmore=1
ans=True
with open("{}/{}.aiml".format(path,pattern), "a+") as f:
	while ans:
		if addmore==1:
			f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml>\n\n<category>\n<pattern>\n{}\n</pattern>\n<template>\n<random>\n<li></li>\n</random>\n</template>\n</category>\n\n".format(srai))
		
		f.write("<category>\n<pattern>\n{}\n</pattern>\n<template>\n<srai>\n{}\n</srai>\n</template>\n</category>\n\n".format(pattern,srai))
		f.write("<category>\n<pattern>\n_ {}\n</pattern>\n<template>\n<srai>\n{}\n</srai>\n</template>\n</category>\n\n".format(pattern,srai))
		f.write("<category>\n<pattern>\n{} *\n</pattern>\n<template>\n<srai>\n{}\n</srai>\n</template>\n</category>\n\n".format(pattern,srai))
		f.write("<category>\n<pattern>\n_ {} *\n</pattern>\n<template>\n<srai>\n{}\n</srai>\n</template>\n</category>\n\n".format(pattern,srai))
		a=input("ADD Alternative pattern")
		if a!="y":
			ans=False
			f.write("</aiml>")
		else:
			pattern=input("\nEnter Pattern").upper()
			addmore=addmore+1
			

