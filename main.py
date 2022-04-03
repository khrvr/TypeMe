import tkinter as tk
import time
import string

frozenColor = "#8f8a89"
frameColor = "#f2eceb"
buttonColor = "#f2eceb"
textLineColor = "#f2eceb"
buttonFont = ("TkTextFont", 7)
textLineFont = ("TkTextFont", 15)
wdth = 700
hght = 350

chars = 50

sessionTime = 0
sessionMistakes = 0
sessionCorrect = 0


class CustomFrame(tk.Frame):
    def __init__(self, window, side, width, height):
        super().__init__(master=window, width=width, height=height, bg=frameColor)
        self.pack(fill=tk.BOTH, side=side)


class CustomButton(tk.Button):
    def __init__(self, frame, side, text, command):
        super().__init__(master=frame, text=text, command=command, font=buttonFont, bg=buttonColor)
        self.pack(side=side, padx=5, pady=5)


class TextLine(tk.Label):
    def __init__(self, frame, filename):
        super().__init__(master=frame, bg=textLineColor, width=40, height=5, font=textLineFont)
        self.pack(fill=tk.BOTH)
        self.focus_set()
        self.config(text="Press enter to start, esc to pause")
        self.text = []
        with open(filename) as f:
            while True:
                c = f.read(1)
                if not c:
                    break
                if not c == "\n":
                    if c == "\t" or c == " ":
                        c = "_"
                    self.text.append(c)
        self.bind("<Return>", self.play)
        self.bind("<Escape>", self.freeze)
        self.textPoint = 0
        self.startTime = 0
        self.mistakes = 0
        self.correct = 0
        self.state = "initial"

    def save_stats(self):
        global sessionTime
        sessionTime += time.time() - self.startTime
        global sessionMistakes
        sessionMistakes += self.mistakes
        global sessionCorrect
        sessionCorrect += self.correct

    def freeze(self, event):
        if self.state == "frozen" or self.state == "initial":
            return
        else:
            self.state = "frozen"
            self.config(bg=frozenColor)
            self.custom_unbind()
            self.save_stats()

    def custom_bind(self, custom_bind=True):
        def smart_unbind(event, *args, **kwargs):
            self.unbind(event)

        if custom_bind:
            current_binding = self.bind
        else:
            current_binding = smart_unbind
        current_binding("<space>", self.handle_user_click)
        # еще большие буквы, цифры и знаки
        alphabet = string.ascii_lowercase
        for letter in list(alphabet):
            current_binding(letter, self.handle_user_click)

    def custom_unbind(self):
        self.custom_bind(custom_bind=False)

    def terminate_run(self):
        self.save_stats()
        self.configure(text="Press enter to start, esc to pause")
        self.state = "initial"
        self.textPoint = 0
        self.custom_unbind()

    def show_text(self):
        if self.textPoint < len(self.text):
            newchars = min(chars, len(self.text) - self.textPoint)
            newtext = ''.join(self.text[self.textPoint:self.textPoint + newchars])
            self.config(text=newtext)
        else:
            self.terminate_run()

    def handle_user_click(self, event):
        nextchar = self.text[self.textPoint]
        key = event.keysym
        if key == "space":
            key = "_"
        if key == nextchar:
            self.textPoint += 1
            self.show_text()

    def play(self, event):
        if self.state == "playing":
            return
        else:
            if self.state == "frozen":
                self.config(bg=textLineColor)
            self.state = "playing"
            self.startTime = time.time()
            self.mistakes = 0
            self.correct = 0
        self.custom_bind()
        self.show_text()

def restart():
    pass

def show_stats():
    pass

def select_text():
    pass


class CustomWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TypeMe")
        self.geometry("{v0}x{v1}+100+100".format(v0=wdth, v1=hght))
        self.resizable(False, False)
        self.bottomFrame = CustomFrame(self, tk.BOTTOM, wdth, hght//3)
        self.mainFrame = CustomFrame(self, tk.TOP, wdth, hght - hght//3)
        self.restartButton = CustomButton(self.bottomFrame, tk.LEFT, "RESTART", restart)
        self.statsButton = CustomButton(self.bottomFrame, tk.LEFT, "STATS", show_stats)
        self.textSelectButton = CustomButton(self.bottomFrame, tk.RIGHT, "SELECT TEXT", select_text)
        self.textLine = TextLine(self.mainFrame, 'test_text.txt')


mainWindow = CustomWindow()

mainWindow.mainloop()
