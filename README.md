# Flask File to CSV

Flask-based API program which takes a user-submitted text file and sends back a CSV file for download through the user's browser. 

## Table of Contents

- [Introduction](#introduction)
- [Goals](#goals)
- [Technologies Used](#technologies-used)
- [Demo](#demo)
- [Challenges](#challenges)
- [Future Plans](#future-plans)

## Introduction

A project where the focus was to create a simple yet complex API where the user submits a text file and converts the file into a CSV. 

The idea was to keep the idea simple, but encourage learning and good programming by having a lot of depth into the codebase. 

The project encouraged a lot of learning as it introduced concepts and functionality I have not yet learned. For example, implementing Flask Responses to generate a download file on the user's browser.

The project was also a good way to reinforce my learning on lists and dictionaries as it involved plenty of complex manipulation of these data types.

Additionally, the focus of this project was less to do with the front-end components, but more the back-end.

## Goals

- To generate a basic Flask front-end website where it allows for users to upload a grid based text file.
- Check that the file is a valid file type (text) and that the file has equal amount of columns per row.
- Use Flask forms to generate the forms.
- To process the file and convert to CSV in the program.
- Send over the file back to the client for download.
- Focus on back-end functionality such as data validation and transformation of the user data.
- To learn new tools such as new libraries and further functionalities with Flask.
 
## Technologies-Used

- Python
- Flask
- HTML
- WTforms
- CSV, OS, Tempfile libraries

## Demo

1) User uploads a text file (Note: The rows must have equal amount of columns) For example:
   
   ![image](https://github.com/Mintydew/flask_file_to_csv/assets/12553525/10ffd3b6-a9fb-4377-8e77-aab275bf14cc)
3) User submits the file and clicks "Submit"
4) If valid, a downloadable csv file (name: output.csv) is sent straight back to the user after processing it's contents in the back-end.
   
   ![image](https://github.com/Mintydew/flask_file_to_csv/assets/12553525/2fcf7cb7-1781-4532-9512-d1587d030e12)

## Challenges

The focus of this project was about diving deep into the back-end capabilities of Flask and processing the files. As such, there were a lot of hurdles along the way which encouraged some fantastic learning opportunities such as:

- Creating a Flask Response as the return. This was a major struggle initially as I was not aware on how to send a downloadable file back to the client.
- Up until so far, I only knew how to create a CSV file through writing straight into the system (e.g. my project folder). The challenge was to find a way to get around this by creating a temporary file and preparing it to send back as a response to the client.
  
![image](https://github.com/Mintydew/flask_file_to_csv/assets/12553525/79698f9e-27c4-4aa6-ad10-969010a5f80a)
- Validation of the file was fairly tricky. As I worked more on the program, I tested the program and found ways to break its functionality by adding in complexity to the uploaded text file. For example, instead of having a single line of space inbetween each content in the text file, what if there were two spaces?

## Future-Plans

I plan to work further into the project, to introduce better functionalities and greater capabilities. Some ideas so far are:

- Unit test more in each function to identify errors and fix them. 
- Optionally, look into using unit testing in GitHub to enhance learning and get my hand around how to unit test in a Github environment.
- Allow for users to enter the name of the file instead of having output.csv as the default.
- Furthermore, identify a way for the user to designate where to upload the file as well. (Essentially a "save as" functionality that is in a lot of programs)
- Allow for more file types as upload than text files.
- Allow for multiple file type exports instead of just CSV (E.g. CSV -> Text)

