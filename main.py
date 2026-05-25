import sqlite3
from datetime import date

DB_NAME = "grades.db"


def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def create_tables():
    """Create the students and courses tables if they do not already exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Create courses table first since students references it
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            instructor TEXT NOT NULL
        )
    """)

    # Create students table with a foreign key to courses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            grade REAL NOT NULL,
            date_added TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)

    conn.commit()
    conn.close()


def seed_courses():
    """Insert three default courses if the courses table is empty."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check how many courses already exist
    cursor.execute("SELECT COUNT(*) FROM courses")
    count = cursor.fetchone()[0]

    if count == 0:
        # INSERT three sample courses so the app has real data on first run
        sample_courses = [
            (1, "CSE 310 Applied Programming", "Brother Smith"),
            (2, "CSE 111 Programming with Functions", "Sister Jones"),
            (3, "CSE 212 Programming with Data Structures", "Brother Williams"),
        ]
        cursor.executemany(
            "INSERT INTO courses (id, course_name, instructor) VALUES (?, ?, ?)",
            sample_courses,
        )
        conn.commit()
        print("Sample courses loaded into the database.")

    conn.close()


def display_courses(cursor):
    """Print the available courses so the user can pick a course_id."""
    cursor.execute("SELECT id, course_name, instructor FROM courses")
    courses = cursor.fetchall()
    print("\n  Available Courses:")
    print(f"  {'ID':<5} {'Course Name':<45} {'Instructor'}")
    print("  " + "-" * 70)
    for row in courses:
        print(f"  {row[0]:<5} {row[1]:<45} {row[2]}")
    return courses


def add_student():
    """Prompt the user for a name, course, and grade, then INSERT a new student row."""
    conn = get_connection()
    cursor = conn.cursor()

    print("\n--- Add a Student ---")
    display_courses(cursor)

    name = input("\n  Enter student name: ").strip()
    if not name:
        print("  Name cannot be empty.")
        conn.close()
        return

    try:
        course_id = int(input("  Enter course ID from the list above: "))
    except ValueError:
        print("  Invalid course ID.")
        conn.close()
        return

    # Verify the chosen course_id actually exists
    cursor.execute("SELECT id FROM courses WHERE id = ?", (course_id,))
    if cursor.fetchone() is None:
        print("  That course ID does not exist.")
        conn.close()
        return

    try:
        grade = float(input("  Enter grade (0.0 - 100.0): "))
    except ValueError:
        print("  Invalid grade value.")
        conn.close()
        return

    today = date.today().isoformat()  # e.g. '2026-05-25'

    # INSERT the new student record into the students table
    cursor.execute(
        "INSERT INTO students (name, course_id, grade, date_added) VALUES (?, ?, ?, ?)",
        (name, course_id, grade, today),
    )
    conn.commit()
    print(f"  Student '{name}' added successfully (ID: {cursor.lastrowid}).")
    conn.close()


def view_all_students():
    """SELECT all rows from students and display them in a formatted table."""
    conn = get_connection()
    cursor = conn.cursor()

    # Retrieve every student record ordered by id
    cursor.execute("SELECT id, name, course_id, grade, date_added FROM students ORDER BY id")
    rows = cursor.fetchall()

    print("\n--- All Students ---")
    if not rows:
        print("  No students found.")
        conn.close()
        return

    print(f"  {'ID':<6} {'Name':<25} {'Course ID':<12} {'Grade':<8} {'Date Added'}")
    print("  " + "-" * 65)
    for row in rows:
        print(f"  {row[0]:<6} {row[1]:<25} {row[2]:<12} {row[3]:<8.1f} {row[4]}")

    conn.close()


def update_grade():
    """UPDATE a student's grade in the students table, identified by student ID."""
    conn = get_connection()
    cursor = conn.cursor()

    print("\n--- Update a Student Grade ---")
    view_all_students()

    try:
        student_id = int(input("\n  Enter the student ID to update: "))
    except ValueError:
        print("  Invalid ID.")
        conn.close()
        return

    # Confirm the student exists before attempting the update
    cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
    result = cursor.fetchone()
    if result is None:
        print("  No student found with that ID.")
        conn.close()
        return

    try:
        new_grade = float(input(f"  Enter new grade for '{result[0]}': "))
    except ValueError:
        print("  Invalid grade.")
        conn.close()
        return

    # UPDATE only the grade column for the matching student
    cursor.execute(
        "UPDATE students SET grade = ? WHERE id = ?",
        (new_grade, student_id),
    )
    conn.commit()
    print(f"  Grade updated to {new_grade} for '{result[0]}'.")
    conn.close()


