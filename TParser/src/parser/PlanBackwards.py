""" 
This module is responsible for parsing the transcript backwards to find the most
recent information about the student, specificially the student's major and specialization. 

This ensures that the program doesnt accidently input information into the state variables
of earlier semesters, which creates an outdated document of the student. 

"""

# This first function is responsible for finding the most recent semester that the student has taken.
# This is because the most recent semester has the updated info about the student 
def studentInfoBackwards(currentPage, afterCP, studentInformation):

    semestersList = []
    
    for lineofInfo in currentPage:  
        modifiedLine = lineofInfo.replace(" ", "")
        if "Spring" in modifiedLine:
            if modifiedLine[6:10].isdigit(): semestersList.append(f'Spring {modifiedLine[6:10]}')
        elif "Summer" in modifiedLine:
            if modifiedLine[6:10].isdigit(): semestersList.append(f'Summer {modifiedLine[6:10]}')
        elif "Winter" in modifiedLine:
            if modifiedLine[6:10].isdigit(): semestersList.append(f'Winter {modifiedLine[6:10]}')
        elif "Fall" in modifiedLine:
            if modifiedLine[4:8].isdigit(): semestersList.append(f'Fall {modifiedLine[4:8]}')

    if len(semestersList) == 0: # No semester was found, so we need to keep searching (Note: return type is string)
        return "Keep Searching" 
    else: # Semester was found, so we call the next function
        return parsePlanInformation(semestersList, currentPage, afterCP, studentInformation) 


