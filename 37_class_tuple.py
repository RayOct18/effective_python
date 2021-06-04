from collections import namedtuple, defaultdict

Grade = namedtuple('Grade', ('score', 'weight'))

class Subject:
    def __init__(self):
        self._grades = []
    
    def report_grade(self, score, weight):
        self._grades.append(Grade(score, weight))
    
    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self):
        self._subjects = defaultdict(Subject)
    
    def get_subject(self, name):
        return self._subjects[name]
    
    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class Gradebook:
    def __init__(self):
        self._students = defaultdict(Student)
    
    def get_student(self, name):
        return self._students[name]


if __name__ == '__main__':
    gradebook = Gradebook()
    john = gradebook.get_student('John')
    math = john.get_subject('Math')
    math.report_grade(90, 0.7)
    math.report_grade(70, 0.3)
    gym = john.get_subject('Gym')
    gym.report_grade(95, 0.4)
    gym.report_grade(60, 0.6)
    print(john.average_grade())