import os
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def get_directory():
    root = tk.Tk()
    root.withdraw()
    directory = filedialog.askdirectory(title="Select Directory")
    return directory

def show_confirmation_dialog(results):
    root = tk.Tk()
    root.withdraw()

    message = "The following files will be renamed:\n\n"
    for on in results:
        message += f"{on['orig']}\n{on['newname']}\n\n"
    message += "\nDo you want to proceed?"

    ret = messagebox.askyesno("Confirmation", message)
    root.destroy()

    return ret

def show_rename_error_dialog(org,new):
    root = tk.Tk()
    root.withdraw()

    message = f"Failed to rename: {org} -> {new}\n\nDo want to try again?\nYES=Try again\nNO=Skip\nCANCEL=Quit"
    
    result = messagebox.askyesnocancel("Error", message)
    root.destroy()

    return result

def renameit(org,new):
    while True:
        try:
            os.rename(org, new)
            return
        except Exception as e:
            print(f"Error: {e}")

            action = show_rename_error_dialog(org,new)
            if action == True:
                continue
            elif action == False:
                print("Skipped.")
                return
            else:
                print("Operation canceled.")
                exit(1)

def rename_files_by_mtime(results):
    for on in results:
        renameit(on['orig_full'], on['newname_full'])


directory_path = get_directory()
if not directory_path:
    exit('No directory selected')

files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
files.sort(key=lambda x: os.path.getmtime(os.path.join(directory_path, x)))

results=[]
for index, filename in enumerate(files, start=1):
    file_path = os.path.join(directory_path, filename)
    newname=f"{index:03d} {filename}"
    results.append({
        'orig':filename,
        'orig_full': file_path,
        'newname':newname,
        'newname_full':os.path.join(directory_path,newname)
    })    

if not show_confirmation_dialog(results):
    exit()


rename_files_by_mtime(results)
