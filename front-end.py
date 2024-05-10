import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from argon2 import PasswordHasher
from PIL import Image
import socket


def connectToServer(server_port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", server_port))
        return client_socket

UUID = None


class LoginPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master) 
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallPresidentsHall = tk.PhotoImage(file="assets/presidents-hall.png")
        self.PresidentsHallPanel = tk.Label(self, image=self.setonHallPresidentsHall)
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.PresidentsHallPanel.pack(side=tk.LEFT)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 

        self.loginBoxes = tk.Frame(self, background="white")
        self.usernameLabel = tk.Label(self.loginBoxes, text="Username: ", background="white", font=self.setonHallFont)
        self.passwordLabel = tk.Label(self.loginBoxes, text="Password: ", background="white", font=self.setonHallFont)
        self.usernameInput = tk.Entry(self.loginBoxes, width=55)
        self.loginLabel = tk.Label(self.loginBoxes, 
                                   text="Sign in", 
                                   background="white", 
                                   foreground="#3369a0", 
                                   font=self.setonHallSignInFont 
                                   )
        self.loginButton = tk.Button(self.loginBoxes, 
                                     text="Login", 
                                     foreground="white",
                                     background="#3369a0",
                                     font=self.setonHallFont,
                                     width=20,
                                     command= lambda: self.attemptLogin(master)
                                     )
        self.registerButton = tk.Button(self.loginBoxes,
                                        text="Register",
                                        foreground="white",
                                        background="#3369a0",
                                        font=self.setonHallFont,
                                        width=20,
                                        command = lambda: master.switch_frame(RegistrationPage))
        self.passwordInput = tk.Entry(self.loginBoxes, width=55)
        self.loginBoxes.grid_rowconfigure(0, minsize=15)
        self.loginLabel.grid(row=1, column=0, sticky=tk.W, columnspan=2)
        self.usernameLabel.grid(row=2, column=0, sticky=tk.W, columnspan=2)
        self.passwordLabel.grid(row=4, column=0, sticky=tk.W, columnspan=2)
        self.usernameInput.grid(row=3, column=0, sticky=tk.W, columnspan=2)
        self.passwordInput.grid(row=5, column=0, sticky=tk.W, columnspan=2)
        self.loginBoxes.grid_rowconfigure(6, minsize="15")
        self.loginButton.grid(row=7, column=0, sticky=tk.W)
        self.registerButton.grid(row=7, column=1, stick=tk.W)
        self.loginBoxes.pack()

    def attemptLogin(self, master):
        client_socket = connectToServer(5000)
        username = self.usernameInput.get()
        password = self.passwordInput.get()
        #ph = PasswordHasher()
        #hashedPassword = ph.hash(password=password)
        request = f"login_attempt|{username}|{password}"
        client_socket.send(request.encode("utf-8"))
        response = client_socket.recv(1024).decode("utf-8").split("|")
        if response[0] == "Sucessful login attempt":
            UUID = response[1]
            if response[2] == "student":
                master.switch_frame(StudentOptionsMenu)
            elif response[2] == "professor":
                master.switch_frame(ProfessorOptionsMenu)
            elif response[2] == "admin":
                master.switch_frame(AdminOptionsMenu)
        else:
            print("Bad Login attempt")

class RegistrationPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallPresidentsHall = tk.PhotoImage(file="assets/presidents-hall.png")
        self.PresidentsHallPanel = tk.Label(self, image=self.setonHallPresidentsHall)
        self.setonHallBranding.pack(side=tk.TOP)
        self.PresidentsHallPanel.pack(side=tk.LEFT)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 

        self.loginBoxes = tk.Frame(self, background="white")
        self.usernameLabel = tk.Label(self.loginBoxes, text="Username: ", background="white", font=self.setonHallFont)
        self.passwordLabel = tk.Label(self.loginBoxes, text="Password: ", background="white", font=self.setonHallFont)
        self.usernameInput = tk.Entry(self.loginBoxes, width=50) 
        self.loginLabel = tk.Label(self.loginBoxes, 
                                   text="Registration", 
                                   background="white", 
                                   foreground="#3369a0", 
                                   font=self.setonHallSignInFont 
                                   )
        self.loginButton = tk.Button(self.loginBoxes, 
                                     text="Register", 
                                     foreground="white",
                                     background="#3369a0",
                                     font=self.setonHallFont,
                                     width=20,
                                     command= lambda: self.registerUser(master)
                                     )
        self.firstNameLabel = tk.Label(self.loginBoxes, text="First Name: ", background="white", font=self.setonHallFont)
        self.firstNameEntry = tk.Entry(self.loginBoxes, width = 50)
        self.lastNameEntry = tk.Entry(self.loginBoxes, width = 50)
        self.lastNameLabel = tk.Label(self.loginBoxes, text="Last Name: ", background="white", font=self.setonHallFont)
        self.userTypeLabel = tk.Label(self.loginBoxes, text="User Type: ", background="white", font=self.setonHallFont)
        self.userTypeVar = tk.StringVar(self)
        self.userTypeMenu = tk.OptionMenu(self.loginBoxes, self.userTypeVar, "student", "professor", "admin")
        self.passwordInput = tk.Entry(self.loginBoxes, width=50)
        self.loginBoxes.grid_rowconfigure(0, minsize=15)
        self.loginLabel.grid(row=1, column=0, sticky=tk.W)
        self.usernameLabel.grid(row=2, column=0, sticky=tk.W)
        self.passwordLabel.grid(row=4, column=0, sticky=tk.W)
        self.usernameInput.grid(row=3, column=0, sticky=tk.W)
        self.passwordInput.grid(row=5, column=0, sticky=tk.W)
        self.firstNameLabel.grid(row=6, column=0, sticky=tk.W)
        self.firstNameEntry.grid(row=7, column=0, sticky=tk.W)
        self.lastNameLabel.grid(row=8, column =0, sticky=tk.W)
        self.lastNameEntry.grid(row=9, column=0, sticky=tk.W)
        self.userTypeLabel.grid(row=10, column = 0, sticky=tk.W)
        self.userTypeMenu.grid(row=11, column = 0, stick=tk.W)

        self.loginBoxes.grid_rowconfigure(12, minsize="15")
        self.loginButton.grid(row=13, column=0, sticky=tk.W)
        self.loginBoxes.pack()

    def registerUser(self, master):
        client_socket = connectToServer(5000)
        username = self.usernameInput.get()
        password = self.passwordInput.get()
        firstName = self.firstNameEntry.get()
        lastName = self.lastNameEntry.get()
        userType = self.userTypeVar.get()
        request = f"register_user|{userType}|{username}|{password}|{firstName}|{lastName}".encode("utf-8")
        print(request)
        client_socket.send(request)
        response = client_socket.recv(1024).decode("utf-8")
        if response == "Sucessful Registration":
            master.switch_frame(LoginPage)
        else:
            print("Failed Registration")

class ProfessorOptionsMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 

         
        self.geometryManager = tk.Frame(self, background="white")
        self.studentDashboardLabel = tk.Label(self.geometryManager, text="Faculty Dashboard", background="white", font=self.setonHallSignInFont)
        self.enrollInCoursesButton = tk.Button(self.geometryManager,
                                               text="Update Contact Information",
                                                foreground="white",
                                                background="#3369a0",
                                                font=self.setonHallFont,
                                                width=20,
                                                command = lambda: master.switch_frame(ProfessorUpdateContactInfoMenu))

        self.viewCoursesButton = tk.Button(self.geometryManager,
                                           text="Post Grades",
                                        foreground="white",
                                        background="#3369a0",
                                        font=self.setonHallFont,
                                        width=20,
                                        command = lambda: master.switch_frame(ProfessorUpdateGradesMenu))

        self.viewGradesButton = tk.Button(self.geometryManager,
                                          text="View Grades",
                                        foreground="white",
                                        background="#3369a0",
                                        font=self.setonHallFont,
                                        width=20,
                                        command = lambda: master.switch_frame(ProfessorsViewGradesMenu))

        self.studentDashboardLabel.grid(row=0, column=0, sticky=tk.W+tk.N)
        self.viewGradesButton.grid(row=1, column=0, sticky=tk.W) 
        self.viewCoursesButton.grid(row=1, column=1, sticky=tk.W, padx=(0,30)) 
        self.enrollInCoursesButton.grid(row=1, column=2, sticky=tk.W) 
        self.geometryManager.pack(side=tk.LEFT)


class AdminOptionsMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 

         
        self.geometryManager = tk.Frame(self, background="white")
        self.studentDashboardLabel = tk.Label(self.geometryManager, text="Administrative Dashboard", background="white", font=self.setonHallSignInFont)
        self.enrollInCoursesButton = tk.Button(self.geometryManager,
                                               text="Edit Courses",
                                                foreground="white",
                                                background="#3369a0",
                                                font=self.setonHallFont,
                                                width=20,
                                                command = lambda: master.switch_frame(AdminCoursesMenu))

        self.viewCoursesButton = tk.Button(self.geometryManager,
                                           text="Edit Users",
                                        foreground="white",
                                        background="#3369a0",
                                        font=self.setonHallFont,
                                        width=20,
                                        command = lambda: master.switch_frame(AdminUsersMenu))

        self.studentDashboardLabel.grid(row=0, column=0, sticky=tk.W+tk.N)
        self.viewCoursesButton.grid(row=1, column=1, sticky=tk.W, padx=(0,30)) 
        self.enrollInCoursesButton.grid(row=1, column=2, sticky=tk.W) 
        self.geometryManager.pack(side=tk.LEFT)





class StudentOptionsMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 

         
        self.geometryManager = tk.Frame(self, background="white")
        self.studentDashboardLabel = tk.Label(self.geometryManager, text="Student Dashboard", background="white", font=self.setonHallSignInFont)
        self.enrollInCoursesButton = tk.Button(self.geometryManager,
                                               text="Register For Classes",
                                                foreground="white",
                                                background="#3369a0",
                                                font=self.setonHallFont,
                                                width=20,
                                                command = lambda: master.switch_frame(EnrollmentMenu))

        self.viewCoursesButton = tk.Button(self.geometryManager,
                                           text="View Available Courses",
                                        foreground="white",
                                        background="#3369a0",
                                        font=self.setonHallFont,
                                        width=20,
                                        command = lambda: master.switch_frame(CoursesMenu))

        self.viewGradesButton = tk.Button(self.geometryManager,
                                          text="View Grades",
                                        foreground="white",
                                        background="#3369a0",
                                        font=self.setonHallFont,
                                        width=20,
                                        command = lambda: master.switch_frame(StudentsGradesMenu))

        self.studentDashboardLabel.grid(row=0, column=0, sticky=tk.W+tk.N)
        self.viewGradesButton.grid(row=1, column=0, sticky=tk.W) 
        self.viewCoursesButton.grid(row=1, column=1, sticky=tk.W, padx=(0,30)) 
        self.enrollInCoursesButton.grid(row=1, column=2, sticky=tk.W) 
        self.geometryManager.pack(side=tk.LEFT)


class AdminCoursesMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL)

class AdminUsersMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 


class CoursesMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 

class EnrollmentMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL)
        
        self.geometryManager = tk.Frame(self, background="white")
        self.enrollmentDashboardLabel = tk.Label(self.geometryManager, text="Enroll For Courses", background="white", font=self.setonHallSignInFont)
        

class ProfessorUpdateContactInfoMenu(tk.Frame):
     def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 



class ProfessorUpdateGradesMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 


class ProfessorsViewGradesMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 


class StudentsGradesMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.width=self.winfo_screenwidth()
        self.height=self.winfo_screenheight()
        self.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self, height=150, width=self.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 

class Client(tk.Tk):
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginPage)
        self.configure(bg="white")
        
    def start(self):
        self.mainloop()
 
def main():
    user = Client()
    user.start()

if __name__ == "__main__":
    main()

