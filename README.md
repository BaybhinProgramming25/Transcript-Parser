This software enables users to place a PDF of their transcript, which will output an XLSX file that displays
their graduation checklist. Note that these PDFs only work for students that are **computer science majors** or 
**information systems majors**. 

More about the program: This program is a **CLI** based software that prompts users to input a PDF of their choosing
for it to be **parsed**. The data that is parsed is then store onto **MongoDB** with the help of the **FastAPI** to handle user request handling as well as perform **CRUD** based operations 

Note: There were some libraries used that may require downloading on the user-end using **pip install**

Modules Used:
- threading
- PyPDF2
- os
- openpyxl
- sys
- requests 
- json 
- datetime

How to Run The Code: 

1) Put any transcripts you wish to parse in the folder labeled 'input'

2) Within the 'src' folder, look for the python module titled 'Main'

3) Run the code in the module. This will prompt the user with a set of **4** options 

4) If a student wishes to **CREATE** an XLSX file, they can select **option 1**, which would prompt them
to enter the PDF file to be parsed. After the file has been parsed, the student may choose to **UPDATE** 
the file if it already exists 

5) If a student wishes to **GET** an XLSX file, they can select **option 2**, which would prompt them to enter 
the name of the file that is stored on the backend. After selecting the name of the file, the file will appear in the **output_xlsx** folder 

-- MORE STEPS TO BE ADDED --

6) Repeat until requests have been satisifed, performing graceful termination by typing the word 'exit' pressing 'Enter'
