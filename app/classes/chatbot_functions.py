"""Class that regroups all the functions that the chatbot can execute."""
import subprocess

from app.utils.talk_wav import talk_wav

class ChatBotFunctions:
    """Class that regroups all the functions that the chatbot can execute."""
    @staticmethod
    def get_availables_functions():
        """Get a list of all the availables functions."""
        return {
            'launch_a_game': ChatBotFunctions.launch_a_game
        }

    @staticmethod
    def launch_a_game(name):
        """Launch a game installed on the computer from its name."""
        # Next: Load dynamically the games installed on the computer
        name = name.lower()

        path = {
            'trackmania': {
                'path': r'E:\SteamLibrary\steamapps\common\Trackmania\Trackmania.exe',
                'alias': ['tm', 'trackmania', 'trackmania2020', 'trackmania 2020']
            },
        }

        for game, data in path.items():
            if name == game or name in data['alias']:
                with subprocess.Popen(data['path']) as _:
                    talk_wav('i_launch_your_game')
                    break