# This function is then responsible for finding the student's major and the student's specialization (if any)
@staticmethod
def parsePlanInformation(semesterList, currentPage, afterCurrent, studentInformation):

    getLatestSemester = semesterList[-1] 
    
    getIndexOfSemester = currentPage.index(getLatestSemester)
    spliceList = currentPage[getIndexOfSemester:]

    # Iterate through the list in order to look for plan 
    parsingPlanBool = False
    majorFound = False 
    specializationFound = False
    iterate_through_splice_counter = 0

    while parsingPlanBool == False:
        if iterate_through_splice_counter >= 0 and iterate_through_splice_counter < len(spliceList) and specializationFound == False: # If the index is within range AND we didn't find the specilization yet, then we execute the code in the if statement
            grabLine = spliceList[iterate_through_splice_counter] # "Grab the info at that line"
            if "Plan" in grabLine and majorFound == False :
                modifiedLine = grabLine.replace("Plan", "").replace(" ", "")
                if "ComputerScience" in modifiedLine and "Major" in modifiedLine: # No "AOI" and no "minor"
                    studentInformation['Major'] = "CSE"
                    majorFound = True
                elif "InformationSystems" in modifiedLine and "Major" in modifiedLine: # No "AOI" and no "minor"
                    studentInformation['Major'] = "ISE"
                    majorFound = True
            elif "Plan" in grabLine and majorFound == True: # Might be a specialization coming up 
                modifiedLine = grabLine.replace("Plan", "").replace(" ", "")
                if studentInformation['Major'] == "CSE" and "Specialization" in modifiedLine: # We are looking at a specialization
                    if "Artificial" in modifiedLine:
                        studentInformation['Spec'] = "Artificial"
                        specializationFound = True
                    elif "Interaction" in modifiedLine:
                        studentInformation['Spec'] = "Interaction"
                        specializationFound = True
                    elif "Game" in modifiedLine:
                        studentInformation['Spec'] = "Game"
                        specializationFound = True
                    elif "Security" in modifiedLine:
                        studentInformation['Spec'] = "Security"
                        specializationFound = True
                    elif "System" in modifiedLine:
                        studentInformation['Spec'] = "System"
                        specializationFound = True
                elif studentInformation['Major'] == "ISE" and "Specialization" in modifiedLine: # We are looking at a specialization
                    if "Network" in modifiedLine:
                        studentInformation['Spec'] = "Network"
                        specializationFound = True
                    elif "Health" in modifiedLine:
                        studentInformation['Spec'] = "Health"
                        specializationFound = True
                    elif "Economics" in modifiedLine:
                        studentInformation['Spec'] = "Economics"
                        specializationFound = True
                    elif "Technological" in modifiedLine:
                        studentInformation['Spec'] = "Technological"
                        specializationFound = True
                    elif "Financial" in modifiedLine:
                        studentInformation['Spec'] = "Financial"
                        specializationFound = True
            iterate_through_splice_counter += 1 # Go to the next index          
        else: # Index is out of range OR the we found the specialization
            if majorFound == True and specializationFound == True:
                break # We found specialization for both CSE and ISE 
            elif majorFound == True and specializationFound == False: # Major found but specialization is not found
                if studentInformation['Major'] == "ISE": 
                    if currentPage == afterCurrent: 
                        break # This means specialization was not found at all and also implies that the line was not cut-off
                    else: # The specialization might have been cut-off, so we need to find it 
                        specializationFoundRetry = False 
                        indexOfNextSemester = -1 
                        for lineOfInfo in afterCurrent:
                            if indexOfNextSemester == -1:
                                modifiedLine = lineOfInfo.replace(" ", "")
                                if "Spring" in modifiedLine:
                                    if modifiedLine[6:10].isdigit(): indexOfNextSemester = afterCurrent.index(lineOfInfo)
                                elif "Summer" in modifiedLine:
                                    if modifiedLine[6:10].isdigit(): indexOfNextSemester = afterCurrent.index(lineOfInfo)
                                elif "Winter" in modifiedLine:
                                    if modifiedLine[6:10].isdigit(): indexOfNextSemester = afterCurrent.index(lineOfInfo)
                                elif "Fall" in modifiedLine:
                                    if modifiedLine[4:8].isdigit(): indexOfNextSemester = afterCurrent.index(lineOfInfo)
                                elif "End" in modifiedLine: indexOfNextSemester = afterCurrent.index(lineOfInfo)
                        if indexOfNextSemester != -1: 
                                second_list_counter = 0
                                before_next_sem_list = afterCurrent[:indexOfNextSemester] # We dont include the next semester
                                while True:
                                    if second_list_counter >= 0 and second_list_counter < len(before_next_sem_list) and specializationFoundRetry == False:
                                        grabLine = before_next_sem_list[second_list_counter]
                                        if "Plan" in grabLine and "Specialization" in grabLine:
                                            modifiedLine = grabLine.replace("Plan", "").replace(" ", "")
                                            if "Network" in modifiedLine:
                                                studentInformation['Spec'] = "Network"
                                                specializationFoundRetry = True
                                            elif "Health" in modifiedLine:
                                                studentInformation['Spec'] = "Health"
                                                specializationFoundRetry = True
                                            elif "Economics" in modifiedLine:
                                                studentInformation['Spec'] = "Economics"
                                                specializationFoundRetry = True
                                            elif "Technological" in modifiedLine:
                                                studentInformation['Spec'] = "Technological"
                                                specializationFoundRetry = True
                                            elif "Financial" in modifiedLine:
                                                studentInformation['Spec'] = "Financial"
                                                specializationFoundRetry = True
                                        second_list_counter += 1
                                    else:
                                        parsingPlanBool = True # Set this to true so we can escape the outer while loop
                                        break # Break from the inner while loop
                        else: break # Also no luck, we only found major, no specialization
                elif studentInformation['Major'] == "CSE": break # We might want to add more here so we come back l
            elif majorFound == False: # Major info was maybe cut-off and thus, the specialization might have also been cut-off
                specializationFoundRetry = False
                indexOfNextSemester = -1
                for lineOfInfo in afterCurrent: # Iterate through the entire list to find 
                    if indexOfNextSemester == -1:
                        modifiedLine = lineOfInfo.replace(" ", "")
                        if "Spring" in modifiedLine:
                            if modifiedLine[6:10].isdigit(): indexOfNextSemester = afterCurrent.index(lineOfInfo)
                        elif "Summer" in modifiedLine:
                            if modifiedLine[6:10].isdigit(): indexOfNextSemester = afterCurrent.index(lineOfInfo)
                        elif "Winter" in modifiedLine:
                            if modifiedLine[6:10].isdigit(): indexOfNextSemester = afterCurrent.index(lineOfInfo)
                        elif "Fall" in modifiedLine:
                            if modifiedLine[4:8].isdigit(): indexOfNextSemester = afterCurrent.index(lineOfInfo)
                        elif "End" in modifiedLine: indexOfNextSemester = afterCurrent.index(lineOfInfo)
                if indexOfNextSemester != -1: # Check to see if an index was found 
                        majorFoundRetry = False 
                        second_list_counter = 0
                        before_next_sem_list = afterCurrent[:indexOfNextSemester] # We dont include the next semester
                        specializationFoundRetry = False 
                        while True:
                            if second_list_counter >= 0 and second_list_counter < len(before_next_sem_list) and specializationFoundRetry == False:
                                grabLine = before_next_sem_list[second_list_counter]
                                modifiedLine = grabLine.replace("Plan", "").replace(" ", "")
                                if "Plan" in modifiedLine and majorFoundRetry == False:
                                    if "ComputerScience" in modifiedLine and "Major" in modifiedLine:
                                        studentInformation['Major'] = "CSE"
                                        majorFoundRetry = True
                                    elif "InformationSystems" in modifiedLine and "Major" in modifiedLine:
                                        studentInformation['Major'] = "ISE"
                                        majorFoundRetry = True
                                elif "Plan" in modifiedLine and majorFoundRetry == True:
                                        modifiedLine = grabLine.replace("Plan", "").replace(" ", "")
                                        if studentInformation['Major'] == "CSE" and "Specialization" in modifiedLine: # We are looking at a specialization
                                            if "Artificial" in modifiedLine:
                                                studentInformation['Spec'] = "Artificial"
                                                specializationFoundRetry = True
                                            elif "Interaction" in modifiedLine:
                                                studentInformation['Spec'] = "Interaction"
                                                specializationFoundRetry = True
                                            elif "Game" in modifiedLine:
                                                studentInformation['Spec'] = "Game"
                                                specializationFoundRetry = True
                                            elif "Security" in modifiedLine:
                                                studentInformation['Spec'] = "Security"
                                                specializationFoundRetry = True
                                            elif "System" in modifiedLine:
                                                studentInformation['Spec'] = "System"
                                                specializationFoundRetry = True
                                        elif studentInformation['Major'] == "ISE" and "Specialization" in modifiedLine: # We are looking at a specialization
                                            if "Network" in modifiedLine:
                                                studentInformation['Spec'] = "Network"
                                                specializationFoundRetry = True
                                            elif "Health" in modifiedLine:
                                                studentInformation['Spec'] = "Health"
                                                specializationFoundRetry = True
                                            elif "Economics" in modifiedLine:
                                                studentInformation['Spec'] = "Economics"
                                                specializationFoundRetry = True
                                            elif "Technological" in modifiedLine:
                                                studentInformation['Spec'] = "Technological"
                                                specializationFoundRetry = True
                                            elif "Financial" in modifiedLine:
                                                studentInformation['Spec'] = "Financial"
                                                specializationFoundRetry = True
                                second_list_counter += 1 # Increase the list incrementor
                            else:
                                parsingPlanBool = True
                                break                  
                else: break # No major and no specialization                                    
    return True # The boolean type does not matter as its either we dont get a specialization or we do (same applies for major)
