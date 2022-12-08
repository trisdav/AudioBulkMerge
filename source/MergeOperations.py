import tkinter as tk
from tkinter import ttk
import ScrollFrame

class MergeOperations:
    primary_window = None

    def __init__(self, window):
        self.primary_window = window
        self.merge_ops = None
        self.operations = {}
        self.op_id_ctr = 0
        self.op_names = ['-- select --','Amplify', 'ChangePitch']
        self.op_funcions = {'Amplify':self.amplify, 'ChangePitch':self.change_pitch}
        self.op_tips={"Amplify":"Increases or decreases the volume of the audio you have selected.\nfloat Ratio, (default:0.9)\nbool AllowClipping, (default:False)",
        "ChangePitch":"Change the pitch of a selection without changing its tempo.\ndouble Percentage, (default:0)\nbool SBSMS, (default:False)"}

    def save(self):
        """ Return a dictionary that can be used later to restore the state of merge operations. """
        save = {}
        for op in self.operations:
            save_op = {}
            save_op["file_path"] = self.operations[op].file_cb.get()
            save_op["operation"] = self.operations[op].op_cb.get()
            index = 0
            params = {}
            for param in self.operations[op].parameters:
                # Try to get it like a combo box
                for key in param:
                    params[key] = param[key].get()
            save_op["parameters"] = params
            save[str(op)] = save_op

        print(save)
        return save

    def load(self, save_obj):
        """ Load operations from a dictionary object. """
        # Get the id of the operation about to be created.
        op_id = self.op_id_ctr
        # Create a new operation.
        self.add_operation()
        # Need to find which id to set...
        values = self.operations[op_id].file_cb['values']
        f_id = 0
        for value in values:
            if value == save_obj['file_path']:
                self.operations[op_id].file_cb.current(f_id)
                break # Exit the for loop when the file is found
            f_id = f_id + 1
        
        # Now find the operation.
        if save_obj['operation'] != "-- select --": # Don't set operation, if operation was never set.
            # Find the position of the operation name in the list.
            op_name_id = 0
            for op in self.op_names:
                if save_obj['operation'] == op:
                    self.operations[op_id].op_cb.current(op_name_id)
                    break
                op_name_id = op_name_id + 1
            # Call the appropriate function to set the parameters of the operation.
            self.op_funcions[save_obj['operation']](op_id, save_obj['parameters'])

    def delete_operations(self):
        """ Delete all operation frames."""
        for item in self.operations:
            self.operations[item].destroy()

        self.operations = {}
        self.op_id_ctr = 0

    def reset_file_cb(self, new_values):
        for item in self.operations:
            self.operations[item].file_cb['values'] = new_values
            self.operations[item].file_cb.current(0)

    def delete_operation(self, op_id):
        """ Deletes an operation based on op_id. """
        self.operations[op_id].destroy()
        del self.operations[op_id]

    def delete_parameters(self, op_id):
        """ Destroy any parameters. """
        for label in self.operations[op_id].labels:
            label.destroy()
        self.operations[op_id].parameters = []
        self.operations[op_id].labels = []

    def get_op_parameters(self, op_id):
        """ Create the parameters appropriate for the chosen operation.
        This is done by using the op_id to identify which combo box to get
        the selection from. """
        # Since a new selection has been made, delete existing parameters.
        self.delete_parameters(op_id)
        # Get the chosen operation
        chosen_op = self.operations[op_id].op_cb.get()
        print(chosen_op)
        # Call the corresponding function for the given operation.
        if chosen_op == "Amplify":
            self.amplify(op_id)
        elif chosen_op == "ChangePitch":
            self.change_pitch(op_id)
    
    def add_operation(self):
        """ Adds an operation frame """
        values = self.primary_window.files_list
        if values == None:
            # Ignore if the user creates an operation without selecting files.
            return

        op_id = self.op_id_ctr
        self.op_id_ctr = self.op_id_ctr + 1
        self.operations[op_id] = tk.LabelFrame(self.merge_ops.viewPort, text="Operation " + str(op_id))
        
        # Create a button to delete the operation.
        del_op = tk.Button(self.operations[op_id])
        del_op["text"] = "X"
        del_op["command"] = lambda: self.delete_operation(op_id)
        del_op.grid(row=0, column=0)

        # Create a combobox to choose the file to operate on.
        label = tk.Label(self.operations[op_id],text="Select File:")
        label.grid(row=0, column=1)
        file_cb = ttk.Combobox(self.operations[op_id])
        file_cb['values'] = values
        file_cb.grid(row=0, column=2)
        # Set the selection to the first file.
        file_cb.current(0)
        self.operations[op_id].file_cb = file_cb

        # Create a combobox to select the operation.
        label = tk.Label(self.operations[op_id], text="Operation:")
        label.grid(row=0, column=3)
        self.operations[op_id].op_cb = ttk.Combobox(self.operations[op_id])
        self.operations[op_id].op_cb["values"] = self.op_names
        #    self.locationBox.bind("<<ComboboxSelected>>", self.justamethod())
        self.operations[op_id].op_cb.bind("<<ComboboxSelected>>", lambda x: self.get_op_parameters(op_id))
        self.operations[op_id].op_cb.grid(row=0, column=4)
        self.operations[op_id].op_cb.current(0)
        # Create a parameters list, this will be used to manage operation parameter inputs.
        self.operations[op_id].parameters = []
        # Create a list of labels, this is necessary so they can be deleted later.
        self.operations[op_id].labels = []
        self.operations[op_id].pack()

    def setMergeOpsFrame(self):

        self.merge_ops = ScrollFrame.ScrollFrame(self.primary_window)
        # Create input for setting the max line width
        self.new_op = tk.Button(self.merge_ops.viewPort)
        self.new_op["text"] = "New Operation"
        self.new_op["command"] = self.add_operation
        self.new_op.pack(side="bottom")
        #self.open_file["command"] = self.input_file
        return self.merge_ops

    def amplify(self, op_id, parameters={"ratio":"0.9", "allowClipping":"0"}):
        """
        id          action
        Amplify:	Amplify...	
        parameters
        float Ratio, (default:0.9), This ratio is linear... I'll have to work out the conversion later.
        bool AllowClipping, (default:False)
        description
        Increases or decreases the volume of the audio you have selected.
        """
        # Create ratio option
        # So I don't have to type a lot
        op = self.operations[op_id]
        label = tk.Label(op, text="Ratio")
        ratioBox = tk.Entry(op, width=10)
        ratioBox.insert(tk.END, parameters["ratio"])
        # Observe the last column used in the add_operation function.
        label.grid(row=0, column=5)
        ratioBox.grid(row=0, column=6)
        # Append to the parameters so it can be referenced later.
        op.labels.append(label)
        op.labels.append(ratioBox)
        
        # Create AllowClipping option
        chkvar = tk.IntVar()
        clippingCheck = tk.Checkbutton(op, text="Allow Clipping", onvalue=1, offvalue=0, variable=chkvar)
        clippingCheck.grid(row=0, column=7)
        
        # Activate the checkbox if necessary
        if parameters["allowClipping"] == 1:
            clippingCheck.select()
        
        op.labels.append(clippingCheck)
        op.parameters.append({"ratio":ratioBox, "allowClipping":chkvar})

    def change_pitch(self, op_id, parameters={"percentage":"0", "sbsms":0}):
        """
        id              action
        ChangePitch:	Change Pitch...	
        parameters
        double Percentage, (default:0)
        bool SBSMS, (default:False)
        description
        Change the pitch of a selection without changing its tempo.
        """
        # Create the percentage box
        # So I don't have to type a lot
        op = self.operations[op_id]
        label = tk.Label(op, text="Percentage")
        # Observe the last column used in the add_operation function.
        label.grid(row=0, column=5)
        pctBox = tk.Entry(op, width=10)
        pctBox.grid(row=0, column=6)
        pctBox.insert(tk.END,parameters["percentage"])
        # Append to the parameters list so these can be managed.
        op.labels.append(label)
        
        op.labels.append(pctBox)

        # Create the SBSMS checkbox
        chkvar = tk.IntVar()
        sbsmsCheck = tk.Checkbutton(op, text="SBSMS", onvalue=1, offvalue=0, variable=chkvar)
        sbsmsCheck.grid(row=0, column=7)

        # Activate the checkbox if sbsms should be activated by default/load.
        if parameters["sbsms"] == 1:
            sbsmsCheck.select()

        # Labels should be renamed so something like, 'widgets' or 'widgets to delete' or something to that effect.
        op.labels.append(sbsmsCheck)
        op.parameters.append({"percentage":pctBox, "sbsms":chkvar})



    



        