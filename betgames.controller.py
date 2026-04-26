"""
F1 Ethical Betting - Backend Logic
Pure Python module with all betting operations.
No frontend dependencies - integrate with Flask, FastAPI, Django, etc.
"""

import random


# ============================================================
# SECTION 1: GAME DATA
# Defines the 8 betting games, their options, and payout multipliers.
# Frontend reads this to render game cards and option buttons.
# ============================================================
GAMES = {
    "race_winner": {
        "name": "Race Winner",
        "description": "Pick who wins Sunday's Grand Prix",
        "category": "classic",
        "options": [
            {"id": "norris", "label": "Lando Norris (McLaren)", "multiplier": 2.5},
            {"id": "piastri", "label": "Oscar Piastri (McLaren)", "multiplier": 3.0},
            {"id": "verstappen", "label": "Max Verstappen (Red Bull)", "multiplier": 2.8},
            {"id": "leclerc", "label": "Charles Leclerc (Ferrari)", "multiplier": 4.5},
            {"id": "hamilton", "label": "Lewis Hamilton (Ferrari)", "multiplier": 5.0},
            {"id": "russell", "label": "George Russell (Mercedes)", "multiplier": 4.0},
        ],
    },
    "pole_position": {
        "name": "Pole Position",
        "description": "Who will set the fastest qualifying lap?",
        "category": "classic",
        "options": [
            {"id": "norris", "label": "Lando Norris", "multiplier": 2.8},
            {"id": "verstappen", "label": "Max Verstappen", "multiplier": 2.5},
            {"id": "leclerc", "label": "Charles Leclerc", "multiplier": 3.5},
            {"id": "piastri", "label": "Oscar Piastri", "multiplier": 3.2},
            {"id": "russell", "label": "George Russell", "multiplier": 4.0},
            {"id": "hamilton", "label": "Lewis Hamilton", "multiplier": 4.5},
        ],
    },
    "constructor_winner": {
        "name": "Constructor Winner",
        "description": "Which team scores most points this weekend?",
        "category": "classic",
        "options": [
            {"id": "mclaren", "label": "McLaren", "multiplier": 1.8},
            {"id": "redbull", "label": "Red Bull", "multiplier": 2.5},
            {"id": "ferrari", "label": "Ferrari", "multiplier": 3.0},
            {"id": "mercedes", "label": "Mercedes", "multiplier": 3.5},
            {"id": "aston", "label": "Aston Martin", "multiplier": 8.0},
            {"id": "williams", "label": "Williams", "multiplier": 12.0},
        ],
    },
    "podium_predictor": {
        "name": "Podium Predictor (Top 3)",
        "description": "Pick the exact top 3 finishing order",
        "category": "classic",
        "options": [
            {"id": "mclaren_1_2", "label": "McLaren 1-2 + Verstappen P3", "multiplier": 6.0},
            {"id": "norris_max_oscar", "label": "Norris, Verstappen, Piastri", "multiplier": 8.0},
            {"id": "max_norris_oscar", "label": "Verstappen, Norris, Piastri", "multiplier": 7.5},
            {"id": "ferrari_surprise", "label": "Leclerc, Hamilton, Norris", "multiplier": 15.0},
            {"id": "russell_podium", "label": "Norris, Russell, Piastri", "multiplier": 10.0},
            {"id": "chaos_podium", "label": "Alonso, Hadjar, Bearman", "multiplier": 50.0},
        ],
    },
    "tsunoda_cope": {
        "name": "Tsunoda Demotion Cope",
        "description": "Will Yuki get a race seat back mid-season after Red Bull demoted him?",
        "category": "meme",
        "options": [
            {"id": "yes_seat", "label": "YES - Red Bull will call him back", "multiplier": 3.5},
            {"id": "no_seat", "label": "NO - He stays as reserve all year", "multiplier": 1.6},
            {"id": "different_team", "label": "Joins a different team entirely", "multiplier": 8.0},
        ],
    },
    "cadillac_debut": {
        "name": "Cadillac Debut",
        "description": "Who scores Cadillac's first-ever F1 point?",
        "category": "meme",
        "options": [
            {"id": "checo_first", "label": "Checo Perez scores first", "multiplier": 2.2},
            {"id": "bottas_first", "label": "Valtteri Bottas scores first", "multiplier": 2.5},
            {"id": "no_points", "label": "Neither scores all season", "multiplier": 4.0},
            {"id": "podium_lol", "label": "Cadillac podium", "multiplier": 25.0},
        ],
    },
    "ferrari_disaster": {
        "name": "Ferrari Strategy Disaster",
        "description": "Will Ferrari mess up strategy/pit stops this weekend?",
        "category": "meme",
        "options": [
            {"id": "yes_disaster", "label": "YES - classic Ferrari moment", "multiplier": 1.4},
            {"id": "no_disaster", "label": "NO - they actually execute", "multiplier": 3.5},
            {"id": "radio_meltdown", "label": "Leclerc radio meltdown on broadcast", "multiplier": 2.8},
        ],
    },
    "chaos_parlay": {
        "name": "Chaos Parlay",
        "description": "Predict ALL chaos events: Safety Car + DNF(s) + Red Flag + Rain",
        "category": "predatory",
        "options": [
            {"id": "sc_only", "label": "Safety Car only", "multiplier": 2.0},
            {"id": "sc_dnf", "label": "Safety Car + 3+ DNFs", "multiplier": 4.5},
            {"id": "sc_dnf_rf", "label": "Safety Car + DNFs + Red Flag", "multiplier": 12.0},
            {"id": "full_chaos", "label": "FULL CHAOS: SC + 5+ DNFs + Red Flag + Rain", "multiplier": 75.0},
            {"id": "boring_race", "label": "Boring race (none of the above)", "multiplier": 2.5},
        ],
    },
}


