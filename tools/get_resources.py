import os
import shutil
from argparse import ArgumentParser
from pathlib import Path

from model import PlayRecord, Profile

data_root = Path(__file__).parent.parent / "src/data"
output_root = Path(__file__).parent.parent / "public/resources"


def get_profile_images(game_root: Path, profile: Profile) -> list[str]:
    name_plate_img = f"name_plate_{profile.nameplateId}.png"
    cond_copy(
        game_root / f"name_plate/image/{profile.nameplateId}.png",
        output_root / name_plate_img,
    )

    chara_img = f"chara_{profile.characterId}.png"
    cond_copy(
        game_root / f"chara/image/{profile.characterId}/02.png",
        output_root / chara_img,
    )

    return [name_plate_img, chara_img]


def get_music_covers(game_root: Path, records: list[PlayRecord]) -> list[str]:
    files = []
    for record in records:
        name = f"music_{record.musicId}.png"
        cond_copy(
            game_root / f"music/cover/{record.musicId}.png",
            output_root / name,
        )
        files.append(name)

    return files


def main():
    parser = ArgumentParser()
    parser.add_argument("game_data_root")
    args = parser.parse_args()
    game_root = Path(args.game_data_root)

    # profile
    profile = Profile.schema().loads(read_file(data_root / "profile.json"))
    required_files = get_profile_images(game_root, profile)

    # music
    records = PlayRecord.schema().loads(read_file(data_root / "rating.json"), many=True) + \
        PlayRecord.schema().loads(read_file(data_root / "recent.json"), many=True)
    required_files += get_music_covers(game_root, records)

    # remove old files
    required_files = set(required_files)
    for file in list(output_root.glob("*.png")):
        if file.name not in required_files:
            os.unlink(file)


def cond_copy(src: Path, dst: Path):
    if dst.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def read_file(file) -> str:
    with open(file, "r", encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    main()
