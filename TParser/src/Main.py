""" 
Our entry point into the program. The main program is responsible
for initializing the state variables and creating threads that will
traverse through the transcript, parse the information, and store the
information within the state variables. 

After the threads have been reaped, the main program will then create the
tabular document as an XLSX file to be sent in the output folder

Note: This program is only meant for CSE or ISE students in the major
"""


import PyPDF2, os, threading, shutil, openpyxl
from tablecreator.CreateTabularDocument import createDocument
from parser.PlanBackwards import studentInfoBackwards
from parser.StudentInfo import trackStudentInformation, resetGlobalVariablesForStudentInfo 
from parser.CumulativeInfo import trackCumulativeInformation, resetGlobalVariablesForCumulativeInformation
from parser.ParseClasses import *


import requests 


def main():

        while True:
            directory = ""
            fileFound = 0
            while fileFound != 1:
                try:
                    directory = str(input("Please specify the path of the PDF (i.e. input\\NAMEOFFILE.pdf), otherwise type 'exit' to end the program: "))
                    if directory.lower() == "exit": break
                    if os.path.exists(directory) and directory.find(".pdf"):
                        with open(directory, "rb") as file:
                            pdf_reader = PyPDF2.PdfReader(file) 
                            fileFound = 1
                    else:
                        print("Not Found!\n")
                except:
                    print("Please input a valid PDF path\n")

            if directory.lower() == "exit": 
                print("Program Ended!\n")
                break

            file = open(directory, "rb")
            pdf_reader = PyPDF2.PdfReader(file)
            totalPages = len(pdf_reader.pages)
            pagesCounter = 0

            # Initialize the state variables that are going to be storing the information that we need for creating the document
            studentInformation, upperDivisionCourses, lowerDivisionCourses, technicalCSECourses, mathRequiredCourses, scienceCourses, sbcCourses, specializeCoursesISE, specalizeCoursesCSE, classesPerSemester = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

            # Perform the first pass, which collects part of the student information
            for i in range(totalPages):

                page = pdf_reader.pages[i]
                text = page.extract_text().split('\n') 

                # Parses some of the student info from this function call, not including major and specialization
                trackStudentInformation(text, studentInformation) 
                pagesCounter += 1
            
            # Perform a second pass, which collects the major and specialization of the student
            # This pass is needed, as we want the most updated version of the transcript, which is located towards the end 
            for i in range(totalPages - 1, -1, -1):

                page = pdf_reader.pages[i] # Get the current page
                try:
                    page2 = pdf_reader.pages[i + 1] # Get the after the current page 
                except:
                    page2 = pdf_reader.pages[i] # If exception created, we simply pass the current page instead  

                text = page.extract_text().split('\n') 
                text2 = page2.extract_text().split('\n')

                # We either return a string or a boolean. If string is returned, we keep running the for loop
                returnType = studentInfoBackwards(text, text2, studentInformation)

                if returnType == True: break # We stop parsing the student information because we have found what we need
            
            # Need to make sure the major is a CSE student or ISE student
            if studentInformation['Major'] == "CSE" or studentInformation['Major'] == "ISE":

                # If successful, perform a third and final pass to parse the actual information 
                # This part of the program will create threads that go through the transcript and store the info
                # Into the state variables. There are no shared resources among the threads 

                # First check and see if a specialization has been determined
                # If the key does not exist, then we simply create it with a value set to empty string 
                if 'Spec' not in studentInformation: 
                    studentInformation['Spec'] = ""

                for i in range(totalPages):

                    page = pdf_reader.pages[i]
                    text = page.extract_text().split('\n') 

                    thread1 = threading.Thread(target=trackCumulativeInformation, args=(text, studentInformation))
                    thread2 = threading.Thread(target=majorClassTracker, args=(text, studentInformation, upperDivisionCourses, lowerDivisionCourses, technicalCSECourses, specializeCoursesISE, specalizeCoursesCSE, mathRequiredCourses))
                    thread3 = threading.Thread(target=mathTracker, args=(text, mathRequiredCourses))
                    thread4 = threading.Thread(target=scienceTracker, args=(text, scienceCourses)) 
                    thread5 = threading.Thread(target=sbcsTracker, args=(text, sbcCourses)) # Get the SBCs for the courses
                    thread6 = threading.Thread(target=classTracker, args=(text, classesPerSemester))

                    thread1.start()
                    thread2.start()
                    thread3.start()
                    thread4.start()
                    thread5.start()
                    thread6.start()

                    thread1.join()
                    thread2.join()
                    thread3.join()
                    thread4.join()
                    thread5.join()
                    thread6.join()
            else:
                # End the program if the student is not a CSE/ISE major
                sys.exit("Student is not a CSE/ISE Major or did not declare their major")


            # Reset the global variables so it doesn't affect parsing behavior for the next transcript, if any 
            resetGlobalVariablesForStudentInfo() 
            resetGlobalVariablesForCumulativeInformation()

            grabSlash = directory.index('\\')
            grabPeriod = directory.index('.')
            fileNameInput = directory[grabSlash+1:grabPeriod]

            fileOpened = False 
            fileExists = False 


            # We also want to make sure the file is closed before the document is made to prevent any data corruption 
            if os.path.isfile(f'output\\{fileNameInput}.xlsx'): 
                fileExists = True
                try: 
                    wb = openpyxl.load_workbook(fileNameInput + '.xlsx', read_only=True)
                    wb.close() # We close the workbook immediately to prevent file descriptor errors 
                except IOError: 
                    for filename in os.listdir('output'):
                        if filename.startswith(f'~${fileNameInput}.xlsx'):
                            fileOpened = True
                        else: # The file is not there, meaning it is closed
                            fileOpened = False

            if fileOpened == False or fileExists == False:
                    
                # We finally create the document
                fileName = createDocument(fileNameInput, studentInformation, upperDivisionCourses, lowerDivisionCourses, technicalCSECourses, mathRequiredCourses, scienceCourses, sbcCourses, classesPerSemester, specializeCoursesISE, specalizeCoursesCSE) 

                print(fileName)
                print("Sucessfully Created!")


            else: print("Please close the file first, then run the program again\n")

        
if __name__ == '__main__':
    main()
