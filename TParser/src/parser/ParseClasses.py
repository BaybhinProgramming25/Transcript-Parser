"""

This is the primary module that will tackle different parts of the transcript

Each thread is responsible for calling a specific function in this module
and each function will be responsible for parsing specific information
and store it in the state variables that are passed 

"""

from classes.UniversalClassObject import *
from classes.MinimalClassObject import *
from classes.SBCClassObject import * 
import sys


# The purpose of this function is to list the required major courses (i.e lower division courses, upper division courses, and technical courses) and to see if the student has satisfied
# any particular major require course. If a student has a major required course, then that particular course is put into state dictionary
# in the form of an Object 
def majorClassTracker(text, studentInformation, upperDivisionCourses, lowerDivisionCourses, technicalCourses, specializeRequiredCourses, specalizeOptionalCourses, mathRequiredCourses):

    # We want our dictionary to hold UpperDivision class objects in the upperDivisonCourse dictionary
    # and we want our dictionary to hold LowerDivision class objects in the lowerDivisonCourses dictionary

    requiredLowerDivisonCourses, requiredUpperDivisionCourses, alternateRequiredCourses, alternateOptionalCourses, ISEcoursestreatedasCSE, ESTcoursestreatedasCSE, MATcoursesttreatedasCSE, AMScoursestreatedasCSE = (), (), {}, {}, {}, {}, {}, {}

    if studentInformation['Major'] == "CSE": # We are looking at a CSE student

        requiredLowerDivisonCourses = ("114", "214", "215", "216", "220")
        requiredUpperDivisionCourses = ("303", "312", "300", "310", "316", "320", "373", "416")
        alternateOptionalCourses = {"PSY": ("260", "366", "368", "369", "384")} # Optional Specialization Courses
        ISEcoursestreatedasCSE = {"ISE": ("300", "301", "311", "312", "323", "332", "333", "334", "337", "364")} # So that these ISE courses can also be used as elective credit
        ESTcoursestreatedasCSE = {"EST": ("323")}
        MATcoursesttreatedasCSE = {"MAT": ("371", "373")}
        AMScoursestreatedasCSE = {"AMS": ("345")}


    elif studentInformation['Major'] == "ISE": # We are looking at ISE student
        requiredLowerDivisonCourses = ("114", "214", "218")
        requiredUpperDivisionCourses = ("300", "305", "316", "320" "312") # We also need to consider the alternatives for some of the classes
        alternateRequiredCourses =  {"CSE": ("215", "311", "331", "323", "337", "370", "377"), # Courses for the ISE specializations
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
                                    "BIO": ("201", "203")}
    semesterText = ""
    semesterYear = ""
    for lineOfInformation in text:
        modifiedLine = lineOfInformation.replace(" ", "")
        if "TermGPA" in modifiedLine: # Reset the semesterText and semesterYear strings 
            semesterText = ""
            semesterYear = ""
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" not in modifiedLine):
            index = 0
            while not (modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                if "Fall" == semesterText or "Winter" == semesterText or "Summer" == semesterText or "Winter" == semesterText: break
                semesterText += modifiedLine[index]
                index += 1
            while (index != len(modifiedLine) and modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                semesterYear += modifiedLine[index]
                index += 1
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" in modifiedLine) and (semesterText == "") and (semesterYear == ""):
            springIndex = modifiedLine.find("Spring")
            fallIndex = modifiedLine.find("Fall")
            winterIndex = modifiedLine.find("Winter")
            summerIndex = modifiedLine.find("Summer")
            if springIndex >= 0:
                semesterText = "Spring"
            elif fallIndex >= 0:
                semesterText = "Fall"
            elif winterIndex >= 0:
                semesterText = "Winter"
            elif summerIndex >= 0:
                semesterText = "Summer"
            findFirstCharacter = modifiedLine.find("/")
            stringAfter = modifiedLine[findFirstCharacter+1::]
            findSecondCharacter = stringAfter.find("/")
            stringAfterSecond = stringAfter[findSecondCharacter+1::]
            index = 0
            while (stringAfterSecond[index] >= '0' and stringAfterSecond[index] <= '9'):
                if len(semesterYear) == 4 and semesterYear.isdigit(): break
                semesterYear += stringAfterSecond[index]
                index += 1
        if "CSE" in modifiedLine and studentInformation['Major'] == "CSE":

            indexLocation = modifiedLine.index("CSE") + 3
            classNumber = ""
            while len(classNumber) != 3:
                classNumber += modifiedLine[indexLocation]
                indexLocation += 1
            if classNumber.isdigit():
                if classNumber == "101": continue # We do not count this 
                elif classNumber in requiredLowerDivisonCourses:
                    createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, lowerDivisionCourses)
                elif classNumber in requiredUpperDivisionCourses:
                    createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, upperDivisionCourses)
                else: # We are looking at a technical course 
                    if classNumber == "495" or classNumber == "496" or classNumber == "475" or classNumber == "301": continue # Won't be counted for credits
                    if (classNumber == "487" and '487' in technicalCourses) or (classNumber == "488" and '488' in technicalCourses): continue # We can only use the class once as a technical elective 
                    createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, technicalCourses) 
            else: sys.exit("Trouble reading data from file.")
        elif "CSE" not in modifiedLine and studentInformation['Major'] == "CSE": # Note: We don't allow ALL ISE courses as CSE technical electives
            classDescription = modifiedLine[0:3]
            classTitle = classDescription
            # More to be implemented here, AMS 345 for example
            indexLocation = modifiedLine.index(classDescription) + 3
            classNumber = ""
            if classDescription in alternateOptionalCourses: # We are most probably looking at a PSY course 
                while len(classNumber) != 3:
                    classNumber += modifiedLine[indexLocation]
                    indexLocation += 1
                if classNumber.isdigit():
                    tupleClass = alternateOptionalCourses[classDescription]
                    if classNumber in tupleClass: # PSY course that counts as specialization 
                        createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, specalizeOptionalCourses)
                    # Discard any other PSY Courss
                else: sys.exit("Trouble reading data from file.")
            elif classDescription in ISEcoursestreatedasCSE:
                while len(classNumber) != 3:
                    classNumber += modifiedLine[indexLocation]
                    indexLocation += 1
                if classNumber.isdigit():
                    tupleClass = ISEcoursestreatedasCSE[classDescription]
                    if classNumber in tupleClass: # ISE course counts as technical elective
                        if classNumber == "300" or classNumber == "312":
                            createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, upperDivisionCourses) # Thread as upper division required course
                        elif classNumber != "301": # Don't count "CSE/ISE 301 as a technical course"
                            createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, technicalCourses)
                    # Discard any other ISE courses 
                else: sys.exit("Trouble reading data from file.")
            elif classDescription in ESTcoursestreatedasCSE:
                while len(classNumber) != 3:
                    classNumber += modifiedLine[indexLocation]
                    indexLocation += 1
                if classNumber.isdigit():
                    tupleClass = ESTcoursestreatedasCSE[classDescription]
                    if classNumber in tupleClass:
                        createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, technicalCourses)
                    # Discard any other EST courses
                else: sys.exit("Trouble reading data from file.")
            elif classDescription in MATcoursesttreatedasCSE:
                while len(classNumber) != 3:
                    classNumber += modifiedLine[indexLocation]
                    indexLocation += 1
                if classNumber.isdigit():
                    tupleClass = MATcoursesttreatedasCSE[classDescription]
                    if classNumber in tupleClass: # ISE course counts as technical elective
                        if classNumber == "373": # Counts as a major course (MAT 373 also treated as CSE 373)
                            createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, upperDivisionCourses)
                        else:
                            createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, technicalCourses)
                    # Discard any other MAT courses 
                else: sys.exit("Trouble reading data from file.")
            elif classDescription in AMScoursestreatedasCSE:
                while len(classNumber) != 3:
                    classNumber += modifiedLine[indexLocation]
                    indexLocation += 1
                if classNumber.isdigit():
                    tupleClass = AMScoursestreatedasCSE[classDescription]
                    if classNumber in tupleClass:
                        createClassObjetctForCSE(semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, technicalCourses)
                    # Discard any other AMS courses
                else: sys.exit("Trouble reading data from file.")
        elif "ISE" in modifiedLine and studentInformation['Major'] == "ISE": # Need to also check if the class is part of a specalization or not
            technical = False 
            specalization = False # Boolean flag to determine if part of a specalization or not 
            classTitle = "ISE"
            indexLocation = modifiedLine.index("ISE") + 3
            classNumber = ""
            while len(classNumber) != 3:
                classNumber += modifiedLine[indexLocation]
                indexLocation += 1
            if classNumber.isdigit(): # Might need to make some modifications here cause stuff might be incorrect 
                if classNumber in requiredLowerDivisonCourses: # Only handles ISE 218
                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                elif classNumber in requiredUpperDivisionCourses: #Handles ISE upper division courses that are requred 
                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                else: # Looks for both ISE electives (ISE 3xx) AND ISE specalization courses, so we need to handle both cases where they are
                    getTuple = alternateRequiredCourses[classTitle] # Check to see if the ISE class is in the specalization class 
                    if classNumber in getTuple: #It is both a technical and a specialization
                        technical = True  
                        specalization = True # Set to true, so we are looking at an elective course AND specalization course
                    else: #It is only a technical, not a specalization as well 
                        technical = True
                        specalization = False 
                    if (classNumber == "475" and '475' in technicalCourses) or (classNumber == "488" and '488' in technicalCourses): continue # We can only count this as one
                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
            else: sys.exit("Trouble reading data from file.")
        elif "ISE" not in modifiedLine and studentInformation['Major'] == "ISE": # Need to consider a lot for ISE students
            # This handles the case for CSE 114 and CSE 214 
            # First check and see if the class description is in the intended required courses
            specalization = False
            technical = False
            classDescription = modifiedLine[0:3]
            classTitle = classDescription # Store the class title, which will be used for the method 
            if classDescription in alternateRequiredCourses:
                # Get the class number
                indexLocation = modifiedLine.index(classDescription) + 3 
                classNumber = ""
                while len(classNumber) != 3:
                    classNumber += modifiedLine[indexLocation]
                    indexLocation += 1
                if classNumber.isdigit():
                    if classNumber in requiredLowerDivisonCourses: # Handles the case for CSE 114 and CSE 214
                        if "215" not in modifiedLine:
                            specalization = False
                        elif "215" in modifiedLine: # Considered to be a specalization class option and also a math required option
                            specalization = True 
                        createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                    else: # We looking at a class number greater than 300 or is in the alternate course directory
                        tupleClass = alternateRequiredCourses[classDescription]
                        if classNumber in tupleClass: # Is a specialization class 
                            if classTitle == "EST" and classNumber == "323": # Counts as CSE/ISE/EST 323 so also an technical course
                                specalization, technical = True, True
                                createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                            elif classTitle == "CSE" and int(classNumber) >= 300: # All upper 300 counts as technical as well
                                specalization, technical = True, True
                                createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                            else:
                                specalization, technical = True, False 
                                createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                        else: # Then we are most likely looking at a technical elective for ISE (only CSE and ISE classes are allowed)
                            if classTitle == "CSE":
                                if classNumber == "300": # CSE/ISE 300
                                    classTitle = "ISE"
                                    classNumber = "300"
                                    specalization, technical = False, False # Required Course
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                                elif classNumber == "312": # CSE/ISE 312
                                    classTitle = "ISE"
                                    classNumber = "312"
                                    specalization, technical = False, False # Required Course
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                                elif classNumber == "310": # CSE 310
                                    specalization, technical = False, False # Required Course
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                                else:
                                    specalization, technical = False, True # Only a CSE technical course
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                            elif classTitle == "EST": 
                                if classNumber == "340" or classNumber == "339": #EST 340 an EST 339 count as ISE technical electives as they are also offered as ISE 340 and ISE 339
                                    specalization, technical = False, True # This is considered to be a technical elective
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                            elif classTitle == "BUS":
                                if classNumber == "340": # Required Course
                                    specalization, technical = False, False
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                            elif classTitle == "POL":
                                if classNumber == "369":
                                    specalization, technical = False, True # Offered as ISE 369 as well
                                    createClassObjectForISE(semesterText, semesterYear, modifiedLine[indexLocation::], classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specalization, technical)
                            # Any other class down here will get discarded 
                else: sys.exit("Trouble reading data from file.")

        
