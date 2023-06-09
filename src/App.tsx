import './App.css';
import Profile from "./model/Profile";
import PlayRecord from "./model/PlayRecord";

const profile = require("./data/profile.json") as Profile;
const b30 = require("./data/rating.json") as PlayRecord[];
const r10 = require("./data/recent.json") as PlayRecord[];

function get_text_width(text: string, font: string) {
  const canvas = document.getElementById("text-width-canvas") as HTMLCanvasElement;
  const context = canvas.getContext("2d")!;
  context.font = font;
  const metrics = context.measureText(text);
  return metrics.width;
}

function get_name_size(name: string) {
  const families = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif"
  let size = 18;
  while (size > 8) {
    const width = get_text_width(name, `${size}px ${families}`);
    if (width <= 320) {
      break;
    }
    size -= 1;
  }
  return size;
}

function score_to_rank(score: number): string {
  const thresholds = [1009000, 1007500, 1005000, 1000000, 990000, 975000, 950000, 925000, 900000];
  const names = ["SSS+", "SSS", "SS+", "SS", "S+", "S", "AAA", "AA", "A"];
  for (let i = 0; i < thresholds.length; ++i) {
    if (score >= thresholds[i]) {
      return names[i];
    }
  }
  return "-";
}

function rating_to_class(rating: number): string {
  const thresholds = [1600, 1525, 1450, 1325, 1200, 1000, 700, 400, 0];
  const names = ["rainbow", "plat", "gold", "silver", "bronze", "purple", "red", "orange", "green"];
  for (let i = 0; i < thresholds.length; ++i) {
    if (rating >= thresholds[i]) {
      return "ra-" + names[i];
    }
  }
  return "";
}

function rating_str(rating: number): string {
  const s = rating.toString();
  return `${s.substring(0, 2)}.${s.substring(2)}`
}

function avg_rating(records: PlayRecord[]): number {
  return Math.floor(records.map(r => r.rating).reduce((a, b) => a+b) / records.length);
}

function Rating(rating: number) {
  return (
    <span className={`rating ${rating_to_class(rating)}`}>{rating_str(rating)}</span>
  )
}

function SongList(title: string, records: PlayRecord[]) {
  return (
    <div className="songList">
    <div className="listTitle">
      <span>{title}</span>
      <span className="rating">{rating_str(avg_rating(records))}</span>
    </div>
    {records.map((record, idx) => (
      <div className="songItem" key={`${record.musicId}-${record.score}`}>
        <img src={`resources/music_${record.musicId}.png`} />
        <div className="songInfo">
          <div className="songMeta">
            <div className="title">
            <span className={`level level-${record.level}`}>
              <span className="rating">{rating_str(record.ratingBase).substring(0, 4)}</span>
            </span>
            <span className="name" style={{
              fontSize: `${get_name_size(record.musicName)}px`
            }}>{record.musicName}</span>
            </div>
            <div className="scoreRank">
              <span className="score">{record.score}</span>
              <span className="rank">{score_to_rank(record.score)}</span>
            </div>
          </div>
          <div className="songRating">
            <span className="rank">#{idx+1}</span>
            {Rating(record.rating)}
          </div>
        </div>
      </div>
    ))}
  </div>
  )
}

export default function App() {
  return (
    <div className="app">
      <div className="profile"
        style={{
          backgroundImage: `url(resources/name_plate_${profile.nameplateId}.png)`,
          backgroundRepeat: "no-repeat",
        }}
      >
        <span className="userName">{profile.userName}</span>
        <span>
          <span className="left">Rating</span>
          <span className="rating-container">{Rating(profile.playerRating)}</span>
        </span>
        <span>
          <span className="left">Highest</span>
          <span className="rating-container">{Rating(profile.highestRating)}</span>
        </span>
        <img src="sun.png" className="game-logo" />
        <img src={`resources/chara_${profile.characterId}.png`} className="avatar" />
      </div>
      {SongList("Best 30", b30)}
      {SongList("Recent 10", r10)}
    </div>
  );
}
