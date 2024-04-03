# data.py

import sqlite3

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS STUDENT (
                        ID INTEGER PRIMARY KEY,
                        NAME TEXT,
                        AGE INTEGER,
                        CGPI REAL,
                        SKILLS TEXT,
                        COMPANY TEXT,
                        EMAIL TEXT
                     )''')
        conn.commit()
        conn.close()

    def insert_student(self, id_val, name, age, cgpi, skills, company):  
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("INSERT INTO STUDENT (ID, NAME, AGE, CGPI, SKILLS, COMPANY) VALUES (?, ?, ?, ?, ?, ?)",
                  (id_val, name, age, cgpi, skills, company))
        conn.commit()
        conn.close()

    def fetch_students_placed(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT ID, NAME, AGE, CGPI, SKILLS, COMPANY FROM STUDENT")
        records = c.fetchall()
        conn.close()
        return records

    def fetch_student_by_id(self, student_id):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("SELECT ID, NAME, AGE, CGPI, SKILLS, COMPANY FROM STUDENT WHERE ID=?", (student_id,))
        record = c.fetchone()
        conn.close()
        return record

    def update_student(self, id_val, name, age, cgpi, skills, company):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute("UPDATE STUDENT SET NAME=?, AGE=?, CGPI=?, SKILLS=?, COMPANY=? WHERE ID=?",
                  (name, age, cgpi, skills, company, id_val))
        conn.commit()
        conn.close()

