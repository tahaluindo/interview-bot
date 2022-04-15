from flask import Flask, render_template, request, jsonify, make_response, session, logging, url_for, redirect, flash, abort
import aiml
import os
from nlp import TextAnalyser
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pdfkit
import json
from passlib.hash import sha256_crypt
from chartGenerators import generateChartsForPDF, getTimeStamp
from score import calculateScore
from db import *
from chatbot import Chatbot
from Auth import *
import threading
from flask import send_from_directory
import glob
import razorpay

kernel = aiml.Kernel()
sid = SentimentIntensityAnalyzer()

razorpay_client = razorpay.Client(auth=("rzp_test_SwjYDE0pT0UJv8", "hmB1IoIy0TVVlnYubGMpbcbI"))
def load_kern(forcereload):
	if os.path.isfile("bot_brain.brn") and not forcereload:
		kernel.bootstrap(brainFile="bot_brain.brn")
	else:
		kernel.bootstrap(learnFiles=os.path.abspath("aiml/std-startup.xml"),
						commands="load aiml b")
		kernel.saveBrain("bot_brain.brn")


load_kern(False)
#db=scoped_session(sessionmaker(bind=engine))
application = Flask(__name__)
application.secret_key = "interviewbot"
application.config['SECRET_KEY'] = 'interviewbot'

totalQuestionToBeAsked = 10


###     ADMIN PANEL
@application.route("/admin")
def admin():
	if "log" in session:
		if "admin" in session:
			return render_template("admin/layout.html",
								users=getAllUsers(),
								interviews=getAllInterviews())
	abort(404)


@application.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(application.root_path, 'static'),
							'favicon.ico',
							mimetype='image/vnd.microsoft.icon')


@application.route("/questionSet")
def questionSet():
	if "log" in session:
		if "admin" in session:
			files = []
			for root, dirnames, filenames in os.walk("aiml"):
				files.extend(glob.glob(root + "/*.aiml"))
			return render_template("admin/bot.html", aiml=files)
	abort(404)


@application.route("/editFile/<file>")
def editFile(file):
	if "log" in session:
		if "admin" in session:
			file = file.replace('__', '/')
			with open(os.path.join(file), 'r') as f:
				return str(f.readlines())
	return "Hello World"


@application.route("/search/<name>")
def search(name):
	interview = getInterview(name)
	user = getUserDetails(name)
	response = {}
	response["interview"] = interview
	response["user"] = user
	return jsonify({"user": "Jitendra"})

################## PAYMENT GATEWAY


@application.route('/charge', methods=['POST'])
def app_charge():
	amount = request.form['amount']
	payment_id = request.form['razorpay_payment_id']
	razorpay_client.payment.capture(payment_id, amount)
	razorpay_client.payment.fetch(payment_id)
	no_of_interview = request.form.get("no")
	addInterviews(session["username"], int(no_of_interview))
	flash("Interviews added", "success")
	return redirect(url_for("subscription"))


###    NORMAL USER


@application.route("/")
def index():
	return render_template("index.html")


@application.route("/home")
def home():
	if 'log' in session:
		for user in User.objects.filter(username=session["username"]):
			return render_template("home.html", user=user)
	abort(404)


@application.route("/register", methods=["GET", "POST"])
def register():
	if 'log' in session:
		flash(
			"Your already logged in your account, logout if you want to create new account",
			"danger")
		return redirect(url_for("home"))
	else:
		if request.method == "POST":
			email = request.form.get("email")
			username = request.form.get("username")
			password = request.form.get("password")
			confirm = request.form.get("confirm")
			secure_password = sha256_crypt.encrypt(str(password))

			if password == confirm:

				user = User(username=username,
							password=secure_password,
							email=email)
				try:
					user.save()
				except:
					flash("Username or Email Id already exists ", "danger")
					return redirect(url_for('register'))
				flash("Registeration successfull , Please Login ", "success")
				return redirect(url_for('login'))
			else:
				flash("Password does not match", "danger")
				return render_template('register.html')
		return render_template("register.html")


@application.route("/login", methods=["GET", "POST"])
def login():
	if 'log' in session:
		flash("Already Logged in , To login with another account logout first",
			"danger")
		return render_template('home.html')
	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")
		for user in User.objects.filter(username=username).fields(username=1,
																password=1,userType=1):

			if sha256_crypt.verify(password, user.password):
				session["log"] = True
				session["username"] = user.username
				flash("Welcome back {} ".format(user.username), "success")
			
				if user.userType == "admin":
					session["admin"] = True
					return redirect(url_for("admin"))
				return redirect(url_for("home"))
			else:
				flash("Wrong password", "danger")
				return render_template("login.html")
		flash("No user found please check your username", "danger")
		return render_template("login.html")
	else:
		return render_template("login.html")


@application.route("/logout")
def logout():
	if 'log' in session:
		session["log"] = False
		session.clear()
		flash("Logged out ,Thank you for using our service", "success")
		return redirect(url_for("index"))
	else:
		flash("For logging out you need to login first", "danger")
		return redirect(url_for("index"))


@application.route("/ppt")
def ppt():
	return render_template("ppt.html")


