import matchautoaccept
import tkinter as tk
import os

class AutoAcceptGui:
    def __init__(self, root: tk.Tk):
        self.process = matchautoaccept.AutoAccept()
        
        self.window = root
        self.window.title("Match autoaccept")

        self.width, self.height = 300, 200
        self.x = (root.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (root.winfo_screenheight() // 2) - (self.height // 2)
        root.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')


        self.isRunning = False

        self.resolutionResetButton = tk.Button(self.window, text="Resolution reset", command=self.process.detect_resolution, width=11, font=("Arial", 10))
        self.resolutionResetButton.pack(pady=10)

        self.startStopButton = tk.Button(self.window, text="Start", command=self.start_stop_process, width=15, font=("Arial", 12))
        self.startStopButton.pack(pady=20)

        self.exitButton = tk.Button(self.window, text="Exit", command=self.exit_app, bg="red", fg="white", width=15, font=("Arial", 12))
        self.exitButton.pack(pady=10)

    def start_stop_process(self):
        if not self.isRunning:
            self.isRunning = True
            self.startStopButton.config(text='Stop')
            self.process.start_autoaccept_no_champselect_thread()
        else:
            self.isRunning = False
            self.startStopButton.config(text='Start')
            self.process.stop_autoaccept_no_champselect_thread()

    def exit_app(self):
        self.window.destroy()
        os._exit(0)

    
if __name__ == '__main__':
    root = tk.Tk()
    app = AutoAcceptGui(root)   
    root.mainloop()         
