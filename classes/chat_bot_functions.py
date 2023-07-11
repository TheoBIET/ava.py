import subprocess

class ChatBotFunctions:
    @staticmethod
    def get_availables_functions():
        return {
            'launch_a_game': lambda name: ChatBotFunctions.launch_a_game(name)
        }
        
    
    @staticmethod
    def launch_a_game(name):
        name = name.lower()
        
        path = {
            'trackmania': {
                'path': 'E:\SteamLibrary\steamapps\common\Trackmania\Trackmania.exe',
                'alias': ['tm', 'trackmania', 'trackmania2020', 'trackmania 2020']
            },
            'counter-strike': {
                'path': 'E:\SteamLibrary\steamapps\common\Counter-Strike Global Offensive\csgo.exe',
                'alias': ['cs', 'counter strike', 'counter strike global offensive', 'counter-strike go', 'counter-strike: go', 'counter-strike: global offensive']
            }
        }
        
        for game in path:
            if name == game or name in path[game]['alias']:
                subprocess.Popen(path[game]['path'])
                break