from db import *
from passlib.hash import sha256_crypt


class User(Document):
    username = StringField(unique=True)
    password = StringField()
    email = StringField(unique=True)
    created = DateTimeField(default=datetime.utcnow())
    availableInterview = IntField(default=5)
    totalInterviews = IntField(default=0)
    reportPaths = ListField()
    userType = StringField(default="user")
    purchaseDate = ListField()
    purchaseAmount = ListField()


def updateAvailableInterview(username):
    User.objects(username=username).update(dec__availableInterview=1)
    User.objects(username=username).update(inc__totalInterviews=1)


def addInterviews(username, no):
    User.objects(username=username).update(inc__availableInterview=no)
    user = User.objects(username=username).get()
    print(user.username)
    user.purchaseDate.append(datetime.utcnow())
    amount = 100
    if no == 5:
        amount = 50
    user.purchaseAmount.append(amount)

    user.save()


def addReportPath(username, reportname):
    user = User.objects(username=username).get()
    print(user.username)
    user.reportPaths.append(reportname)
    user.save()


def getUserDetails(username):
    for user in User.objects(username=username):
        return user


def getUserReportPaths(username):
    for user in User.objects(username=username):
        return user.reportPaths


def getAvailableInterviews(username):
    for user in User.objects(username=username):
        return user.availableInterview


def getAllUsers():
    return User.objects()