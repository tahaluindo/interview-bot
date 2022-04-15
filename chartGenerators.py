import os
import time
import matplotlib.pyplot as plt
import numpy as np

def generateChartsForPDF(emotions,sentiments,username):
    a=generateChartForEmotions(emotions,username)
    #generateChartForSentiment(sentiments)
    return a,generateChartForSentiment(sentiments,username)

def generateChartForEmotions(emotions,username):
    ts = time.time()
    echartname="{}_{}_emotion.png".format(username,ts)
    emotion_values=list(emotions.values())
    emotion_names=list(emotions.keys())
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedges, texts = ax.pie(emotion_values, wedgeprops=dict(width=0.5), startangle=-80)
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(xycoords='data', textcoords='data', arrowprops=dict(arrowstyle="-"),bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2.6 + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(emotion_names[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                    horizontalalignment=horizontalalignment, **kw)

    ax.set_title("Emotion Analysis")

    plt.savefig('{}/Plots/{}'.format(os.getcwd(),echartname))
    return '{}/Plots/{}'.format(os.getcwd(),echartname)

def generateChartForSentiment(sentiments,username):
    plt.clf()
    ts = time.time()
    schartname="{}_{}_sentiment.png".format(username,ts)
    sentiment_labels=list(sentiments.keys())[0:3]
    sentiment_values=list(sentiments.values())[0:3]
    sentiment_values[1]=-1*sentiment_values[1]
    n = np.arange(len(sentiment_labels))
    plt.barh(n, sentiment_values,color=["green","red","plum"])
    plt.yticks(n, sentiment_labels)
    plt.savefig('{}/Plots/{}'.format(os.getcwd(),schartname))
    return '{}/Plots/{}'.format(os.getcwd(),schartname)

def getTimeStamp():
    return time.time()