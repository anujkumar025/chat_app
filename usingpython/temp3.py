import tkinter as tk

root = tk.Tk()
root.geometry("400x300")

frame = tk.Frame(root, bg="lightgray")
frame.grid(row=0, column=0, sticky="nsew")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Label 1 with sticky="ns"
label1 = tk.Label(frame, text="Label 1", bg="red")
label1.grid(row=0, column=0, sticky="ns")

# Label 2 with sticky="nsew"
label2 = tk.Label(frame, text="Label 2", bg="blue")
label2.grid(row=1, column=0, sticky="nsew")

# Label 3 with no sticky
label3 = tk.Label(frame, text="Label 3", bg="green")
label3.grid(row=2, column=0)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=2)
frame.grid_rowconfigure(2, weight=1)
frame.grid_columnconfigure(0, weight=1)

root.mainloop()
