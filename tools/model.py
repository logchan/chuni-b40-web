from dataclasses import dataclass

from dataclasses_json import Undefined, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Profile:
    userName: str
    playerRating: int
    highestRating: int
    nameplateId: int
    characterId: int
    trophyId: int


@dataclass_json
@dataclass
class PlayRecord:
    musicId: int
    musicName: str
    artistName: str
    level: int
    score: int
    ratingBase: int
    rating: int
