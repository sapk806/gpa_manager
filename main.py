from src.database import Database
from src.calculations import Calculator

def run(db_path):
    db = Database(db_path)
    calc = Calculator()
    running = True
    while running:
        user_choice = input("What would you like to do?: ").upper()
        match user_choice:
            case "ADD COURSE":
                add_course_name = input("Enter course name: ")
                add_course_credits = int(input("How many credits is this course worth?: "))
                db.add_course(add_course_name, add_course_credits)
                while True:
                    try:
                        n_categories = int(input("How many categories are weighted?: "))
                        break
                    except:
                        print("Enter a valid number.")

                for i in range(n_categories):
                    add_category_name = input(f"Enter category {i+1} name: ")
                    add_categeory_weight = float(input(f"Enter category {i+1} weight: "))
                    db.add_weightings(add_course_name, add_category_name, add_categeory_weight)

                cutoffs = []
                for i in range(4):
                    add_category_gpa_cutoff = int(input(f"What is the minimum grade for grade {chr(i+1+64)}: "))
                    cutoffs.append(add_category_gpa_cutoff)
                db.add_gpa_cutoffs(cutoffs, add_course_name)

            case "ADD ASSIGNMENT":
                add_assignment_course = input("What course is this assignment for?: ")
                add_assignment_name = input("Enter assignment name:")
                add_assignment_category = input("What category is the assignment?: ")
                while True:
                    try:
                        add_assignment_earned_points = float(input("How many points did you earn?: "))
                        add_assignment_max_points = float(input("How many points was it out of?: "))
                        break
                    except:
                        print("Enter a valid number.")
                db.add_assignment(add_assignment_course, add_assignment_name, add_assignment_category,
                                  add_assignment_earned_points, add_assignment_max_points)
            case "REMOVE ASSIGNMENT":
                remove_assignment_name = input("Enter assignemnt name: ")
                remove_assignment_course = input("Enter assignment course name: ")
                db.remove_assignment(remove_assignment_course, remove_assignment_name)
            case "REMOVE COURSE":
                remove_course_name = input("What course would you like to remove?: ")
                db.remove_course(remove_course_name)
            case "CHECK COURSE GRADES":
                check_course_name = input("What course would you like to look at?: ")
                overview = db.course_overview(check_course_name)
                print(overview)
            case "CHECK COURSE FINAL GRADE":
                course_final_grade_name = input("What course would you like to look at?: ")
                final_grade = calc.course_grade(db.course_overview(course_final_grade_name))
                letter_grade = db.get_letter_grade(course_final_grade_name, float(final_grade))
                print(f"Final Grade: {round(final_grade, 2)}%\nLetter Grade: {str(letter_grade[0][0])}")
            case "CALCULATE OVERALL GPA":
                print(calc.overall_gpa(db.get_all_letter_grade()))
            case "QUIT":
                db.close()
                break

if __name__ == "__main__":
    run("gpa.db")