"""Functions that play wav voice files."""
import os
from playsound import playsound

def talk_wav(file_name):
    """Method that plays a prerecorded voice file."""
    os_path = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    file_path = os_path + f'/../../voices/{file_name}.mp3'
    playsound(file_path)
