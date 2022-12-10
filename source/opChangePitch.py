import tkinter as tk

class opChangePitch:
    def __init__(self, operation_row, parameters={"Percentage":"0", "SBSMS":0}):
        """
        id              action
        ChangePitch:	Change Pitch...	
        parameters
        double Percentage, (default:0)
        bool SBSMS, (default:False)
        description
        Change the pitch of a selection without changing its tempo.
        """
        # List of object which can be destroyed.
        self.destroy_list = []
        # A dictionary of the operation parameters.
        self.parameters_ = {"Percentage":None, "allowClipping":None}

        # Create the percentage box
        label = tk.Label(operation_row, text="Percentage")
        # Observe the last column used in the add_operation function.
        label.grid(row=0, column=5)
        pctBox = tk.Entry(operation_row, width=10)
        pctBox.grid(row=0, column=6)
        pctBox.insert(tk.END,parameters["Percentage"])

        # Create the SBSMS checkbox
        chkvar = tk.IntVar()
        sbsmsCheck = tk.Checkbutton(operation_row, text="SBSMS", onvalue=1, offvalue=0, variable=chkvar)
        sbsmsCheck.grid(row=0, column=7)

        # Activate the checkbox if sbsms should be activated by default/load.
        if parameters["SBSMS"] == 1:
            sbsmsCheck.select()
        
        # Append to list of items to be destroyed.
        self.destroy_list.append(label)
        self.destroy_list.append(pctBox)
        self.destroy_list.append(sbsmsCheck)
        
        self.parameters_["Percentage"] = pctBox
        self.parameters_["SBSMS"] = chkvar

    def destroy(self):
        for item in self.destroy_list:
            item.destroy()

    def parameters(self):
        """ Build and return a dictionary of the parameter values. """
        param_values = {}
        param_values['Percentage'] = self.parameters_['Percentage'].get()
        param_values['SBSMS'] = self.parameters_['SBSMS'].get()
        return param_values