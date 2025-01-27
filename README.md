# Class-Analytics-Generator
This repository contains source code of project "Real-Time Monitoring of Student's Behaviour to Generate Class Analytics".

# Functional Requirements
1. Accept Live Video Feed from Camera
2. Detect and Extract Students Faces from video frame
3. Recognise Facial Emotion from extracted faces
4. Enable faculty to create quizzes
5. Enable admin and faculty to login
6. Enable faculty to communicate with admin
7. Enable admin to manage faculty
8. Detect student posture in the classroom 
9. Generate Visualisations, Excel file
10. Give strategies and advices to faculty

# Non-Functional Requirements
1. Low Latency
2. Available to only faculty and admin

# Description of different modules of project

**Admin**
- Create an endpoint for admin to access UI
- Create admin login form to accept admin id and password
- Create database to store Admin details, Faculty details, Departments and Classrooms details
- Store all the passwords in encrypted form
- Admin should add/remove/update faculty and classroom details through excel file and manually also
- Create and maintain Deep Learning Models which measure Engagement
- Create a Deep Learning Model which accept Video frames to detect students faces and predict their facial emotion
- Create a Deep Learning Model which analyse students behaviour
- View all the messages received from faculty and respond to them

**Faculty**
- Create a Login form for faculty to Login
- Create a dashboard for faculty to view classrooms, and view analytics, stragtegies for each classroom
- Create a option to message Admin and view response from the admin

