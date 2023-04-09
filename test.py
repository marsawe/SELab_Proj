import tkinter as tk

root = tk.Tk()

# Define a function to change the frame width
def change_width():
    frame.configure(width=300)

# Create a frame with width 200
frame = tk.Frame(root, width=200)
frame.pack()

# Create a button to change the frame width
button = tk.Button(root, text="Change Width", command=change_width)
button.pack()

root.mainloop()
