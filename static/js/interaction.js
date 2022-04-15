//speech synthesis
         var synth = window.speechSynthesis;
         window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
         const recognition = new SpeechRecognition();
         recognition.interimResults = true;
         recognition.lang = 'en-US';
         

         p=document.getElementById("words");
         text="";
         recognition.addEventListener('result', e => {
         //console.log(e)
         const transcript = Array.from(e.results)
         .map(result => result[0])
         .map(result => result.transcript)
         .join('');
         const script = transcript; //replace anything here
         
         $('#messageText').val(script);
         if (e.results[0].isFinal) {
         //p = document.createElement('p');
         //words.appendChild(p);
         //$('#messageText').val(text);
         }
         });
         recognition.addEventListener('end', recognition.start);
         recognition.start();
