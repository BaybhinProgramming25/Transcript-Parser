"""
This module is responsible for extracting the remainder of the student's information
specifically the Cumulative GPA, Cumulative Credits, and Upper Division Credits
"""

import sys 
import threading
from typing import Union

# Similar to StudentInfo.py, we declare these module-bound global variables to retain state
# and ensure that parsing behavior isn't modified 
_splitterFlag = False 
_upperDivisonCredits = 0.00 

# This function is responsible for finding the Upper Division Credits and
# calling other functions within the module that find more student information
def trackCumulativeInformation(text, cumulativeInformation):
    global _splitterFlag, _upperDivisonCredits
    # To determine if we are looking at a class category, we need to see if our line of Information
    # is at a specific semester (Fall, Spring, etc) 
    for findSemester in text: #Iterating over a list
        modifiedLine = findSemester.replace(" ", "") # Create a line with no whitespace 
        if _splitterFlag == True:
            indexLocation = text.index(findSemester)
            slicedTextList = text[indexLocation::]
            floatOrBoolValue = findUpperDivisonCreditsWithinSemester(slicedTextList)
            if isinstance(floatOrBoolValue, float):
                _splitterFlag = False #Reset the global variable back to its original phase 
                _upperDivisonCredits = _upperDivisonCredits + floatOrBoolValue
            elif isinstance(floatOrBoolValue, bool): #We have discovered that the transcript, is split, so we need to go on to the next page 
                _splitterFlag = True 
        if "UndergraduateCareerTotals" in modifiedLine: # Tells us we have reached the end of the transcript
            indexLocation = text.index(findSemester)
            handleCumulativeCreditsandGPA(text[indexLocation + 1], cumulativeInformation)
            return cumulativeInformation # Exit the program
        if ("Fall" in modifiedLine or "Spring" in modifiedLine or "Winter" in modifiedLine or "Summer" in modifiedLine) and "Session" not in modifiedLine: #There is also a chance that the transcript page gets cut off and the classes are in the next page, so we need to handle that
            indexLocation = text.index(findSemester)
            slicedTextList = text[indexLocation::] 
            floatOrBoolValue = findUpperDivisonCreditsWithinSemester(slicedTextList)
            if isinstance(floatOrBoolValue, float):
                _splitterFlag = False #Reset the global variable back to its original phase 
                _upperDivisonCredits = _upperDivisonCredits + floatOrBoolValue
            elif isinstance(floatOrBoolValue, bool): #We have discovered that the transcript, is split, so we need to go on to the next page 
                _splitterFlag = True 
    # This part of the program is reached when we have reached the end of this part of the PDF page
    cumulativeInformation['Upper Division Credits'] = _upperDivisonCredits 

# This static function updates a counter that stores the number of upperDivisionCredits and returns that counter alongside
# a boolean value that is Union'ed 
@staticmethod
def findUpperDivisonCreditsWithinSemester(text) -> Union[float, bool]:
    upperDivisonCreditsCounter = 0.000
    for findClasses in text:
        modifiedClassLine = findClasses.replace(" ", "")
        if "TermGPA" in modifiedClassLine: # Signifies the end of the semester
            return upperDivisonCreditsCounter
        classNumberof3 = modifiedClassLine[3:6] #We only need to check a certain parameter like this (this may also lead to potential of bugs but we will try to circumvent this in the future)
        try:
            if int(classNumberof3) >= 300:
                modifiedClassLine = modifiedClassLine[6::]
                creditsValue = validateUpperClassCredits(findClasses) # We send in the regular text 
                upperDivisonCreditsCounter += creditsValue
        except: pass
    return True

# The purpose of this function is to validate the number of credits for the upper division class
@staticmethod
def validateUpperClassCredits(modifiedClassLine) -> float:
    indexCounter = 0
    creditsEarned = ""
    while not (modifiedClassLine[indexCounter] >= '0' and modifiedClassLine[indexCounter] <= '9'): indexCounter += 1
    while (modifiedClassLine[indexCounter] >= '0' and modifiedClassLine[indexCounter] <= '9') or modifiedClassLine[indexCounter] == '.': indexCounter += 1
    while not (modifiedClassLine[indexCounter] >= '0' and modifiedClassLine[indexCounter] <= '9'): indexCounter += 1
    while (modifiedClassLine[indexCounter] >= '0' and modifiedClassLine[indexCounter] <= '9') or modifiedClassLine[indexCounter] == '.': 
        creditsEarned += modifiedClassLine[indexCounter]
        indexCounter += 1
    try:
        if float(creditsEarned) != 0.000: return float(creditsEarned)
    except:
        sys.exit("Could not determine the credits earned. Invalid PDF File. Exiting Program")
    return 0.000


# This function creates two threads that both look for the cumulative GPA of the student and the
# cumulative Credits of the student
@staticmethod
def handleCumulativeCreditsandGPA(text, cumulativeInformation) -> dict:
    thread1 = threading.Thread(target=cumulativeGPAThread, args=(text, cumulativeInformation))
    thread2 = threading.Thread(target=cumulativeCreditsThread, args=(text, cumulativeInformation))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return cumulativeInformation

# The thread calling this function is responsible for setting the Cumulative GPA inside the state variable after
# it has finished parsing
@staticmethod
def cumulativeGPAThread(text, cumulativeInformation):
    indexLocation = text.index("Cum GPA:")
    gpaString = ""
    while not (text[indexLocation] >= '0' and text[indexLocation] <= '9'): indexLocation += 1
    while (text[indexLocation] >= '0' and text[indexLocation] <= '9') or text[indexLocation] == '.':
        gpaString += text[indexLocation]
        indexLocation += 1
    cumulativeInformation['Cumulative GPA'] = gpaString 



# The thread calling this function is responsible for setting the Cumulative Credits inside the state variable after
# it has finished parsing
@staticmethod
def cumulativeCreditsThread(text, cumulativeInformation): # We will send in an unmodified text to deal with this 
    indexLocation = text.index("Cum Totals") 
    cumulativeCreditsString = ""
    while not (text[indexLocation] >= '0' and text[indexLocation] <= '9'): indexLocation += 1
    while (text[indexLocation] >= '0' and text[indexLocation] <= '9') or text[indexLocation] == '.': indexLocation += 1
    while not (text[indexLocation] >= '0' and text[indexLocation] <= '9'): indexLocation += 1
    while (text[indexLocation] >= '0' and text[indexLocation] <= '9') or text[indexLocation] == '.': 
        cumulativeCreditsString += text[indexLocation]
        indexLocation += 1
    cumulativeInformation['Cumulative Credits'] = cumulativeCreditsString


# We need to reset these global variables for other sets of transcripts that the user wish to also input. This is so
# we can reset the program to its initial behaviour
def resetGlobalVariablesForCumulativeInformation():
    global _splitterFlag, _upperDivisonCredits
    _splitterFlag = False 
    _upperDivisonCredits = 0.00
    