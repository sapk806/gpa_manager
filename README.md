# GPA Manager
This project allows users to keep track of their grades across multiple courses. Overall number and letter grade can be calculated for each course, and overall GPA can be calculated using all course letter grades. A relational SQLite3 database allows for data to be saved between uses.

## Features
- ADD COURSE: Accepts user input for course name and credits to enter into the courses table, containing course id, name, credits, and GPA. Prompts the user to add assignment categories and their weightings, and GPA cutoffs corresponding with the course.
- ADD ASSIGNMENT: Accepts user input for the course the assignment is associated with, the category the assignment falls under, the name of the assignment, the points earned, and the maximum possible points.
- REMOVE ASSIGNMENT: Accepts user input for the course the assignment is associated with and the name of the assignment, before removing it from the assignments table.
- REMOVE COURSE: Accepts user input for the name of the course requested to be removed, and deletes all dependent entries containing the id of the course across all tables.
- CHECK COURSE GRADES: Returns a DataFrame containing all assignments for the requested course, along with the grade received and weighted grade received.
- CHECK COURSE FINAL GRADE: Returns both the percent and letter grade of the requested course.
- CALCULATE OVERALL GPA: Returns GPA on a 4.0 scale.
- QUIT: Closes the SQLite3 connection and stops the program.

## Technologies Used
- Python
- sqlite3
- Pandas
- NumPy

## Installation
1) Clone or download repository.
2) Navigate to project directory.
3) Install required dependencies(provided in requirements).
4) Run the program using `python main.py`

## Current Limitations and Future Improvements
- Current version blind to -/+ grades. Future improvement involves implementing and accounting for +/- grades in GPA calculation.
- Current version contains very little input validation. Future improvement involves handling more errors pertaining to user input.