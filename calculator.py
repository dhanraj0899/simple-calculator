import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("300x400")

        # Entry field for display
        self.display = tk.Entry(root, width=20, font=("Arial", 16), justify="right")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.display.focus_set()  # Set focus to entry for immediate keyboard input

        # Buttons layout
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C'
        ]
        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            tk.Button(root, text=button, width=5, height=2, font=("Arial", 14), command=cmd).grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.current = ""
        self.operation = ""
        self.first_num = 0
        self.expression = ""

        # Bind keyboard events
        self.root.bind('<Key>', self.handle_keypress)

    def handle_keypress(self, event):
        char = event.char
        if char in '0123456789.':
            self.click(char)
        elif char in '+-*/':
            self.click(char)
        elif char.lower() == 'c':
            self.click('C')
        elif event.keysym == 'Return':
            self.click('=')
        elif event.keysym == 'BackSpace':
            if self.current:
                self.current = self.current[:-1]
                self.expression = self.expression[:-1]
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, self.expression)
            elif self.operation:
                self.operation = ""
                self.expression = str(self.first_num)
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, self.expression)

    def click(self, char):
        if char == 'C':
            self.current = ""
            self.operation = ""
            self.first_num = 0
            self.expression = ""
            self.display.delete(0, tk.END)
        elif char in '0123456789.':
            self.current += char
            self.expression = self.expression.rstrip() + char
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, self.expression)
        elif char in '+-*/':
            if self.current:
                try:
                    self.first_num = float(self.current)
                    self.operation = char
                    self.expression = f"{self.first_num} {char} "
                    self.current = ""
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, self.expression)
                except ValueError:
                    messagebox.showerror("Error", "Invalid number!")
            elif self.operation and not self.current:
                self.operation = char
                self.expression = f"{self.first_num} {char} "
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, self.expression)
        elif char == '=':
            if self.current and self.operation:
                try:
                    second_num = float(self.current)
                    result = None
                    if self.operation == '+':
                        result = self.first_num + second_num
                    elif self.operation == '-':
                        result = self.first_num - second_num
                    elif self.operation == '*':
                        result = self.first_num * second_num
                    elif self.operation == '/':
                        if second_num != 0:
                            result = self.first_num / second_num
                        else:
                            messagebox.showerror("Error", "Cannot divide by zero!")
                    if result is not None:
                        self.current = str(result)
                        self.expression = str(result)
                        self.display.delete(0, tk.END)
                        self.display.insert(tk.END, self.expression)
                        self.operation = ""
                        self.first_num = result
                except ValueError:
                    messagebox.showerror("Error", "Invalid input!")
            self.current = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()