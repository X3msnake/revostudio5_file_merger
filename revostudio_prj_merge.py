import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import Label
import json
import os
import shutil


last_selected_folder = './'  # Default folder path


def merge_files():
    main_file = mainfileBox.get()
    merge_files = mergefilesLst.get(0, tk.END)

    if not main_file or not merge_files:
        return

    try:
        with open(main_file, 'r') as f:
            main_data = json.load(f)
    except FileNotFoundError:
        print("Main file not found.")
        return
    except json.JSONDecodeError:
        print("Invalid JSON format in the main file.")
        return

    merged_file_path = filedialog.asksaveasfilename(defaultextension='.revo',
                                                    filetypes=[('Revostudio Files', '*.revo')],
                                                    initialdir=last_selected_folder,
                                                    title='Save Merged File')
    if merged_file_path:
        total_files = sum(1 for merge_file in merge_files if os.path.isdir(os.path.join(os.path.dirname(merge_file), 'data')))
        
        # Create progress bar
        progress = 0
        progress_bar = Progressbar(root, orient=tk.HORIZONTAL, length=500, mode='determinate')
        progress_bar.place(relx=0.083, rely=0.778, relwidth=0.833, relheight=0.0, height=73)
        progress_bar['maximum'] = total_files
        
        # Create spinner label
        spinner_label = Label(root, text="Merging files...", font=("Arial", 12))
        spinner_label.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

        # Copy data folder content from main file to merged file
        main_data_path = os.path.dirname(main_file)
        main_data_folder_path = os.path.join(main_data_path, 'data')
        if os.path.isdir(main_data_folder_path):
            new_data_folder_path = os.path.join(os.path.dirname(merged_file_path), 'data')
            if not os.path.exists(new_data_folder_path):
                os.makedirs(new_data_folder_path)
            else:
                print(f"Destination folder '{new_data_folder_path}' already exists. Merging files.")
            merge_data_files(main_data_folder_path, new_data_folder_path)
            progress += 1
            progress_bar['value'] = progress
            root.update()

        for merge_file in merge_files:
            merge_data_path = os.path.dirname(merge_file)
            data_folder_path = os.path.join(merge_data_path, 'data')
            
            # Update spinner Label
            filename = os.path.basename(merge_file)
            spinner_label.config(text=filename)
            
            if os.path.isdir(data_folder_path):
                new_data_folder_path = os.path.join(os.path.dirname(merged_file_path), 'data')
                if not os.path.exists(new_data_folder_path):
                    os.makedirs(new_data_folder_path)
                else:
                    print(f"Destination folder '{new_data_folder_path}' already exists. Merging files.")
                merge_data_files(data_folder_path, new_data_folder_path)
                progress += 1
                progress_bar['value'] = progress
                root.update()
                

        for merge_file in merge_files:
            try:
                with open(merge_file, 'r') as f:
                    merge_data = json.load(f)
            except FileNotFoundError:
                print(f"Merge file '{merge_file}' not found.")
                continue
            except json.JSONDecodeError:
                print(f"Invalid JSON format in the merge file '{merge_file}'.")
                continue

            main_data['nodes'].extend(merge_data['nodes'])

        with open(merged_file_path, 'w') as f:
            json.dump(main_data, f, indent=4)
        print("Files merged successfully.")
        
        # Hide progress bar after 100%
        progress_bar['value'] = total_files
        root.update()
        spinner_label.destroy()  # Remove the spinner label from the UI
        progress_bar.destroy()  # Remove the progress bar from the UI
   
        # Show popup window with result and options
        choice = messagebox.askquestion("Files merged successfully!", "Do you want to merge more files?")
        if choice == "yes":
            # Return to the script
            pass  # Reset the file lists
            mainfileBox.delete(0, tk.END)
            mergefilesLst.delete(0, tk.END)
        else:
            # Exit the application
            root.quit()
            
            
def merge_data_files(src_dir, dst_dir):
    for root, dirs, files in os.walk(src_dir):
        rel_root = os.path.relpath(root, src_dir)
        dst_root = os.path.join(dst_dir, rel_root)
        os.makedirs(dst_root, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dst_root, file)
            shutil.copy2(src_file, dst_file)
        

def add_main_file():
    global last_selected_folder

    file_path = filedialog.askopenfilename(filetypes=[('Revostudio Files', '*.revo')],
                                           initialdir=last_selected_folder,
                                           title='Select Main Project File')
    if file_path:
        mainfileBox.delete(0, tk.END)
        mainfileBox.insert(0, file_path)
        
        # Update the last selected folder
        last_selected_folder = os.path.dirname(os.path.dirname(file_path))


def add_merge_files():
    global last_selected_folder

    file_paths = filedialog.askopenfilenames(filetypes=[('Revostudio Files', '*.revo')],
                                             initialdir=last_selected_folder,
                                             title='Select Project Files to Merge')
    if file_paths:
        for file_path in file_paths:
            mergefilesLst.insert(tk.END, file_path)
        
        # Update the last selected folder
        last_selected_folder = os.path.dirname(os.path.dirname(file_paths[0]))
        
        
