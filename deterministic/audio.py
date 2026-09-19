#turns a decision string into a spoken audio cue
import pyttsx3


class Speaker:
        def __init__(self, rate: int = 190):
                self._engine = pyttsx3.init()
                self._engine.setProperty("rate", rate)

        def say(self, text: str) -> None:
                self._engine.say(text)
                self._engine.runAndWait()
