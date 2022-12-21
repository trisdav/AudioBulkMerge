# Much of this is ripped from pipe_test.py and so isn't necessarily tailored to the gui implementation.
import os
import sys
import json

class merge:
    def __init__(self):
        if sys.platform == 'win32':
            print("pipe-test.py, running on windows")
            self.TONAME = '\\\\.\\pipe\\ToSrvPipe'
            self.FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
            self.EOL = '\r\n\0'
        else:
            print("pipe-test.py, running on linux or mac")
            self.TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
            self.FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
            self.EOL = '\n'

        print("Write to  \"" + self.TONAME +"\"")
        if not os.path.exists(self.TONAME):
            print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
            sys.exit()

        print("Read from \"" + self.FROMNAME +"\"")
        if not os.path.exists(self.FROMNAME):
            print(" ..does not exist.  Ensure Audacity is running with mod-script-pipe.")
            sys.exit()

        print("-- Both pipes exist.  Good.")

        self.TOFILE = open(self.TONAME, 'w')
        print("-- File to write to has been opened")
        self.FROMFILE = open(self.FROMNAME, 'rt')
        print("-- File to read from has now been opened too\r\n")

    def send_command(self, command):
        """Send a single command."""
        print("Send: >>> \n"+command)
        self.TOFILE.write(command + self.EOL)
        self.TOFILE.flush()

    def get_response(self):
        """Return the command response."""
        result = ''
        line = ''
        while True:
            result += line
            line = self.FROMFILE.readline()
            if line == '\n' and len(result) > 0:
                break
        return result

    def do_command(self, command):
        """Send one command, and return the response."""
        self.send_command(command)
        response = self.get_response()
        print("Rcvd: <<< \n" + response)
        return response

    def quick_test(self):
        """Example list of commands."""
        self.do_command('Help: Command=Help')
        self.do_command('Help: Command="GetInfo"')
        #do_command('SetPreference: Name=GUI/Theme Value=classic Reload=1')

    def get_sound_files(self, filepath):
        all_files = os.listdir(filepath)
        audio_files = []
        # Filter out files that aren't audio files.
        for a_file in all_files:
            # Need to update to support more than just mp3
            if a_file.endswith(('.mp3', '.wav', '.aiff', '.au', '.ogg')):
                audio_files.append(a_file)
        return audio_files

    def process_merge(self, request, export, numCh=1):
        """ Request is a dictionary. This is done to de-couple this from the GUI.
        This leaves open the possibility of bypassing the GUI entirely, which will
        be quicker if the user has a predefined operation they want to perform.
        Potentially even making a shortcut to perform the operation with a simple
        double-click.

        Default to mono because there was time distortion when the input was mono.
        """
        # Get a list of audio files.
        files_to_merge = self.get_sound_files(request["working_dir"])
        # Load them into audacity
        for a_file in files_to_merge:
            # Import2: https://forum.audacityteam.org/viewtopic.php?t=108538
            self.do_command("Import2: Filename=" + request["working_dir"] + "/" + a_file)
        
        operation_list = request["merge_ops"]
        for op_id in operation_list:
            op = operation_list[op_id]
            
            # Select the track to modify
            select_track_string = "SelectTracks: Track=" + str(files_to_merge.index(op["file_path"]))
            self.do_command(select_track_string)
            
            # Now perform the operation
            operation_string = op["operation"] + ": "
            for param in op["parameters"]:
                operation_string += param + "=" + str(op["parameters"][param]) + " "
            self.do_command(operation_string)
        
        # Select all tracks
        self.do_command("SelAllTracks: ")
        # Now merge the tracks
        self.do_command("MixAndRender: ")
        # Now save as the export option
        self.do_command("Export2: Filename=" + export + " NumChannels=" + str(numCh))

if __name__ == "__main__":
    # This is intended for testing purposes.
    fp = "C:\\Users\\tristan\\Documents\\Audacity\\test2.json"
    ep  = "C:\\Users\\tristan\\Documents\\Audacity\\test2.mp3"
    jobj = None
    with open(fp) as file_in:
        lines = file_in.read()
        jobj = json.loads(lines)
    mg = merge()
    mg.process_merge(jobj, ep)
