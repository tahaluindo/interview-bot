import csv
import os
current_directory=os.getcwd()
category="Technical"
path="{}/aiml/{}".format(current_directory,category)
with open('ques.csv') as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=',')
	for row in csv_reader:
		if len(row)>0:
			pattern=row[0].split(" ")[0].upper()
			srai="{}1".format(pattern)
			with open("{}/{}.aiml".format(path,pattern), "a+") as f:
				f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<aiml>\n\n<category>\n<pattern>\n{}\n</pattern>\n<template>\n<random>\n<li></li>\n</random>\n</template>\n</category>\n\n".format(srai))
		
				f.write("<category>\n<pattern>\n{}\n</pattern>\n<template>\n<srai>\n{}\n</srai>\n</template>\n</category>\n\n".format(pattern,srai))
				f.write("<category>\n<pattern>\n_ {}\n</pattern>\n<template>\n<srai>\n{}\n</srai>\n</template>\n</category>\n\n".format(pattern,srai))
				f.write("<category>\n<pattern>\n{} *\n</pattern>\n<template>\n<srai>\n{}\n</srai>\n</template>\n</category>\n\n".format(pattern,srai))
				f.write("<category>\n<pattern>\n_ {} *\n</pattern>\n<template>\n<srai>\n{}\n</srai>\n</template>\n</category>\n\n".format(pattern,srai))
				f.write("</aiml>")
