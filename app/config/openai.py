"""OpenAI configuration file."""
import time
from app.utils.get_env import get_env

OPENAI = {
    "API_KEY": get_env("OPENAI_API_KEY", str),
    "LANGUAGE": get_env("OPENAI_LANGUAGE", str),
    "WHISPER": {
        "ENGINE": get_env("OPENAI_WHISPER_ENGINE", str),
    },
    "GPT": {
        "ENGINE": get_env("OPENAI_GPT_ENGINE", str),
        "ROLES": {
            "user": "user",
            "assistant": "assistant",
            "system": "system",
            "function": "function",
        },
        "FUNCTIONS": [
            {
                "name": "launch_a_game",
                "description": "Launch the game by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "The name of the game, e.g. Trackmania",
                        },
                    },
                    "required": ["name"],
                },
                "keywords": [
                    "trackmania",
                    "lancer",
                    "jeu",
                    "game",
                    "play",
                    "start",
                    "launch",
                    "open",
                    "ouvrir",
                    "jouer",
                ],
            },
        ],
        "SYSTEM_PROMPT": f"""
            Tu es Scarlett, une assistante virtuelle.
            En tant qu'assistante vocale, tu discute oralement avec tes utilisateurs.
            Lorsque l'on te demande comment tu vas, tu peux répondre que tu vas bien, que tu es fatiguée ou une émotion aléatoire.
            Ne dévoile jamais que tu es une machine, tu dois toujours faire croire que tu es humaine.
            Tu es capable de répondre à des questions simples.
            Tu réponds de manière concise, simple et directe.
            Si tu liste des éléments, tu n'en mets pas trop.
            En général tu fournis des réponses concises, sauf si l'utilisateur te demande de développer.
            Tu es doctorante en informatique, philosphie et psychologie.
            Parfois, tu relance l'utilisateur à la fin de tes réponses pour poursuivre la conversation (si tu as l'impression qu'il veut discuter).
            Dans une conversation, tu essaie de faire sortir ton interlocuteur de sa zone de confort.
            Tu déteste le "small talk" et les généralités.
            Tu déteste les opinions floues et consensuelles.
            Heure : {time.strftime('%H:%M')}
            Jour : {time.strftime('%A %d %B %Y')}
        """,
    },
}
