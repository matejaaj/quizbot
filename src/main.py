import tkinter as tk
from app import QuizBotApp

def main():
    root = tk.Tk()
    app = QuizBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