def delete_selected_entry(event):
    selected_indices = mergefilesLst.curselection()
    if selected_indices:
        index = selected_indices[0]
        mergefilesLst.delete(index)


root = tk.Tk()

# UI initialization code

root.geometry("600x450+558+61")
root.minsize(600, 150)
root.maxsize(150, 600)
root.resizable(1,  1)
root.title("Revostudio5 Project Merger")
root.configure(background="#b3b3b0")
root.configure(highlightbackground="#d9d9d9")
root.configure(highlightcolor="black")

mergefilesLst = tk.Listbox(root)
mergefilesLst.place(relx=0.083, rely=0.311, relheight=0.333, relwidth=0.833)
mergefilesLst.configure(background="white")
mergefilesLst.configure(disabledforeground="#a3a3a3")
mergefilesLst.configure(font="TkFixedFont")
mergefilesLst.configure(foreground="#000000")
mergefilesLst.configure(highlightbackground="#d9d9d9")
mergefilesLst.configure(highlightcolor="black")
mergefilesLst.configure(selectbackground="#c4c4c4")
mergefilesLst.configure(selectforeground="black")

mainfileBox = tk.Entry(root)
mainfileBox.place(relx=0.083, rely=0.067, height=35, relwidth=0.833)
mainfileBox.configure(background="white")
mainfileBox.configure(disabledforeground="#a3a3a3")
mainfileBox.configure(font="TkFixedFont")
mainfileBox.configure(foreground="#000000")
mainfileBox.configure(highlightbackground="#d9d9d9")
mainfileBox.configure(highlightcolor="black")
mainfileBox.configure(insertbackground="black")
mainfileBox.configure(selectbackground="#c4c4c4")
mainfileBox.configure(selectforeground="black")

mainfileBtn = tk.Button(root)
mainfileBtn.place(relx=0.083, rely=0.156, height=35, width=500)
mainfileBtn.configure(activebackground="beige")
mainfileBtn.configure(activeforeground="black")
mainfileBtn.configure(background="#fbebb3")
mainfileBtn.configure(compound='left')
mainfileBtn.configure(disabledforeground="#a3a3a3")
mainfileBtn.configure(foreground="#000000")
mainfileBtn.configure(highlightbackground="#d9d9d9")
mainfileBtn.configure(highlightcolor="black")
mainfileBtn.configure(pady="0")
mainfileBtn.configure(text='''ADD MAIN PROJECT FILE''')
mainfileBtn.configure(command=add_main_file)

mergeBtn = tk.Button(root)
mergeBtn.place(relx=0.358, rely=0.778, height=73, width=335)
mergeBtn.configure(activebackground="beige")
mergeBtn.configure(activeforeground="black")
mergeBtn.configure(background="#e2fcb1")
mergeBtn.configure(compound='left')
mergeBtn.configure(disabledforeground="#a3a3a3")
mergeBtn.configure(foreground="#000000")
mergeBtn.configure(highlightbackground="#d9d9d9")
mergeBtn.configure(highlightcolor="black")
mergeBtn.configure(pady="0")
mergeBtn.configure(text='''MERGE FILES''')
mergeBtn.configure(command=merge_files)

cancelBtn = tk.Button(root)
cancelBtn.place(relx=0.083, rely=0.778, height=73, width=146)
cancelBtn.configure(activebackground="#ffffff")
cancelBtn.configure(activeforeground="black")
cancelBtn.configure(background="#fdb0b0")
cancelBtn.configure(compound='left')
cancelBtn.configure(disabledforeground="#a3a3a3")
cancelBtn.configure(foreground="#000000")
cancelBtn.configure(highlightbackground="#d9d9d9")
cancelBtn.configure(highlightcolor="black")
cancelBtn.configure(pady="0")
cancelBtn.configure(text='''EXIT''')
cancelBtn.configure(command=root.quit)

mergefilesBtn = tk.Button(root)
mergefilesBtn.place(relx=0.083, rely=0.667, height=35, width=500)
mergefilesBtn.configure(activebackground="beige")
mergefilesBtn.configure(activeforeground="black")
mergefilesBtn.configure(background="#b8b3fb")
mergefilesBtn.configure(compound='left')
mergefilesBtn.configure(disabledforeground="#a3a3a3")
mergefilesBtn.configure(foreground="#000000")
mergefilesBtn.configure(highlightbackground="#d9d9d9")
mergefilesBtn.configure(highlightcolor="black")
mergefilesBtn.configure(pady="0")
mergefilesBtn.configure(text='''ADD PROJECTS TO MERGE''')
mergefilesBtn.configure(command=add_merge_files)

# Bind the Delete key event to the delete_selected_entry function
mergefilesLst.bind("<Delete>", delete_selected_entry)

root.mainloop()
