import urllib.request  as urllib2 
from bs4 import BeautifulSoup

ip=input("Enter url\n")#"http://iteslj.org/questions/photography.html"#input("Enter URL\n")

url = urllib2.urlopen(ip)

content = url.read()

soup = BeautifulSoup(content)
seprator=". "#input("Enter Separator for nos\n")
find="td"#input("Element\n")

mydivs = soup.findAll(find)#soup.findAll("span", {"style": "font-size: x-large;"})
#with open('category.txt', 'w+') as f:

#print(mydivs)
i=1
for d in mydivs:
	if i%2==0:
		d=d.get_text()
		try:

			print("<li>{}</li>".format(d))
		except:
			continue
	i=i+1	
	'''
	try:
		d=d.split("<{}>".format(find))[1]
		d=d.split("</{}>".format(find))[0]
		d=d.replace("<ul>","")
		d=d.replace("</ul>","")
		d=d.replace("<span>","")
		d=d.replace("</span>","")
		#d=d.split("{}".format(seprator))[1]
		#f.write(d+"\n")
		if "png" not in d:
			print("<li>{}</li>".format(d))
	except:
		print("",end="")
	'''

