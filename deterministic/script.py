#periodic loop: pulls a classification reading, turns it into a decision, and speaks it
import time
from typing import Callable

from audio import Speaker
from plan import Classification, ObjectClass, Zone, decision

ClassificationSource = Callable[[], list[Classification]]


def run(get_classifications: ClassificationSource, speaker: Speaker, poll_interval: float = 1.0) -> None:
        last_spoken = None
        while True:
                message = decision(get_classifications())
                if message != last_spoken:  # avoid repeating the same cue every cycle
                        speaker.say(message)
                        last_spoken = message
                time.sleep(poll_interval)


def _demo_source() -> ClassificationSource:
        scenarios = [
                [],
                [Classification(Zone.CENTER, ObjectClass.CHAIR, 0.9)],
                [Classification(Zone.CENTER, ObjectClass.CHAIR, 0.9),
                 Classification(Zone.RIGHT, ObjectClass.PERSON, 0.8)],
                [Classification(Zone.CENTER, ObjectClass.TABLE, 0.7),
                 Classification(Zone.RIGHT, ObjectClass.OTHER_OBJECT, 0.6),
                 Classification(Zone.LEFT, ObjectClass.TRASH_CAN, 0.95)],
                [Classification(Zone.CENTER, ObjectClass.NO_OBJECT, 0.99)],
        ]
        state = {"i": 0}

        def source() -> list[Classification]:
                reading = scenarios[state["i"] % len(scenarios)]
                state["i"] += 1
                return reading

        return source


if __name__ == "__main__":
        demo = _demo_source()
        speaker = Speaker()
        try:
                run(demo, speaker, poll_interval=2.0)
        except KeyboardInterrupt:
                pass
