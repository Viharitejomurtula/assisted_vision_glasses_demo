#depending on where an object is a decision will be made on which way to guide the user
#will need to embed this in a periodic loop
from dataclasses import dataclass
from enum import Enum

CONFIDENCE_THRESHOLD = 0.5


class ObjectClass(Enum):
        TABLE = "Table"
        TRASH_CAN = "Trash Can"
        PERSON = "Person"
        FURNITURE = "Furniture"
        DOOR = "Door"
        CHAIR = "Chair"
        NO_OBJECT = "No Object"
        OTHER_OBJECT = "Other Object"


class Zone(Enum):
        CENTER = "center"
        RIGHT = "right"
        LEFT = "left"


@dataclass
class Classification:
        zone: Zone
        obj_class: ObjectClass
        confidence: float


class State(Enum):
        c = "center"
        cr = "center+right"
        cl = "center+left"
        r = "right"
        l = "left"
        crl = "stop"
        n = "none"


def _is_obstacle(c: Classification) -> bool:
        return c.obj_class != ObjectClass.NO_OBJECT and c.confidence > CONFIDENCE_THRESHOLD


def convert_to_state(classifications: list[Classification]) -> State:
        active_zones = {c.zone for c in classifications if _is_obstacle(c)}

        c = Zone.CENTER in active_zones
        r = Zone.RIGHT in active_zones
        l = Zone.LEFT in active_zones

        if c and r and l:
                return State.crl
        if c and r:
                return State.cr
        if c and l:
                return State.cl
        if c:
                return State.c
        if r:
                return State.r
        if l:
                return State.l
        return State.n


def _spoken_name(obj_class: ObjectClass) -> str:
        return "Object" if obj_class == ObjectClass.OTHER_OBJECT else obj_class.value


def build_message(state: State, classifications: list[Classification]) -> str:
        if state == State.n:
                return "Safe to proceed"
        if state == State.crl:
                return "Path obstructed, stop"

        by_zone = {c.zone: c for c in classifications if _is_obstacle(c)}

        if state == State.c:
                return f"{_spoken_name(by_zone[Zone.CENTER].obj_class)} in front, slow down"
        if state == State.r:
                return f"{_spoken_name(by_zone[Zone.RIGHT].obj_class)} on right, steer left"
        if state == State.l:
                return f"{_spoken_name(by_zone[Zone.LEFT].obj_class)} on left, steer right"
        if state == State.cr:
                return (f"{_spoken_name(by_zone[Zone.CENTER].obj_class)} in front and "
                        f"{_spoken_name(by_zone[Zone.RIGHT].obj_class)} on right, steer left")
        if state == State.cl:
                return (f"{_spoken_name(by_zone[Zone.CENTER].obj_class)} in front and "
                        f"{_spoken_name(by_zone[Zone.LEFT].obj_class)} on left, steer right")

        raise AssertionError(f"unhandled state: {state}")


def decision(classifications: list[Classification]) -> str:
        state = convert_to_state(classifications)
        return build_message(state, classifications)
