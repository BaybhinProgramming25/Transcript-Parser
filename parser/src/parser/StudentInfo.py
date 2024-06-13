"""
This module is responsible for finding most
of the student Information that is on the transcript 
"""

import datetime

def trackStudentInformation(text: list[str], studentInfoDict : dict, option: str) -> dict: # May not be our exact return date 
        
        # This will hold the updated values of our pre reqs 
        extract_pre_reqs = handlePreReqs(text, studentInfoDict)
        studentInfoDict.update(extract_pre_reqs) # Update the original 

        if option == "REQUIREMENT":
                requirementOption(text, studentInfoDict)
        elif option == "CUMULATIVE":
                cumulativeOption(text, studentInfoDict)
        
        return studentInfoDict


def handlePreReqs(text: list[str], studentInfoDict: dict) -> dict:
    # First go through some few student information parameters (time, name, and id number) 
        last_updated_time = studentInfoDict.get('Last Updated')
        name = studentInfoDict.get('Name')
        id_number = studentInfoDict.get('ID Number')
        cshp_boolean = studentInfoDict.get('CSHP')

        if last_updated_time is None:
                # Handle Time
                current_time = datetime.datetime.now()
                formatted_date_time = current_time.strftime("%m/%d/%Y %I:%M %p")
                studentInfoDict['Last Updated'] = formatted_date_time
        
        if name is None: 
                # Handle name
                for line_info in text:
                        if "Name" in line_info:
                                stripped_line = line_info.strip("Name: ").strip(" ")
                                studentInfoDict['Name'] = stripped_line
                                break
        if id_number is None:
                for line_info in text:
                        if "Student ID" in line_info:
                                stripped_line = line_info.strip("Student ID: ").strip(" ")
                                studentInfoDict['ID Number'] = stripped_line
                                break 
        
        # Not too sure about this approach but we don't worry too much about it 
        if cshp_boolean is None:
                cshp_found = False 
                for line_info in text:
                        if "CSHP" in line_info:
                                cshp_found = True 
                                break 
                studentInfoDict['CSHP'] = "Yes" if cshp_found else "No"


        return studentInfoDict

def requirementOption(text: list[str], studentInfoDict: dict) -> dict:
        index_of_requirement = -1

        for index, line_info in enumerate(text):
                if "Beginning" in line_info:
                        index_of_requirement = index; 

        studentInfoDict['Requirement Term'] = text[index_of_requirement+2]
        return studentInfoDict

def cumulativeOption(text: list[str], studentInfo: dict) -> dict: 
        index_of_cumulative = -1

        for index, line_info in enumerate(text):
                if "Career" in line_info:
                        index_of_cumulative = index 
                        break 
        
        # Find the Cumulative GPA 
        cumulative_gpa_string = text[index_of_cumulative+1].strip("Cum GPA:")
        index_of_cumulative_totals = cumulative_gpa_string.index("Cum Totals")
        cumulative_gpa_value = cumulative_gpa_string[0:index_of_cumulative_totals]

        # Find the Cumulative Total 
        cumulative_section = cumulative_gpa_string[index_of_cumulative_totals:].strip("Cum Totals")
        first_whitespace_index = cumulative_section.index(' ')
        totals_value_string = cumulative_section[first_whitespace_index+1:]
        second_whitespace_index = totals_value_string.index(' ')

        totals_value = totals_value_string[0:second_whitespace_index]
        
        studentInfo['Cumulative GPA'] = cumulative_gpa_value
        studentInfo['Cumulative Credits'] = totals_value

        return studentInfo 