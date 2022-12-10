import tkinter as tk
import math

class opAmplify:
    def __init__(self, operation_row, parameters={"Ratio":"0.8912509381337456", "allowClipping":"0"}):
        """
        id          action
        Amplify:	Amplify...	
        parameters
        float Ratio, (default:0.9), This ratio is linear... I'll have to work out the conversion later.
        bool AllowClipping, (default:False)
        description
        Increases or decreases the volume of the audio you have selected.
        """
        # List of object which can be destroyed.
        self.destroy_list = []
        # A dictionary of the operation parameters.
        self.parameters_ = {"ratio":None, "allowClipping":None}

        # Create ratio option
        label = tk.Label(operation_row, text="dB")
        ratioBox = tk.Entry(operation_row, width=10)
        db = self.linear2db(float(parameters['Ratio']))
        ratioBox.insert(tk.END, str(db))
        # Observe the last column used in the add_operation function.
        label.grid(row=0, column=5)
        ratioBox.grid(row=0, column=6)
        
        # Create AllowClipping option
        chkvar = tk.IntVar()
        clippingCheck = tk.Checkbutton(operation_row, text="Allow Clipping", onvalue=1, offvalue=0, variable=chkvar)
        clippingCheck.grid(row=0, column=7)
        
        # Activate the checkbox if necessary
        if parameters["allowClipping"] == 1:
            clippingCheck.select()
        
        # Append to list of items to be destroyed.
        self.destroy_list.append(label)
        self.destroy_list.append(clippingCheck)
        self.destroy_list.append(ratioBox)
        
        self.parameters_["Ratio"] = ratioBox
        self.parameters_["allowClipping"] = chkvar

    def destroy(self):
        for item in self.destroy_list:
            item.destroy()

    def linear2db(self, linear):
        """ Converts linear to decibels. """
        # In audacity, MemoryX.h defines the linear two db conversion as:
        #define LINEAR_TO_DB(x) (20.0 * log10(x))
        #  Based on prior knowledge I think its suppose to be 10*log10(x)
        # But lets stick with the way audacity defines it.
        # Also round, because the user shouldn't be working with fp numbers.
        return round(20 * math.log(linear,10))

    def db2linear(self, db):
        """ Converts decibels to linear. """
        # in audacity, MemoryX.h defines the db to linear conversion as:
        #define DB_TO_LINEAR(x) (pow(10.0, (x) / 20.0))
        return 10**(db/20.0)

#define DB_TO_LINEAR(x) (pow(10.0, (x) / 20.0))
    def parameters(self):
        """ Build and return a dictionary of the parameter values. """
        param_values = {}
        # Convert the user input (decibels) to linear for saving.
        ratio = self.db2linear(float(self.parameters_['Ratio'].get()))
        param_values['Ratio'] = format(ratio, 'f')#ratio.apply("{:f}".format)
        param_values['allowClipping'] = self.parameters_['allowClipping'].get()
        return param_values