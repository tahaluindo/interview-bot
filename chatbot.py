import aiml
import os
from db import *
from nlp import TextAnalyser
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from score import calculateScore
from QuestionDetail import QuestionDetail
class Chatbot():
	def __init__(self):
			self.kernel = aiml.Kernel()
			if os.path.isfile("bot_brain.brn"):
				self.kernel.bootstrap(brainFile= "bot_brain.brn")
			else:
				self.kernel.bootstrap(learnFiles = os.path.abspath("aiml/std-startup.xml"), commands = "load aiml b")
				self.kernel.saveBrain("bot_brain.brn")
			self.sid=SentimentIntensityAnalyzer()
				
	
	def interact(self,username=None,interviewId=None,answer=None,mode=0,emotion={},previousQuestion=""):
		'''
		mode determines where to run the chatbot on the console or the as web api
		mode=0 web
		mode=1 console
		'''
		#beginInterview(username,interviewId)
		#question=""
		#print(emotion)
		if mode==0:
			#answer=input("user :")
			notasked=True
			times=0
			question=""
			while notasked:
				if times<5:
					question = self.kernel.respond(answer)

					notasked=checkIfQuestionAlreadyAsked(interviewId,question)
					times=times+1
				else:
					break
			if times==5:
				question=self.kernel.respond("ASK QUESTION")
				print(question)

			sentiment=self.sentiment(answer)
			textAnalysis=self.textAnalysis(answer)
			#print("Bot: ",question)
			#saveInterview(interviewId,previousQuestion,answer,0.5)
			#previousQuestion=question
			
			q=getQuestionDetails(previousQuestion)
			if q is not None:
				evaluable=q.evaluable
				keywords=list(q.keywords)
				#print(keywords)
				#print(q.question)
				#print("Chatbot ",q.keywords,type(keywords))
			else:
				evaluable=False
				keywords=None
				
			score=calculateScore(emotion=emotion,
			sentiment=sentiment,
			lexical=textAnalysis["Lexical"],
			evaluable=evaluable,
			keywords=keywords,
			answer=answer
			)
			#print(score)
			#print("Bot: ",question)
			
			saveInterview(interviewId,previousQuestion,answer,score=score,emotion=emotion,sentiment=sentiment,
			textAnalysis=textAnalysis)
			
			response={}
			response["question"]=question
			response["sentiment"]=sentiment
			response["textAnalytics"]=textAnalysis
			response["score"]=score
			response["previousQuestion"]=previousQuestion
			response["answer"]=answer
			#print(response)
			return response

		else:
			while True:
				print("=="*10)
				answer=input("user :")
				question = self.kernel.respond(answer)

				sentiment=self.sentiment(answer)
				emotion={"neutral":random.randint(1,1000),
				"sad":random.randint(1,100),
				"fear":random.randint(1,100),
				"disgust":random.randint(1,100),
				"anger":random.randint(1,100),
				"happy":random.randint(1,500),
				"suprise":random.randint(1,100)}
				textAnalysis=self.textAnalysis(answer)
				
				q=getQuestionDetails(previousQuestion)
				if q is not None:
					evaluable=q.evaluable
					keywords=list(q.keywords)
					#print("Chatbot ",q.keywords,type(keywords))
				else:
					evaluable=False
					keywords=None
					
				score=calculateScore(emotion=emotion,
				sentiment=sentiment,
				lexical=textAnalysis["Lexical"],
				evaluable=evaluable,
				keywords=keywords,
				answer=answer
				)
				#print(score)
				print("Bot: ",question)
				
				saveInterview(interviewId,
				previousQuestion,
				answer,
				score=score,
				emotion=emotion,
				sentiment=sentiment,
				textAnalysis=textAnalysis)

				previousQuestion=question			
	
	def sentiment(self,answer):
		sentiment=''
		scores = self.sid.polarity_scores(answer)
		if scores['compound'] > 0:
			sentiment='Positive'
		elif scores['compound']< 0:
			sentiment='Negative'
		else:
			sentiment='Neutral'
		sentiments={'sentiment_positive':scores['pos'],'sentiment_negative':scores['neg'],
'sentiment_neutral':scores['neu']}
		return sentiments
	
	def textAnalysis(self,userText):
		stemmingType = TextAnalyser.STEM
		language = "EN"
		myText = TextAnalyser(userText, language)
		myText.preprocessText(lowercase = userText,removeStopWords = userText,stemming = stemmingType)
		if myText.uniqueTokens() == 0:
		   		uniqueTokensText = 1
		else:
			uniqueTokensText = myText.uniqueTokens()
		numChars=myText.length()
		numSentences=myText.getSentences()
		numTokens=myText.getTokens()
		top=myText.getMostCommonWords(10)
		try:
			lexical=uniqueTokensText/myText.getTokens()
		except:
			lexical=0
		return {'numTokens': myText.getTokens(),'uniqueTokens':uniqueTokensText,'topwords':top,'Lexical':lexical}

			

		


#chatbot=Chatbot()

'''
chatbot.interact(username="jitendra",
				interviewId=generateInterviewId(),
				mode=0,
				emotion={"neutral":random.randint(1,1000),
				"sad":random.randint(1,100),
				"fear":random.randint(1,100),
				"disgust":random.randint(1,100),
				"anger":random.randint(1,100),
				"happy":random.randint(1,500),
				"suprise":random.randint(1,100)
				},
				previousQuestion="Mention some commonly used Docker command?"
)
'''

#answer=microservicesis cloud is docker is ps is pull 
