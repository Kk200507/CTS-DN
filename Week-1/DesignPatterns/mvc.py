"""Week-1 MVC example showing how model, view, and controller work together."""

# =====================================================================
# Model
# =====================================================================
# The model stores the data and business rules.


class Student:
    def __init__(self, name: str, roll_no: int) -> None:
        self.name = name
        self.roll_no = roll_no


# =====================================================================
# View
# =====================================================================
# The view displays the model data.


class StudentView:
    def show_student(self, student: Student) -> None:
        print(f"Student Name: {student.name}")
        print(f"Roll Number: {student.roll_no}")


# =====================================================================
# Controller
# =====================================================================
# The controller updates the model and asks the view to display it.


class StudentController:
    def __init__(self, student: Student, view: StudentView) -> None:
        self.student = student
        self.view = view

    def set_student_name(self, name: str) -> None:
        self.student.name = name

    def set_student_roll_no(self, roll_no: int) -> None:
        self.student.roll_no = roll_no

    def update_view(self) -> None:
        self.view.show_student(self.student)


def main() -> None:
    student = Student("Asha", 101)
    view = StudentView()
    controller = StudentController(student, view)

    print("Initial student data")
    controller.update_view()

    print("\nUpdated student data")
    controller.set_student_name("Rahul")
    controller.set_student_roll_no(102)
    controller.update_view()


if __name__ == "__main__":
    main()
