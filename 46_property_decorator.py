

class Grade2:
    def __init__(self):
        self._value = 0
    
    def __get__(self):
        return self._value
    
    def __set__(self, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100.')
        self._value = value


class Exam2:
    def __init__(self):
        # create different object when Exam2 is created
        self.math_grade = Grade2()
        self.writing_grade = Grade2()
        self.science_grade = Grade2()


class Grade:
    # use dictionary to save different instance's value
    def __init__(self):
        self._value = {}
    
    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._value.get(instance, 0)
    
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100.')
        self._value[instance] = value


class Exam:
    # use same object
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


if __name__ == '__main__':
    first_exam = Exam()
    first_exam.writing_grade = 82
    first_exam.science_grade = 99
    print('Writing', first_exam.writing_grade)
    print('Science', first_exam.science_grade)

    second_exam = Exam()
    second_exam.writing_grade = 88
    second_exam.science_grade = 95
    print('Writing', second_exam.writing_grade)
    print('Science', second_exam.science_grade)

    print('Writing', first_exam.writing_grade)
    print('Science', first_exam.science_grade)

    print('=' * 20)

    first_exam = Exam2()
    first_exam.writing_grade = 82
    first_exam.science_grade = 99
    print('Writing', first_exam.writing_grade)
    print('Science', first_exam.science_grade)

    second_exam = Exam2()
    second_exam.writing_grade = 88
    second_exam.science_grade = 95
    print('Writing', second_exam.writing_grade)
    print('Science', second_exam.science_grade)

    print('Writing', first_exam.writing_grade)
    print('Science', first_exam.science_grade)