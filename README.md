# MEDHA(Online-Test-Portal) 
(Online-Test-Portal) project has been made very interactive keeping in mind since this pandemic has started, all the work, studies, examinations.., are on-going with the online mode, it’s very difficult to conduct physical examinations for the students, so we developed this website.
# OVERVIEW
A test portal for students who are willing to take small quiz and basic exams with its re-usability and user-friendliness the Admin can access with the database where information is stored and can be retrieved at any time whenever required and the system generates a unique ID from Google fire-base so that the user admin can access the database to host Quiz, Small assessments and multiple type of examinations. The project has been developed using HTML as a front end and Flask, Sqlite3 DB as a back end. According to today’s requirement Online examination system is significantly important to the educational institution to prepare the exams, saving the time and effort that is required to check the exam papers and to prepare the results reports. Online examination system helps the educational institutions to monitor their students and keep eyes on their progress. The best use of this system in Scholastic Institute and training centres because it helps in managing the exams and get the results in easy and an efficient manner. Until today the preparing for exams and preparing the results was performed manually, this required more time to complete
#  SOFTWARE's USED
 * Visual Studio code
 * Sqlite3 DB
 * Google Firebase
 * Python
# Methodology
 In software engineering, this developing methodology called ‘waterfall model’ which one portion of work follows after another in a linear sequence.
# BASIC THEORY
Methodology
The key concept is to minimize the amount of paper and convert all forms of documentation to digital form. It can observe that the information required can be obtained with ease and accuracy in the computerized system. The user with minimum knowledge about computer can be able operate the system easily. The system also produces brief result required by the management. Responses will be checked automatically. Reduce the hectic job of assessing answers. It will reduce paper work. Can generate reports instantly. The students will be able to access their exam results online without coming to school to get to know the results. This will reduce the time, money and effort through the use of this application. To provide registration for students done by themselves. To not provide facility of copy and paste while attempting the Subjective questions on the web page. When the student starts the exam the timer will start automatically and show the student how much time is left. We are going to make an attractive examination portal in which user can create an account after which user have to sign in to attempt the test. Most of the currently existing portals we know have some problems like crashing or getting hanged. We will try to overcome these problems. We tried to make this site robust, reliable and it takes less bandwidth to move from one page to next page. We have also working on encryption decryption of the password using some algorithm.
# Software Design and Implementation:
## 1. Login system
* Login as admin:- By using already stored admin name and password the individual can log on to the system any time he/she desires as an admin to manage the admin activities. Logging is successful only if the input detail is matched with the database, else an error message is displayed.
* Login as student:- The information of each student will be sorted by the admin upon the registration process, enabling this way the particular student to log on the system without having to undergo the process of registration again. Logging is successful only if the input detail is matched with the database, else an error message is displayed.
## 2. Admin activities
* Admin activities contain the following programs:
* Questions management Managing questions contain two main operations: 
 1. Adding Questions: - include adding three type of questions according to the admin desires either (true/false, multiple choices, image matching).
 2. Deleting Questions:- include deleting questions of the three types of questions (true/false, multiple choices, image matching).
### Students management
* Managing students contain two main operations: 
 1. Registering students:- include inserting the information of each student (student name, email, and password) to complete the registration process.
 2. Deleting student:- by inserting the (name and email) of the student to be deleted the admin can delete any student. 
 ## 3. Students activities 
 * Student activities contain the following operations:
 1. Give the exam:- After the student logging in, a group of questions will be displayed to him to start and give an exam.
 2. Get the results:- After answering all the questions, the student will finish the exam and his/her score will be displayed on the screen.
 ## 4. Database design:-
 * In order to fully use SQLite3 server technology, it is essential to make sure that the database is well designed. The files names chosen to label all the tables created within the database attempt to reflect the table's purpose and, therefore, contribute to well-design system. The intimal step in designing was to decide, according to the requirements and specifications of the project, which tables should be created, and what type of information each one should hold.
 # STEPS INVOLVED TO EXECUTE
 - create a virtual environment on command prompt or on your terminal.
 -  Install requirements
 -  Run the command in virtual environment(flask run/python app.py)
 -  Click on the generated link and access the portal

### For quires contact - reddy89190@gmail.com
