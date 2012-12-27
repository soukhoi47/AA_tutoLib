# -*- coding: utf-8 -*-
"""Programme de configuration de Git
Alexandre Aury - 12/2012
Licence GPL
Release notes: 0.12.12
"""



#GitHub
cd ~/Documents/workspace/gitHub
#Private Git server
cd ~/Documents/workspace/gitPrivate


import os
import sys
import platform
import getopt
import shutil
import logging
import getpass
import ConfigParser

# Global variables
#-----------------------------------------------------------------------------
_VERSION = "0.12.12"

#Temporary Global Variables
#-----------------------------------------------------------------------------
_NAME="Alexandre Aury"
_MAIL="alexandre.aury@free.fr"
_MAIN_GIT_FOLDER="~/Documents/workspace/"
_REPO_SERVER=[{"name":"gitHub","repo":[git@github.com:soukhoi47/AA_tutoLib.git]}]

# System commands
#-----------------------------------------------------------------------------


# Classes
#-----------------------------------------------------------------------------
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    ORANGE = '\033[93m'
    NO = '\033[0m'

    def disable(self):
        self.RED = ''
        self.GREEN = ''
        self.BLUE = ''
        self.ORANGE = ''
        self.NO = ''

# Functions
#-----------------------------------------------------------------------------
def init():
    """
    Init the script
    """
    # Globals variables
    global _VERSION
    global _DEBUG

    # Set the log configuration
    logging.basicConfig( \
        filename=_LOG_FILE, \
        level=logging.DEBUG, \
        format='%(asctime)s %(levelname)s - %(message)s', \
         datefmt='%d/%m/%Y %H:%M:%S', \
     )

def showexec(description, command, exitonerror = 0, presskey = 0, waitmessage = ""):
    """
    Exec a system command with a pretty status display (Running / Ok / Warning / Error)
    By default (exitcode=0), the function did not exit if the command failed
    """

    if _DEBUG:
        logging.debug("%s" % description)
        logging.debug("%s" % command)

    # Wait message
    if (waitmessage == ""):
        waitmessage = description

    # Manage very long description
    if (len(waitmessage) > 65):
        waitmessage = waitmessage[0:65] + "..."
    if (len(description) > 65):
        description = description[0:65] + "..."

    # Display the command
    if (presskey == 1):
        status = "[ ENTER ]"
    else:    
        status = "[Running]"
    statuscolor = colors.BLUE
    sys.stdout.write (colors.NO + "%s" % waitmessage + statuscolor + "%s" % status.rjust(79-len(waitmessage)) + colors.NO)
    sys.stdout.flush()

    # Wait keypressed (optionnal)
    if (presskey == 1):
        try:
            input = raw_input
        except: 
            pass
        raw_input()

    # Run the command
    returncode = os.system ("/bin/sh -c \"%s\" >> /dev/null 2>&1" % command)
    
    # Display the result
    if ((returncode == 0) or (returncode == 25600)):
        status = "[  OK   ]"
        statuscolor = colors.GREEN
    else:
        if exitonerror == 0:
            status = "[Warning]"
            statuscolor = colors.ORANGE
        else:
            status = "[ Error ]"
            statuscolor = colors.RED

    sys.stdout.write (colors.NO + "\r%s" % description + statuscolor + "%s\n" % status.rjust(79-len(description)) + colors.NO)

    if _DEBUG: 
        logging.debug ("Returncode = %d" % returncode)

    # Stop the program if returncode and exitonerror != 0
    if ((returncode != 0) & (exitonerror != 0)):
        if _DEBUG: 
            logging.debug ("Forced to quit")
        exit(exitonerror)

def getstring(message = "Enter a value: "):
    """
    Ask user to enter a value
    """
    try:
        input = raw_input
    except: 
        pass
    return raw_input(message)


def waitenterpressed(message = "Press ENTER to continue..."):
    """
    Wait until ENTER is pressed
    """
    try:
        input = raw_input
    except: 
        pass
    raw_input(message)
    return 0


def main(argv):
    """
    Main function
    """
