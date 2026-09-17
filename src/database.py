import sqlite3
import pandas as pd

class Database():
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.create_tables()

    def close(self):
        self.connection.close()

    def create_tables(self):
        self.connection.execute("PRAGMA foreign_keys = ON;")
        
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY,
                credits INTEGER,
                course_name TEXT,
                current_letter_grade TEXT
            );
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
                assignment_id INTEGER PRIMARY KEY,
                assignment_name TEXT,
                category TEXT,
                earned_points FLOAT,
                max_points FLOAT
            );
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS weightings (
                weighting_id INTEGER PRIMARY KEY,
                course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
                category TEXT,
                weight FLOAT
            );
        """)
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS gpa_cutoffs (
                gpa_id INTEGER PRIMARY KEY,
                course_id INTEGER REFERENCES courses(course_id) ON DELETE CASCADE,
                A INTEGER,
                B INTEGER,
                C INTEGER,
                D INTEGER,
                UNIQUE (course_id)
            )
        """)
        self.connection.commit()

    def add_course(self, course_name: str, course_credits: int):
        query = """
            INSERT INTO courses (course_name, credits)
            VALUES (?, ?);
        """
        try: 
            self.connection.execute(query, (course_name, course_credits))
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def remove_course(self, course_name: str):
        """Remove a course and it's dependent entries."""

        query = """
            DELETE FROM courses
            WHERE course_name = ?;
        """
        try:
            self.connection.execute(query, (course_name,))
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def add_assignment(self, course_name: str, assignment_name: str, category: str, points_earned: int, max_points: int):
        query="""
            INSERT INTO assignments (assignment_name, category, earned_points, max_points, course_id)
            VALUES (?, ?, ?, ?, ?);
        """
        data = (assignment_name, category, points_earned, max_points, self.connection.execute("""
            SELECT course_id FROM courses
            WHERE course_name = ?;
        """, (course_name,)).fetchall()[0][0],)
        try:
            self.connection.execute(query, data)
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def remove_assignment(self, course_name, assignment_name):
        query = """
            DELETE FROM assignments
            WHERE assignment_name = ? AND course_id = ?;
        """
        try:
            self.connection.execute(query, (assignment_name, self.connection.execute("""SELECT course_id FROM courses WHERE course_name = ?""", (course_name,)).fetchall()[0][0]))
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def add_weightings(self, course_name, category, weight):
        query = """
            INSERT INTO weightings (category, weight, course_id)
            VALUES (?, ?, ?);
        """
        data = (category, weight, self.connection.execute("""
            SELECT course_id 
            FROM courses
            WHERE course_name = (?);
        """, (course_name,)).fetchall()[0][0],)
        try:
            self.connection.execute(query, data)
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def add_gpa_cutoffs(self, cutoffs: list, course_name: str):
        query = """
        INSERT INTO gpa_cutoffs (course_id, A, B, C, D)
        VALUES (?, ?, ?, ?, ?);
        """
        data = (self.connection.execute("""
            SELECT course_id
            FROM courses
            WHERE course_name = ?
        """, (course_name,)).fetchall()[0][0], cutoffs[0], cutoffs[1], cutoffs[2], cutoffs[3])
        try:
            self.connection.execute(query, data)
            self.connection.commit()
        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def course_overview(self, course_name):
        """Returns a DataFrame containing every assigment associated to a given course, and the raw and weighted grade received."""

        query = """
            SELECT assignments.assignment_name, assignments.assignment_id, 
            assignments.category, assignments.earned_points, assignments.max_points, 
            weightings.weight, (earned_points/max_points*100) AS grade,
            (earned_points/max_points * 100) * weightings.weight AS weighted_grade
        
            FROM assignments
            JOIN weightings 
                ON assignments.course_id = weightings.course_id AND assignments.category = weightings.category
            WHERE assignments.course_id = ?;
        """
        data = (self.connection.execute("""
            SELECT course_id
            FROM courses
            WHERE course_name = ?;
        """, (course_name,)).fetchall()[0][0],)

        return pd.read_sql_query(query, self.connection, params=(data), index_col="assignment_id")

    def get_letter_grade(self, course_name, final_grade):
        course_id = self.connection.execute("""
            SELECT course_id
            FROM courses
            WHERE course_name = ?
        """, (course_name,)).fetchall()[0][0]

        query = """
            SELECT 
                CASE
                    WHEN A <= :grade THEN 'A'
                    WHEN B <= :grade THEN 'B'
                    WHEN C <= :grade THEN 'C'
                    WHEN D <= :grade THEN 'D'
                    ELSE 'F'
                END AS letter_grade
            FROM gpa_cutoffs
            WHERE course_id = :id;
        """
        data = ({"id": course_id, "grade": final_grade})
        try:
            letter_grade = self.connection.execute(query, data).fetchall()[0][0]
            print(letter_grade)
            data = ({"id": course_id, "letter": letter_grade})
            self.connection.execute("""
                UPDATE courses
                SET current_letter_grade = :letter
                WHERE course_id = :id;
        """, data)
            self.connection.commit()
            return letter_grade

        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Error: {e}")

    def get_all_letter_grade(self):
        return self.connection.execute("""SELECT current_letter_grade, credits FROM courses""").fetchall()

    def test(self):
        print(self.connection.execute("""SELECT * FROM courses""").fetchall())
        print(self.connection.execute("""SELECT * FROM assignments""").fetchall())
        print(self.connection.execute("""SELECT * FROM weightings""").fetchall())
        print(self.connection.execute("""SELECT * FROM gpa_cutoffs""").fetchall())
