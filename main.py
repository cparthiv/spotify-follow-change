#!/usr/bin/env python3
import json
import os
from pathlib import Path
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

verbose_logs = False
verbose_logs_webhook = ""
if verbose_logs:
    verbose_logs_webhook = os.getenv("VERBOSE_LOGS_WEBHOOK")

SCRIPT_DIR = Path(__file__).resolve().parent
TOKEN_CACHE = SCRIPT_DIR / ".token_cache.json"
STATE_FILE = SCRIPT_DIR / ".followers_state.json"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-read-private",
    cache_path=str(TOKEN_CACHE)))
r = requests.post(os.getenv("VERBOSE_LOGS_WEBHOOK"),
                  json={"content": "Authenticating..."})
r.raise_for_status()


def follower_total() -> int:
    return sp.current_user()["followers"]["total"]


def notify(delta: int, new_total: int) -> None:
    arrow = "▲" if delta > 0 else "▼"
    text = f"{arrow} {abs(delta)} follower{'s' if abs(delta) != 1 else ''} → {new_total}"
    r = requests.post(os.getenv("DISCORD_WEBHOOK_URL"), json={"content": text})
    r.raise_for_status()


now = follower_total()
prev = None
if STATE_FILE.exists():
    try:
        prev = json.loads(STATE_FILE.read_text()).get("count")
    except json.JSONDecodeError:
        # corrupted file; ignore and overwrite
        r = requests.post(os.getenv("VERBOSE_LOGS_WEBHOOK"),
                          json={"content": "corrupted file; ignore and overwrite"})
    r.raise_for_status()
    pass


print("Current spotify followers:", now)

if prev is not None and now != prev:
    print("Δ", now-prev)                            # prints only on change
    notify(now-prev, now)

if prev is not None:
    r = requests.post(os.getenv("VERBOSE_LOGS_WEBHOOK"), json={
        "content": f"Previous: {prev}, current: {now}"})
    r.raise_for_status()

# save snapshot for next run
STATE_FILE.write_text(json.dumps({"count": now}))
r = requests.post(os.getenv("VERBOSE_LOGS_WEBHOOK"), json={
                  "content": "save snapshot for next run"})
r.raise_for_status()