@application.route("/subscription", methods=["POST", "GET"])
def subscription():
	availableInterview = getAvailableInterviews(session["username"])
	if request.method == "POST":
		no_of_interview = request.form.get("no")
		addInterviews(session["username"], int(no_of_interview))
		flash("Interviews added", "success")
		return redirect(url_for("subscription"))
	return render_template("subscription.html", available=availableInterview)


#route for main page


@application.route("/chatbot")
def chatbot():

	if 'log' in session:
		if getUserDetails(session["username"]).availableInterview < 1:
			flash(
				"Your interview Limit has been reached, get more from subscription page",
				"danger")
			return redirect(url_for("home"))
		session["InterviewId"] = generateInterviewId()
		session["previousQuestion"] = ""
		session["questionNo"] = 0
		return render_template(
			'beginInterview.html',
			username=session["username"],
			interviewid=session["InterviewId"])  #chatbot.html
	return render_template('notallowed.html')


@application.route("/interview", methods=["POST"])
def interview():
	if 'log' in session:
		if getUserDetails(session["username"]).availableInterview < 1:
			flash(
				"Your interview Limit has been reached, get more from subscription page",
				"danger")
			return redirect(url_for("home"))
		beginInterview(session["username"], session["InterviewId"])
		updateAvailableInterview(session["username"])
		return render_template('interview.html',
							interviewId=session["InterviewId"])
	return render_template('notallowed.html')


@application.route("/interact", methods=["POST"])
def interact():

	answer = str(request.form['messageText'])
	emotion = json.loads(request.form['escore'])
	#print(session["questionNo"])
	chatbot = Chatbot()
	response = chatbot.interact(username=session["username"],
								interviewId=session["InterviewId"],
								answer=answer,
								mode=0,
								emotion=emotion,
								previousQuestion=session["previousQuestion"])
	if session["questionNo"] == 0:
		response["question"] = "Introduce Yourself"

	if session["questionNo"] > totalQuestionToBeAsked:
		response[
			"question"] = "Thank you for giving the interview, you can click on finish interview for generating pdf"
	session["previousQuestion"] = response["question"]
	session["questionNo"] = session["questionNo"] + 1
	response["questionNo"] = session["questionNo"]
	return jsonify(response)


def savePdftoFile(name, data):
	directory = "Report/{}".format(session["username"])
	if not os.path.exists(directory):
		os.makedirs(directory)
	f = open('{}/{}.pdf'.format(directory, name), 'w+b')
	binary_format = bytearray(data)
	f.write(binary_format)
	f.close()
	addReportPath(session["username"], '{}/{}.pdf'.format(directory, name))


@application.route('/generate', methods=['POST', 'GET'])
def pdf_template():
	if 'log' in session:
		if request.method == 'POST':
			try:
				print("ok 1")

				#icon = "{}/static/images/icon.png".format(os.getcwd())
				response = getUserResponse(session["InterviewId"])
				#echart, schart = generateChartsForPDF(response["totalEmotion"], response["totalSentiment"],session["username"])
				#rendered=render_template("report.html",icon=icon,user=response,echart=echart,schart=schart)
				#pdf=pdfkit.from_string(rendered,False)#true for client sending
				print("ok")
				#savePdftoFile("{}".format(session["InterviewId"]),pdf)
				#endInterview(session["InterviewId"])
				print(response)
				return render_template("report.html",user=response)
				#return render_template("interviewComplete.html")
			except:
				abort(500)

	abort(404)


@application.route('/report', methods=['POST', 'GET'])
def getReport():
	if 'log' in session:
		if request.method == 'POST':
			try:
				response = getUserResponse(session["InterviewId"])
				addReportPath(session["username"], session["InterviewId"])

				return render_template("report.html",user=response)
			except:
				abort(404)
	abort(404)

@application.route('/report/<interviewId>', methods=['POST', 'GET'])
def getReportById(interviewId):
	if 'log' in session:
		if request.method == 'GET':
			try:
				if interviewId in getUserReportPaths(session["username"]):
					response = getUserResponse(interviewId)
					return render_template("report.html",user=response)
			except:
				abort(404)
	abort(404)

@application.route("/viewInterview")
def viewInterviews():
	if "log" in session:
		userdata = getAllInterviewsOfUser(session["username"])
		for user in User.objects.filter(username=session["username"]):
			return render_template("viewAllInterview.html",
								user=userdata,
								info=user)
	abort(404)


@application.route("/viewReport")
def viewReport():
	if "log" in session:
		for user in User.objects.filter(username=session["username"]):
			return render_template("viewReports.html", user=user)
	abort(404)


@application.route('/uploaded_file/<filename>', methods=["GET", "POST"])
def uploaded_file(filename):
	afile = session["username"] + "/" + filename
	return send_from_directory(os.path.join("Report", session["username"]),
							filename)


@application.route("/profile", methods=["GET", "POST"])
def profile():
	if "log" in session:
		for user in User.objects.filter(username=session["username"]):
			return render_template("profile.html", user=user)
	abort(404)


#error handlers
@application.errorhandler(404)
def error404(error):
	return render_template("notallowed.html"), 404


@application.errorhandler(405)
def error405(error):
	return render_template("noaccess.html"), 405


if __name__ == "__main__":

	application.run(port=5002,threaded=True,debug=True)
