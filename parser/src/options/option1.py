# This is for creating the Transcript File 
import PyPDF2, threading, os

# Import the needed functions for the various modules 
from parser.PlanBackwards import studentInfoBackwards, calculateUpperDivCredits
from parser.StudentInfo import trackStudentInformation
from parser.ParseClasses import *
from tablecreator.CreateTabularDocument import *

# Import the needed functions for sending the xlsx file to the backend 
import requests, json

def option1():
    
    # Now here we wil ask the user to specify the name of the PDF file
    directory_name, pdf_file_name = "", ""

    while True:

        pdf_file_name = str(input("Specify the name of the PDF file in the input folder (without .pdf). Otherwise, type exit to end the transaction: \n"))
        pdf_file_name_extended = pdf_file_name + '.pdf'

        if pdf_file_name.lower() == "exit": return 


        # Now check to see if this file exists
        input_folder_path = "..\\input\\"
        input_folder_files = os.listdir(input_folder_path)

        if pdf_file_name_extended in input_folder_files:
            directory_name = input_folder_path + pdf_file_name_extended
            break 
        else: print("The file does not exist. Please try again and input a valid file name\n")
    
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
        print("Student is not a CSE or ISE major. Please input a different transcript. Returning to the options menu\n") 
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
    
        
    # We then get the file name 
    fileNameInput = pdf_file_name.strip(".pdf")
    
    # Create the file_location as to where we are going to put the transcript 
    file_location = f'..\\output\\{fileNameInput}.xlsx'

    # Create a large dictionary that will store needed information 
    buffer_to_store = {

        'student_information': studentInformation, # This is already in JSON 
        'lower_division_courses': convertObjectsToJSON(lowerDivisionCourses), # We need to convert the rest to JSON 
        'upper_division_courses': convertObjectsToJSON(upperDivisionCourses),
        'technical_cse_courses': convertObjectsToJSON(technicalCSECourses),
        'math_required_courses': convertObjectsToJSON(mathRequiredCourses),
        'science_courses': convertObjectsToJSON(scienceCourses),
        'sbc_courses': convertObjectsToJSON(sbcCourses),
        'specialize_courses_ISE': convertObjectsToJSON(specializeCoursesISE),
        'specialize_courses_CSE': convertObjectsToJSON(specalizeCoursesCSE),
        'classes_per_semester': convertObjectsToJSON(classesPerSemester)
    }

    
    # Now we make a POST request and convert the file to a CSV and store it to the backend 
    json_to_send = {'file_name': fileNameInput, 'file': file_location, 'file_info_buffer': buffer_to_store}  
    
    # POST Request 
    send_transcript_response = requests.post("http://127.0.0.1:8000", json=json_to_send)

    # Display the JSON returned to us from the POST request 
    send_transcript_response_json = send_transcript_response.json()
    print(f'HTTP Status Code: {send_transcript_response.status_code}: {send_transcript_response_json.get("message")}', end="\n\n")

    if "UPDATE" in send_transcript_response_json.get('message'):

        update_request_input = input(str("Do you wish to UPDATE the file? (Y/N): "))

        if update_request_input == "Y" or update_request_input == "y":
            
            # PUT request 
            send_transcript_update = requests.put("http://127.0.0.1:8000", json=json_to_send)
            
            # Display the JSON returned to us from the PUT request
            send_transcript_update_json = send_transcript_update.json()
            print(f'HTTP Status Code: {send_transcript_update.status_code}: {send_transcript_update_json.get("message")}', end="\n\n")

        elif update_request_input == "N" or update_request_input == "n":
            print("Request to UPDATED Denied. Returning program to the options menu\n")
        else:
            print("Unrecognized Command. Returing program back to the options menu\n")
    return 
  
    
def convertObjectsToJSON(dictionary_to_convert: dict) -> dict:
    
    dictionary_to_return = {}

    for keys, values in dictionary_to_convert.items():
        if type(values) == list:
            dictionary_to_return[keys] = []
            for value in values:
                dictionary_to_return[keys].append(json.dumps(value.to_json()))
        else:
            dictionary_to_return[keys] = json.dumps(values.to_json())
    
    return dictionary_to_return