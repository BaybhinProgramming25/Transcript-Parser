"""
This module is responsible for finding student information, not including 
the student's major and specialization. 

The entire transcript is taken into consideration and extra information,
such as the date and time as to when the program was invoked, is also kept
into the state variable 
"""

from datetime import datetime 


# This module uses module-bounded global variables, as we need to retain the state of these variables 
# for when we are iterating through multiple parts of the transcript so that the program parsing behaviour
# is as intended
_year, _month, _day, _hour, _modifiedHour, _minutes, _timeString, _totalString, _termString, _day_month_yearString = "", "", "", "", "", "", "", "", "", ""
_lastUpdated, _name, _idNumber, _requirementTerm, _cshp, _hoursComplete, _minutesComplete, _PMFlag = False, False, False, False, False, False, False, False
_atYDMSection = True


# Find and store student information that is around different parts of the transcript
def trackStudentInformation(text, studentInformation):
                
                global _year, _month, _day, _hour, _modifiedHour, _minutes, _timeString, _totalString, _termString, _day_month_yearString, _lastUpdated, _name, _idNumber, _requirementTerm, _cshp, _hoursComplete, _minutesComplete, _PMFlag, _atYDMSection

                to_daysDate = str(datetime.now())
                for informationInTo_daysDate in to_daysDate:
                        if _atYDMSection == True and _lastUpdated == False:
                                if informationInTo_daysDate == ' ':
                                        _atYDMSection = False
                                elif len(_year) != 4 and informationInTo_daysDate != '-':
                                        _year += informationInTo_daysDate
                                elif len(_month) != 2 and informationInTo_daysDate != '-':
                                        _month += informationInTo_daysDate
                                elif len(_day) != 2 and informationInTo_daysDate != '-':
                                        _day += informationInTo_daysDate
                        elif _atYDMSection == False and _lastUpdated == False:
                                if len(_hour) != 2 and _hoursComplete == False:
                                        _hour += informationInTo_daysDate
                                        if len(_hour) == 2:
                                                if _hour[0:1] == '0' and _hour[1:2] == '0': # 12 AM
                                                        _hour = "12"
                                                        _hoursComplete = True 
                                                elif _hour[0:1] == '0' and _hour[1:2] != '0': # 1 AM to 9 AM
                                                        _hour = _hour[1:2]
                                                        _hoursComplete = True
                                                elif _hour[0:1] == '1' and (_hour[1:2] == '0' or _hour[1:2] == '1'):
                                                        if _hour[1:2] == '0': _hour = "10"
                                                        else:_hour = "11"
                                                        _hoursComplete = True
                                                else:
                                                        _modifiedHour = str(int(_hour) - 12)
                                                        if _modifiedHour == "0": _modifiedHour = "12" # 12 PM
                                                        _PMFlag = True
                                                        _hoursComplete = True
                                elif len(_minutes) != 2 and informationInTo_daysDate != ':':
                                        _minutes += informationInTo_daysDate
                                        if len(_minutes) == 2:
                                                _minutesComplete = True
                                if _hoursComplete == True and _minutesComplete == True:
                                        if _month[0:1] == '0':
                                                _month = _month[1:2]
                                        if _day[0:1] == '0':
                                                _day = _day[1:2]
                                        _day_month_yearString = _month + "/" + _day + "/" + _year
                                        if _PMFlag == True:
                                                _timeString = _modifiedHour + ":" + _minutes + " PM"
                                        elif _PMFlag == False:
                                                _timeString = _hour + ":" + _minutes + " AM"
                                        _totalString = _day_month_yearString + " " + _timeString
                                        studentInformation['Last Updated'] = _totalString
                                        _lastUpdated = True
                for lineInformation in text:
                        if "Name" in lineInformation and _name == False:
                                name = ""
                                characterFound = False
                                modifiedName = lineInformation.replace("Name:", "")
                                for characters in modifiedName:
                                        if characters != " ":
                                                characterFound = True
                                                name += characters
                                        elif characters == " " and characterFound == True:
                                                name += characters 
                                studentInformation['Name'] = name
                                _name = True
                        elif "Student ID: " in lineInformation and _idNumber == False:
                                modifiedId = lineInformation.replace("Student ID:", "").replace(" ", "")
                                studentInformation["ID Number"] = modifiedId
                                _idNumber = True
                        elif "Fall" in lineInformation and _requirementTerm == False:
                                find_year = lineInformation.replace("Fall", "").replace(" ", "")
                                _termString  = "Fall " + find_year 
                                studentInformation['Requirement Term'] = _termString
                                _requirementTerm = True
                        elif "Spring" in lineInformation and _requirementTerm == False:
                                find_year = lineInformation.replace("Spring", "").replace(" ", "")
                                _termString = "Spring " + find_year
                                studentInformation['Requirement Term'] = _termString
                                _requirementTerm = True                                          
                        if _lastUpdated == True and _name == True and _idNumber == True and _requirementTerm == True: break
                if _cshp == True: #If CSHP, then set to yes
                        studentInformation['CSHP'] = "YES"
                else: #Otherwise, set CSHP to no
                        studentInformation['CSHP'] = "NO" 


# We need to reset these global variables for other sets of transcripts that the user wish to also input. This is so
# we can reset the program to its initial behaviour
def resetGlobalVariablesForStudentInfo():
        global _year, _month, _day, _hour, _modifiedHour, _minutes, _timeString, _totalString, _termString, _day_month_yearString, _lastUpdated, _name, _idNumber, _requirementTerm, _cshp, _hoursComplete, _minutesComplete, _PMFlag, _atYDMSection
        _year, _month, _day, _hour, _modifiedHour, _minutes, _timeString, _totalString, _termString, _day_month_yearString = "", "", "", "", "", "", "", "", "", ""
        _lastUpdated, _name, _idNumber, _requirementTerm, _cshp, _hoursComplete, _minutesComplete, _PMFlag = False, False, False, False, False, False, False, False
        _atYDMSection = True

