# GET an XLSX fie 

from mongo.mongoclient import collection_name
from tablecreator.CreateTabularDocument import createDocument

from classes.UniversalClassObject import *
from classes.MinimalClassObject import *
from classes.SBCClassObject import * 

import requests, json 

def option2():
    
    # Get all the documents in the database and get the one that is needed from the user 
    database_documents = collection_name.find()

    if not database_documents:

        print("There are no documents in the database. Please select option 1 to create a transcript\n")
        return
    
    else:
        # We list out the names of the documents
        list_of_document_names = []
        for index, document in enumerate(database_documents):
            print(f'Document #{index+1}: {document.get("xlsx_name")}\n')
            list_of_document_names.append(document.get('xlsx_name'))
        
        transcript_option = str(input("Please select which of the following transcripts to GET. MAKE SURE ALL XLSX FILES ARE CLOSED\n"))


        option_found = False 
        for name in list_of_document_names:
            if transcript_option == name:
                option_found = True 
                break 
        
        if option_found:
            
            file_to_retrieve = {'file_name': transcript_option}
            get_transcript_response = requests.get("http://127.0.0.1:8000", json=file_to_retrieve)

            get_transcript_response_json = get_transcript_response.json()

            if get_transcript_response.status_code == 404:
                print(f'HTTP Status Code {get_transcript_response.status_code}: {get_transcript_response_json.get("message")}', end="\n\n")
                return 
            
            # We get the file path and now we want to put it in the output folder 
            xlsx_file_path = get_transcript_response_json.get('xlsx_file_path')
            xlsx_buffer_data = get_transcript_response_json.get('xlsx_file_info')

            # Grab the information from the backend 
            studentInformation = xlsx_buffer_data.get('student_information') 
            lowerDivisionCourses = convertJSONToObject(xlsx_buffer_data.get('lower_division_courses'), "UNIVERSAL")
            upperDivisionCourses = convertJSONToObject(xlsx_buffer_data.get('upper_division_courses'), "UNIVERSAL") 
            technicalCSECourses = convertJSONToObject(xlsx_buffer_data.get('technical_cse_courses'), "UNIVERSAL")
            mathRequiredCourses = convertJSONToObject(xlsx_buffer_data.get('math_required_courses'), "UNIVERSAL")
            scienceCourses = convertJSONToObject(xlsx_buffer_data.get('science_courses'), "UNIVERSAL")
            sbcCourses = convertJSONToObject(xlsx_buffer_data.get('sbc_courses'), "SBCCLASS") 
            classesPerSemester = convertJSONToObject(xlsx_buffer_data.get('classes_per_semester'), "MINIMAL") 
            specializeCoursesISE = convertJSONToObject(xlsx_buffer_data.get('specialize_courses_ISE'), "UNIVERSAL") 
            specializeCoursesCSE = convertJSONToObject(xlsx_buffer_data.get('specialize_courses_CSE'), "UNIVERSAL") 

            # Then we create the document with the given path 
            workbook_reference = createDocument(studentInformation, upperDivisionCourses, lowerDivisionCourses, technicalCSECourses, mathRequiredCourses, scienceCourses, sbcCourses, classesPerSemester, specializeCoursesISE, specializeCoursesCSE)
            workbook_reference.save(xlsx_file_path)

            print(f'HTTP Status Code {get_transcript_response.status_code}: {get_transcript_response_json.get("message")}', end="\n\n")
            return 
        
        else:
            print("Could not find the requested document. Returning back to the options menu\n")
            return 
        
def convertJSONToObject(json_to_convert: dict, option: str) -> dict:

   dict_to_return = {}
   
   for keys, values in json_to_convert.items():
        # We first convert the values to a JSON cause they are currently in string format at the moment 
        if option != "MINIMAL":
            string_to_dict = json.loads(values)

            if option == "UNIVERSAL":
                dict_to_object = UniversalClassObject(string_to_dict.get("courseName"), string_to_dict.get("grade"), string_to_dict.get("credits"), string_to_dict.get("term"), string_to_dict.get("year"), string_to_dict.get("comments"))
            elif option == "SBCCLASS":
                dict_to_object = SBCCourse(string_to_dict.get("sbc"), string_to_dict.get("courseName"), string_to_dict.get("grade"), string_to_dict.get("credits"), string_to_dict.get("term"), string_to_dict.get("year"), string_to_dict.get("comments"))
            dict_to_return[keys] = dict_to_object
        else: # Handles the case with classes_per_semester

            dict_to_return[keys] = []
            for value in values:
                string_to_dict = json.loads(value)
                dict_to_object = SimpleClassObject(string_to_dict.get("courseName"), string_to_dict.get("credits"), string_to_dict.get("grade"), string_to_dict.get("term"), string_to_dict.get("year"))
                dict_to_return[keys].append(dict_to_object)

   return dict_to_return