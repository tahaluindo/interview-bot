from mongoengine import *
from datetime import datetime
import random
import string
import csv

from QuestionDetail import QuestionDetail
#connect('interviewbot', host='localhost', port=27017) #localhost
connect(
    db='interviewbot',
    username='Jitendra',
    password='InterviewBot',
    host=
    'mongodb+srv://Jitendra:InterviewBot@cluster0-kyhd2.mongodb.net/test?retryWrites=true'
)


class InterviewEvaluation(EmbeddedDocument):
    #squestionCount=IntField()
    question = StringField()
    answer = StringField()
    time = FloatField()
    score = FloatField()
    sentiment = DictField()
    emotion = DictField()
    textAnalysis = DictField()


class Interview(Document):
    created = DateTimeField(default=datetime.utcnow())
    username = StringField(required=True)
    interviewId = StringField(required=True, unique=True)
    user_response = ListField(EmbeddedDocumentField(InterviewEvaluation))
    ended = DateTimeField(default=datetime.utcnow())
    reportGenerated = BooleanField(default=False)


class Questionset(Document):
    questionId = StringField()
    questionType = StringField()
    question = StringField()
    category = StringField()
    subcategory = StringField()
    keywords = ListField()
    evaluable = BooleanField()


def getQuestionDetails(question):
    for q in Questionset.objects(question=question):
        ques = QuestionDetail(q.questionId, q.questionType, q.question,
                              q.category, q.subcategory, q.keywords,
                              q.evaluable)
        return ques


def questionSet(qid, qtype, question, category, subcategory, keywords,
                evaluable):
    '''
	ADDS QUESTION TO MONGODB
	'''
    if evaluable:
        question = Questionset(questionId=qid,
                               questionType=qtype,
                               question=question,
                               category=category,
                               subcategory=subcategory,
                               keywords=keywords,
                               evaluable=evaluable)
    else:
        question = Questionset(questionId=qid,
                               questionType=qtype,
                               question=question,
                               category=category,
                               subcategory=subcategory,
                               evaluable=evaluable)
    question.save()
    print("question saved")


def addQuestions():
    '''
	READS CSV AND SAVE TO DB
	
	'''
    filename = input("enter filename\n")
    typ = input("questiontype\n")
    evaluable = False
    if typ == "t":
        evaluable = True
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
            if line_count == 0 or line_count == 1:
                #print(row[0],row[1],row[2],row[3])
                line_count += 1
            else:
                row = row[0].split(',')
                print(row)
                questionSet(qid=typ + str(line_count - 1),
                            qtype=row[1],
                            question=row[0],
                            category=row[2],
                            subcategory=row[3],
                            keywords=row[4:],
                            evaluable=evaluable)
                line_count += 1
        print(f'Processed {line_count} lines.')


def beginInterview(username, interviewId):
    #user=Interview(username=username,interviewId=interviewId)
    #user.user_response=[InterviewEvaluation(question="",answer="start interview")]
    #user.save()
    user = Interview.objects(interviewId=interviewId).modify(
        upsert=True,
        new=True,
        set__username=username,
        set__created=datetime.utcnow(),
        set__ended=datetime.utcnow())


def endInterview(interviewId):
    user = Interview.objects(interviewId=interviewId).modify(
        upsert=True,
        new=True,
        set__ended=datetime.utcnow(),
        set__reportGenerated=True)


def saveInterview(interviewId,
                  question,
                  answer,
                  score,
                  sentiment=None,
                  emotion=None,
                  textAnalysis=None):
    time = datetime.timestamp(datetime.now())
    Interview.objects(interviewId=interviewId).update_one(
        push__user_response=InterviewEvaluation(question=question,
                                                answer=answer,
                                                time=int(time),
                                                score=score,
                                                emotion=emotion,
                                                sentiment=sentiment,
                                                textAnalysis=textAnalysis))


def generateInterviewId():
    while True:
        interviewId = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=15))
        check = Interview.objects(interviewId=interviewId)
        if (len(check) == 0):
            return interviewId


def getAllInterviewsOfUser(username):
    return Interview.objects(username=username)


def getInterview(interviewId):
    for interview in Interview.objects(interviewId=interviewId):
        return interview


def checkIfQuestionAlreadyAsked(interviewId, question):
    #i = Interview.objects.filter(interviewId=interviewId).fields(username=1, user_response={'$elemMatch': {'question': "Tell me about an instance where you have failed and what you learned from it."}})

    #for i in Interview.objects.filter(user_response__match={'answer': "ASK QUESTION"}):
    for i in Interview.objects(interviewId=interviewId):
        for j in i.user_response:
            if j.question == question:
                return True

    return False


def getUserResponse(interviewId):
    for user in Interview.objects(interviewId=interviewId):
        total_answers = len(user.user_response)
        score = 0
        sentiment = {
            "sentiment_positive": 0,
            "sentiment_negative": 0,
            "sentiment_neutral": 0
        }
        for response in user.user_response:
            score = score + int(response.score)
            for k, v in dict(response.sentiment).items():
                sentiment[k] = sentiment[k] + v
            emotion = dict(response.emotion)
        if score > 100:
            score = score - random.randint(1, 10)
        smsg = ""
        emsg = ""
        pEmotion = max(emotion, key=emotion.get)
        pSentiment = max(sentiment, key=sentiment.get).split("_")[-1]
        if pSentiment == "neutral":
            smsg = "Keeping Neutral Sentiment is not a bad idea and it's way better than having a negative impression on the interviewer. A little more positive answers would definetly work for you, and you should try the same."
        elif pSentiment == "positive":
            smsg = "Having Positive Sentiment can be proved as a great advantage to you as it gives the message that your thought process is good, and you know how to tackle the tricky questions with grace. Keep it up"
        else:
            smsg = "Negative Sentimental answer to the questions create a negative impact in front of your interviewer and you should restrain yourself from giving negative Answer. Remember each negative answer can be given in a positive way. If you are givining negative answers then try to potrait it in a positive way"

        if pEmotion in ["neutral", "happy"]:
            emsg = "Your emotion analysis is telling us either you were having neutral or happy emotion during the interview process. This is good as it creates a good impression in front of interviewer. An interviewer is looking for a person who will work with them and evryone like friendly people. Keep Smiling it will work in your favour."
        elif pEmotion in ["fear", "sad"]:
            emsg = "Your emotion analysis is telling us either you were having fear or sad during the interview process. You need to be confident and anser confidently during the interviews. Fear or sadness signifies that you are nervous. Keep practising and remember Confidence is the key."
        elif pEmotion in ["angry", "disgust"]:
            emsg = "Your emotion analysis is telling us that either you were angry or having a disgust emotion expression during the interview. This gives a very negative impression to the interviewer. You need to  work hard , and try not to get offended. This may turn out a biggest mistake for you"
        else:
            emsg = "Your emotion analysis is telling us that you were suprised during the interview. This shows that you were not prepared for the interview. You need to preapre before hand for the interview as you need to show best of your skills and capability. All the best"
        response = {
            "interviewId": interviewId,
            "totalEmotion": emotion,
            "prominentEmotion": pEmotion,
            "totalSentiment": sentiment,
            "prominentSentiment": pSentiment,
            "smsg": smsg,
            "emsg": emsg,
            "totalScore": score / total_answers,
            "user_response": user.user_response
        }

        return response


def getAllInterviews():
    return Interview.objects()
