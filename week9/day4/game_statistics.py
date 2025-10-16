import random
import json
import os
import glob

# --- Constants ---
_PLAYERS_FILE = "players.json"
_LEADERBOARD_FILE = "leaderboard.json"
_LEGACY_STATS_FILE = "game_stats.json"
_PER_PLAYER_PATTERN = "game_stats_*.json"

# --- Small utilities ---
def _safe_load_json(path: str, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        return default
    return default

def _safe_save_json(path: str, data) -> None:
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass

def _delete_if_exists(path: str) -> bool:
    if os.path.exists(path):
        try:
            os.remove(path)
            return True
        except OSError:
            return False
    return False


class GameStats: # Class to hold game statistics
    def __init__(self):
        self.games = 0
        self.wins = 0
        self.losses = 0
        self.ties = 0
        self.score = 0

    def to_dict(self): # Convert stats to dictionary for JSON serialization
        return {
            "games": self.games,
            "wins": self.wins,
            "losses": self.losses,
            "ties": self.ties,
            "score": self.score,
        }

    @staticmethod
    def from_dict(data: dict): # Create GameStats from dictionary
        stats = GameStats()
        stats.games = int(data.get("games", 0))
        stats.wins = int(data.get("wins", 0))
        stats.losses = int(data.get("losses", 0))
        stats.ties = int(data.get("ties", 0))
        # Ensure score is never negative when loading
        stats.score = max(0, int(data.get("score", 0)))
        return stats
    
def _player_stats_path(player_name: str) -> str:
    safe = "".join(c.lower() if c.isalnum() else "_" for c in (player_name or "")).strip("_") or "player"
    return f"game_stats_{safe}.json"

def load_stats(player_name: str) -> GameStats: # Load game stats from file for a player
    path = _player_stats_path(player_name)
    if not os.path.exists(path):
        # fallback to legacy global file
        legacy = _LEGACY_STATS_FILE
        if not os.path.exists(legacy):
            return GameStats()
        path = legacy
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return GameStats.from_dict(data)
            else:
                print("Stats file format unexpected; starting fresh.")
                return GameStats()
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error loading stats: {e}. Starting fresh.")
        return GameStats()
    
def save_stats(stats: GameStats, player_name: str): # Save game stats to file for a player
    try:
        path = _player_stats_path(player_name)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(stats.to_dict(), f, indent=2)
        print("Game statistics saved.")
    except OSError as e:
        print(f"Error saving stats: {e}")

def display_stats(stats: GameStats): # Display current game statistics
    print("\n=== Game Statistics ===")
    print(f"Total Games: {stats.games}")
    print(f"Wins:        {stats.wins}")
    print(f"Losses:      {stats.losses}")
    print(f"Ties:        {stats.ties}")
    print(f"Score:       {stats.score}")
    # Show global high score and who achieved it (best-effort)
    try:
        lb = _load_leaderboard()
        hs = int(lb.get("high_score", 0))
        hn = str(lb.get("high_scorer", ""))
        if hs > 0:
            who = f" by {hn}" if hn else ""
            print(f"High Score:  {hs}{who}")
        else:
            print("High Score:  0")
    except Exception:
        print("High Score:  0")
    # Show known player count (best-effort)
    try:
        pc = get_player_count()
        if pc > 0:
            print(f"Players:     {pc}")
    except Exception:
        pass
    print("=======================\n")

# --- Players registry helpers ---

def _normalize_name(name: str) -> str: # Normalize player name
    return (name or "").strip()

def _load_players() -> set: # Load players from registry file
    data = _safe_load_json(_PLAYERS_FILE, [])
    if isinstance(data, list):
        return set(_normalize_name(x) for x in data if isinstance(x, str) and _normalize_name(x))
    return set()

def _save_players(players: set) -> None: # Save players to registry file
    _safe_save_json(_PLAYERS_FILE, sorted(players))

def register_player(name: str) -> None: # Add a player to registry
    n = _normalize_name(name)
    if not n:
        return
    players = _load_players()
    if n not in players:
        players.add(n)
        _save_players(players)

def get_player_count() -> int: # Get count of registered players
    players = _load_players()
    if players:
        return len(players)
    # Fallback: scan saved per-player stats files
    try:
        files = glob.glob(_PER_PLAYER_PATTERN)
        return len(files)
    except Exception:
        return 0

def unregister_player(name: str) -> None: # Remove a player from registry
    n = _normalize_name(name)
    if not n:
        return
    players = _load_players()
    if n in players:
        players.remove(n)
        if players:
            _save_players(players)
        else:
            # If no players remain, remove the registry file
            _delete_if_exists(_PLAYERS_FILE)

def wipe_all(stats: GameStats) -> GameStats: # Wipe all saved statistics and players
    # Reset in-memory statistics
    stats.games = 0
    stats.wins = 0
    stats.losses = 0
    stats.ties = 0
    stats.score = 0

    # Delete all per-player stats files
    deleted = 0
    for path in glob.glob(_PER_PLAYER_PATTERN):
        if _delete_if_exists(path):
            deleted += 1

    # Delete legacy shared stats file if present
    if _delete_if_exists(_LEGACY_STATS_FILE):
        deleted += 1

    # Delete players registry
    _delete_if_exists(_PLAYERS_FILE)

    # Delete leaderboard file
    _delete_if_exists(_LEADERBOARD_FILE)

    if deleted:
        print("All game data has been wiped (files deleted).")
    else:
        print("All game data has been wiped (no files were present).")

    # Do NOT save after wipe to avoid recreating files
    return stats

def rock_paper_scissors(stats: GameStats, player_name: str): # Play looping Rock-Paper-Scissors
    choices = ['rock', 'paper', 'scissors']
    while True:
        user_choice = input("Enter rock/paper/scissors (or q to stop): ").strip().lower()
        if user_choice in ("q", "quit", "exit"):
            print("Returning to menu.\n")
            break
        if user_choice not in choices:
            print("Invalid choice. Please choose rock, paper, or scissors.\n")
            continue
        comp_choice = random.choice(choices)
        print(f"Computer chose: {comp_choice}")

        if user_choice == comp_choice:
            stats.ties += 1
            stats.games += 1
            print("It's a tie!\n")
        elif (user_choice == 'rock' and comp_choice == 'scissors') or \
             (user_choice == 'paper' and comp_choice == 'rock') or \
             (user_choice == 'scissors' and comp_choice == 'paper'):
            stats.wins += 1
            stats.games += 1
            stats.score += 1
            print("You win!\n")
        else:
            stats.losses += 1
            stats.games += 1
            # Clamp score to never go below 0
            stats.score = max(0, stats.score - 1)
            print("You lose!\n")

    # Update global leaderboard first so display reflects current top
    try:
        _update_leaderboard_if_needed(stats.score, player_name)
    except Exception:
        pass
    display_stats(stats) # Show stats after exiting game loop
    # Save stats after exiting game loop
    save_stats(stats, player_name)

# --- Leaderboard helpers (global high score) ---
def _load_leaderboard() -> dict:
    data = _safe_load_json(_LEADERBOARD_FILE, {"high_score": 0, "high_scorer": ""})
    if isinstance(data, dict):
        hs = int(data.get("high_score", 0))
        hn = str(data.get("high_scorer", ""))
        return {"high_score": max(0, hs), "high_scorer": hn}
    return {"high_score": 0, "high_scorer": ""}

def _save_leaderboard(high_score: int, high_scorer: str) -> None:
    _safe_save_json(_LEADERBOARD_FILE, {"high_score": int(max(0, high_score)), "high_scorer": str(high_scorer or "")})

def _update_leaderboard_if_needed(current_score: int, player_name: str) -> None:
    lb = _load_leaderboard()
    if int(current_score) > int(lb.get("high_score", 0)):
        _save_leaderboard(int(current_score), str(player_name or ""))

def menu(): # Display menu options
    print("=== Game Menu ===")
    print("1. Play Rock-Paper-Scissors")
    print("2. View Statistics")
    print("3. Wipe All Statistics")
    print("4. Exit")
    print("=================")

def main(): # Main program loop
    print("Welcome to the Game Statistics Tracker!")
    player_name = input("Enter your name: ").strip()
    stats = load_stats(player_name)
    # Register this player for counting
    register_player(player_name)
    
    while True:
        menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            rock_paper_scissors(stats, player_name)
        elif choice == "2":
            display_stats(stats)
        elif choice == "3":
            confirm = input("This will delete ALL saved stats and players. Type 'YES' to confirm: ").strip()
            if confirm == "YES":
                stats = wipe_all(stats)
            else:
                print("Wipe canceled.\n")
        elif choice == "4":
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()