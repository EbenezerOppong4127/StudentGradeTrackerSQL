# SQL Relational Database — Student Grade Tracker

**Name:** Tro Opong Ebenezer Jules Samuel
**Date:** June 2026
**Course:** CSE 310 Applied Programming — BYU-Idaho

## Demo Video
https://youtu.be/pJxB8kwChUE

## Overview
This program is a command-line Student Grade Tracker that uses a SQLite relational database to store and manage student records. It lets users add students to courses, view their grades, update records, and delete entries through a numbered menu. The program demonstrates all core SQL operations — INSERT, SELECT, UPDATE, DELETE, JOIN, and aggregate functions — using Python's built-in sqlite3 library.

## Relational Database
This program uses a SQLite database (grades.db) with the following tables:

| Table | Purpose |
|-------|---------|
| students | Stores student name, course, grade, and date added |
| courses | Stores course name and instructor name |

The two tables are related by course_id (foreign key in students → id in courses).

## Features
- Add a new student with name, course, and grade
- View all students in a formatted table
- Update any student's grade by ID
- Delete a student record by ID
- View students with full course info (JOIN query)
- View statistics per course (COUNT and AVG aggregate functions)

## How to Run
1. Make sure Python 3 is installed
2. No extra libraries needed (sqlite3 is built into Python)
3. Run: `python main.py`
4. The database file `grades.db` will be created automatically on first run

## SQL Operations Demonstrated
| Operation | Description |
|-----------|-------------|
| INSERT | Add a new student record |
| SELECT | Query and display all students |
| UPDATE | Modify a student's grade |
| DELETE | Remove a student record |
| JOIN | Link students table with courses table |
| COUNT / AVG | Aggregate statistics per course |

## Time Log
| Day | Task | Hours |
|-----|------|-------|
| Mon Week 1 | Read SQLite3 docs, watch SQL YouTube tutorial, install DB Browser | 3 |
| Tue Week 1 | Set up project, GitHub repo, create tables in Python | 3 |
| Wed Week 1 | Write INSERT and SELECT functions, test with sample data | 3 |
| Thu Week 1 | Build main menu loop, connect all functions | 2 |
| Fri Week 1 | Write UPDATE, DELETE, test all 4 CRUD operations end-to-end | 3 |
| Sat Week 1 | Research JOIN and aggregate functions in SQLite | 2 |
| Mon Week 2 | Implement JOIN query and statistics function | 3 |
| Tue Week 2 | Add seed data, test JOIN with real data | 3 |
| Wed Week 2 | Add comments to all functions, verify 100+ lines | 3 |
| Thu Week 2 | Record 4-5 min video with Zoom, upload to YouTube | 2 |
| Fri Week 2 | Complete README, final GitHub push, submit on Canvas | 1 |
| Sat Week 2 | Post in Microsoft Teams, review peer videos | 1 |
| **Total** | | **29 hrs** |

## Learning Reflection
**What strategies helped you learn SQLite and Python sqlite3?**
Reading the official Python sqlite3 documentation gave me a solid foundation for understanding how to connect, query, and close the database correctly. Watching YouTube tutorials on relational database design helped me understand why foreign keys matter and how JOIN queries work across tables. I also practiced by building small isolated test scripts — just one table, one query — before combining everything into the full program. Typing out each SQL statement manually instead of copying and pasting forced me to actually read and understand the syntax. Finally, using DB Browser for SQLite to inspect the grades.db file visually made it much easier to catch mistakes in my table structure.

**What would you do differently?**
I would plan the database schema on paper before writing any code, because I had to revise my table structure mid-project when I realized I needed the foreign key relationship. I would also add input validation earlier rather than at the end, since invalid inputs caused confusing bugs during testing that took extra time to trace back to the source.
