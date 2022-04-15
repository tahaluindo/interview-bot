var options = {
  controls: false,
  width: 450,
  height: 100,
  fluid: false,
  plugins: {
    wavesurfer: {
      src: "live",
      waveColor: "white",
      progressColor: "black",
      debug: false,
      cursorWidth: 1,
      msDisplayMax: 20,
      hideScrollbar: true
    },
    record: {
      audio: true,
      video: false,
      maxLength: 20,
      debug: true
    }
  }
};

var userTranscript = {
  username: "",
  interviewTime: "",
  transcript: []
};
var userSentiment = {
  positive: 0,
  negative: 0,
  neutral: 0,
  answerCount: 0
};
var script = "";
var rdata = "";
var sentimentFlag = false;
var freqFlag = false;
var schart = null;
var fchart = null;
var totalWords = 0;
var totalDuration = 0;
var containerElement = $("#container");
//audio
var player = videojs("myAudio", options, function() {});
var msg;
//Pre initialization of chatbot
function chatbotInstruction(instruct) {
  $(".media-list").append(
    '<li class="media"><div class="media-body"><div class="media"><div class="media-body chat-bot">' +
      instruct +
      "</div></div></div></li>"
  );
  $(".fixed-panel")
    .stop()
    .animate({ scrollTop: $(".fixed-panel")[0].scrollHeight }, 1000);
  msg.text = "";
  msg.text = instruct;
  userTranscript.transcript.push("IBot: " + instruct);
  speechSynthesis.speak(msg);
}
//Main functionalities
$(function() {
  $(".toast").toast("show");
  loadModelFunction();
  const sizeTypeSelect = sizeType;

  var asked_questions = [];
  var previousQuestion = "";
  var reportData = {
    interviewTime: "0",
    overallSentiment: ""
  };
  $("#startInterviewButton").click(function() {
    $("#myModal").modal("toggle");
  });

  //chartjs context
  var ctx = document.getElementById("myChart").getContext("2d");

  //speech synthesis
  var synth = window.speechSynthesis;
  window.SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.interimResults = true;
  recognition.lang = "en-gb";
  //recognition.continuous = true;  //continous dictation

  p = document.getElementById("words");
  text = "";
  recognition.addEventListener("result", e => {
    //console.log(e);
    const transcript = Array.from(e.results)
      .map(result => result[0])
      .map(result => result.transcript)
      .join("");

    const confidence = Array.from(e.results)
      .map(result => result[0])
      .map(result => result.confidence)
      .join("");
    script = transcript; //replace anything here

    $("#confidenceS").val(confidence * 100 + " %");
    $("#messageText").val(script);
    if (e.results[0].isFinal) {
      //console.log("event interpretation :  - "+e.interpretation);

      //$('#messageText').val(text);
      $("#messageText").val(script);

      $("#s_status").val("You / Bot Are Not Speaking");
    } else {
      $("#s_status").val("You / Bot Are Speaking");
    }
  }); //end event

  recognition.addEventListener("end", recognition.start);
  recognition.start();
  msg = new SpeechSynthesisUtterance();
  var voices = synth.getVoices();
  //Tuning
  msg.voice = voices[7];
  msg.rate = 1;
  msg.pitch = 0.9;

  //Interview finish
  $("#finishInterviewButton").click(function(e) {
    e.preventDefault();

    $("#finishModal").modal("toggle");
    $("#iTime").val($("#timerText").text());
  });

  //calls for pdf

  $("#finsihModalButton").click(function(e) {
    $("#timerText").hide();
    $("#timerText").prop("disabled", false);
    userTranscript.transcript.push("You : END INTERVIEW.");
    userTranscript.emotion = emotionDisplay;
    userTranscript.sentiment = userSentiment;
    userTranscript.interviewTime = $("#timerText").text();
    $("#data").val(JSON.stringify(userTranscript));
    $("#finishForm").submit();
  });

  //timer
  $("#timerText").click(function(e) {
    var start = new Date();
    setInterval(function() {
      $("#timerText").text(
        Math.round((new Date() - start) / 1000) + " Seconds"
      );
    }, 1000);
  });

  //hide timer
  $("#timerText").hide();

  //start Interview action
  $("#continueInterview").click(function(e) {
    loadModel("{{ url_for('static',filename='model.json') }}"); //https://js.tensorflow.org/api/0.15.3/#loadModel
    //const sizeTypeSelect =160
    //run()
    //initEmotion();
    //enabling buttons	S
    run();
    $("#chatbot-form-btn-clear-input").prop("disabled", false);
    $("#chatbot-form-btn").prop("disabled", false);
    $("#chatbot-form-btn-voice").prop("disabled", false);
    $("#chatbot-form-btn-clear").prop("disabled", false);
    $("#finishInterviewButton").prop("disabled", false);
    $("#startInterviewButton").prop("disabled", true);
    $("#messageText").prop("disabled", false);
    $("#timerText").click();
    $("#timerText").show();
    $("#timerText").prop("disabled", true);

    //full screen
    //openFullscreen()
    toggleFullscreen();

    const chatPanel = document.getElementById("chatPanel");
    setTimeout(
      chatbotInstruction(
        "Hello , I am a interview bot whose task is to ask you interview Questions.To start interview speak START INTERVIEW and submit your response."
      ),
      1500
    );
    setTimeout(
      chatbotInstruction(
        "You would be asked to tell your name , please speak in the following format.. My name is XYZ..if bot is not asking you any question please speak NEXT QUESTION..."
      ),
      2000
    );
  });

  // error handling
  player.on("deviceError", function() {
    console.log("device error:", player.deviceErrorCode);
  });
  player.on("error", function(element, error) {
    console.error(error);
  });
  // user clicked the record button and started recording
  player.on("startRecord", function() {
    console.log("started recording!");
  });
  // user completed recording and stream is available
  player.on("finishRecord", function() {
    // the blob object contains the recorded data that
    // can be downloaded by the user, stored on server etc.
    console.log("finished recording: ", player.recordedData);
  });

  $("#chatbot-form-btn").click(function(e) {
    e.preventDefault();
    $("#escore").val(JSON.stringify(emotionDisplay));
    $("#chatbot-form").submit();
  });
  //clear chat history
  $("#chatbot-form-btn-clear").click(function(e) {
    e.preventDefault();
    $("#chatPanel")
      .find(".media-list")
      .html("");
  });
  //clear input text
  $("#chatbot-form-btn-clear-input").click(function(e) {
    $("#messageText").val("");
  });

  $("#fullScreenMode").click(function(e) {
    toggleFullscreen();
  });
  //voice button interaction
  $("#chatbot-form-btn-voice").click(function(e) {
    e.preventDefault();
    //console.log("clicked");

    var onAnythingSaid = function(text) {
      console.log("Interim text: ", text);
    };

    var onFinalised = function(text) {
      console.log("Finalised text: ", text);
      $("#messageText").val(text);
    };
    var onFinishedListening = function() {
      // $('#chatbot-form-btn').click();
    };

    try {
      var listener = new SpeechToText(
        onAnythingSaid,
        onFinalised,
        onFinishedListening
      );
      listener.startListening();

      setTimeout(function() {
        listener.stopListening();
        if ($("#messageText").val()) {
          $("#chatbot-form-btn").click();
        }
      }, 5000);
    } catch (error) {
      console.log(error);
    }
  }); //end voice button
  questionlist = [];
  //on submit button
  $("#chatbot-form").submit(function(e) {
    //console.log(userTranscript);
    e.preventDefault();
    var message = $("#messageText")
      .val()
      .toUpperCase();
    var message_validation = message.split(" ");
    userTranscript.transcript.push("You: " + message);
    var wpm = getReadingTime(message);
    $("#ss").val(wpm);
    //begin if
    if (
      message_validation.length > 3 ||
      message.indexOf("MY NAME IS") != -1 ||
      message.indexOf("START INTERVIEW") != -1 ||
      message.indexOf("NEXT QUESTION") != -1 ||
      message.indexOf("ASK QUESTION") != -1
    ) {
      $(".media-list").append(
        '<li class="media"><div class="media-body"><div class="media"><div class="media-body user-chat">' +
          message +
          "</div></div></div></li>"
      );

      //ajax for chatbot
      $.ajax({
        type: "POST",
        url: "/ask",
        data: $(this).serialize(),
        success: function(response) {
          //$('#messageText').val('');

          var answer = response.answer.toUpperCase();
          previousQuestion = answer;

          //console.log(answer);
          if (questionlist.includes(answer)) {
            //console.log(questionlist)
            //console.log("Already asked");
            $("#messageText").val("ASK QUESTION");
            e.preventDefault();
            $("#chatbot-form").submit();
          } //re ask
          else {
            //console.log("new 1");
            questionlist.push(answer);
            const chatPanel = document.getElementById("chatPanel");
            $(".media-list").append(
              '<li class="media"><div class="media-body"><div class="media"><div class="media-body chat-bot">' +
                answer +
                "</div></div></div></li>"
            );
            $(".fixed-panel")
              .stop()
              .animate({ scrollTop: $(".fixed-panel")[0].scrollHeight }, 1000);
            userTranscript.transcript.push("IBot: " + answer);
            msg.text = "";
            msg.text = answer;
            speechSynthesis.speak(msg);
          }
        },
        error: function(error) {
          console.log(error);
        }
      }); //end ajax
    } else {
      //end if start else

      $(".media-list").append(
        '<li class="media"><div class="media-body"><div class="media"><div class="media-body chat-bot">' +
          "Please give detailed answer " +
          "</div></div></div></li>"
      );
      $(".media-list").append(
        '<li class="media"><div class="media-body"><div class="media"><div class="media-body chat-bot">' +
          previousQuestion +
          "</div></div></div></li>"
      );
      var answer =
        "Please provide a detailed answer to the question. This is very important";
      $(".fixed-panel")
        .stop()
        .animate({ scrollTop: $(".fixed-panel")[0].scrollHeight }, 1000);
      msg.text = "";
      var answer_check = previousQuestion.split(".");
      msg.text = answer + ". \n" + answer_check.pop();
      userTranscript.transcript.push("IBot: " + answer);
      speechSynthesis.speak(msg);
    }

    if (message.indexOf("ASK QUESTION") == -1) {
      //Sentiment request
      $.ajax({
        type: "POST",
        url: "/sentiment",
        data: $(this).serialize(),
        success: function(response) {
          console.log("Response is " + response["score"]);
          //$( ".p1" ).append("<p><b>Score for your answer is : &nbsp;&nbsp;</b>"+response['score']*2+"</p>");
          //$(".p1").stop().animate({ scrollTop: $(".p1")[0].scrollHeight}, 1000);
          var positive = response.sentiment_positive;
          var negative = response.sentiment_negative;
          var neutral = response.sentiment_neutral;
          userSentiment.positive = userSentiment.positive + positive;
          userSentiment.negative = userSentiment.negative + negative;
          userSentiment.neutral = userSentiment.neutral + neutral;
          userSentiment.answerCount = userSentiment.answerCount + 1;
          console.log(userSentiment);
          //userTranscript.sentiment.push(response.overall_sentiment);
          //console.log(positive,negative,neutral);
          if (sentimentFlag) {
            schart.destroy();
          }
          sentimentFlag = true;
          schart = new Chart($("#myChart"), {
            type: "horizontalBar",
            data: {
              labels: ["Positive", "Negative", "Neutral"],
              datasets: [
                {
                  label: "Sentiment in terms of %",
                  backgroundColor: ["#03c637", "#f4424b", "#8e5ea2"],
                  data: [positive, -1 * negative, neutral]
                }
              ]
            },
            options: {
              animation: { duration: 0 },
              legend: { display: false },
              title: {
                display: true,
                text:
                  "Sentiment Analysis : Overall Sentiment " +
                  response.overall_sentiment
              }
            }
          }); //end chart
        }, //end success
        error: function(error) {
          console.log("Not working" + error);
        } //end error
      }); //end sentiment ajax

      //text request
      $.ajax({
        type: "POST",
        url: "/textAnalysis",
        data: $(this).serialize(),
        success: function(response) {
          //console.log(response)
          $("#word").val(response["numTokens"]);
          $("#nos").val(response["uniqueTokens"]);
          $("#ld").val(response["Lexical"]);
          $("#frequentword").val(response["topwords"]);

          var flabels = [];
          var fval = [];
          for (var i = 0; i < response["topwords"].length; i++) {
            flabels.push(response["topwords"][i][0]);
            fval.push(response["topwords"][i][1]);
          }

          if (freqFlag) {
            fchart.destroy();
          }
          freqFlag = true;
          fchart = new Chart($("#freqChart"), {
            type: "polarArea",
            data: {
              labels: flabels,
              datasets: [
                {
                  label: "Most Frequent Word",
                  backgroundColor: [
                    "#03c637",
                    "#f4424b",
                    "#8e5ea2",
                    "#ff5722",
                    "#827717",
                    "#6200ea",
                    "#c51162",
                    "#3f51b5",
                    "#004d40",
                    "#9e9e9e"
                  ],
                  data: fval
                }
              ]
            },
            options: {
              animation: { duration: 0 },
              legend: { display: false },
              title: {
                display: true
              }
            }
          }); //end chart
        }, //end success
        error: function(error) {
          console.log("Not working" + error);
        } //end error
      }); //end sentiment ajax
    }
  });
}); //end onload

function toggleFullscreen(elem) {
  elem = elem || document.documentElement;
  if (
    !document.fullscreenElement &&
    !document.mozFullScreenElement &&
    !document.webkitFullscreenElement &&
    !document.msFullscreenElement
  ) {
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.msRequestFullscreen) {
      elem.msRequestFullscreen();
    } else if (elem.mozRequestFullScreen) {
      elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) {
      elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
    }
    $("#fullScreenMode").text("Exit Full Screen");
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
    $("#fullScreenMode").text("Enter Full Screen");
  }
}