# A thread calls this function in order to find and parse and store the required math courses
def mathTracker(text, mathRequiredCourses):
    semesterText = ""
    semesterYear = ""
    for lineOfInformation in text:
        modifiedLine = lineOfInformation.replace(" ", "")
        if "TermGPA" in modifiedLine or "TestTransGPA" in modifiedLine: # Reset the semesterText and semesterYear strings 
                semesterText = ""
                semesterYear = ""
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and "Session" not in modifiedLine:
                index = 0
                while not (modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                    if "Fall" == semesterText or "Winter" == semesterText or "Summer" == semesterText or "Winter" == semesterText: break
                    semesterText += modifiedLine[index]
                    index += 1
                while (index != len(modifiedLine) and modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                    if len(semesterYear) == 4 and semesterYear.isdigit(): break
                    semesterYear += modifiedLine[index]
                    index += 1
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" in modifiedLine) and (semesterText == "") and (semesterYear == ""):
            springIndex = modifiedLine.find("Spring")
            fallIndex = modifiedLine.find("Fall")
            winterIndex = modifiedLine.find("Winter")
            summerIndex = modifiedLine.find("Summer")
            if springIndex >= 0:
                semesterText = "Spring"
            elif fallIndex >= 0:
                semesterText = "Fall"
            elif winterIndex >= 0:
                semesterText = "Winter"
            elif summerIndex >= 0:
                semesterText = "Summer"
            findFirstCharacter = modifiedLine.find("/")
            stringAfter = modifiedLine[findFirstCharacter+1::]
            findSecondCharacter = stringAfter.find("/")
            stringAfterSecond = stringAfter[findSecondCharacter+1::]
            index = 0
            while (stringAfterSecond[index] >= '0' and stringAfterSecond[index] <= '9'):
                if len(semesterYear) == 4 and semesterYear.isdigit(): break
                semesterYear += stringAfterSecond[index]
                index += 1
        if "AMS" in modifiedLine or "MAT" in modifiedLine:
                indexLocation = 0
                classTitle = ""
                if "AMS" in modifiedLine:
                    indexLocation = modifiedLine.index("AMS") + 3
                    classTitle = "AMS"
                elif "MAT" in modifiedLine:
                    indexLocation = modifiedLine.index("MAT") + 3
                    classTitle = "MAT"
                classNumber = ""
                while len(classNumber) != 3:
                    classNumber += modifiedLine[indexLocation]
                    indexLocation += 1
                if classNumber == "LVL": continue # Tells us Math Placement Test, so we skip this 
                if classNumber.isdigit():
                    createClassObjectForMathCourses(classTitle, semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, mathRequiredCourses)
                else: sys.exit("Trouble reading data from file.")
    
# Only for the CSE majors there is a science course requirement, so this thread calls this function
# in order to parse and store science courses in order to meet the 9 credits/1 lab requirement
def scienceTracker(text, scienceCourses):
    semesterText = ""
    semesterYear = ""
    for lineOfInformation in text:
        modifiedLine = lineOfInformation.replace(" ", "")
        if "TermGPA" in modifiedLine: # Reset the semesterText and semesterYear strings 
                semesterText = ""
                semesterYear = ""
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" not in modifiedLine):
                index = 0
                while not (modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                    if "Fall" == semesterText or "Winter" == semesterText or "Summer" == semesterText or "Winter" == semesterText: break # We are done parsing
                    semesterText += modifiedLine[index]
                    index += 1
                while (index != len(modifiedLine) and modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                    if len(semesterYear) == 4 and semesterYear.isdigit(): break
                    semesterYear += modifiedLine[index]
                    index += 1
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" in modifiedLine) and (semesterText == "") and (semesterYear == ""):
            springIndex = modifiedLine.find("Spring")
            fallIndex = modifiedLine.find("Fall")
            winterIndex = modifiedLine.find("Winter")
            summerIndex = modifiedLine.find("Summer")
            if springIndex >= 0:
                semesterText = "Spring"
            elif fallIndex >= 0:
                semesterText = "Fall"
            elif winterIndex >= 0:
                semesterText = "Winter"
            elif summerIndex >= 0:
                semesterText = "Summer"
            findFirstCharacter = modifiedLine.find("/")
            stringAfter = modifiedLine[findFirstCharacter+1::]
            findSecondCharacter = stringAfter.find("/")
            stringAfterSecond = stringAfter[findSecondCharacter+1::]
            index = 0
            while (stringAfterSecond[index] >= '0' and stringAfterSecond[index] <= '9'):
                if len(semesterYear) == 4 and semesterYear.isdigit(): break
                semesterYear += stringAfterSecond[index]
                index += 1
        if "PHY" in modifiedLine or "BIO" in modifiedLine or "CHE" in modifiedLine or "GEO" in modifiedLine or "AST" in modifiedLine:
                classTitle = modifiedLine
                indexLocation = 0
                if "PHY" in modifiedLine:
                    indexLocation = modifiedLine.index("PHY") + 3
                    classTitle = "PHY"
                elif "BIO" in modifiedLine:
                    indexLocation = modifiedLine.index("BIO") + 3
                    classTitle = "BIO"
                elif "GEO" in modifiedLine:
                    indexLocation = modifiedLine.index("GEO") + 3
                    classTitle = "GEO"
                elif "AST" in modifiedLine:
                    indexLocation = modifiedLine.index("AST") + 3
                    classTitle = "AST"
                elif "CHE" in modifiedLine:
                    indexLocation = modifiedLine.index("CHE") + 3
                    classTitle = "CHE"
                classNumber = ""
                while len(classNumber) != 3:
                    classNumber += modifiedLine[indexLocation]
                    indexLocation += 1
                if classNumber.isdigit():
                    createClassObjectForScienceCourses(classTitle, semesterText, semesterYear, modifiedLine[indexLocation::], classNumber, scienceCourses)
                else: sys.exit("Trouble reading data from file.")

# A thread calls this function in order to find and store any SBCs that satisfy the CSE and ISE SBCs requirement
def sbcsTracker(text, sbcCourses):
    # For transfering (we only consider the possible AP classes)
    transferEquivalency = {('AFS', 'ECO', 'POL', 'HIS', 'PSY'): 'SBS', ('AFS', 'HIS', 'POL'): 'USA', ('AFS', 'PSY'): 'CER', ('ARH', 'ARS', 'MUS'): 'ARTS', ('BIO', 'CHE', 'SUS', 'PHY'): 'SNW', ('MAT', 'AMS'): 'QPS', ('CHI', 'FRN', 'GER', 'ITL', 'JPN', 'LAT', 'SPN'): 'LANG', ('CHI', 'FRN', 'GER', 'HIS', 'ITL', 'JPN', 'SPN'): 'GLO', ('CHI', 'EGL', 'FRN', 'GER', 'ITL', 'JPN', 'SPN'): 'HUM', ('CSE'): 'TECH', ('LAT'): 'HFA+'}

    semesterText = ""
    semesterYear = ""
    semesterDateInfoParsed = False
    keepSkipping, keepSkippingSecond = False, False  
    for lineinformation in text:
        modifiedLine = lineinformation.replace(" ", "")
        classInfo = modifiedLine[0:3]
        if "TestCredits" in modifiedLine and keepSkipping == False:
            indexOfUnmodifiedLine = text.index(lineinformation)
            listAfterwards = text[indexOfUnmodifiedLine+2::]
            handleTestCreditsSbcs(listAfterwards, sbcCourses, transferEquivalency)
            keepSkipping = True
        if "TransferCredit" in modifiedLine and keepSkippingSecond == False:
            indexOfUnmodifiedLine = text.index(lineinformation)
            listAfterwards = text[indexOfUnmodifiedLine+2::]
            handleTestCreditsSbcs(listAfterwards, sbcCourses, transferEquivalency)
            keepSkippingSecond = True 
        if "TestTransGPA" in modifiedLine:
            keepSkipping = False
        if "TermGPA" in modifiedLine:
            semesterText = ""
            semesterYear = ""
            semesterDateInfoParsed = False
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" not in modifiedLine) and semesterDateInfoParsed == False:
                index = 0
                while not (modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                    if "Fall" == semesterText or "Winter" == semesterText or "Summer" == semesterText or "Winter" == semesterText: break # We are done parsing
                    semesterText += modifiedLine[index]
                    index += 1
                while (index != len(modifiedLine) and modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                    if len(semesterYear) == 4 and semesterYear.isdigit(): break
                    semesterYear += modifiedLine[index]
                    index += 1
                semesterDateInfoParsed = True
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" in modifiedLine) and (semesterText == "") and (semesterYear == ""):
            springIndex = modifiedLine.find("Spring")
            fallIndex = modifiedLine.find("Fall")
            winterIndex = modifiedLine.find("Winter")
            summerIndex = modifiedLine.find("Summer")
            if springIndex >= 0:
                semesterText = "Spring"
            elif fallIndex >= 0:
                semesterText = "Fall"
            elif winterIndex >= 0:
                semesterText = "Winter"
            elif summerIndex >= 0:
                semesterText = "Summer"
            findFirstCharacter = modifiedLine.find("/")
            stringAfter = modifiedLine[findFirstCharacter+1::]
            findSecondCharacter = stringAfter.find("/")
            stringAfterSecond = stringAfter[findSecondCharacter+1::]
            index = 0
            while (stringAfterSecond[index] >= '0' and stringAfterSecond[index] <= '9'):
                if len(semesterYear) == 4 and semesterYear.isdigit(): break
                semesterYear += stringAfterSecond[index]
                index += 1
        elif keepSkipping == False:
            checkSubString = modifiedLine[3:6]
            if checkSubString.isdigit(): pass # We do nothing
            else: continue

            offsetIndex = 1
            getIndex = text.index(lineinformation)
            lengthCounter = getIndex + 1 # Gets the actual current length of the list, so lengthCounter will always be 1 greater than the index we are accessing
            attributesLine = False
            notFound = False
            attributesLineInfo = ""

            while notFound == False and attributesLine == False and lengthCounter < len(text):
                lengthCounter += 1
                nextLine = text[getIndex+offsetIndex] 
                modifiedNextLine = nextLine.replace(" ", "")
                # check and see if we are reading a class line
                classInfoTemp = modifiedNextLine[3:6]
                if "CourseAttributes" in modifiedNextLine:
                    attributesLineInfo = nextLine
                    attributesLine = True # We found the attributesLine
                elif "TermGPA" in modifiedNextLine and attributesLine == False:
                    notFound = True
                else:
                    offsetIndex += 1
                    if classInfoTemp.isdigit(): notFound = True
                    else: continue
            # Once we have found the line with the course attribute, we want to parse it 
            if notFound == True: continue

            if attributesLine == True:
                if "Controlled Access" in attributesLineInfo:
                    # Then we still need to keep looking for the actual line that contains the SBC
                    # Go to the next line:
                    # 1) Next line will have the SBC we are looking for
                    # 2) Next line will be another class, which in that case, we don't create an object
                    controlledAccessLine = text.index(attributesLineInfo)
                    nextLine = text[controlledAccessLine + 1]
                    checkForClass = nextLine[3:6]
                    if checkForClass.isdigit(): continue # Means we are looking at a new class line, so we continue
                    else:
                        # This line is an SBC, so we can parse
                        index = 0
                        sbcStringList = []
                        sbcLine = ""
                        while nextLine[index] >= 'A'and nextLine[index] <= 'Z':
                            sbcLine += nextLine[index]
                            index += 1
                        sbcStringList.append(sbcLine)
                        
                        # Might be more SBCs after this, so we need to continue parsing further

                        offsetIndex += 2
                        stillParsingSbcs = False
                        while stillParsingSbcs == False:
                            furtherLine = text[getIndex+offsetIndex] 
                            furtherLineModified = furtherLine.replace(" ", "")
                            # Check to see if there is also a class character or not 
                            classInfoMoreTemp = furtherLineModified[3:6]
                            if "TermGPA" in furtherLineModified:
                                stillParsingSbcs = True 
                            else:
                                if classInfoMoreTemp.isdigit():
                                    stillParsingSbcs = True # Set to True
                                else:
                                    offsetIndex += 1
                                    # We have found a line that contains another SBC, so we need to parse this line as well
                                    startingIndexTemp = 0
                                    sbcStringTemp = ""
                                    while furtherLine[startingIndexTemp] != ' ':
                                        sbcStringTemp += furtherLine[startingIndexTemp]
                                        startingIndexTemp += 1
                                    sbcStringList.append(sbcStringTemp)
                        if '' in sbcStringList:
                            indexOfEmpty = sbcStringList.index('')
                            sbcStringList = sbcStringList[0:indexOfEmpty]
                    createClassObjectForSBCCourses(classInfo, sbcStringList, semesterText, semesterYear, modifiedLine, checkSubString, sbcCourses)        
                else:
                    colonIndex = attributesLineInfo.index(':')
                    attributesLineInfoModified = attributesLineInfo[colonIndex+2::]
                    sbcStringList = []
                    sbcString = ""
                    startingIndex = 0
                    while attributesLineInfoModified[startingIndex] != ' ':
                        sbcString += attributesLineInfoModified[startingIndex]
                        startingIndex += 1
                    sbcStringList.append(sbcString)

                    # Might be more to parse, so we don't know 
                    offsetIndex += 1
                    lengthCounterTemp = getIndex + offsetIndex + 1
                    stillParsingSbcs = False
                    while stillParsingSbcs == False and lengthCounterTemp < len(text):
                        lengthCounterTemp += 1
                        furtherLine = text[getIndex+offsetIndex]
                        furtherLineModified = furtherLine.replace(" ", "")
                        # Check to see if there is also a class character or not 
                        classInfoMoreTemp = furtherLineModified[3:6]
                        if "TermGPA" in furtherLineModified:
                            stillParsingSbcs = True 
                        else:
                            if classInfoMoreTemp.isdigit():
                                stillParsingSbcs = True # Set to True
                            else:
                                offsetIndex += 1
                                # We have found a line that contains another SBC, so we need to parse this line as well
                                startingIndexTemp = 0
                                sbcStringTemp = ""
                                while furtherLine[startingIndexTemp] != ' ':
                                    sbcStringTemp += furtherLine[startingIndexTemp]
                                    startingIndexTemp += 1
                                sbcStringList.append(sbcStringTemp)
                    if '' in sbcStringList:
                        indexOfEmpty = sbcStringList.index('')
                        sbcStringList = sbcStringList[0:indexOfEmpty]
                    createClassObjectForSBCCourses(classInfo, sbcStringList, semesterText, semesterYear, modifiedLine, checkSubString, sbcCourses)

# A thread calls this function in order to keep track of the classes taken by the student per semester
def classTracker(text, classesPerSemester): #Responsible for keeping a dictionary of what classes the student is taking per semester

    transferEquivalency = {('AFS', 'ECO', 'POL', 'HIS', 'PSY'): 'SBS', ('AFS', 'HIS', 'POL'): 'USA', ('AFS', 'PSY'): 'CER', ('ARH', 'ARS', 'MUS'): 'ARTS', ('BIO', 'CHE', 'SUS', 'PHY'): 'SNW', ('MAT', 'AMS'): 'QPS', ('CHI', 'FRN', 'GER', 'ITL', 'JPN', 'LAT', 'SPN'): 'LANG', ('CHI', 'FRN', 'GER', 'HIS', 'ITL', 'JPN', 'SPN'): 'GLO', ('CHI', 'EGL', 'FRN', 'GER', 'ITL', 'JPN', 'SPN'): 'HUM', ('CSE'): 'TECH', ('LAT'): 'HFA+'}

    semesterText = ""
    semesterYear = ""
    keepSkipping, keepSkippingSecond = False, False # The second variable is going to be used for the transfer credit from other colleges 
    for lineofInformation in text:
        modifiedLine = lineofInformation.replace(" ", "")
        classNumberTracker = modifiedLine[3:6]
        if "TestCredits" in modifiedLine and keepSkipping == False:
            indexOfUnmodifiedLine = text.index(lineofInformation)
            listAfterwards = text[indexOfUnmodifiedLine+2::]
            keepSkipping = True
            handleTestCreditsNormal(listAfterwards, classesPerSemester, transferEquivalency)
        if "TransferCredit" in modifiedLine and keepSkippingSecond == False: # We are looking at transfer credits from another college 
            # So we also want to handle test credits that satisfy specific classes for the student
            indexOfUnmodifiedLine = text.index(lineofInformation)
            listAfterwards = text[indexOfUnmodifiedLine+2::]
            handleTestCreditsNormal(listAfterwards, classesPerSemester, transferEquivalency)
            keepSkippingSecond = True 
        if "TestTransGPA" in modifiedLine:
            keepSkipping = False
        if "TermGPA" in modifiedLine:
            semesterText = ""
            semesterYear = ""
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" not in modifiedLine) and keepSkipping == False:
                index = 0
                while not (modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                    if "Fall" == semesterText or "Winter" == semesterText or "Summer" == semesterText or "Winter" == semesterText: break # We are done parsing
                    semesterText += modifiedLine[index]
                    index += 1
                while (index != len(modifiedLine) and modifiedLine[index] >= '0' and modifiedLine[index] <= '9'):
                    if len(semesterYear) == 4 and semesterYear.isdigit(): break # We successfully parsed the year 
                    semesterYear += modifiedLine[index]
                    index += 1
        if ("Spring" in modifiedLine or "Fall" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and ("Session" in modifiedLine) and (semesterText == "") and (semesterYear == "") and keepSkipping == False:
            springIndex = modifiedLine.find("Spring")
            fallIndex = modifiedLine.find("Fall")
            winterIndex = modifiedLine.find("Winter")
            summerIndex = modifiedLine.find("Summer")
            if springIndex >= 0:
                semesterText = "Spring"
            elif fallIndex >= 0:
                semesterText = "Fall"
            elif winterIndex >= 0:
                semesterText = "Winter"
            elif summerIndex >= 0:
                semesterText = "Summer"
            findFirstCharacter = modifiedLine.find("/")
            stringAfter = modifiedLine[findFirstCharacter+1::]
            findSecondCharacter = stringAfter.find("/")
            stringAfterSecond = stringAfter[findSecondCharacter+1::]

            index = 0 # Reset the index back to 0 
            while (stringAfterSecond[index] >= '0' and stringAfterSecond[index] <= '9'):
                if len(semesterYear) == 4 and semesterYear.isdigit(): break
                semesterYear += stringAfterSecond[index]
                index += 1
                
        if keepSkipping == False:
            if classNumberTracker.isdigit():
                classTitle = modifiedLine[0:3]
                createClassInformation(classTitle, classNumberTracker, semesterText, semesterYear, modifiedLine, classesPerSemester)
            else:
                continue # We are not looking at a class line, so we continue
        
# This function creates an object for a CSE course
@staticmethod
def createClassObjetctForCSE(semesterText, semesterYear, modifiedLine, classNumber, courseDictionary):

    dictInformation = parseSpecificClassInformation("", "", "", modifiedLine)

    list_of_cross_over_classes = ["300", "301", "311", "312", "323", "332", "333", "334", "337", "364"]

    list_of_cross_over_classes_mat = ["371", "373"]

    list_of_cross_over_classe_ams = ["345"]

    # Create our class object
    if int(classNumber) < 300:
        lowerDivisionObject = UniversalClassObject("CSE " + classNumber, dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        courseName = lowerDivisionObject.courseName
        courseDictionary[courseName] = lowerDivisionObject
    elif int(classNumber) >= 300:
        stringName = "CSE"
        decisionString = "" if classNumber in list_of_cross_over_classe_ams else " " + classNumber
        if classNumber in list_of_cross_over_classes: # Also considered to be an ISE class 
            if classNumber == "323":
                stringName = "CSE/ISE/EST"
            else:
                stringName = "CSE/ISE" # Consider to be both classes
        elif classNumber in list_of_cross_over_classes_mat:
            stringName = "CSE/MAT"
        elif classNumber in list_of_cross_over_classe_ams:
            stringName = "CSE 355/AMS 345"
        upperDivisonObject = UniversalClassObject(stringName + f'{decisionString}', dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        courseName = upperDivisonObject.courseName
        courseDictionary[courseName] = upperDivisonObject

# This function creates an object for an ISE course
@staticmethod
def createClassObjectForISE(semesterText, semesterYear, modifiedLine, classTitle, classNumber, lowerDivisionCourses, upperDivisionCourses, technicalCourses, specializeRequiredCourses, mathRequiredCourses, specBool, techBool): 

    dictInformation = parseSpecificClassInformation("", "", "", modifiedLine)

    list_of_cross_over_classes = ["300", "301", "311", "312", "323", "332", "333", "334", "337", "364"] # CSE/ISE courses and ONE EST course

    list_of_cross_over_classes_with_est = ["310", "339", "340"] # ISE/EST Courses

    list_of_cross_over_classes_with_pol = ["369"] # Only one course in this case, which is ISE 369/POL 369

    if int(classNumber) < 300: # Lower division courses cant be considered electives, as they are required to be 300+ courses
        lowerDivisionObject = UniversalClassObject(classTitle + " " + classNumber, dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        courseName = lowerDivisionObject.courseName
        # Need to do some stuff here to determine where the objects go
        if specBool == True:
            specializeRequiredCourses[courseName] = lowerDivisionObject
            mathRequiredCourses[courseName] = lowerDivisionObject # Only 215 fits this category 
        else:
            lowerDivisionCourses[courseName] = lowerDivisionObject
    elif int(classNumber) >= 300: # Many things we need to do for handling
        stringName = classTitle
        decisionString = "" if (classNumber == "310" and classTitle == "EST")  or (classNumber == "340" and classTitle == "ISE") else " " + classNumber
        if classNumber in list_of_cross_over_classes: # Cross-over classes with CSE
            if classNumber == "323" and (classTitle == "CSE" or classTitle == "ISE" or classTitle == "EST"): # Only one CSE/ISE Course
                stringName = "CSE/ISE/EST"
            elif (classTitle == "CSE" or classTitle == "ISE"): # CSE/ISE Course
                stringName = "CSE/ISE"
        elif classNumber in list_of_cross_over_classes_with_est: # 1 cross-over class with EST
            if (classNumber == "310" and classTitle == "EST")  or (classNumber == "340" and classTitle == "ISE"): 
                stringName = "ISE 340/EST 310"
            elif classNumber == "339":
                stringName = "ISE/EST"
        elif classNumber in list_of_cross_over_classes_with_pol:
            stringName = "ISE/POL"
        upperDivisionObject = UniversalClassObject(stringName + f'{decisionString}', dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        courseName = upperDivisionObject.courseName
        # This is where we need to handle multiple cases
        if specBool == True and techBool == True:
            specializeRequiredCourses[courseName] = upperDivisionObject
            technicalCourses[courseName] = upperDivisionObject
        elif specBool == True and techBool == False:
            specializeRequiredCourses[courseName] = upperDivisionObject
        elif specBool == False and techBool == True:
            technicalCourses[courseName] = upperDivisionObject
        else: 
            upperDivisionCourses[courseName] = upperDivisionObject # This is a required course
    
# This function is responsible for handling SBCs that are satisfied for courses that the student
# took before their undergraduate record at SBU started
@staticmethod
def handleTestCreditsSbcs(text, sbcCourses, transferEquivalency):
    semesterText = "Transfer"
    semesterYear = "Credits"
    for lineOfInformation in text:
        modifiedLine = lineOfInformation.replace(" ", "")
        if "TestTransGPA" in modifiedLine: break
        classNumberTracker = modifiedLine[3:6] # Find a class number
        if classNumberTracker.isdigit():
            classTitle = modifiedLine[0:3]
            list_of_keys = transferEquivalency.keys()
            list_of_sbcs = []
            for keys in list_of_keys:
                if classTitle in keys:
                    getSBCValue = transferEquivalency[keys]
                    list_of_sbcs.append(getSBCValue)
            if len(list_of_sbcs) != 0:
                createClassObjectForSBCCourses(classTitle, list_of_sbcs, semesterText, semesterYear, modifiedLine, classNumberTracker, sbcCourses)
        else: 
            classTitle = modifiedLine[0:3]
            list_of_keys = transferEquivalency.keys()
            list_of_sbcs = []
            for keys in list_of_keys:
                if classTitle in keys:
                    getSBCValue = transferEquivalency[keys]
                    list_of_sbcs.append(getSBCValue)
            if len(list_of_sbcs) != 0: #Means we found a class that is associated with an SBC
                createClassObjectForSBCCourses(classTitle, list_of_sbcs, semesterText, semesterYear, modifiedLine, classNumberTracker, sbcCourses)   
            continue
           

# This function is responsible for handling the courses that are satisfied for when the student transfered in these
# courses before their Undergraduate record at SBU began 
@staticmethod 
def handleTestCreditsNormal(text, classesPerSemester, transferEquivalency): # To Handle Any Transfer Credits 
    semesterText = "Transfer"
    semesterYear = "Credits"
    for lineOfInformation in text:
        modifiedLine = lineOfInformation.replace(" ", "")
        if "TestTransGPA" in modifiedLine or "Beginning" in modifiedLine: break # We are done parsing 
        classNumberTracker = modifiedLine[3:6] # Find a class number
        if classNumberTracker.isdigit():
            classTitle = modifiedLine[0:3]
            createClassInformation(classTitle, classNumberTracker, semesterText, semesterYear, modifiedLine, classesPerSemester)
        else: 
            if classNumberTracker == "LVL":
                classTitle = modifiedLine[0:3]
                grabLevel = modifiedLine[6]
                createClassInformation(classTitle, f'LVL{str(grabLevel)}', semesterText, semesterYear, modifiedLine, classesPerSemester)
            else:
                list_of_keys = transferEquivalency.keys()
                classTitle = modifiedLine[0:3]
                for keys in list_of_keys:
                    if classTitle in keys: 
                        grabSBCValue = transferEquivalency[keys]
                        createClassInformation(classTitle, grabSBCValue, semesterText, semesterYear, modifiedLine, classesPerSemester)
            continue # Dont think this is necessary but Im gonna keep it here just in case 


# This function makes a call to parse specific information about a particular class (any class), creates an object after parsing 
# is finished and stores the Object in the state variable
@staticmethod
def createClassInformation(classTitle, classNumber, semesterText, semesterYear,  modifiedLine, classesPerSemester):

    dictInformation = parseSpecificClassInformation("", "", "", modifiedLine)
    if dictInformation: # Dict is not empty 
        ClassObject = SimpleClassObject(classTitle + " " + classNumber, dictInformation['classCreditsAmount'], dictInformation['classGrade'], semesterText, semesterYear)
        
        if (semesterText + " " + semesterYear) in classesPerSemester: # The Key Exists 
            getList = classesPerSemester[semesterText + " " + str(semesterYear)]
            getList.append(ClassObject)
        else: # Does not exist, so we create a list for that particular semester
            listOfClassesInSemester = []
            listOfClassesInSemester.append(ClassObject)
            classesPerSemester[semesterText + " " + str(semesterYear)] = listOfClassesInSemester
    
# This function makes a call to parse specific information about a particular math class, creates an object after parsing 
# is finished and stores the Object in the state variable
@staticmethod
def createClassObjectForMathCourses(classTitle, semesterText, semesterYear, modifiedLine, classNumber, mathRequiredCourses):
    dictInformation = parseSpecificClassInformation("", "", "", modifiedLine)
    if dictInformation:
        MathObject = UniversalClassObject(classTitle + " " + classNumber, dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        mathRequiredCourses[classTitle + " " + classNumber] = MathObject

# This function makes a call to parse specific information about a particular science class, creates an object after parsing 
# is finished and stores the Object in the state variable
@staticmethod
def createClassObjectForScienceCourses(classTitle, semesterText, semesterYear, modifiedLine, classNumber, scienceCourses):
    dictInformation = parseSpecificClassInformation("", "", "", modifiedLine)
    if dictInformation:
        scienceObject = UniversalClassObject(classTitle + " " +  classNumber + " (SNW)" if int(classNumber) in [132, 131, 141, 152, 201, 102, 103, 122, 125, 127, 142] else (classTitle + " " + classNumber if int(classNumber) in [133, 204, 154, 322, 332, 112, 113, 134, 252] else classTitle + classNumber + " (STEM+)"), dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        scienceCourses[classTitle + " " + classNumber] = scienceObject

# This function makes a call to parse specific information about a particular class with an SBC, creates an object after parsing 
# is finished and stores the Object in the state variable
@staticmethod
def createClassObjectForSBCCourses(classTitle, sbcLabel, semesterText, semesterYear, modifiedLine, classNumber, sbcCourses):
    dictInformation = parseSpecificClassInformation("", "", "", modifiedLine)
    if dictInformation:
        SBCObject = SBCCourse(sbcLabel, classTitle + " " + classNumber, dictInformation['classGrade'], dictInformation['classCreditsAmount'], semesterText, semesterYear, dictInformation['classComments'])
        sbcCourses[classTitle + " " + classNumber] = SBCObject


# This function is responsible for parsing one line in the transcript that holds all the required information we need to 
# make an object afterwards
@staticmethod
def parseSpecificClassInformation(classCreditsAmount, classGrade, classComments, modifiedLine) -> dict:
    if '.' in modifiedLine:
        indexOfColon = modifiedLine.index('.') # Somehow an SBC ended up here, so any SBCs that end up here we can remove from the dictionary 
    else: 
        return {} # Empty dictionary, telling us that this is some error so we need to handle the error 
    
    modifiedLine = modifiedLine[indexOfColon+1::] # Make a new modified line 
    indexOfColonSecond = -1 # Set default to -1 
    
    if '.' in modifiedLine:
        indexOfColonSecond = modifiedLine.index('.') # Find the second colon to signify the number of credits earned 
    else: # If the colon is not found, then we will check for the letter grade that is next to the credits 
        indexOfColonSecond = indexOfColon 
    modifiedLine = modifiedLine[indexOfColonSecond-1::]
    for characters in modifiedLine:
        if ((characters >= '0' and characters <= '9') or characters == '.') and len(classCreditsAmount) != 5: # We found the class attempted 
            classCreditsAmount += characters
        elif len(classCreditsAmount) == 5:
            if (characters >= 'A' and characters <= 'Z') or characters == '+' or characters == '-':
                if characters == 'I' or characters == 'W' or characters == 'Q':
                    classComments += characters
                    classGrade += characters # Might have side effects, so we will have to see 
                elif characters == 'T':
                    classGrade = "XFER"
                else:
                    if characters == '+':
                        classGrade += "+"
                    elif characters == '-':
                        classGrade += "-"
                    else:
                        classGrade += characters
    return {'classCreditsAmount': classCreditsAmount, 'classGrade': classGrade, 'classComments': classComments}