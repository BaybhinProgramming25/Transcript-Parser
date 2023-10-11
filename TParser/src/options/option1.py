# This is for creating the Transcript File 
import PyPDF2, os, threading, shutil, openpyxl

# Import the needed functions for the various modules 
from parser.PlanBackwards import studentInfoBackwards, calculateUpperDivCredits
from parser.StudentInfo import trackStudentInformation
from parser.ParseClasses import *
from tablecreator.CreateTabularDocument import *

# Import the needed functions for sending the xlsx file to the backend 
import requests 

def option1():
    
    # Now here we wil ask the user to specify the name of the PDF file
    directory_name, pdf_file_name = "", ""

    while True:

        pdf_file_name = str(input("Specify the name of the PDF file in the input folder. Otherwise, type exit to end the transaction: \n"))

        if pdf_file_name.lower() == "exit": return 

        # Now check to see if this file exists
        input_folder_path = os.getcwd() + "\\TParser\\input\\"
        input_folder_files = os.listdir(input_folder_path)

        if pdf_file_name in input_folder_files:
            directory_name = input_folder_path + pdf_file_name
            break 
        else: print("The file does not exist. Please input a valid file name\n")
    
    # 1) Open the file in read-binary mode 
    file = open(directory_name, "rb")
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)

    # 2) Initialize our data buffers 
    studentInformation, upperDivisionCourses, lowerDivisionCourses, technicalCSECourses, mathRequiredCourses, scienceCourses, sbcCourses, specializeCoursesISE, specalizeCoursesCSE, classesPerSemester = {}, {}, {}, {}, {}, {}, {}, {}, {}, {}

    # References to the first page & last page 
    first_page = pdf_reader.pages[0]
    last_page = pdf_reader.pages[total_pages - 1]

    extract_firstpage_info = trackStudentInformation(first_page.extract_text().split("\n"), studentInformation, "REQUIREMENT")   
    extract_lastpage_info = trackStudentInformation(last_page.extract_text().split("\n"), studentInformation, "CUMULATIVE")

    studentInformation.update(extract_firstpage_info) # Update Dictionary 
    studentInformation.update(extract_lastpage_info) # Update Dictionary 

    # Perform a second pass, which collects the major and specialization of the student from the back 
    for i in range(total_pages - 1, -1, -1):

        page = pdf_reader.pages[i] # Get the current page
        text = page.extract_text().split('\n')[::-1]

        extracted_major_spec = studentInfoBackwards(text, studentInformation)
        extracted_upper_cred = calculateUpperDivCredits(text, studentInformation)
        
        studentInformation.update(extracted_major_spec)
        studentInformation.update(extracted_upper_cred)

    check_major_exists = studentInformation.get('Major')

    # Need to make sure the major is a CSE student or ISE student
    if check_major_exists == "CSE" or check_major_exists == "ISE":
        if studentInformation.get('Spec') is None: studentInformation['Spec'] = "" # Keep as empty string
    else: 
        print("Student is not a CSE or ISE major. Please input a different transcript\n") 
        return 

    for i in range(total_pages):

        page = pdf_reader.pages[i]
        text = page.extract_text().split('\n') 

        #Have multiple threads to find the information concurrently 
        thread2 = threading.Thread(target=majorClassTracker, args=(text, studentInformation, upperDivisionCourses, lowerDivisionCourses, technicalCSECourses, specializeCoursesISE, specalizeCoursesCSE, mathRequiredCourses))
        thread3 = threading.Thread(target=mathTracker, args=(text, studentInformation, mathRequiredCourses))
        thread4 = threading.Thread(target=scienceTracker, args=(text, studentInformation, scienceCourses))
        thread5 = threading.Thread(target=sbcsTracker, args=(text, studentInformation, sbcCourses))
        thread6 = threading.Thread(target=classTracker, args=(text, studentInformation, classesPerSemester))

        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()

        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
    
    # 5) Get the name of the transcript
    excel_file = directory_name[::directory_name.index('.')] + '.xlsx'

    # 6) Check to see if the file exists or the file is currently opened 
    fileOpened, fileExists = False, False 

    if os.path.isfile(f'{os.getcwd()}\\TParser\\output_xlsx\\{excel_file}'): 
        fileExists = True
        try: 
            wb = openpyxl.load_workbook(excel_file, read_only=True)
            wb.close() # We close the workbook immediately to prevent file descriptor errors 
        except IOError: 
            for filename in os.listdir('output_xlsx'):
                if filename.startswith(f'~${excel_file}'):
                    fileOpened = True
                else: # The file is not there, meaning it is closed
                    fileOpened = False

    # 7) Create the document and throw error if need be 
    if not fileOpened or not fileExists:
        
        # Create Document
        fileNameInput = pdf_file_name.strip(".pdf")
        workbook_and_file = createDocument(fileNameInput, studentInformation, upperDivisionCourses, lowerDivisionCourses, technicalCSECourses, mathRequiredCourses, scienceCourses, sbcCourses, classesPerSemester, specializeCoursesISE, specalizeCoursesCSE) 
        
        # Create the file_location as to where we are going to put the transcript 
        file_location = f'{os.getcwd()}\\TParser\\output_xlsx\\{workbook_and_file[1]}'

        # Now we make a POST request and convert the file to a CSV and store it to the backend 
        json_to_send = {'file_name': fileNameInput, 'file': file_location}  
        send_transcript = requests.post("http://127.0.0.1:8000", json=json_to_send)

        if send_transcript: print("\nSuccesfully Created the file!", end="\n\n")
        else: print("\nThe transcript failed to be made!", end="\n\n")
        
        return 
    
    else:
        print("Please close the file first before proceeding\n")
        return