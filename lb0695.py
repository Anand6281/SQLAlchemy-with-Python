import mysql.connector
from mysql.connector import Error
def connect_to_database(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_tables(conn):
    cursor = conn.cursor()

    # SQL statements to create tables
    create_table_sql = """
    create table classroom(building		varchar(15),
	 room_number		varchar(7),
	 capacity		numeric(4,0),
	 primary key (building, room_number)
	);
create table department
	(dept_name		varchar(20), 
	 building		varchar(15), 
	 budget		        numeric(12,2) check (budget > 0),
	 primary key (dept_name)
	);
create table course
	(course_id		varchar(8), 
	 title			varchar(50), 
	 dept_name		varchar(20),
	 credits		numeric(2,0) check (credits > 0),
	 primary key (course_id),
	 foreign key (dept_name) references department (dept_name)
		on delete set null
	);
create table instructor
	(ID			varchar(5), 
	 name			varchar(20) not null, 
	 dept_name		varchar(20), 
	 salary			numeric(8,2) check (salary > 29000),
	 primary key (ID),
	 foreign key (dept_name) references department (dept_name)
		on delete set null
	);
create table section
	(course_id		varchar(8), 
         sec_id			varchar(8),
	 semester		varchar(6)
		check (semester in ('Fall', 'Winter', 'Spring', 'Summer')), 
	 year			numeric(4,0) check (year > 1701 and year < 2100), 
	 building		varchar(15),
	 room_number		varchar(7),
	 time_slot_id		varchar(4),
	 primary key (course_id, sec_id, semester, year),
	 foreign key (course_id) references course (course_id)
		on delete cascade,
	 foreign key (building, room_number) references classroom (building, room_number)
		on delete set null
	);
create table teaches
	(ID			varchar(5), 
	 course_id		varchar(8),
	 sec_id			varchar(8), 
	 semester		varchar(6),
	 year			numeric(4,0),
	 primary key (ID, course_id, sec_id, semester, year),
	 foreign key (course_id, sec_id, semester, year) references section (course_id, sec_id, semester, year)
		on delete cascade,
	 foreign key (ID) references instructor (ID)
		on delete cascade
	);
create table student
	(ID			varchar(5), 
	 name			varchar(20) not null, 
	 dept_name		varchar(20), 
	 tot_cred		numeric(3,0) check (tot_cred >= 0),
	 primary key (ID),
	 foreign key (dept_name) references department (dept_name)
		on delete set null
	);
create table takes
	(ID			varchar(5), 
	 course_id		varchar(8),
	 sec_id			varchar(8), 
	 semester		varchar(6),
	 year			numeric(4,0),
	 grade		        varchar(2),
	 primary key (ID, course_id, sec_id, semester, year),
	 foreign key (course_id, sec_id, semester, year) references section (course_id, sec_id, semester, year)
		on delete cascade,
	 foreign key (ID) references student (ID)
		on delete cascade
	);
create table advisor
	(s_ID			varchar(5),
	 i_ID			varchar(5),
	 primary key (s_ID),
	 foreign key (i_ID) references instructor (ID)
		on delete set null,
	 foreign key (s_ID) references student (ID)
		on delete cascade
	);
create table time_slot
	(time_slot_id		varchar(4),
	 day			varchar(1),
	 start_hr		numeric(2) check (start_hr >= 0 and start_hr < 24),
	 start_min		numeric(2) check (start_min >= 0 and start_min < 60),
	 end_hr			numeric(2) check (end_hr >= 0 and end_hr < 24),
	 end_min		numeric(2) check (end_min >= 0 and end_min < 60),
	 primary key (time_slot_id, day, start_hr, start_min)
	);
create table prereq
	(course_id		varchar(8), 
	 prereq_id		varchar(8),
	 primary key (course_id, prereq_id),
	 foreign key (course_id) references course (course_id)
		on delete cascade,
	 foreign key (prereq_id) references course (course_id)
	);
    """

    for query in create_table_sql.split(';'):
        try:
            cursor.execute(query)
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn.rollback()

def insert_data(conn):
    cursor = conn.cursor()

    # SQL statements to insert data
    insert_data_sql = """
delete from prereq;
delete from time_slot;
delete from advisor;
delete from takes;
delete from student;
delete from teaches;
delete from section;
delete from instructor;
delete from course;
delete from department;
delete from classroom;
insert into classroom values ('Packard', '101', '500');
insert into classroom values ('Painter', '514', '10');
insert into classroom values ('Taylor', '3128', '70');
insert into classroom values ('Watson', '100', '30');
insert into classroom values ('Watson', '120', '50');
insert into department values ('Biology', 'Watson', '90000');
insert into department values ('Comp. Sci.', 'Taylor', '100000');
insert into department values ('Elec. Eng.', 'Taylor', '85000');
insert into department values ('Finance', 'Painter', '120000');
insert into department values ('History', 'Painter', '50000');
insert into department values ('Music', 'Packard', '80000');
insert into department values ('Physics', 'Watson', '70000');
insert into course values ('BIO-101', 'Intro. to Biology', 'Biology', '4');
insert into course values ('BIO-301', 'Genetics', 'Biology', '4');
insert into course values ('BIO-399', 'Computational Biology', 'Biology', '3');
insert into course values ('CS-101', 'Intro. to Computer Science', 'Comp. Sci.', '4');
insert into course values ('CS-190', 'Game Design', 'Comp. Sci.', '4');
insert into course values ('CS-315', 'Robotics', 'Comp. Sci.', '3');
insert into course values ('CS-319', 'Image Processing', 'Comp. Sci.', '3');
insert into course values ('CS-347', 'Database System Concepts', 'Comp. Sci.', '3');
insert into course values ('EE-181', 'Intro. to Digital Systems', 'Elec. Eng.', '3');
insert into course values ('FIN-201', 'Investment Banking', 'Finance', '3');
insert into course values ('HIS-351', 'World History', 'History', '3');
insert into course values ('MU-199', 'Music Video Production', 'Music', '3');
insert into course values ('PHY-101', 'Physical Principles', 'Physics', '4');
insert into instructor values ('10101', 'Srinivasan', 'Comp. Sci.', '65000');
insert into instructor values ('12121', 'Wu', 'Finance', '90000');
insert into instructor values ('15151', 'Mozart', 'Music', '40000');
insert into instructor values ('22222', 'Einstein', 'Physics', '95000');
insert into instructor values ('32343', 'El Said', 'History', '60000');
insert into instructor values ('33456', 'Gold', 'Physics', '87000');
insert into instructor values ('45565', 'Katz', 'Comp. Sci.', '75000');
insert into instructor values ('58583', 'Califieri', 'History', '62000');
insert into instructor values ('76543', 'Singh', 'Finance', '80000');
insert into instructor values ('76766', 'Crick', 'Biology', '72000');
insert into instructor values ('83821', 'Brandt', 'Comp. Sci.', '92000');
insert into instructor values ('98345', 'Kim', 'Elec. Eng.', '80000');
insert into section values ('BIO-101', '1', 'Summer', '2017', 'Painter', '514', 'B');
insert into section values ('BIO-301', '1', 'Summer', '2018', 'Painter', '514', 'A');
insert into section values ('CS-101', '1', 'Fall', '2017', 'Packard', '101', 'H');
insert into section values ('CS-101', '1', 'Spring', '2018', 'Packard', '101', 'F');
insert into section values ('CS-190', '1', 'Spring', '2017', 'Taylor', '3128', 'E');
insert into section values ('CS-190', '2', 'Spring', '2017', 'Taylor', '3128', 'A');
insert into section values ('CS-315', '1', 'Spring', '2018', 'Watson', '120', 'D');
insert into section values ('CS-319', '1', 'Spring', '2018', 'Watson', '100', 'B');
insert into section values ('CS-319', '2', 'Spring', '2018', 'Taylor', '3128', 'C');
insert into section values ('CS-347', '1', 'Fall', '2017', 'Taylor', '3128', 'A');
insert into section values ('EE-181', '1', 'Spring', '2017', 'Taylor', '3128', 'C');
insert into section values ('FIN-201', '1', 'Spring', '2018', 'Packard', '101', 'B');
insert into section values ('HIS-351', '1', 'Spring', '2018', 'Painter', '514', 'C');
insert into section values ('MU-199', '1', 'Spring', '2018', 'Packard', '101', 'D');
insert into section values ('PHY-101', '1', 'Fall', '2017', 'Watson', '100', 'A');
insert into teaches values ('10101', 'CS-101', '1', 'Fall', '2017');
insert into teaches values ('10101', 'CS-315', '1', 'Spring', '2018');
insert into teaches values ('10101', 'CS-347', '1', 'Fall', '2017');
insert into teaches values ('12121', 'FIN-201', '1', 'Spring', '2018');
insert into teaches values ('15151', 'MU-199', '1', 'Spring', '2018');
insert into teaches values ('22222', 'PHY-101', '1', 'Fall', '2017');
insert into teaches values ('32343', 'HIS-351', '1', 'Spring', '2018');
insert into teaches values ('45565', 'CS-101', '1', 'Spring', '2018');
insert into teaches values ('45565', 'CS-319', '1', 'Spring', '2018');
insert into teaches values ('76766', 'BIO-101', '1', 'Summer', '2017');
insert into teaches values ('76766', 'BIO-301', '1', 'Summer', '2018');
insert into teaches values ('83821', 'CS-190', '1', 'Spring', '2017');
insert into teaches values ('83821', 'CS-190', '2', 'Spring', '2017');
insert into teaches values ('83821', 'CS-319', '2', 'Spring', '2018');
insert into teaches values ('98345', 'EE-181', '1', 'Spring', '2017');
insert into student values ('00128', 'Zhang', 'Comp. Sci.', '102');
insert into student values ('12345', 'Shankar', 'Comp. Sci.', '32');
insert into student values ('19991', 'Brandt', 'History', '80');
insert into student values ('23121', 'Chavez', 'Finance', '110');
insert into student values ('44553', 'Peltier', 'Physics', '56');
insert into student values ('45678', 'Levy', 'Physics', '46');
insert into student values ('54321', 'Williams', 'Comp. Sci.', '54');
insert into student values ('55739', 'Sanchez', 'Music', '38');
insert into student values ('70557', 'Snow', 'Physics', '0');
insert into student values ('76543', 'Brown', 'Comp. Sci.', '58');
insert into student values ('76653', 'Aoi', 'Elec. Eng.', '60');
insert into student values ('98765', 'Bourikas', 'Elec. Eng.', '98');
insert into student values ('98988', 'Tanaka', 'Biology', '120');
insert into takes values ('00128', 'CS-101', '1', 'Fall', '2017', 'A');
insert into takes values ('00128', 'CS-347', '1', 'Fall', '2017', 'A-');
insert into takes values ('12345', 'CS-101', '1', 'Fall', '2017', 'C');
insert into takes values ('12345', 'CS-190', '2', 'Spring', '2017', 'A');
insert into takes values ('12345', 'CS-315', '1', 'Spring', '2018', 'A');
insert into takes values ('12345', 'CS-347', '1', 'Fall', '2017', 'A');
insert into takes values ('19991', 'HIS-351', '1', 'Spring', '2018', 'B');
insert into takes values ('23121', 'FIN-201', '1', 'Spring', '2018', 'C+');
insert into takes values ('44553', 'PHY-101', '1', 'Fall', '2017', 'B-');
insert into takes values ('45678', 'CS-101', '1', 'Fall', '2017', 'F');
insert into takes values ('45678', 'CS-101', '1', 'Spring', '2018', 'B+');
insert into takes values ('45678', 'CS-319', '1', 'Spring', '2018', 'B');
insert into takes values ('54321', 'CS-101', '1', 'Fall', '2017', 'A-');
insert into takes values ('54321', 'CS-190', '2', 'Spring', '2017', 'B+');
insert into takes values ('55739', 'MU-199', '1', 'Spring', '2018', 'A-');
insert into takes values ('76543', 'CS-101', '1', 'Fall', '2017', 'A');
insert into takes values ('76543', 'CS-319', '2', 'Spring', '2018', 'A');
insert into takes values ('76653', 'EE-181', '1', 'Spring', '2017', 'C');
insert into takes values ('98765', 'CS-101', '1', 'Fall', '2017', 'C-');
insert into takes values ('98765', 'CS-315', '1', 'Spring', '2018', 'B');
insert into takes values ('98988', 'BIO-101', '1', 'Summer', '2017', 'A');
insert into takes values ('98988', 'BIO-301', '1', 'Summer', '2018', null);
insert into advisor values ('00128', '45565');
insert into advisor values ('12345', '10101');
insert into advisor values ('23121', '76543');
insert into advisor values ('44553', '22222');
insert into advisor values ('45678', '22222');
insert into advisor values ('76543', '45565');
insert into advisor values ('76653', '98345');
insert into advisor values ('98765', '98345');
insert into advisor values ('98988', '76766');
insert into time_slot values ('A', 'M', '8', '0', '8', '50');
insert into time_slot values ('A', 'W', '8', '0', '8', '50');
insert into time_slot values ('A', 'F', '8', '0', '8', '50');
insert into time_slot values ('B', 'M', '9', '0', '9', '50');
insert into time_slot values ('B', 'W', '9', '0', '9', '50');
insert into time_slot values ('B', 'F', '9', '0', '9', '50');
insert into time_slot values ('C', 'M', '11', '0', '11', '50');
insert into time_slot values ('C', 'W', '11', '0', '11', '50');
insert into time_slot values ('C', 'F', '11', '0', '11', '50');
insert into time_slot values ('D', 'M', '13', '0', '13', '50');
insert into time_slot values ('D', 'W', '13', '0', '13', '50');
insert into time_slot values ('D', 'F', '13', '0', '13', '50');
insert into time_slot values ('E', 'T', '10', '30', '11', '45 ');
insert into time_slot values ('E', 'R', '10', '30', '11', '45 ');
insert into time_slot values ('F', 'T', '14', '30', '15', '45 ');
insert into time_slot values ('F', 'R', '14', '30', '15', '45 ');
insert into time_slot values ('G', 'M', '16', '0', '16', '50');
insert into time_slot values ('G', 'W', '16', '0', '16', '50');
insert into time_slot values ('G', 'F', '16', '0', '16', '50');
insert into time_slot values ('H', 'W', '10', '0', '12', '30');
insert into prereq values ('BIO-301', 'BIO-101');
insert into prereq values ('BIO-399', 'BIO-101');
insert into prereq values ('CS-190', 'CS-101');
insert into prereq values ('CS-315', 'CS-101');
insert into prereq values ('CS-319', 'CS-101');
insert into prereq values ('CS-347', 'CS-101');
insert into prereq values ('EE-181', 'PHY-101');
"""
    # ... other insert statements

    for query in insert_data_sql.split(';'):
        try:
            cursor.execute(query)
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            conn.rollback()


def main_menu(conn):
    while True:
        print("\nMain Menu:")
        print("1. View Courses")
        print("2. Add Student")
        print("3. View Students")
        print("4. Search")
        print("5. Enroll a Student")
        print("6. Exit")

        choice = input("Enter your choice: ")
        cursor = conn.cursor()
        def add_student(conn):
            print("enter format as follows ->'00128', 'Zhang', 'Comp. Sci.', '102'")
            sid = input("Enter student ID: ")
            name = input("Enter student name: ")
            major = input("Enter student dept_name: ")
            gpa = int(input("Enter student tot_cred: "))
            try:
                cursor.execute("INSERT INTO Student (ID, name, dept_name, tot_cred) VALUES (%s, %s, %s, %s)", (sid, name, major, gpa))
                conn.commit()
                print("Student added successfully.")
            except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    conn.rollback()
           
        def view_courses(conn):
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Course")
            for row in cursor:
                print(row)
        def view_students(conn):
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM student")
            for row in cursor:
                print(row)
        def search_menu(conn):
            def search_opt_1(conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT course.title, course.dept_name, department.building FROM course JOIN department ON course.dept_name = department.dept_name")
                    for row in cursor:
                         print(row)
            def search_opt_2(conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT student.ID ,student.name, instructor.name AS advisor FROM student JOIN advisor ON student.ID = Advisor.i_ID JOIN Instructor ON Advisor.i_Id = Instructor.ID")
                    for row in cursor:
                         print(row)
            def search_opt_3(conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT dept_name, AVG(salary) FROM instructor GROUP BY dept_name")
                    for row in cursor:
                         print(row)
            def search_opt_4(conn):
                    cursor = conn.cursor()
                    course_name=input("enter the course name : ")
                    cursor.execute("SELECT student.name FROM student JOIN takes ON student.ID = takes.ID JOIN course ON takes.course_id = course.course_id WHERE course.title = %s",(course_name,))
                    for row in cursor:
                         for i in row:
                            print(f"student {i} took course {course_name}")
            def search_opt_5(conn):
                    cursor = conn.cursor()
                    course_name=input("enter the course name : ")
                    cursor.execute("SELECT instructor.name FROM Instructor JOIN teaches ON instructor.ID = teaches.ID JOIN course ON teaches.course_id = course.course_id WHERE course.title = %s",(course_name,))
                    for row in cursor:
                         for i in row:
                            print(f"instructor {i} teaches course {course_name}")
            def search_opt_6(conn):
                    cursor = conn.cursor()
                    cursor.execute("SELECT course.title, section.room_number, classroom.capacity FROM course JOIN section ON course.course_id = section.course_id JOIN classroom ON section.room_number = classroom.room_number")
                    for row in cursor:
                         print(row)
            def search_opt_7(conn):
                    cursor = conn.cursor()
                    credits_min = float(input("Enter the minimum credits to see the students applicable : "))
                    cursor.execute("SELECT student.name FROM student JOIN takes ON Student.ID = takes.ID JOIN course ON takes.course_id = course.course_id GROUP BY student.ID HAVING SUM(course.credits) >= %s",(credits_min,))
                    for row in cursor:
                         print(row)

            while True:
                print("\nSearch Menu:")
                print("1. View Courses with Department Details")
                print("2. View Students with Advisors")
                print("3. Average Salary by Department")
                print("4. Find Students by Course")
                print("5. Find Instructors by Course")
                print("6. View Course Sections with Room Capacity")
                print("7. Find Students by Minimum Credits")
                print("8. Go Back to Main Menu")
                search_choice=input("enter the chosen option : ")
                if search_choice=="1":
                     search_opt_1(conn)
                elif search_choice=="2":
                     search_opt_2(conn)
                elif search_choice=="3":
                     search_opt_3(conn)
                elif search_choice=="4":
                     search_opt_4(conn)
                elif search_choice=="5":
                     search_opt_5(conn)
                elif search_choice=="6":
                     search_opt_6(conn)
                elif search_choice=="7":
                     search_opt_7(conn)
                else:
                     break
        def enroll_a_student(conn,student_id, course_id, sec_id, semester, year, grade=None):
            cursor.execute("SELECT * FROM student WHERE ID = %s", (student_id,))
            student = cursor.fetchone()
            if not student:
                print("Student does not exist.")
                return

            # Step 2: Check if Section exists
            cursor.execute("""
                SELECT * FROM section 
                WHERE course_id = %s AND sec_id = %s AND semester = %s AND year = %s
            """, (course_id, sec_id, semester, year))
            section = cursor.fetchone()
            if not section:
                print("Section does not exist.")
                return

            # Step 3: Check if Student is already enrolled in this section
            cursor.execute("""
                SELECT * FROM takes 
                WHERE ID = %s AND course_id = %s AND sec_id = %s AND semester = %s AND year = %s
            """, (student_id, course_id, sec_id, semester, year))
            enrollment = cursor.fetchone()
            if enrollment:
                print("Student is already enrolled in this section.")
                return

            # Step 4: Insert Enrollment into takes table
            try:
                cursor.execute("""
                    INSERT INTO takes (ID, course_id, sec_id, semester, year, grade)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (student_id, course_id, sec_id, semester, year, grade))
                conn.commit()
                print("Enrollment record added successfully.")
            except Error as e:
                print(f"Error while enrolling student: {e}")
                conn.rollback()
                return

            # Step 5: Update Total Credits in student table
            try:
                cursor.execute("SELECT credits FROM course WHERE course_id = %s", (course_id,))
                course = cursor.fetchone()
                if course:
                    course_credits = course[0]
                    cursor.execute("""
                        UPDATE student SET tot_cred = tot_cred + %s WHERE ID = %s
                    """, (course_credits, student_id))
                    conn.commit()
                    print("Student's total credits updated successfully.")
            except Error as e:
                print(f"Error updating student's credits: {e}")
                conn.rollback()

        if choice == "1":
            view_courses(conn)
        elif choice == "2":
            add_student(conn)
        elif choice == "3":
            view_students(conn)
        elif choice == "4":
            search_menu(conn)
        elif choice == "5":
            student_id = input("Enter the Student ID: ")
            course_id = input("Enter the Course ID: ")
            sec_id = input("Enter the Section ID: ")
            semester = input("Enter the Semestervtype (e.g., 'summer/fall/spring'): ")
            year=input("enter the year : ")

            enroll_a_student(conn,student_id, course_id, sec_id, semester, year, grade=None)
        else:
             break

def main():
    try:
        temp_Conn=mysql.connector.connect(
            host="localhost",
            user="test",
            passwd="Anand@456"
        )
        temp_Cursor=temp_Conn.cursor()
        temp_Cursor.execute("CREATE DATABASE IF NOT EXISTS testdatabase")
        print("database created successfully")
        temp_Conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    conn = connect_to_database("localhost", "test", "Anand@456","testdatabase")# enter your credentials and db details
    if conn:
        create_tables(conn)
        insert_data(conn)
        main_menu(conn)
        conn.close()

if __name__ == "__main__":
    main()