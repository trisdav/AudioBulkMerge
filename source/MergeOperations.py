import tkinter as tk
from tkinter import ttk
import ScrollFrame
import opAmplify
import opChangePitch

class MergeOperations:
    primary_window = None

    def __init__(self, window):
        self.primary_window = window
        self.merge_ops = None
        self.operation_rows = {}
        self.op_id_ctr = 0
        self.op_names = ['-- select --','Amplify', 'ChangePitch']
        self.opClassDictionary = {'Amplify':opAmplify.opAmplify, 'ChangePitch':opChangePitch.opChangePitch}
        self.op_tips={"Amplify":"Increases or decreases the volume of the audio you have selected.\nfloat Ratio, (default:0.9)\nbool AllowClipping, (default:False)",
        "ChangePitch":"Change the pitch of a selection without changing its tempo.\ndouble Percentage, (default:0)\nbool SBSMS, (default:False)"}

    def save(self):
        """ Return a dictionary that can be used later to restore the state of merge operations. """
        save = {}
        for op in self.operation_rows:
            save_op = {}
            save_op["file_path"] = self.operation_rows[op].file_cb.get()
            save_op["operation"] = self.operation_rows[op].op_cb.get()
            save_op["parameters"] = self.operation_rows[op].opClass.parameters()
            save[str(op)] = save_op

        print(save)
        return save

    def load(self, save_obj):
        """ Load operations from a dictionary object. """
        # Get the id of the operation about to be created.
        op_id = self.op_id_ctr
        # Create a new operation.
        self.add_operation()
        # Set the operation file path
        values = self.operation_rows[op_id].file_cb['values']
        f_id = 0
        for value in values:
            if value == save_obj['file_path']:
                self.operation_rows[op_id].file_cb.current(f_id)
                break # Exit the for loop when the file is found
            f_id = f_id + 1
        


        # Now find the operation.
        if save_obj['operation'] != "-- select --": # Don't set operation, if operation was never set.
            # Set the operation combo box
            index = 0
            for name in self.op_names:
                if name == save_obj['operation']:
                    self.operation_rows[op_id].op_cb.current(index)
                    break
                index = index + 1

            # Initialize the operation parameters.
            op_name = save_obj['operation']
            op_row = self.operation_rows[op_id]
            op_row.opClass = self.opClassDictionary[op_name](op_row, save_obj['parameters'])

    def delete_operations(self):
        """ Delete all operation frames."""
        for item in self.operation_rows:
            self.operation_rows[item].destroy()

        self.operation_rows = {}
        self.op_id_ctr = 0

    def reset_file_cb(self, new_values):
        for item in self.operation_rows:
            self.operation_rows[item].file_cb['values'] = new_values
            self.operation_rows[item].file_cb.current(0)

    def delete_operation(self, op_id):
        """ Deletes an operation based on op_id. """
        self.operation_rows[op_id].destroy()
        del self.operation_rows[op_id]

    def delete_parameters(self, op_id):
        """ Destroy any parameters. """
        if self.operation_rows[op_id].opClass:
            self.operation_rows[op_id].opClass.destroy()

    def get_op_parameters(self, op_id):
        """ Create the parameters appropriate for the chosen operation.
        This is done by using the op_id to identify which combo box to get
        the selection from. """
        # Since a new selection has been made, delete existing parameters.
        self.delete_parameters(op_id)
        # Get the chosen operation
        chosen_op = self.operation_rows[op_id].op_cb.get()
        print(chosen_op)
        # Call the corresponding function for the given operation.
        if chosen_op != "-- select --":
            self.operation_rows[op_id].opClass = self.opClassDictionary[chosen_op](self.operation_rows[op_id])
    
    def add_operation(self):
        """ Adds an operation frame """
        values = self.primary_window.files_list
        if values == None:
            # Ignore if the user creates an operation without selecting files.
            return

        op_id = self.op_id_ctr
        self.op_id_ctr = self.op_id_ctr + 1
        self.operation_rows[op_id] = tk.LabelFrame(self.merge_ops.viewPort, text="Operation " + str(op_id))
        
        # Create a button to delete the operation.
        del_op = tk.Button(self.operation_rows[op_id])
        del_op["text"] = "X"
        del_op["command"] = lambda: self.delete_operation(op_id)
        del_op.grid(row=0, column=0)

        # Create a combobox to choose the file to operate on.
        label = tk.Label(self.operation_rows[op_id],text="Select File:")
        label.grid(row=0, column=1)
        file_cb = ttk.Combobox(self.operation_rows[op_id])
        file_cb['values'] = values
        file_cb.grid(row=0, column=2)
        # Set the selection to the first file.
        file_cb.current(0)
        self.operation_rows[op_id].file_cb = file_cb

        # Create a combobox to select the operation.
        label = tk.Label(self.operation_rows[op_id], text="Operation:")
        label.grid(row=0, column=3)
        self.operation_rows[op_id].op_cb = ttk.Combobox(self.operation_rows[op_id])
        self.operation_rows[op_id].op_cb["values"] = self.op_names
        #    self.locationBox.bind("<<ComboboxSelected>>", self.justamethod())
        self.operation_rows[op_id].op_cb.bind("<<ComboboxSelected>>", lambda x: self.get_op_parameters(op_id))
        self.operation_rows[op_id].op_cb.grid(row=0, column=4)
        self.operation_rows[op_id].op_cb.current(0)
        # Create a parameters list, this will be used to manage operation parameter inputs.
        self.operation_rows[op_id].parameters = []
        # Create a list of labels, this is necessary so they can be deleted later.
        self.operation_rows[op_id].labels = []
        self.operation_rows[op_id].pack()
        self.operation_rows[op_id].opClass = None

    def setMergeOpsFrame(self):
        self.merge_ops = ScrollFrame.ScrollFrame(self.primary_window)
        # Create input for setting the max line width
        self.new_op = tk.Button(self.merge_ops.viewPort)
        self.new_op["text"] = "New Operation"
        self.new_op["command"] = self.add_operation
        self.new_op.pack(side="bottom")
        return self.merge_ops
