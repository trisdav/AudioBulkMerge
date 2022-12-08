import tkinter as tk
import tkinter.filedialog
import os
import MergeOperations
import json
import merge

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.pack()
        self.create_widgets()
        self.files_list = None

    def create_widgets(self):
        # A menu bar with basic selections
        self.menubar = tk.Frame(self)
        # File picker for file to open
        self.menubar.open_folder = tk.Button(self.menubar)
        self.menubar.open_folder["text"] = "Select Input Folder"
        self.menubar.open_folder["command"] = self.input_folder

        # Label for displaying the currently selected folder.
        self.menubar.output_path = tk.Label(self.menubar)
        self.menubar.output_path["text"] = "..."
        # Chosen File
        self.menubar.folder_path = tk.Label(self.menubar)
        self.menubar.folder_path["text"] = "..."

        # Sound files to merge
        self.menubar.sound_list_label = tk.Label(self.menubar)
        self.menubar.sound_list_label["text"] = "Sound Files Found:"
        self.menubar.sound_list = tk.Label(self.menubar)

        # File picker for output folder
        self.menubar.output_folder = tk.Button(self.menubar)
        self.menubar.output_folder["text"] = "Export As"
        self.menubar.output_folder["command"] = self.select_output

        # Save config
        self.menubar.save_config = tk.Button(self.menubar)
        self.menubar.save_config["text"] = "Save Config"
        self.menubar.save_config["command"] = self.save
        
        # Load config
        self.menubar.load_config = tk.Button(self.menubar)
        self.menubar.load_config["text"] = "Load Config"
        self.menubar.load_config["command"] = self.load

        # Button to quit
        self.menubar.quit = tk.Button(self.menubar, text="QUIT", fg="red")
        self.menubar.quit["command"] = self.quit_safe

        # Frame to hold merge operations
        self.merge_ops = MergeOperations.MergeOperations(self)
        self.merge_ops_frame = self.merge_ops.setMergeOpsFrame()

        # Positioning
        self.menubar.open_folder.grid(row=0, column=0)
        self.menubar.folder_path.grid(row=1, column=0)
        self.menubar.output_folder.grid(row=0, column=1)
        self.menubar.output_path.grid(row=1, column=1)
        self.menubar.save_config.grid(row=0, column=2)
        self.menubar.load_config.grid(row=0, column=3)
        self.menubar.quit.grid(row=0, column=4)
        self.menubar.sound_list_label.grid(row=2, column=0)
        self.menubar.sound_list.grid(row=2, column=1)
        self.menubar.pack(side="top")

        self.merge_ops_frame.pack(side="bottom", fill="both", expand=True)
        self.pack(fill="both", expand=True)

    def input_folder(self, working_dir=None):
        """
        Select an input folder and load the results into the display.
        """
        if working_dir == None:
            # Get the folder path from the user.
            working_dir = tkinter.filedialog.askdirectory()
        
        # Set the working directory
        self.menubar.folder_path["text"]  = working_dir

        # Load a list of the files.
        self.files_list = self.get_sound_files(self.menubar.folder_path["text"])
        print(self.files_list)
        # Reset file selections
        self.merge_ops.reset_file_cb(self.files_list)
        # Create a comma separated string to display to the user.
        files_string = ", ".join(self.files_list)
        self.menubar.sound_list["text"] = files_string


    def select_output(self):
        fout = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.mp3')
        fout_name = fout.name
        fout.close()
        self.menubar.output_path["text"] = fout_name
        save = self.get_save_obj()
        mg = merge.merge()
        mg.process_merge(save, fout_name)

    def get_sound_files(self, filepath):
        all_files = os.listdir(filepath)
        audio_files = []
        # Filter out files that aren't audio files.
        for a_file in all_files:
            # Need to update to support more than just mp3
            if a_file.endswith(('.mp3', '.wav', '.aiff', '.au', '.ogg')):
                audio_files.append(a_file)
        return audio_files

    def quit_safe(self):
        self.master.destroy()

    def get_save_obj(self):
        save = {}
        save["working_dir"] = self.menubar.folder_path["text"]
        save["merge_ops"] = self.merge_ops.save()
        return save

    def save(self):
        """ Save the status of the application so that it can be restored later. """
        save_file = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.json')

        # Make sure save file selection succeeded before doing anything.
        if save_file:
            save = self.get_save_obj()
            save_file.write(json.dumps(save))
            save_file.close()
        else:
            messagebox.showingo("Error", "Cancelled")

    def load(self):
        """ Load a save file. """
        load_file = tkinter.filedialog.askopenfile(filetypes=[("json files", "*.json")])

        # Only continue processing if the file was chosen without error.
        if load_file:
            # Delete existing merge operations.
            self.merge_ops.delete_operations()
            # Load the file into an object.
            saved_str = load_file.read()
            saved = json.loads(saved_str)
            
            # Set the working directory.
            self.input_folder(saved["working_dir"])
            
            # Get the merge operations
            saved_ops = saved["merge_ops"]
            for op_id in saved_ops:
                print(saved_ops[op_id])
                self.merge_ops.load(saved_ops[op_id])
            


root = tk.Tk()
app = Application(master=root)
app.mainloop()