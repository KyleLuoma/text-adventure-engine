from pydub import AudioSegment
from pydub.playback import play

class GameNarrator:

    def __init__(self) -> None:
        pass

    def text_to_mp3(self, text: str) -> str:
        pass


class GameNarratorAWS(GameNarrator):

    from boto3 import Session
    from botocore.exceptions import BotoCoreError, ClientError

    def __init__(self) -> None:
        self.session = self.Session(profile_name="default")
        self.polly = self.session.client("polly")

    def text_to_mp3(self, text: str) -> str:
        try:
            response = self.polly.synthesize_speech(
                Text=text, 
                OutputFormat="mp3", 
                VoiceId="Joey"
            )
        except (self.BotoCoreError, self.ClientError) as error:
            print(error)
            raise error

        file = open(".tmp/speech.mp3", "wb")
        file.write(response['AudioStream'].read())
        file.close()

        play(AudioSegment.from_mp3(".tmp/speech.mp3"))

        return ".tmp/speech.mp3"