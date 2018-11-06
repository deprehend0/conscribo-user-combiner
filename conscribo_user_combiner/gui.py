import tkinter
from tkinter import messagebox, Label, filedialog, Button, Text

# import combiner.combiner as c
import conscribo_user_combiner.combiner.combiner as c

window = tkinter.Tk()
window.title("Conscribo User Combiner")
window.geometry("500x300")


def combine():
    c.combine(t_old_users.get("1.0", "end"), t_new_users.get("1.0", "end"), t_export.get("1.0", "end"))
    messagebox.showinfo("Success", "The combining was succesful.\n You can find the files under {}".format(
        t_export.get("1.0", "end")))


def helloCallBack():
    messagebox.showinfo("Hello Python", "export_location: {}\n\nsignup_location: {}\n\nexport_folder: {}".format(
        t_new_users.get("1.0", "end"),
        t_old_users.get("1.0", "end"),
        t_export.get("1.0", "end")))


def openExportFolder():
    window.export_folder_location = filedialog.askdirectory(initialdir="~/Documents",
                                                            title="Select the target location")

    # t_export.delete(1.0, "END")
    t_export.insert(1.0, window.export_folder_location)


def openExportFile():
    window.export_location = filedialog.askopenfilename(initialdir="~/Downloads", title="Select conscribo export",
                                                        filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    try:
        with open(window.export_location, 'r'):
            print("File exists")
        # t_old_users.delete(1.0, "END")
        t_old_users.insert(1.0, window.export_location)
    except:
        messagebox.showinfo("Error",
                            "The file couldn't be found. Please make sure that you choose an actual file, not a folder.")


def openSingupFile():
    window.signup_location = filedialog.askopenfilename(initialdir="~/Downloads", title="Select conscribo export",
                                                        filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))

    try:
        with open(window.signup_location, 'r'):
            print("File exists")
        # t_new_users.delete(1.0, "END")
        t_new_users.insert(1.0, window.signup_location)
    except:
        messagebox.showinfo("Error",
                            "The file couldn't be found. Please make sure that you choose an actual file, not a folder.")


l_old_users = Label(window, text="Conscribo export file")
t_old_users = Text(window, height=1, width=30)
e_old_users = Button(window, text="Select conscribo export", command=openExportFile)

l_old_users.pack()
t_old_users.pack()
e_old_users.pack()

l_new_users = Label(window, text="Sign ups")
t_new_users = Text(window, height=1, width=30)
e_new_users = Button(window, text="Select sign up file", command=openSingupFile)

l_new_users.pack()
t_new_users.pack()
e_new_users.pack()

l_export = Label(window, text="The location where the files should be created")
t_export = Text(window, height=1, width=30)
e_export = Button(window, text="Select the export location", command=openExportFolder)

l_export.pack()
t_export.pack()
e_export.pack()

B = Button(window, text="abc", command=helloCallBack)
B.pack()

combine_button = Button(window, text="Combine", command=combine)
combine_button.pack()

window.mainloop()
