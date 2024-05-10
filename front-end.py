import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import socket

class Client:
    #__slots__ = ["mainWindow"]

    def __init__(self):
        self.mainWindow = tk.Tk()
        self.mainWindow.geometry(f"{self.mainWindow.winfo_screenwidth()}x{self.mainWindow.winfo_screenheight()}") 
        self.mainWindow.configure(bg="white")

        self.setonHallBranding = tk.Canvas(self.mainWindow, height=150, width=self.mainWindow.winfo_screenwidth(), background="#004488")
        self.setonHallLogo = tk.PhotoImage(file="assets/university-logo-desktop.png")
        self.setonHallPresidentsHall = tk.PhotoImage(file="assets/presidents-hall.png")
        self.PresidentsHallPanel = tk.Label(self.mainWindow, image=self.setonHallPresidentsHall)
        self.setonHallBranding.create_image(175,150/2, image=self.setonHallLogo)
        self.setonHallBranding.pack(side=tk.TOP)
        self.PresidentsHallPanel.pack(side=tk.LEFT)
        self.setonHallFont = tkFont.Font(family="TisaPro", size=12, weight=tkFont.NORMAL)
        self.setonHallSignInFont = tkFont.Font(family="TisaPro", size=24, weight=tkFont.NORMAL) 

        self.loginBoxes = tk.Frame(self.mainWindow, background="white")
        self.usernameLabel = tk.Label(self.loginBoxes, text="Username: ", background="white", font=self.setonHallFont)
        self.passwordLabel = tk.Label(self.loginBoxes, text="Password: ", background="white", font=self.setonHallFont)
        self.usernameInput = tk.Entry(self.loginBoxes, width=50) 
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
                                     width=20
                                     )
        self.passwordInput = tk.Entry(self.loginBoxes, width=50)
        self.loginBoxes.grid_rowconfigure(0, minsize=15)
        self.loginLabel.grid(row=1, column=0, sticky=tk.W)
        self.usernameLabel.grid(row=2, column=0, sticky=tk.W)
        self.passwordLabel.grid(row=4, column=0, sticky=tk.W)
        self.usernameInput.grid(row=3, column=0, sticky=tk.W)
        self.passwordInput.grid(row=5, column=0, sticky=tk.W)
        self.loginBoxes.grid_rowconfigure(6, minsize="15")
        self.loginButton.grid(row=7, column=0, sticky=tk.W)
        self.loginBoxes.pack()

    def connectToServer(self, server_port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("localhost", server_port))
        return client_socket

    def start(self):
        self.mainWindow.mainloop()
 
def main():
    user = Client()
    user.start()

if __name__ == "__main__":
    main()

