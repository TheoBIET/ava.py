"""Core module of the voice assistant."""
from app.classes.voice_assistant import VoiceAssistant
from app.utils.talk_wav import talk_wav

if __name__ == '__main__':
    va = VoiceAssistant()
    talk_wav('how_can_i_help_you')
    va.run()