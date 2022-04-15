# Interview Bot - A chatbot based Approach for interview preparation.

Preparing for job interviews is very difficult. A lot of candidates are not prepared for the interviews and so they are not able to fetch their dream jobs. Mostly candidate's selection is based on the answers given in the interview. Using deep learning techniques we are proposing an application framework which would help candidates in preparing for the interviews.


## Our Solution for this problem
We wanted to provide candidates a realtime  analysis of their interviews.
We utilized Flask as our backend for simple reason that it was microframework and was easier to setup and get started.
We utlized AIML for our chatbot interaction.
We trained the cnn model for emotion analyis using FER+ dataset.
Realtie audio visulaization is provided with the help of RecordJS,VideoJS and waveformJS libraries.
PDFKit is utlized for generation of dynamic pdfs.

## What next?
We have lots of idea regarding this project and would add more features in near future.
 **Planned for now**
 - Answer Evaluation (Using cosine Similarity) ( Collecting data regarding the same)
 - Fixed and chat mode for interview
 - 3d interviewer ( looking for 3d face models online, unable to find them yet, if not not found we have to create it on our own, we would utilize Three.js for the same and render the model using webgl)
 
## Our Goal
To evolve this project as a end to end platform for interview preparations.

## Technologies Used

 - Python 3.6
 - Flask
 - SQLAlchemy
 - TensorflowJS
 - Keras
 - RecordJS
 - VideoJS
 - WaveformJS
 - Web-RTC
 - My-SQL Database (will migrate to mongodb in future)
 - Bootstrap 4
 - AIML (v1.1)

