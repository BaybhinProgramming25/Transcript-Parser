# We define a UniversalClassObject to have the following parameters
# This object is going to be put into the state variables for them to be used later 
class UniversalClassObject: 
    def __init__(self, courseName, grade, credits, term, year, comments): 
        self.courseName = courseName
        self.grade = grade
        self.credits = credits
        self.term = term
        self.year = year
        self.comments = comments
    