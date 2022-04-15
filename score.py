
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
stop_words = set(stopwords.words('english')) 
import random
def minMaxScaler(array):
	try:
		minimum=min(array)
		maximum=max(array)
		scaled=[]
		for elem in array:
			scaled.append((elem-minimum)/(maximum-minimum))
		return np.asarray(scaled)
	except:
		return np.asarray([0.,0.,0.,0.,0.,0.,0.,])
	
def emotionScore(emotion,scalingFactor):
	#print(evaluable)
	emo={"neutral":120,"sad":0,"fear":12,"disgust":0,"anger":10,"happy":70,"suprise":20}
	emotion_multiplier=np.asarray([1.4,-0.35,-0.35,-1.4,-1.4,1.4,-0.35])
	scaled=minMaxScaler(emotion.values())
	#print("scaled",scaled)
	#print("SCACLING FACTOR IS ",scalingFactor)
	score=sum(emotion_multiplier*scaled)*scalingFactor
	if score<0.1:
		score=score*10
	elif score>1:
		score=0.5
	elif score<-1:
		score=0.5
	print("Emotion",score)

	return score


def sentimentScore(sentiment,scalingFactor):
	#print(sentiment)
	sentiment_multilier=[3,1.9,0.9]
	s=np.asarray(list(sentiment.values()))*np.asarray(sentiment_multilier)
	score=(sum(s)/3)
	print("Sentiment",score)
	return score*scalingFactor

def keywordsMatch(answer,keywords):
	keywords=[w.upper() for w in keywords]
	word_tokens = word_tokenize(answer.upper()) 
	match=0
	print(keywords,type(keywords))
	for w in word_tokens:
		if w in keywords:
			match=match+1
		else:
			continue
			#print(keywords)
	
	score=match/int((len(keywords)*0.60))
	if(match>1):
		score=1
	return score*0.5
			
	
def calculateScore(emotion,sentiment,lexical,evaluable=False,keywords=None,answer=None):
	#print(emotion,type(emotion))
	
	#check if evaluable or not
	if evaluable:
		scalingFactor=0.15
	else:
		scalingFactor=0.40
		
	#Keywords score
	keyword_score=0
	if keywords is not None:
		if len(keywords)!=0:
			keyword_score=keywordsMatch(answer,keywords[0].split(','))
			
	e=emotionScore(emotion,scalingFactor=scalingFactor) #calculate emotion score
	s=sentimentScore(sentiment,scalingFactor=scalingFactor)					#calculate sentiment score
	l=lexical*0.2								#calculate lexical score
	
	#print("lexical",l)
	#score=(s+e)/2
	score=s+e+l+keyword_score
	score=score*100
	#print("actual score ",score)

	print("final",score)
	if abs(score) > 99:
		print("again",score)
		score=abs(score)
		score=99-random.randint(1,7)
	return abs(score)
