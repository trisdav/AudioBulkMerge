# About
This is a project to merge several audio files into a single file, while simultaneously applying effects to each audio file being merged. It is an automation script for Audacity, using the mod-script-pipe functionality of audacity. This script was written with python verion 3.9.13 on Windows 10.

# Using
## Setting up Audacity
* First, go into Audacity preferences and enable mod-script-pipe, as shown in the image below.
![setup-audacity](https://github.com/trisdav/AudioBulkMerge/tree/initial/documentation/audacity-settings.PNG)
* Restart Audacity for the change to take effect.
## Running the script
* Run the main_interface.py script
'''bash
python3 main_interface.py
'''
![empty-project](https://github.com/trisdav/AudioBulkMerge/tree/initial/documentation/empty-project.PNG)
* Next select an input folder, that is a folder which contains the audio files to be merged.
![select-input-folder](https://github.com/trisdav/AudioBulkMerge/tree/documentation/select-input-folder.png)
* Then press the "New Operation" button to add an effect to a audio file.
![operations-added](https://github.com/trisdav/AudioBulkMerge/tree/initial/documentation/operations-added.PNG)
* When an operation is chosen the row will expand with the parameters for that operation, as shown below.
![operations-set](https://github.com/trisdav/AudioBulkMerge/tree/initial/documentation/operations-set.PNG)
* Export As will ask what to export the new audio file as, then perform all operations and merge all files.
* Save Config can be used to save a set of operations for later use.
* Once a config is loaded the Input Folder can be changed, but each operation row will need the Select File field to be reset.