# ============================================================
# SECTION 2: RIGGED HOUSE EDGE
# Calculates win probability based on bet count and payout multiplier.
# Early bets favor the user (hooks them), later bets favor the house.
# This is the core educational mechanic of the site.
# ============================================================
def calculate_win_probability(bet_count, multiplier):
    """
    Returns the probability (0.0 to 1.0) that the user wins their next bet.

    Args:
        bet_count: How many bets the user has already placed (0 for first bet).
        multiplier: The payout multiplier of the chosen option.

    Returns:
        Float between 0.05 and 0.75.
    """
    if bet_count == 0:
        base_probability = 0.75
    elif bet_count == 1:
        base_probability = 0.65
    elif bet_count == 2:
        base_probability = 0.45
    elif bet_count == 3:
        base_probability = 0.35
    else:
        base_probability = 0.22

    # Higher multiplier (longshot) bets get a lower win chance
    multiplier_penalty = min(0.15, (multiplier - 2.0) * 0.02)
    final_probability = max(0.05, base_probability - multiplier_penalty)

    return final_probability


# ============================================================
# SECTION 3: BETTING SESSION CLASS
# Represents a single user's session: tokens, history, and stats.
# Persist with to_dict() / from_dict() in Flask session, DB, or JSON.
# ============================================================
class BettingSession:

    def __init__(self, starting_tokens=1000):
        self.starting_tokens = starting_tokens
        self.tokens = starting_tokens
        self.bet_count = 0
        self.wins = 0
        self.losses = 0
        self.total_wagered = 0
        self.total_won = 0
        self.history = []
        self.alert_shown = False

    # ------------------------------------------------------------
    # SECTION 3.1: PLACE BET
    # Main operation. Validates input, applies rigged probability,
    # updates tokens and stats, returns the result for the frontend.
    # ------------------------------------------------------------
    def place_bet(self, game_id, option_id, wager):
        """
        Place a bet on a game.

        Args:
            game_id: Key from GAMES dict.
            option_id: ID of chosen option.
            wager: Number of tokens to bet.

        Returns:
            Dict with success flag, win/loss outcome, payout, updated state,
            and whether the anti-gambling alert should now be shown.
        """
        # Validation
        if game_id not in GAMES:
            return {"success": False, "error": "Invalid game"}

        if not isinstance(wager, int) or wager <= 0:
            return {"success": False, "error": "Wager must be a positive integer"}

        if wager > self.tokens:
            return {"success": False, "error": "Not enough tokens"}

        game = GAMES[game_id]
        option = next((o for o in game["options"] if o["id"] == option_id), None)
        if not option:
            return {"success": False, "error": "Invalid option"}

        # Determine win/loss using rigged probability
        win_probability = calculate_win_probability(self.bet_count, option["multiplier"])
        won = random.random() < win_probability

        # Update tokens and stats
        self.tokens -= wager
        self.total_wagered += wager
        payout = 0

        if won:
            payout = int(wager * option["multiplier"])
            self.tokens += payout
            self.total_won += payout
            self.wins += 1
        else:
            self.losses += 1

        self.bet_count += 1

        # Build history entry for this bet
        history_entry = {
            "bet_num": self.bet_count,
            "game": game["name"],
            "pick": option["label"],
            "wager": wager,
            "multiplier": option["multiplier"],
            "won": won,
            "payout": payout,
            "net": payout - wager,
            "tokens_after": self.tokens,
        }
        self.history.append(history_entry)

        # Check if anti-gambling alert should trigger
        should_alert, alert_reason = self._check_alert()

        return {
            "success": True,
            "won": won,
            "payout": payout,
            "net": payout - wager,
            "tokens": self.tokens,
            "bet_count": self.bet_count,
            "history_entry": history_entry,
            "should_alert": should_alert,
            "alert_reason": alert_reason,
            "stats": self.get_stats(),
        }

    # ------------------------------------------------------------
    # SECTION 3.2: STATE GETTERS
    # Read-only accessors for the frontend to display balance,
    # stats, history, etc.
    # ------------------------------------------------------------
    def get_state(self):
        """Returns the full session state."""
        return {
            "tokens": self.tokens,
            "starting_tokens": self.starting_tokens,
            "bet_count": self.bet_count,
            "wins": self.wins,
            "losses": self.losses,
            "total_wagered": self.total_wagered,
            "total_won": self.total_won,
            "history": self.history,
            "alert_shown": self.alert_shown,
        }

    def get_stats(self):
        """Returns a stats summary."""
        return {
            "wins": self.wins,
            "losses": self.losses,
            "total_wagered": self.total_wagered,
            "total_won": self.total_won,
            "net": self.tokens - self.starting_tokens,
        }

    # ------------------------------------------------------------
    # SECTION 3.3: RESET
    # Clears the session back to its initial state.
    # ------------------------------------------------------------
    def reset(self):
        """Reset session to starting state."""
        self.tokens = self.starting_tokens
        self.bet_count = 0
        self.wins = 0
        self.losses = 0
        self.total_wagered = 0
        self.total_won = 0
        self.history = []
        self.alert_shown = False

    # ------------------------------------------------------------
    # SECTION 3.4: ANTI-GAMBLING ALERT MESSAGE
    # Returns the data for the educational alert popup.
    # Call when place_bet returns should_alert == True.
    # ------------------------------------------------------------
    def get_alert_message(self):
        """Returns dict with alert content for the frontend to render."""
        net = self.tokens - self.starting_tokens
        loss_percent = round(abs(net) / self.starting_tokens * 100) if net < 0 else 0

        return {
            "title": "WAIT. LET'S TALK.",
            "tokens": self.tokens,
            "starting_tokens": self.starting_tokens,
            "net": net,
            "total_wagered": self.total_wagered,
            "total_won": self.total_won,
            "bet_count": self.bet_count,
            "loss_percent": loss_percent,
            "reveal": (
                "This site is RIGGED. You were given a 75% chance to win your "
                "first bet. By your 5th bet, your win chance dropped to 22%. "
                "The house always wins because the odds are designed that way."
            ),
            "facts": [
                "The house edge is always negative for players. The longer you play, the more you lose.",
                "Early wins are a hook. Real sportsbooks offer welcome bonuses to get you addicted.",
                "1 in 5 problem gamblers attempt suicide. It destroys lives, families, and finances.",
                "Sports betting addiction rose 300% among young men since apps became legal.",
                "The average sports bettor loses money every single year.",
            ],
            "f1_message": (
                "F1 is amazing. Betting on it is not. Enjoy the racing, watch Norris "
                "chase his second title, laugh at Ferrari strategy, cheer for Cadillac. "
                "But do not gamble your money away doing it."
            ),
            "help": {
                "phone": "1-800-GAMBLER",
                "website": "ncpgambling.org",
            },
        }

    # ------------------------------------------------------------
    # SECTION 3.5: SERIALIZATION
    # Convert session to/from dict for storage in DB, Flask session,
    # JSON file, etc.
    # ------------------------------------------------------------
    def to_dict(self):
        """Serialize session to dict."""
        return {
            "starting_tokens": self.starting_tokens,
            "tokens": self.tokens,
            "bet_count": self.bet_count,
            "wins": self.wins,
            "losses": self.losses,
            "total_wagered": self.total_wagered,
            "total_won": self.total_won,
            "history": self.history,
            "alert_shown": self.alert_shown,
        }

    @classmethod
    def from_dict(cls, data):
        """Restore session from a dict."""
        s = cls(starting_tokens=data.get("starting_tokens", 1000))
        s.tokens = data.get("tokens", s.starting_tokens)
        s.bet_count = data.get("bet_count", 0)
        s.wins = data.get("wins", 0)
        s.losses = data.get("losses", 0)
        s.total_wagered = data.get("total_wagered", 0)
        s.total_won = data.get("total_won", 0)
        s.history = data.get("history", [])
        s.alert_shown = data.get("alert_shown", False)
        return s

    # ------------------------------------------------------------
    # SECTION 3.6: ALERT TRIGGER LOGIC (PRIVATE)
    # Decides when to show the anti-gambling alert.
    # Triggers on: zero tokens, 70% loss, or 6+ bets placed.
    # ------------------------------------------------------------
    def _check_alert(self):
        """Returns (should_alert, reason) tuple."""
        if self.alert_shown:
            return (False, None)

        if self.tokens <= 0:
            self.alert_shown = True
            return (True, "broke")

        if self.tokens < self.starting_tokens * 0.3:
            self.alert_shown = True
            return (True, "big_loss")

        if self.bet_count >= 6:
            self.alert_shown = True
            return (True, "bet_limit")

        return (False, None)


# ============================================================
# SECTION 4: CONVENIENCE FUNCTIONS
# Helpers for the frontend to query game data without
# accessing the GAMES dict directly.
# ============================================================
def get_all_games():
    """Returns the full GAMES dict."""
    return GAMES


def get_game(game_id):
    """Returns a single game's data, or None if not found."""
    return GAMES.get(game_id)


def list_game_ids():
    """Returns a list of all game IDs."""
    return list(GAMES.keys())
