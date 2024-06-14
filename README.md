# Transcript-Parser

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
- Docker Compose 

# Running The Program 

1) Put any transcripts you wish to parse in the folder labeled **input**

2) Within the 'src' folder, look for the python module titled **main.py**

3) Run the code in the module


```
python3 main.py
```

This will give the user a command line interface with **4 options:** 

- **CREATE** an XLSX file, where you can select **1**, which would prompt you
    to enter the PDF file to be parsed. After the file has been parsed, you may choose to **UPDATE** 
    the file if it already exists.

- **GET** an XLSX file, where you can select **2**, which would prompt you to enter 
    the name of the file that is stored on the backend. After selecting the name of the file, the file will appear in the **output** folder 

- **DELETE** an XLSX file, where you can select **3**, which would prompt them to enter the name of the file that is stored on the backend. After selecting the name of the file, not only will it delete the file on the backend, but if the file exists in the output directory, it will be deleted there as well. 

- **EXIT** the program. wnhere you can select **4**, which would terminate the program 

# Running The Program With Docker 

