class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.courses = []  # list of course names the student is enrolled in

    def display_info(self):
        print(f"Student Name: {self.name}, ID: {self.student_id}")

    def enroll(self, course_name: str):
        # avoid duplicate enrollments
        if course_name in self.courses:
            print(f"{self.name} is already enrolled in {course_name}.")
            return
        self.courses.append(course_name)
        print(f"{self.name} has enrolled in {course_name}.")

    def drop(self, course_name: str):
        if course_name in self.courses:
            self.courses.remove(course_name)
            print(f"{self.name} has dropped {course_name}.")
        else:
            print(f"{self.name} is not enrolled in {course_name}.")

    def list_courses(self):
        if not self.courses:
            print(f"{self.name} is not enrolled in any courses.")
            return
        print(f"{self.name}'s courses: " + ", ".join(self.courses))



