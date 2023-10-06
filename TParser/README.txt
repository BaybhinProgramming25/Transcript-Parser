The purpose of this program is to convert CSE/ISE student transcripts into a dynamic, tabular document for ease of readibility and maintainability. The program functions as a parser that will interpret and store information to be used upon development of the document. 

Note: There were some libraries used that may require downloading on the user-end.

Modules Used:
- threading
- PyPDF2
- os
- shututil
- openpyxl
- sys
- typing

How to Run The Parser: 

1) Place any transcripts to undergo parsing in the folder labeled 'input'.

2) Run the code in the module Main.py, prompting an input of the name of the transcript to be parsed in the input folder.

3) Type in the name of the transcript with the input path specified and press 'Enter' (i.e. if you have a transcript in the input folder titled 'Example.pdf', then you would need to specify the user input as: input\Example.pdf)

4) An XLSX sheet will be produced with the same name as the transcript in the 'output' folder.

5) Repeat until requests have been satisifed, performing graceful termination by entering 'exit' and pressing 'Enter'.

Note: In the program's current state, the program will ONLY parse the current format of Unofficial Transcripts. This program will likely to be updated overtime in order to slowly reflect multiple formats.