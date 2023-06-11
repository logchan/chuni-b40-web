import json
from argparse import ArgumentParser
from os.path import isfile
from pathlib import Path
from typing import Any, Callable

import requests
from model import Profile

data_root = Path(__file__).parent.parent / "src/data"


def write_file(file: Path, content: str):
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)


def patch_rating(ratings: str, get_resp: Callable[[str], str]) -> str:
    rating_list = json.loads(ratings)
    for ra in rating_list:
        music_id = ra["musicId"]
        play_data = json.loads(get_resp(f"song/{music_id}"))[0]
        ra["isFullCombo"] = play_data["isFullCombo"]
        ra["isAllJustice"] = play_data["isAllJustice"]
    return json.dumps(rating_list, ensure_ascii=False)


def main():
    parser = ArgumentParser()
    parser.add_argument("server")
    parser.add_argument("aime")
    args = parser.parse_args()

    def get_resp(ep: str) -> str:
        return requests.get(f"{args.server}/api/game/chuni/v2/{ep}?aimeId={args.aime}").text

    profile: Profile = Profile.schema().loads(get_resp("profile"))
    if isfile(data_root / "override.json"):
        with open(data_root / "override.json", "r", encoding="utf-8") as f:
            overrides = json.load(f)

    profile.characterId = overrides.get("characterId", profile.characterId)
    profile.nameplateId = overrides.get("nameplateId", profile.nameplateId)
    profile.trophyId = overrides.get("trophyId", profile.trophyId)

    write_file(data_root / "profile.json", Profile.schema().dumps(profile, indent=2, sort_keys=True, ensure_ascii=False))

    write_file(data_root / "recent.json", get_resp("rating/recent"))
    write_file(data_root / "rating.json", patch_rating(get_resp("rating"), get_resp))


if __name__ == "__main__":
    main()
