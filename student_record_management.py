import csv
import json
from pathlib import Path

DATA_DIR = Path("data")
CSV_FILE = DATA_DIR / "students.csv"
JSON_FILE = DATA_DIR / "students.json"
FIELDS = ["id", "name", "age", "course", "email", "marks"]


def setup_files():
    DATA_DIR.mkdir(exist_ok=True)
    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=FIELDS).writeheader()
    if not JSON_FILE.exists():
        JSON_FILE.write_text("[]", encoding="utf-8")


def load_students():
    try:
        data = json.loads(JSON_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError) as e:
        print(f"Could not read data: {e}")
        return []


def save_students(students):
    try:
        JSON_FILE.write_text(json.dumps(students, indent=4), encoding="utf-8")
        with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(students)
    except OSError as e:
        print(f"Could not save data: {e}")


def get_next_id(students):
    ids = [int(s["id"]) for s in students if str(s.get("id", "")).isdigit()]
    return str(max(ids, default=0) + 1)


def get_number(prompt, minimum, maximum, kind=int):
    while True:
        try:
            value = kind(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def add_student():
    students = load_students()
    student = {
        "id": get_next_id(students),
        "name": input("Name: ").strip(),
        "age": get_number("Age: ", 1, 120),
        "course": input("Course: ").strip(),
        "email": input("Email: ").strip(),
        "marks": get_number("Marks (0-100): ", 0, 100, float)
    }
    if not all([student["name"], student["course"], student["email"]]):
        print("Name, course and email cannot be empty.")
        return
    students.append(student)
    save_students(students)
    print(f"Student added successfully. ID: {student['id']}")


def display_students(students=None):
    students = load_students() if students is None else students
    if not students:
        print("No student records found.")
        return
    print("\n" + "=" * 90)
    print(f"{'ID':<5}{'Name':<20}{'Age':<6}{'Course':<18}{'Email':<28}{'Marks':<8}")
    print("-" * 90)
    for s in students:
        print(f"{s['id']:<5}{s['name'][:18]:<20}{s['age']:<6}{s['course'][:16]:<18}{s['email'][:26]:<28}{s['marks']:<8}")
    print("=" * 90)


def find_student(student_id, students):
    return next((s for s in students if str(s["id"]) == str(student_id)), None)


def update_student():
    students = load_students()
    student = find_student(input("Student ID: ").strip(), students)
    if not student:
        print("Student not found.")
        return
    print("Press Enter to keep the current value.")
    name = input(f"Name [{student['name']}]: ").strip()
    course = input(f"Course [{student['course']}]: ").strip()
    email = input(f"Email [{student['email']}]: ").strip()
    marks = input(f"Marks [{student['marks']}]: ").strip()
    if name: student["name"] = name
    if course: student["course"] = course
    if email: student["email"] = email
    if marks:
        try:
            value = float(marks)
            if not 0 <= value <= 100: raise ValueError
            student["marks"] = value
        except ValueError:
            print("Invalid marks; old value kept.")
    save_students(students)
    print("Student updated successfully.")


def delete_student():
    students = load_students()
    student = find_student(input("Student ID: ").strip(), students)
    if not student:
        print("Student not found.")
        return
    students.remove(student)
    save_students(students)
    print("Student deleted successfully.")


def search_students():
    students = load_students()
    keyword = input("Search name/course/email: ").strip().lower()
    results = [s for s in students if keyword in s["name"].lower()
               or keyword in s["course"].lower()
               or keyword in s["email"].lower()]
    display_students(results)


def show_sorted_students():
    students = load_students()
    results = sorted(students, key=lambda s: float(s["marks"]), reverse=True)
    display_students(results)


def menu():
    setup_files()
    while True:
        print("\n===== STUDENT RECORD MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Sort by Marks")
        print("7. Exit")
        try:
            choice = input("Choose an option: ").strip()
            if choice == "1": add_student()
            elif choice == "2": display_students()
            elif choice == "3": search_students()
            elif choice == "4": update_student()
            elif choice == "5": delete_student()
            elif choice == "6": show_sorted_students()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Please choose 1-7.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    menu()
