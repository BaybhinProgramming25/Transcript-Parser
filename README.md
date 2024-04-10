# Distributed-Transcript-Parser

This software enables users to place a PDF of their transcript, which will output an XLSX file that displays
their graduation checklist. Note that these PDFs only work for students that are **computer science majors** or 
**information systems majors**. 

More about the program: This program is a **CLI** based software that prompts users to input a PDF of their choosing
for it to be **parsed**. The data that is parsed is then store onto **MongoDB** with the help of the **FastAPI** to handle user request handling as well as perform **CRUD** based operations 

# Technologies Used

- Python
- FastAPI
- MongoDB
- Docker

How to Run The Code: 

1) Put any transcripts you wish to parse in the folder labeled 'input'

2) Within the 'src' folder, look for the python module titled 'Main'

3) Run the code in the module. This will prompt the user with a set of **4** options 

4) If a student wishes to **CREATE** an XLSX file, they can select **option 1**, which would prompt them
to enter the PDF file to be parsed. After the file has been parsed, the student may choose to **UPDATE** 
the file if it already exists 

5) If a student wishes to **GET** an XLSX file, they can select **option 2**, which would prompt them to enter 
the name of the file that is stored on the backend. After selecting the name of the file, the file will appear in the **output_xlsx** folder 

6) If a student wishes to **DELETE** an XLSX file, they can select **option 3**, which would prompt them to enter the name of the file that is stored on the backend. After selecting the name of the file, not only will it delete the file on the backend, but if the file exists in the output_xlsx directory, the file will be deleted there as well.

7) Repeat such requests until the user is satisfied. If so, the user can select **option 4** to terminate the program and close connection to the database 
