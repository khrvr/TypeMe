import tkinter as tk
import time
import string

frameColor = "gray"
buttonColor = "gray"
textLineColor = "floral white"
buttonFont = ("TkTextFont", 10)
wdth = 700
hght = 350

chars = 80

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


class TextLine(tk.Text):
    def __init__(self, frame, filename):
        super().__init__(master=frame, bg=textLineColor, width=40, height=5, wrap=tk.WORD)
        self.pack(fill=tk.BOTH)
        self.insert(1.0, "Press enter to start, esc to pause")
        # self.config(state="disabled")
        # разобраться с отключением ввода или же перейти на label
        self.text = []
        with open(filename) as f:
            while True:
                c = f.read(1)
                if not c:
                    break
                if not c == "\n":
                    self.text.append(c)
        self.textPoint = 0
        self.bind("<Return>", self.play)
        self.bind("<Escape>", self.freeze)
        self.tag_config("frozen", background="black")
        self.startTime = 0
        self.mistakes = 0
        self.correct = 0
        self.state = "initial"
        self.rightButton = False

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
            self.tag_add("frozen", 1.0, tk.END)
            self.save_stats()

    def terminate_run(self):
        self.save_stats()
        self.delete(1.0, "end")
        self.insert(1.0, "Press enter to start, esc to pause")
        self.state = "initial"
        self.textPoint = 0
        self.unbind("<Space>")
        alphabet = string.ascii_lowercase
        for letter in list(alphabet):
            self.unbind(letter)

    def pressed(self, event):
        nextchar = self.text[self.textPoint]
        key = event.keysym
        if key == "space":
            key = " "
        if key == nextchar:
            self.textPoint += 1
            if self.textPoint < len(self.text):
                self.delete(1.0, tk.END)
                newchars = min(self.textPoint + chars, len(self.text))
                newtext = ''.join(self.text[self.textPoint:self.textPoint + newchars])
                self.insert(1.0, newtext)
            else:
                self.terminate_run()

    def play(self, event):
        if self.state == "playing":
            return
        else:
            if self.state == "frozen":
                self.tag_remove("frozen", 1.0, tk.END)
            self.state = "playing"
            self.startTime = time.time()
            self.mistakes = 0
            self.correct = 0
        self.bind("<space>", self.pressed)
        # еще большие буквы, цифры и знаки
        alphabet = string.ascii_lowercase
        for letter in list(alphabet):
            self.bind(letter, self.pressed)
        if self.textPoint < len(self.text):
            self.delete(1.0, tk.END)
            newchars = min(self.textPoint + chars, len(self.text))
            newtext = ''.join(self.text[self.textPoint:self.textPoint + newchars])
            self.insert(1.0, newtext)
        else:
            self.terminate_run()

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
