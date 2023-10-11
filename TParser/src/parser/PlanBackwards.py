""" 
This module is responsible for parsing the transcript backwards to find the most
recent information about the student, specificially the student's major and specialization. 

This ensures that the program doesnt accidently input information into the state variables
of earlier semesters, which creates an outdated document of the student. 
"""
                                    
def studentInfoBackwards(current_page: list[str], studentInformation: dict) -> dict:

    bundled_specializations = ["Artificial", "Interaction", "Game", "Security", "System", "Network", "Health", "Economics", "Technological", "Finance"]

    # First check to see if major or specialization has been found 
    major_found, specialization_found = False, False 

    major_value = studentInformation.get('Major')
    specialization_value = studentInformation.get('Spec')

    if major_value is not None: major_found = True 
    if specialization_value is not None: specialization_found = True 


    for line_info in current_page:

        if "Plan" in line_info:

            # We don't know if we are looking at a specialization line or major line 
            stripped_line = line_info.replace("Plan", "").replace(" ", "")
            
            # We are looking at a specialization 
            if "Specialization" in stripped_line and not specialization_found:

                for specialization in bundled_specializations:
                    if specialization in stripped_line:
                        studentInformation['Spec'] = specialization
                        break 
            
            if "ComputerScience" in stripped_line and "Major" in stripped_line and not major_found:
                studentInformation['Major'] = "CSE"
            elif "InformationSystems" in stripped_line and "Major" in stripped_line and not major_found:
                studentInformation["Major"] = "ISE"
                
    return studentInformation


def calculateUpperDivCredits(current_page: list[str], studentInformation: dict) -> dict:

    current_upper_credits = studentInformation.get("Upper Division Credits")

    if current_upper_credits is None: 
        studentInformation["Upper Division Credits"] = 0 # We set it to 0 for now 
        
    upper_div_credit_counter = studentInformation.get("Upper Division Credits")

    classes_parsed = [] # Keep a track of which classes we have parsed
 
    for line_info in current_page:

        stripped_upper_line = line_info.replace(" ", "")

        if stripped_upper_line[3:6].isdigit():
            
            class_number_int = int(stripped_upper_line[3:6])
            class_description = stripped_upper_line[0:6]

            occurences_occured_three = stripped_upper_line.count("3.000")

            if occurences_occured_three > 1 and class_description not in classes_parsed and class_number_int >= 300:
                classes_parsed.append(class_description)
                upper_div_credit_counter += 3
    
    studentInformation['Upper Division Credits'] = upper_div_credit_counter

    return studentInformation
