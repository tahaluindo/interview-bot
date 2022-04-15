from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from keywords import getKeywords


def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


raw_html = simple_get(
    'https://www.edureka.co/blog/interview-questions/top-50-hadoop-interview-questions-2016/'
)
soup = BeautifulSoup(raw_html, 'html.parser')
question = []
answer = []
for element in soup.findAll(
        True,
    {'class': ['blog-content', 'mt-md-4', 'mt-lg-4', 'mt-xl-4', 'color-4a']}):
    for h3 in element.select('h3'):
        question.append(h3.getText())
    i = 0
    for p in element.find_all('p', attrs={'style': "text-align: justify;"}):
        if i < 6:
            i = i + 1
            continue
        print(p.getText())
        answer.append(p.getText())

with open('i.txt', 'w') as f:
    for i in range(len(question)):
        f.write(question[i])
        f.write("\n")
        f.write(getKeywords(answer[i]))
        f.write("\n")
