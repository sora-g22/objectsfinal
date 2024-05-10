import socket
import uuid
import threading
from argon2 import PasswordHasher

import mysql.connector

class Server:
    def __init__(self, database_name, port, server_timeout, client_timeout):
        self.database_name = database_name
        self.port = port
        self.server_timeout = server_timeout
        self.client_timeout = client_timeout
        self.ph = PasswordHasher() 
        self.connection = mysql.connector.connect(host="localhost", user="demoUser", passwd="test", database="piratenetDB")
        cursor = self.connection.cursor()
        with open("table-generation.sql") as tableGenFile:
            data = tableGenFile.read().split(";")
            for command in data:
                cursor.execute(command.replace("\n",""))
            cursor.close()
        self.connection.commit()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(self.server_timeout)

    def handle_requests(self, client_socket, client_address):
        client_socket.settimeout(self.client_timeout)

        try:
            data = client_socket.recv(1024).decode().split("|")
            command = data[0]
            if command == "login_attempt":
                cursor = self.connection.cursor()
                result = False
                userUuid = None
                role = None
                try:
                    cursor.execute(f"SELECT password FROM users WHERE username='{data[1]}'")
                    retrieved_hash = cursor.fetchall()
                    cursor.execute(f"SELECT UUID FROM users WHERE username='{data[1]}'")
                    userUuid = cursor.fetchall()[0][0]
                    cursor.execute(f"SELECT roleID FROM roles WHERE users_UUID='{userUuid}'")
                    role = cursor.fetchall()[0][0]
                    result = self.ph.verify(retrieved_hash[0][0], data[2])
                except Exception as ex:
                    result = False
                #retrieved_hash = None
                finally:
                    cursor.close()
                    if result == True:
                        client_socket.send(f"Sucessful login attempt|{userUuid}|{role}".encode())
                    elif result == False:
                        client_socket.send("Bad login attempt".encode())
            elif command == "register_user":
                cursor = self.connection.cursor()
                newUUID = uuid.uuid4()
                sucessful = False
                try:
                    hashedPassword = self.ph.hash(data[3])
                    cursor.execute(f"INSERT INTO users (UUID, username, password, salt) VALUES ('{newUUID}', '{data[2]}', '{hashedPassword}', 'NA')")
                    if data[1] == "student":
                        cursor.execute(f"INSERT INTO students (users_UUID, firstName, lastName, enrollmentStatus) VALUES ('{newUUID}', '{data[4]}', '{data[5]}', 'OK')")
                        cursor.execute(f"INSERT INTO roles (roleID, users_UUID) VALUES ('student', '{newUUID}')")
                    elif data[1] == "professor":
                        cursor.execute(f"INSERT INTO professors (UUID, firstName, lastName, contactInfo) VALUES ('{newUUID}', '{data[4]}', '{data[5]}', ' ')")
                        cursor.execute(f"INSERT INTO roles (roleID, users_UUID) VALUES ('professor', '{newUUID}')")
                    elif data[2] == "admins":
                        cursor.execute(f"INSERT INTO admins (users_UUID, firstName, lastName) VALUES ('{newUUID}', '{data[4]}', '{data[5]}')")
                        cursor.execute(f"INSERT INTO roles (roleID, users_UUID) VALUES ('admin', '{newUUID}')")
                    self.connection.commit()
                    sucessful = True
                except Exception as ex:
                    print(ex)
                    sucessful = False
                finally:
                    cursor.close()
                    if sucessful:
                        client_socket.send("Sucessful Registration".encode())
                    else:
                        client_socket.send("Failed Registration".encode())


            elif command == "get_students":
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT * FROM students")
                students = cursor.fetchall()
                response = ""
                for student in students:
                    response += f"{student[1]}|{student[2]}|{student[3]}\n"
                return response
            elif command == "get_course_info":
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT * FROM courses")
                courses = cursor.fetchall()
                response = ""
                for course in courses:
                    response += f"{course[0]}|{course[1]}|{course[2]}|{course[3]}\n"
                return response
            elif command == "edit_course":
                pass
            elif command == "add_course":
                cursor = self.connection.cursor()
                cursor.execute(f"INSERT INTO courses (courseID, professors_users_UUID, meetingTime, meetinDays) VALUES ('{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}')")
                self.connection.commit()
            elif command == "delete_course":
                cursor = self.connection.cursor()
                cursor.execute(f"DELETE FROM courses_has_students WHERE courseID='{data[1]}'")
                cursor.execute(f"DELETE FROM courses WHERE courseID='{data[1]}'")
                self.connection.commit()
            elif command == "enroll_student":
                cursor = self.connection.cursor()
                cursor.execute(f"INSERT INTO course_has_students (courseID, professors_users_UUID, students_users_UUID) VALUES ('{data[1]}', '{data[2]}', '{data[3]}')")
                self.connection.commit()
            elif command == "get_grades":
                cursor = self.connection.cursor()
                cursor.execute(f"SELECT percentageGrade FROM grades WHERE courseID='{data[1]}' AND students_users_UUID='{data[2]}' AND professors_users_UUID='{data[3]}'")
                grades = cursor.fetchall()
                response = ""
                for grade in grades:
                    response = f"{grade[0]}|{grade[1]}|{grade[2]}|{grade[3]}\n"
                return response
            elif command == "update_contact_info":
                cursor = self.connection.cursor()
                cursor.execute(f"UPDATE professors SET contactInfo='{data[1]}' WHERE UUID='{data[2]}'")
                self.connection.commit()
            # possibly need to add more, fix later
            else:
                print("")
        except socket.timeout:
            client_socket.send("Client connection timed out.".encode())
            client_socket.close()
        finally:
            client_socket.close()
    def start(self):
        try:
            while True:
                connection, client_address = self.server_socket.accept()
                #clientThread = threading.Thread(target=self.handle_requests, args=(connection, client_address))
                #clientThread.start()
                self.handle_requests(connection, client_address)
        finally:
            self.server_socket.close()

def main():
    backendServer = Server("piratenetDB", 5000, 60, 60)
    backendServer.start()

if __name__ == "__main__":
    main()
