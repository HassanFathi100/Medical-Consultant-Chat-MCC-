import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import pandas as pd

#ٌReading doctors names from an excel sheet
df = pd.read_excel (r'D:\Biomedical\Networks\Chat room\Doctors database.xlsx')
doctorsList = df['Name'].to_list()


HOST = '127.0.0.1'
PORT = 9090

class Client:
    
    def __init__(self, host, port):
        
        #Opening the socket from client side
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        
        msg = tkinter.Tk()
        msg.withdraw()
        
        #Type your username
        self.name = simpledialog.askstring("Name", "Please choose a nickname", parent = msg)
        
        #Checking if the username is that of a doctor
        if (self.name in doctorsList):
            self.name = 'Dr. ' + self.name
        
        self.gui_done = False
        self.running = True
        
        gui_thread = threading.Thread(target = self.GUI_Window)
        receive_thread = threading.Thread(target = self.receive)
        
        gui_thread.start()
        receive_thread.start()
        
    
    #GUI Function using TKinter
    def GUI_Window(self):
        self.window = tkinter.Tk()
        self.window.configure(bg = "lightgrey")
        
        self.chatLabel = tkinter.Label(self.window, text = "Chat", bg = "lightgrey")
        self.chatLabel.config(font = ('Areal', 12))
        self.chatLabel.pack(padx = 20, pady = 5)
        
        self.textArea = tkinter.scrolledtext.ScrolledText(self.window)
        self.textArea.config(state = "disabled")
        self.textArea.pack(padx = 20, pady = 5)
        
        self.msgLabel = tkinter.Label(self.window, text = "Message", bg = "lightgrey")
        self.msgLabel.config(font = ('Areal', 12))
        self.msgLabel.pack(padx = 20, pady = 5)
        
        self.inputArea = tkinter.Text(self.window, height = 3)
        self.inputArea.pack(padx = 20, pady = 5)
        
        self.btn = tkinter.Button(self.window, text = "Send", command = self.write)
        self.btn.config(font = ('Areal', 12))
        self.btn.pack(padx = 20, pady = 5)
        
        self.gui_done = True
        
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        
        self.window.mainloop()
        
        
    
    #Write the message and send it to the server
    def write(self):
        message = f"{self.name}: {self.inputArea.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.inputArea.delete('1.0', 'end')
    
    
    #When we close the window
    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)
    
    
    #ٌReceiving messages from other other clients and handeling errors
    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024)
                if message == "NICK":
                    self.sock.send(self.name.encode('utf-8'))
                    
                else:
                    if self.gui_done:
                        self.textArea.config(state = 'normal')
                        self.textArea.insert('end', message)
                        self.textArea.yview('end')
                        self.textArea.config(state = 'disabled')
                        
            except ConnectionAbortedError:
                break
            
            except:
                print("Error")
                self.sock.close()
                break


client = Client(HOST, PORT)