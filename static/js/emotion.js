/*
Realtime emotion detection and analysis using tendorflow and chartjs
*/

let scoreThreshold = 0.5
let sizeType = '160'
let modelLoaded = false
var cImg;

var constraints = {
	audio: false,
	video: {
		width: 460,
		height: 370
	}
};

var charts = [];

var emotionDisplay = {
	"neutral":0,
	"angry":0,
	"disgust":0,
	"fear":0,
	"happy":0,
	"sad":0,
	"surprise":0	
};

var EmotionModel;
var offset_x = 34;
var offset_y = 20;
var emotion_labels = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"];
var emotion_colors = ["#ff5722","#827717","#6200ea","#c51162","#3f51b5","#004d40","#9e9e9e"];

let forwardTimes = []
var chart=null;
var flag=false;



//updates the fps
function updateTimeStats(timeInMs) {
            forwardTimes = [timeInMs].concat(forwardTimes).slice(0, 30)
            const avgTimeInMs = forwardTimes.reduce((total, t) => total + t) / forwardTimes.length
            //$('#time').val(`${Math.round(avgTimeInMs)} ms`)
            $('#fps').val(`${faceapi.round(1000 / avgTimeInMs)}`)
}

//update chart in realtime

function updateCharts(){
	var ctx = document.getElementById("myChart2").getContext("2d");

	if (flag){
		chart.destroy();
	}
	flag=true;
	//plots emotion chart
  	chart=new Chart(ctx,{
			    type: 'doughnut',
			    data: {
			      labels: ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"],
			      datasets: [
				{
				  label: "Emotions",
				  backgroundColor:["#ff5722","#827717","#6200ea","#c51162","#3f51b5","#004d40","#9e9e9e"],
				  data: [emotionDisplay["angry"],emotionDisplay["disgust"],emotionDisplay["fear"],emotionDisplay["happy"],emotionDisplay["sad"],emotionDisplay["surprise"],emotionDisplay["neutral"]]
				}
			      ]
			    },
			    options: {
				animation: {
					duration: 0
				    },
	      			legend: { 
					display: true,
					position: 'right'
				},
			      	title: {
					display: true,
					text: 'Emotion Analysis '
				       }
				    }
				});
} //end update chart


/*
plays and replaces emotion in realtime over a canvas
*/

async function onPlay(videoEl) {
	videoEl.height=constraints.video.height;
	videoEl.width=constraints.video.width;
//check if video is playing or not if not then return no need to process it
	if (videoEl.paused || videoEl.ended || !modelLoaded){
		return false;
	}1
	const {
       		width,
                height
            } = faceapi.getMediaDimensions(videoEl) //get frame dimension
    	const canvas = $('#overlay').get(0)    //canvas over video
    	canvas.width = width                   //assign height and width to the canvas
    	canvas.height = height

	const forwardParams = {
		inputSize: parseInt(sizeType),
		scoreThreshold
	}

    	const ts = Date.now()
	//detects face
    	const result = await faceapi.detectAllFaces(videoEl, new faceapi.TinyFaceDetectorOptions(forwardParams))
        //console.result


	if (result.length != 0) {
		const context = canvas.getContext('2d')
                context.drawImage(videoEl, 0, 0, width, height
) //draw new frame 

                let ctx = context;
                ctx.lineWidth = 4;
                ctx.font = "25px Arial"
                ctx.fillText('Result', 0, 0);

                for (var i = 0; i < result.length; i++) {
                    ctx.beginPath();
                    var item = result[i].box;
                    let s_x = Math.floor(item._x+offset_x);
                    if (item.y<offset_y){
                        var s_y = Math.floor(item._y);
                    }
                    else{
                        var s_y = Math.floor(item._y-offset_y);
                    }
                    let s_w = Math.floor(item._width-offset_x);
                    let s_h = Math.floor(item._height);
                    let cT = ctx.getImageData(s_x, s_y, s_w, s_h);
                    cT = preprocess(cT);

                    z = EmotionModel.predict(cT)
                    let index = z.argMax(1).dataSync()[0]
                    let label = emotion_labels[index]; //detected emotion
		    //console.log(label);
		    emotionDisplay[label]=emotionDisplay[label]+1;
		    //console.log(emotionDisplay[label]);
updateCharts();
		    updateCharts();		    
                    ctx.strokeStyle = emotion_colors[index];
                    ctx.rect(s_x, s_y, s_w, s_h);
                    ctx.stroke();
                    ctx.fillStyle = emotion_colors[index];
                    ctx.fillText(label, s_x, s_y);
                    ctx.closePath();
                }//end for

            }//end if
            updateTimeStats(Date.now() - ts)
	    setTimeout(() => onPlay(videoEl))
            //var status = document.getElementById('status');
            //status.innerHTML = "Running the model ... ";
}


async function loadNetWeights(uri) {
            return new Float32Array(await (await fetch(uri)).arrayBuffer())
        }
        // create model
        async function createModel(path) {
            let model = await tf.loadModel(path)
            return model
        }
        // load emotion model
        async function loadModel(path) {
           
            EmotionModel = await createModel(path)
           
        }

        function preprocess(imgData) {
            return tf.tidy(() => {
                let tensor = tf.fromPixels(imgData).toFloat();
                tensor = tensor.resizeBilinear([100, 100])
                tensor = tf.cast(tensor, 'float32')
                const offset = tf.scalar(255.0);
               const normalized = tensor.div(offset);
                const batched = normalized.expandDims(0)
                return batched
            })
        }
	//success handler for webcam
        function successCallback(stream) {
            var videoEl = $('#inputVideo').get(0)
            videoEl.srcObject = stream;
        }
	//Error handler for webcam
        function errorCallback(error) {
            alert(error)
            console.log("navigator.getUserMedia error: ", error);

        }

        
