import socket
from argon2 import PasswordHasher as ph

import sqlite3

class Server:
    def __init__(self, database_name, port, server_timeout, client_timeout):
        self.database_name = database_name
        self.port = port
        self.server_timeout = server_timeout
        self.client_timeout = client_timeout
        
        self.connection = sqlite3.connect(self.database_name)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("localhost", self.port))
        self.server_socket.listen(5)
        self.server_socket.settimeout(self.server_timeout)

    def handle_requests(self, client_socket: socket.socket):
        client_socket.settimeout(self.client_timeout)

        try:
            data = client_socket.recv(1024).decode().split("|")
            command = data[0]
            if command == "login_attempt":
                retrieved_hash = None
                result = ph.verify(retrieved_hash, data[1])
                if result == True:
                    client_socket.send("Sucessful login attempt".encode())
                elif result == False:
                    client_socket.send("Bad login attempt".encode())
            elif command == "register_student":
                pass
            elif command == "get_students":
                pass
            elif command == "get_course_info":
                pass
            elif command == "edit_course":
                pass
            elif command == "add_course":
                pass
            elif command == "delete_course":
                pass
            elif command == "enroll_student":
                pass
            elif command == "get_grades":
                pass
            elif command == "update_contact_info":
                pass
            # possibly need to add more, fix later
            else:
                print("Sometime went horribly wrong here")
        except socket.timeout:
            client_socket.send("Client connection timed out.".encode())
            client_socket.close()

def main():
    backendServer = Server("piratenetDB.db", 5000, 5, 5)

if __name__ == "__main__":
    main()
