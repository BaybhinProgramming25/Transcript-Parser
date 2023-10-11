"""
This is the primary module that will tackle different parts of the transcript

Each thread is responsible for calling a specific function in this module
and each function will be responsible for parsing specific information
and store it in the state variables that are passed 
"""

from classes.UniversalClassObject import *
from classes.MinimalClassObject import *
from classes.SBCClassObject import * 


def majorClassTracker(text: list[str], studentInformation: dict, upperDivisionCourses: dict, lowerDivisionCourses: dict, technicalCourses: dict, specializeRequiredCourses: dict, specalizeOptionalCourses: dict, mathRequiredCourses: dict):

    requiredLowerDivisonCourses, requiredUpperDivisionCourses = (), ()
    alternateRequiredCourses, PSYCSECourses, ISEcoursestreatedasCSE, ESTcoursestreatedasCSE, MATcoursesttreatedasCSE, AMScoursestreatedasCSE = {}, {}, {}, {}, {}, {}

    # Probaby want to define my constants somewhere else so we will come back here later 
    if studentInformation['Major'] == "CSE": # CSE Student

        requiredLowerDivisonCourses = ("114", "214", "215", "216", "220")
        requiredUpperDivisionCourses = ("303", "312", "300", "310", "316", "320", "373", "416")

        # We need to consider these following courses 
        PSYCSECourses = ("260", "366", "368", "369", "384") 
        ISEcoursestreatedasCSE = ("300", "301", "311", "312", "323", "332", "333", "334", "337", "364") 
        ESTcoursestreatedasCSE = ("323")
        MATcoursesttreatedasCSE = ("371", "373")
        AMScoursestreatedasCSE = ("345")

    else: # ISE Student

        requiredLowerDivisonCourses = ("114", "214", "218")
        requiredUpperDivisionCourses = ("300", "305", "316", "320" "312") 

        alternateRequiredCourses =  {
            "CSE": ("215", "311", "331", "323", "337", "370", "377"), # Courses for the ISE specializations
            "BUS": ("215", "220", "294", "330", "331", "346", "348", "353", "355", "356", "393"), 
            "ECO": ("108", "326", "327", "345", "348", "389"), 
            "ESE": ("201", "442"), 
            "ACC": ("210", "214"), 
            "EST": ("201", "202", "304", "305", "310", "320", "323", "325", "326", "327", "364", "391", "392", "393", "421"), 
            "POL": ("319", "359", "364"), 
            "SOC": ("381"), 
            "ISE": ("311", "321", "323", "331", "337", "340", "390", "391", "475", "488"),
            "AMS": ("311", "315", "316", "318", "320", "341", "394", "441"),
            "HAN": ("200", "202"),
            "PSY": ("103"),
            "BME": ("205"),
            "BCP": ("405"),
            "BIO": ("201", "203")
        }

    # Begin parsing     
    semesterText, semesterYear = "", ""
    list_of_seasons = ["Spring", "Summer", "Winter", "Fall"]

    for lineOfInformation in text:

        modifiedLine = lineOfInformation.replace(" ", "")

        if "TermGPA" in modifiedLine: semesterText, semesterYear = "", ""
        
        if not semesterText and not semesterYear:
            for season in list_of_seasons:
                if season in modifiedLine and "Session" in modifiedLine:
                    semesterText = season 
                    requirement_term_string = studentInformation['Requirement Term']
                    requirement_term_year = requirement_term_string[requirement_term_string.index(' ')+1:]

                    for _ in range(1, 11, 1): # We run this loop 10 times to check if one of the years exist
                        if requirement_term_year in modifiedLine:
                            semesterYear = requirement_term_year
                        else:
                            requirement_term_year = str(int(requirement_term_year) + 1)
                
        if "CSE" in modifiedLine and studentInformation['Major'] == "CSE":

            classNumber = modifiedLine[3:6]

            uncounted_courses = ["301", "475", "495", "496"]
            possibly_counted = ["487", "488"]

            if classNumber.isdigit(): 

                if classNumber == "101": continue # We do not count this 

                elif classNumber in requiredLowerDivisonCourses:
                    createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, lowerDivisionCourses)
                elif classNumber in requiredUpperDivisionCourses:
                    createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, upperDivisionCourses)
                else: 
                    if (classNumber in uncounted_courses) or (classNumber in possibly_counted and classNumber in technicalCourses): continue 
                    createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, technicalCourses) 

        elif "CSE" not in modifiedLine and studentInformation['Major'] == "CSE": # Note: We don't allow ALL ISE courses as CSE technical electives
            
            classDescription = modifiedLine[0:3]
            classNumber = modifiedLine[3:6]

            if classDescription == "PSY": # We are most probably looking at a PSY course 
                if classNumber.isdigit() and classNumber in PSYCSECourses:
                        createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, specalizeOptionalCourses)
            

            elif classDescription == "ISE":
                if classNumber.isdigit() and classNumber in ISEcoursestreatedasCSE:
                        if classNumber == "300" or classNumber == "312":
                            createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, upperDivisionCourses) 
                        elif classNumber != "301": # Don't count "CSE/ISE 301 as a technical course"
                            createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, technicalCourses)

            elif classDescription == "EST":
                if classNumber.isdigit() and classNumber in ESTcoursestreatedasCSE:
                    if classNumber in tupleClass:
                        createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, technicalCourses)
       
            elif classDescription == "MAT":
                if classNumber.isdigit() and classNumber in MATcoursesttreatedasCSE:
                        if classNumber == "373":
                            createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, upperDivisionCourses)
                        else:
                            createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, technicalCourses)
 
            elif classDescription == "AMS":
                if classNumber.isdigit() and classNumber in AMScoursestreatedasCSE:
                    if classNumber in tupleClass:
                        createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, technicalCourses)
  

        elif "ISE" in modifiedLine and studentInformation['Major'] == "ISE": # Need to also check if the class is part of a specalization or not
           
            technical, specalization = False, False 

            classTitle = "ISE"
            classNumber = modifiedLine[3:6]

            possibly_counted = ["475", "488"]

            if classNumber.isdigit(): # Might need to make some modifications here cause stuff might be incorrect 
                if classNumber in requiredLowerDivisonCourses or classNumber in requiredUpperDivisionCourses:
                    createClassObjectForISE(semesterText, semesterYear, modifiedLine, classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                else: # Looks for both ISE electives (ISE 3xx) AND ISE specalization courses, so we need to handle both cases where they are
                    if classNumber in possibly_counted and classNumber in technicalCourses: continue 

                    getTuple = alternateRequiredCourses[classTitle]

                    if classNumber in getTuple: technical, specalization = True, True 
                    else: technical, specalization = True, False 

                    createClassObjectForISE(semesterText, semesterYear, modifiedLine, classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
    

        elif "ISE" not in modifiedLine and studentInformation['Major'] == "ISE": # Need to consider a lot for ISE students
    
            technical, specalization = False, False 
            classTitle = modifiedLine[0:3]
            classNumber = modifiedLine[3:6]

            if classTitle in alternateRequiredCourses:

                if classNumber.isdigit():

                    if classNumber in requiredLowerDivisonCourses: # Handles the case for CSE 114 and CSE 214
                        specalization = False if "215" not in modifiedLine else True 
                        createClassObjectForISE(semesterText, semesterYear, modifiedLine, classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                    
                    else: 
                        tupleClass = alternateRequiredCourses[classDescription]

                        if classNumber in tupleClass: # We are looking at a specialization class 
                            if classTitle == "EST" and classNumber == "323": # Counts as CSE/ISE/EST 323 so also an technical course
                                specalization, technical = True, True
                            elif classTitle == "CSE" and int(classNumber) >= 300: # All upper 300 counts as technical as well
                                specalization, technical = True, True
                            else:
                                specalization, technical = True, False 
                            createClassObjectForISE(semesterText, semesterYear, modifiedLine, classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)

                        else: # Then we are most likely looking at a technical elective for ISE (only CSE and ISE classes are allowed)
                            
                            if classTitle == "CSE":

                                if classNumber == "300": # CSE/ISE 300
                                    specalization, technical = False, False # Required Course
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine, "ISE", classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                                elif classNumber == "312": # CSE/ISE 312
                                    classNumber = "312"
                                    specalization, technical = False, False # Required Course
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine, "ISE", classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                                elif classNumber == "310": # CSE 310
                                    specalization, technical = False, False # Required Course
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine, "ISE", "316", lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                                else:
                                    specalization, technical = False, True # Only a CSE technical course
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine, classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                            else:

                                if classTitle == "EST": 
                                    if classNumber == "340" or classNumber == "339": # EST 340 an EST 339 count as ISE technical electives as they are also offered as ISE 340 and ISE 339
                                        specalization, technical = False, True # This is considered to be a technical elective
                            
                                elif classTitle == "BUS":
                                    if classNumber == "340": # Required Course
                                        specalization, technical = False, False
                            
                                elif classTitle == "POL":
                                    if classNumber == "369":
                                        specalization, technical = False, True # Offered as ISE 369 as well

                                createClassObjectForISE(semesterText, semesterYear, modifiedLine[3::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)

        
# Thread calls to track the math courses 
def mathTracker(text: list[str], studentInformation: dict, mathRequiredCourses: dict):

    list_of_seasons = ["Spring", "Summer", "Winter", "Fall"]

    semesterText = ""
    semesterYear = ""

    for lineOfInformation in text:

        modifiedLine = lineOfInformation.replace(" ", "")

        if "CumGPA" in modifiedLine or "TestTransGPA" in modifiedLine: semesterText, semesterYear = "", ""

        if not semesterText and not semesterYear:
            for season in list_of_seasons:
                if season in modifiedLine and "Session" in modifiedLine:
                    semesterText = season 
                    requirement_term_string = studentInformation['Requirement Term']
                    requirement_term_year = requirement_term_string[requirement_term_string.index(' ')+1:]

                    for _ in range(1, 11, 1): # We run this loop 10 times to check if one of the years exist
                        if requirement_term_year in modifiedLine:
                            semesterYear = requirement_term_year
                        else:
                            requirement_term_year = str(int(requirement_term_year) + 1)

        possible_math_courses = ["AMS", "MAT"]    

        for math_course in possible_math_courses:
            if math_course in modifiedLine:
                classNumber = modifiedLine[3:6]
                if classNumber.isdigit():
                    createClassObjectForMathCourses(math_course, semesterText, semesterYear, modifiedLine, classNumber, mathRequiredCourses)
    

# Thread calls to track the science courses 
def scienceTracker(text: list[str], studentInformation: dict, scienceCourses: dict):

    semesterText, semesterYear = "", ""

    list_of_seasons = ["Spring", "Summer", "Winter", "Fall"]

    for lineOfInformation in text:

        modifiedLine = lineOfInformation.replace(" ", "")
        
        if "CumGPA" in modifiedLine: semesterText, semesterYear = "", "" # Reset the semesterText and semesterYear strings 

        if not semesterText and not semesterYear:        
            for season in list_of_seasons:
                if season in modifiedLine and "Session" in modifiedLine:
                    semesterText = season 
                    requirement_term_string = studentInformation['Requirement Term']
                    requirement_term_year = requirement_term_string[requirement_term_string.index(' ')+1:]

                    for _ in range(1, 11, 1): # We run this loop 10 times to check if one of the years exist
                        if requirement_term_year in modifiedLine:
                            semesterYear = requirement_term_year
                        else:
                            requirement_term_year = str(int(requirement_term_year) + 1)
        
        possible_science_courses = ["PHY", "BIO", "CHE", "GEO", "AST"]

        for science_course in possible_science_courses:
            if science_course in modifiedLine:
                classNumber = modifiedLine[3:6]
                if classNumber.isdigit():
                    createClassObjectForScienceCourses(science_course, semesterText, semesterYear, modifiedLine, classNumber, scienceCourses)

# A thread calls this function in order to find and store any SBCs that satisfy the CSE and ISE SBCs requirement
def sbcsTracker(text: list[str], studentInformation: dict, sbcCourses: dict):

    transferEquivalency = {('AFS', 'ECO', 'POL', 'HIS', 'PSY'): 'SBS', ('AFS', 'HIS', 'POL'): 'USA', ('AFS', 'PSY'): 'CER', ('ARH', 'ARS', 'MUS'): 'ARTS', ('BIO', 'CHE', 'SUS', 'PHY'): 'SNW', ('MAT', 'AMS'): 'QPS', ('CHI', 'FRN', 'GER', 'ITL', 'JPN', 'LAT', 'SPN'): 'LANG', ('CHI', 'FRN', 'GER', 'HIS', 'ITL', 'JPN', 'SPN'): 'GLO', ('CHI', 'EGL', 'FRN', 'GER', 'ITL', 'JPN', 'SPN'): 'HUM', ('CSE'): 'TECH', ('LAT'): 'HFA+'}
    
    # We can have a separate loop that will handle test credits 
    line_counter = 0
    keepSkipping, keepSkippingSecond = False, False

    beginning_seen = studentInformation.get('Beginning SBCTracker')

    if beginning_seen is None: 
        studentInformation['Beginning SBCTracker'] = False 
        beginning_seen = False 

    while not beginning_seen: 

        test_credits_line = text[line_counter].replace(" ", "")
    
        if "Beginning" in test_credits_line: # We are at the actual 
            studentInformation['Beginning SBCTracker'] = True 
            break 

        if "TestCredits" in test_credits_line and not keepSkipping:
            listAfterwards = text[line_counter::]
            line_counter += handleTestCreditsSbcs(listAfterwards, sbcCourses, transferEquivalency) 
            keepSkipping = True

        if "TransferCredit" in test_credits_line and not keepSkippingSecond:
            listAfterwards = text[line_counter::]
            line_counter += handleTestCreditsSbcs(listAfterwards, sbcCourses, transferEquivalency)
            keepSkippingSecond = True 
        else:
            line_counter += 1
    
    # This loop will handle normal semester information 
    semesterText, semesterYear = "", ""
    class_found = False 
    list_of_seasons = ["Spring", "Summer", "Winter", "Fall"]
    sbc_possibilities = ["EXP+", "HFA+", "SBS+", "STEM+", "ARTS", "GLO", "HUM", "LANG", "QPS", "SBS", "SNW", "TECH", "USA", "WRT", "STAS", "CER", "DIV", "ESI", "SPK", "WRTD"]
    class_reference = ""

    new_text = text[line_counter::]
    new_counter = 0 

    classDescription = ""
    classNumber = ""

    while new_counter < len(new_text):

        modifiedLine = new_text[new_counter].replace(" ", "")
        
        if "CumGPA" in modifiedLine: semesterText, semesterYear = "", "" # Reset the strings

        if not semesterText and not semesterYear:
            for season in list_of_seasons:
                    if season in modifiedLine and "Session" in modifiedLine:
                        semesterText = season 
                        requirement_term_string = studentInformation['Requirement Term']
                        requirement_term_year = requirement_term_string[requirement_term_string.index(' ')+1:]

                        for _ in range(1, 11, 1): # We run this loop 10 times to check if one of the years exist
                            if requirement_term_year in modifiedLine:
                                semesterYear = requirement_term_year
                            else:
                                requirement_term_year = str(int(requirement_term_year) + 1) 
        
        if modifiedLine[3:6].isdigit() and not class_found:

            classDescription = modifiedLine[0:3]
            classNumber = modifiedLine[3:6]
            class_reference = modifiedLine # Keep a reference to the class we are going to parse 
            new_counter += 1

            # Search for Course Attributes line 
            temp_counter = new_counter
            class_found = False 
            while not new_text[temp_counter].replace(" ", "")[3:6].isdigit() and not "CumGPA" in new_text[temp_counter].replace(" ", ""):
                if "CourseAttributes" in new_text[temp_counter].replace(" ", ""):
                    class_found = True 
                    break 
                temp_counter += 1
    
        elif "CourseAttributes" in modifiedLine and class_found:
            # Parse the attirbutes until we have reached another class 
            parse_attributes_list = new_text[new_counter::]

            attributes_counter = 0
            sbcs_list = [] # Keep a list of the class

            while True: 

                possible_attribute_line = parse_attributes_list[attributes_counter].replace(" ", "")
                possible_class_number = possible_attribute_line[3:6]

                if possible_class_number.isdigit() or "CumGPA" in possible_attribute_line: # We have found the next class
                    
                    if len(sbcs_list) > 0: createClassObjectForSBCCourses(classDescription, sbcs_list, semesterText, semesterYear, class_reference, classNumber, sbcCourses)
                    class_reference = ""
                    class_found = False # Reset the variable 
                    new_counter += attributes_counter - 1
                    break 
                else: # We are possibly looking at a SBC class 
                    for sbc_item in sbc_possibilities:
                        if sbc_item in possible_attribute_line:
                            sbcs_list.append(sbc_item) 
                            break 
                    attributes_counter += 1
        else: new_counter += 1    

            
# A thread calls this function in order to keep track of the classes taken by the student per semester
def classTracker(text: list[str], studentInformation: dict,  classesPerSemester: dict): #Responsible for keeping a dictionary of what classes the student is taking per semester

    transferEquivalency = {('AFS', 'ECO', 'POL', 'HIS', 'PSY'): 'SBS', ('AFS', 'HIS', 'POL'): 'USA', ('AFS', 'PSY'): 'CER', ('ARH', 'ARS', 'MUS'): 'ARTS', ('BIO', 'CHE', 'SUS', 'PHY'): 'SNW', ('MAT', 'AMS'): 'QPS', ('CHI', 'FRN', 'GER', 'ITL', 'JPN', 'LAT', 'SPN'): 'LANG', ('CHI', 'FRN', 'GER', 'HIS', 'ITL', 'JPN', 'SPN'): 'GLO', ('CHI', 'EGL', 'FRN', 'GER', 'ITL', 'JPN', 'SPN'): 'HUM', ('CSE'): 'TECH', ('LAT'): 'HFA+'}

    beginning_seen = studentInformation.get('Beginning NormalTracker')

    if beginning_seen is None: 
        studentInformation['Beginning NormalTracker'] = False 
        beginning_seen = False 

    line_counter = 0
    keepSkipping, keepSkippingSecond = False, False # The second variable is going to be used for the transfer credit from other colleges

    while not beginning_seen: 

        test_credits_line = text[line_counter].replace(" ", "")
    
        if "Beginning" in test_credits_line: # We are at the actual 
            studentInformation['Beginning NormalTracker'] = True 
            break 

        if "TestCredits" in test_credits_line and not keepSkipping:
            listAfterwards = text[line_counter::]
            line_counter += handleTestCreditsNormal(listAfterwards, classesPerSemester, transferEquivalency) 
            keepSkipping = True

        if "TransferCredit" in test_credits_line and not keepSkippingSecond:
            listAfterwards = text[line_counter::]
            line_counter += handleTestCreditsNormal(listAfterwards, classesPerSemester, transferEquivalency)
            keepSkippingSecond = True 
        else:
            line_counter += 1

    list_of_seasons = ["Spring", "Summer", "Winter", "Fall"]
    
    new_text = text[line_counter::]
    new_counter = 0 

    semesterText, semesterYear = "", ""

    while new_counter < len(new_text):

        modified_line = new_text[new_counter].replace(" ", "")

        if "CumGPA" in modified_line: semesterText, semesterYear = "", "" 
        
        
        if not semesterText and not semesterYear:
            for season in list_of_seasons:
                if season in modified_line and "Session" in modified_line:
                    semesterText = season 
                    requirement_term_string = studentInformation['Requirement Term']
                    requirement_term_year = requirement_term_string[requirement_term_string.index(' ')+1:]

                    for _ in range(1, 11, 1): # We run this loop 10 times to check if one of the years exist
                        if requirement_term_year in modified_line:
                            semesterYear = requirement_term_year
                        else:
                            requirement_term_year = str(int(requirement_term_year) + 1)

        if modified_line[3:6].isdigit(): createClassInformation(modified_line[0:3], modified_line[3:6], semesterText, semesterYear, modified_line, classesPerSemester)
        new_counter += 1


# This function creates an object for a CSE course
@staticmethod
def createClassObjetctForCSE(semesterText: str, semesterYear: str, modifiedLine: str, classNumber: str, courseDictionary: dict):

    dictInformation = parseSpecificClassInformation(modifiedLine)

    dict_cross_over = {('300', '301', '311', '312', '332', '333', '334', '337', '364'): 'CSE/ISE', ('371', '373'): 'CSE/MAT', ('345'): 'CSE 355/AMS 345', ('323'): 'CSE/ISE/EST'}
   
    # Lower Division Classes
    if int(classNumber) < 300:

        courseName = f'CSE {classNumber}' 
        lowerDivisionObject = UniversalClassObject(courseName, dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        courseDictionary[courseName] = lowerDivisionObject

    # Upper Division Classes and possibly any cross over classes 
    elif int(classNumber) >= 300:

        # Go through our dictionary cross over
        courseName = f'CSE {classNumber}'
        for tuple_section in dict_cross_over.keys():
            for class_number in tuple_section:
                if class_number == classNumber:
                    courseName = f'{dict_cross_over.get(tuple_section)} {classNumber}' if class_number != '345' else dict_cross_over.get(tuple_section)

        upperDivisonObject = UniversalClassObject(courseName, dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        courseDictionary[courseName] = upperDivisonObject

# This function creates an object for an ISE course
@staticmethod
def createClassObjectForISE(semesterText: str, semesterYear: str, modifiedLine: str, classTitle: str, classNumber: str, lowerDivisionCourses: dict, upperDivisionCourses: dict, technicalCourses: dict, specializeRequiredCourses: dict, mathRequiredCourses: dict, specBool: bool, techBool: bool): 

    dictInformation = parseSpecificClassInformation(modifiedLine)

    dict_cross_over = {('300', '301', '311', '312', '332', '333', '334', '337', '364'): 'CSE/ISE', ('339'): 'ISE/EST', ('310','340'): 'ISE 340/EST 310', ('369'): 'ISE/POL', ('323'): 'CSE/ISE/EST'}

    if int(classNumber) < 300: # Lower division courses cant be considered electives, as they are required to be 300+ courses

        lowerDivisionObject = UniversalClassObject(f'{classTitle} {classNumber}', dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        courseName = lowerDivisionObject.courseName

        if specBool:
            specializeRequiredCourses[courseName], mathRequiredCourses[courseName] = lowerDivisionObject, lowerDivisionObject
        else:
            lowerDivisionCourses[courseName] = lowerDivisionObject


    elif int(classNumber) >= 300: 

        courseName = f'{classTitle} {classNumber}'
        for tuple_section in dict_cross_over.keys():
            for class_number in tuple_section:
                if class_number == classNumber:
                    courseName = f'{dict_cross_over.get(tuple_section)} {classNumber}' if f'{classTitle} {classNumber}' != "EST 310" and f'{classTitle} {classNumber}' != "ISE 340" else dict_cross_over.get(tuple_section)


        upperDivisionObject = UniversalClassObject(courseName, dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        courseName = upperDivisionObject.courseName
    
        # Handle different ISE possibilities 
        if specBool and techBool:
            specializeRequiredCourses[courseName], technicalCourses[courseName] = upperDivisionObject, upperDivisionObject
        elif specBool and not techBool:
            specializeRequiredCourses[courseName] = upperDivisionObject
        elif not specBool and techBool:
            technicalCourses[courseName] = upperDivisionObject
        else: 
            upperDivisionCourses[courseName] = upperDivisionObject # Required Course 
    
# This function is responsible for handling SBCs that are satisfied for courses that the student
# took before their undergraduate record at SBU started
@staticmethod
def handleTestCreditsSbcs(text: list[str], sbcCourses: dict, transferEquivalency: dict) -> int:

    semesterText, semesterYear = "Transfer", "Credits"

    for index, lineOfInformation in enumerate(text):

        modifiedLine = lineOfInformation.replace(" ", "")

        if "TestTransGPA" in modifiedLine or "Beginning" in modifiedLine: 
            return index

        classTitle, classNumber = modifiedLine[0:3], modifiedLine[3:6]

        list_of_keys = transferEquivalency.keys()
        list_of_sbcs = []

        for keys in list_of_keys:
            if classTitle in keys:
                getSBCValue = transferEquivalency[keys]
                list_of_sbcs.append(getSBCValue)

        if len(list_of_sbcs) > 0: createClassObjectForSBCCourses(classTitle, list_of_sbcs, semesterText, semesterYear, modifiedLine, classNumber, sbcCourses)
 

# Handles Test Credits prior to official first semester of the student 
@staticmethod 
def handleTestCreditsNormal(text: list[str], classesPerSemester: dict, transferEquivalency: dict) -> int: # To Handle Any Transfer Credits 

    semesterText, semesterYear = "Transfer", "Credits"

    for index, lineOfInformation in enumerate(text):

        modifiedLine = lineOfInformation.replace(" ", "")

        if "TestTransGPA" in modifiedLine or "Beginning" in modifiedLine: 
            return index 
  
        if modifiedLine[3:6].isdigit():
            createClassInformation(modifiedLine[0:3], modifiedLine[3:6], semesterText, semesterYear, modifiedLine, classesPerSemester)
        else: 
            if modifiedLine[3:6] == "LVL":

                classTitle = modifiedLine[0:3]
                grabLevel = modifiedLine[6]
                createClassInformation(classTitle, f'LVL{str(grabLevel)}', semesterText, semesterYear, modifiedLine, classesPerSemester)
            else:
                classTitle = modifiedLine[0:3]
                list_of_keys = transferEquivalency.keys()
                for keys in list_of_keys:
                    if modifiedLine[0:3] in keys: 
                        grabSBCValue = transferEquivalency[keys]
                        createClassInformation(classTitle, grabSBCValue, semesterText, semesterYear, modifiedLine, classesPerSemester)


# This function makes a call to parse specific information about a particular class (any class), creates an object after parsing 
# is finished and stores the Object in the state variable
@staticmethod
def createClassInformation(classTitle: str, classNumber: str, semesterText: str, semesterYear: str,  modifiedLine: str, classesPerSemester: dict):
    
    dictInformation = parseSpecificClassInformation(modifiedLine)

    ClassObject = SimpleClassObject(f'{classTitle} {classNumber}', dictInformation['classCreditsAmount'], dictInformation['classGrade'], semesterText, semesterYear)
        
    if (f'{semesterText} {semesterYear}') in classesPerSemester:
        getList = classesPerSemester[f'{semesterText} {semesterYear}']
        getList.append(ClassObject)
    else: # Does not exist, so we create a list for that particular semester
        listOfClassesInSemester = []
        listOfClassesInSemester.append(ClassObject)
        classesPerSemester[f'{semesterText} {semesterYear}'] = listOfClassesInSemester
    
# This function makes a call to parse specific information about a particular math class, creates an object after parsing 
# is finished and stores the Object in the state variable
@staticmethod
def createClassObjectForMathCourses(classTitle: str, semesterText: str, semesterYear: str, modifiedLine: str, classNumber: str, mathRequiredCourses: dict):
    dictInformation = parseSpecificClassInformation(modifiedLine)
    MathObject = UniversalClassObject(f'{classTitle} {classNumber}', dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
    mathRequiredCourses[f'{classTitle} {classNumber}'] = MathObject

# This function makes a call to parse specific information about a particular science class, creates an object after parsing 
# is finished and stores the Object in the state variable
@staticmethod
def createClassObjectForScienceCourses(classTitle: str, semesterText: str, semesterYear: str, modifiedLine: str, classNumber: str, scienceCourses: dict):
    dictInformation = parseSpecificClassInformation(modifiedLine)
    ScienceObject = UniversalClassObject(f'{classTitle} {classNumber}' + " (SNW)" if int(classNumber) in [132, 131, 141, 152, 201, 102, 103, 122, 125, 127, 142] else (classTitle + " " + classNumber if int(classNumber) in [133, 204, 154, 322, 332, 112, 113, 134, 252] else classTitle + classNumber + " (STEM+)"), dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
    scienceCourses[f'{classTitle} {classNumber}'] = ScienceObject 

# This function makes a call to parse specific information about a particular class with an SBC, creates an object after parsing 
# is finished and stores the Object in the state variable
@staticmethod
def createClassObjectForSBCCourses(classTitle: str, sbcLabel: list[str], semesterText: str, semesterYear: str, modifiedLine: str, classNumber: str, sbcCourses: dict):
    dictInformation = parseSpecificClassInformation(modifiedLine)
    SBCObject = SBCCourse(sbcLabel, f'{classTitle} {classNumber}', dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
    sbcCourses[f'{classTitle} {classNumber}'] = SBCObject


# We parse the specific class information 
@staticmethod
def parseSpecificClassInformation(modifiedLine: str) -> dict:

    possible_letters = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'F': 'F', 'S': 'S', 'U': 'U', 'T': 'XFER', 'P': 'P', 'I': 'I', 'W': 'W', 'Q': 'Q', 'NC': 'NC', 'NR': 'NR', 'R': 'R'}
    comment_grades = ['I', 'W', 'Q', 'NC', 'NR', 'R']
    plus_or_minus = ["+", "-"]

    classDescription, classNumber = modifiedLine[0:3], modifiedLine[3:6]

    strip_class_info = modifiedLine.replace(classDescription, "").replace(classNumber, "")

    # Look for the index 
    credits_location = -1
    for index, character in enumerate(strip_class_info):
        if character == '.':
            credits_location = index - 1
            break 
    
    # Parse the credits amount 
    credits_amount = ""
    while len(credits_amount) != 5:
        credits_amount += strip_class_info[credits_location]
        credits_location += 1
    
    # Parse the class grade and the class comments 
    new_info = strip_class_info[strip_class_info.index(credits_amount)::]
    class_grade = ""
    class_comments = ""
    for grade in list(possible_letters.keys()):
        if grade in new_info:
            class_grade = possible_letters.get(grade)
            for symbol in plus_or_minus:
                if symbol in new_info:
                    class_grade += symbol 
            if grade in comment_grades:
                class_comments = class_grade 
    
    return {'classCreditsAmount': credits_amount, 'classGrade': class_grade, 'classComments': class_comments}