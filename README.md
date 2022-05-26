# Capture-Attend
A face recognition attendance management website using Python, Open-CV, Django and SQLite for Microsoft Engage 2022.

# Engage2022
 #### Problem Statement
Develop a browser-based application or a native mobile application to demonstrate application of Face Recognition technology. <br>

 This is my project under Microsoft Engage 2022 Mentorship programme aimed at using Computer Vision to detect a face and mark the attendance of a student. The detector created is pretty   accurate and trains itself perfectly with just one picture that is uploaded by the respective student. The project runs on the server built using Django.
 This project can be used in educational institutions or work places to register students or employees with minimal manual work.
 
 ## Project Structure
  #### As instructed by my mentor, I have implemented a few elements of Agile methodology to ensure this project comes into shape
  Week 1 : Creation of the login page, creation of the database for saving information, implementing face recognition features and ensuring detection of faces.
  <br> Week 2: Getting the information and displaying it on the attendance report page, making sure that the details are printed correctly along with date.
<br> Week 3: Working on a system that would allow exporting the attendance report in the form of Excel sheet and doing any minor changes in the other portions to ensure smooth working.
<br> Week 4: Creating a sign up interface (I was working with making every new individual superuser which didn’t seem efficient), final touches and plans to deploy.

 ## 💻Features
 1. Real Time Camera
 2. Face Recognition in the frame
 3. Marking attendance along with date
4. Taking the information into a database that can be exported to an Excel sheet

 ## Tech Stack Used
 [![My Skills](https://skills.thijs.gg/icons?i=python,js,html,css,django)](https://skills.thijs.gg)
 1. Python 
 2. Open-CV
 3. Django
 4. db.sqlite
 5. HTML
 6. CSS
 7. Javascript 
 
 
## Running this project

To get this project up and running you should start by having Python and pip installed on your computer.You can refer to the links below <br>
https://www.python.org/downloads/ <br>
https://pip.pypa.io/en/stable/installation/ <br>

Clone or download this repository and open it in your editor of choice or use Command Prompt terminal
```
git clone https://github.com/harshi1122/Capture-Attend.git
```
In the terminal, run the following commands in the base directory of this project.<br> 
Note: If using Command Prompt, to navigate to the base directory after cloning, run the following command
```
cd capture-attend
```
Install the project dependencies with
```
pip install -r requirements.txt
```
Now you can run the project with the below command
```
python manage.py runserver
```
or
```
py manage.py runserver
```



