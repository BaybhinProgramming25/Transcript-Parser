# We define a SimpleClassObject to have the following parameters
# This object is going to be put into the state variables for them to be used later 
class SimpleClassObject:
    def __init__(self, courseName, credits, grade, term, year):
        self.courseName = courseName
        self.credits = credits
        self.grade = grade
        self.term = term
        self.year = year
    
    def to_json(self):
        return  {'courseName': self.courseName, 'credits': self.credits, 'grade': self.grade, 'term': self.term, 'year': self.year }