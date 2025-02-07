# Class-Analytics-Generator
This repository contains source code of project "Real-Time Monitoring of Student's Behaviour to Generate Class Analytics".

# Functional Requirements
1. Accept Live Video Feed from Camera (p)
2. Detect and Extract Students Faces from video frame (p)
3. Recognise Facial Emotion from extracted faces (p)
4. Enable faculty to create quizzes (p)
5. Enable admin and faculty to login (c)
6. Enable faculty to communicate with admin (c)
7. Enable admin to manage faculty (c)
8. Detect student posture in the classroom (p)
9. Generate Visualisations, Excel file (partial)
10. Give strategies and advices to faculty (p)

# Non-Functional Requirements
1. Low Latency
2. Available to only faculty and admin

# Description of different modules of project

**Admin**
- Create an endpoint for admin to access UI (c)
- Create admin login form to accept admin id and password (c)
- Create database to store Admin details, Faculty details, Departments and Classrooms details (c)
- Store all the passwords in encrypted form (p)
- Admin should add/remove/update faculty and classroom details through excel file and manually also 
- Create and maintain Deep Learning Models which measure Engagement
- Create a Deep Learning Model which accept Video frames to detect students faces and predict their facial emotion
- Create a Deep Learning Model which analyse students behaviour
- View all the messages received from faculty and respond to them

**Faculty**
- Create a Login form for faculty to Login (c)
- Create a dashboard for faculty to view classrooms (c), and view analytics, stragtegies for each classroom
- Create a option to message Admin and view response from the admin (c)

