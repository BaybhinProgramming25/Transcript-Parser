# We define a SBCClassObject to have the following parameters
# This object is going to be put into the state variables for them to be used later 
class SBCCourse:
    def __init__(self, sbc, courseName, grade, credits, term, year, comments): 
        self.sbc = sbc 
        self.courseName = courseName
        self.grade = grade
        self.credits = credits
        self.term = term
        self.year = year
        self.comments = comments
    
    def to_json(self):
        return  {
                'sbc': self.sbc,
                'courseName': self.courseName,
                'grade': self.grade,
                'credits': self.credits,
                'term': self.term,
                'year': self.year,
                'comments': self.comments
                }