def delete_student():
    """DELETE a student row from the students table by ID."""
    conn = get_connection()
    cursor = conn.cursor()

    print("\n--- Delete a Student ---")
    view_all_students()

    try:
        student_id = int(input("\n  Enter the student ID to delete: "))
    except ValueError:
        print("  Invalid ID.")
        conn.close()
        return

    # Check the student exists so we can confirm who will be removed
    cursor.execute("SELECT name FROM students WHERE id = ?", (student_id,))
    result = cursor.fetchone()
    if result is None:
        print("  No student found with that ID.")
        conn.close()
        return

    confirm = input(f"  Delete '{result[0]}'? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Deletion cancelled.")
        conn.close()
        return

    # DELETE the student record permanently
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    print(f"  Student '{result[0]}' deleted.")
    conn.close()


def view_with_join():
    """
    SELECT student name, course name, instructor, and grade using an
    INNER JOIN between students and courses on course_id = courses.id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    print("\n--- Students with Course Info (JOIN) ---")

    # JOIN students to courses to display human-readable course names
    cursor.execute("""
        SELECT students.name,
               courses.course_name,
               courses.instructor,
               students.grade
        FROM students
        JOIN courses ON students.course_id = courses.id
        ORDER BY students.id
    """)
    rows = cursor.fetchall()

    if not rows:
        print("  No student records found.")
        conn.close()
        return

    print(f"  {'Student Name':<25} {'Course':<45} {'Instructor':<20} {'Grade'}")
    print("  " + "-" * 100)
    for row in rows:
        print(f"  {row[0]:<25} {row[1]:<45} {row[2]:<20} {row[3]:.1f}")

    conn.close()


def view_statistics():
    """
    Display per-course statistics using aggregate functions COUNT and AVG,
    joining courses to students and grouping by course id.
    """
    conn = get_connection()
    cursor = conn.cursor()

    print("\n--- Course Statistics (COUNT / AVG) ---")

    # Aggregate: count enrolled students and compute their average grade per course
    cursor.execute("""
        SELECT courses.course_name,
               COUNT(students.id)   AS num_students,
               AVG(students.grade)  AS avg_grade
        FROM courses
        JOIN students ON students.course_id = courses.id
        GROUP BY courses.id
        ORDER BY courses.id
    """)
    rows = cursor.fetchall()

    if not rows:
        print("  No data available (add students first).")
        conn.close()
        return

    print(f"  {'Course':<45} {'Students':<12} {'Avg Grade'}")
    print("  " + "-" * 70)
    for row in rows:
        avg = row[2] if row[2] is not None else 0.0
        print(f"  {row[0]:<45} {row[1]:<12} {avg:.2f}")

    conn.close()


def main_menu():
    """Display the main menu in a loop and dispatch to the appropriate function."""
    print("\n" + "=" * 50)
    print("   Student Grade Tracker -- SQLite Edition")
    print("=" * 50)

    # Set up the database and seed data once at startup
    create_tables()
    seed_courses()

    while True:
        print("\n  1. Add a student")
        print("  2. View all students")
        print("  3. Update a student grade")
        print("  4. Delete a student")
        print("  5. View students with course info (JOIN)")
        print("  6. View course statistics (COUNT / AVG)")
        print("  7. Exit")

        choice = input("\n  Select an option (1-7): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            update_grade()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            view_with_join()
        elif choice == "6":
            view_statistics()
        elif choice == "7":
            print("\n  Goodbye! Database connection closed.\n")
            break
        else:
            print("  Invalid option. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main_menu()
