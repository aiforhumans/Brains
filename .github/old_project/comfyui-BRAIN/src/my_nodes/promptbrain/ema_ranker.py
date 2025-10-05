"""
PromptBrain — EMA Tag Ranker
Maintains exponential moving averages per tag based on incoming scores and feedback.

Stores state in a local SQLite DB next to the node.
"""
from typing import Any, Dict, Tuple, List
import os, sqlite3, time, json, math

DB_PATH = os.path.join(os.path.dirname(__file__), "promptbrain_ema.db")

def _ensure_schema(conn: sqlite3.Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS ema (
               tag TEXT PRIMARY KEY,
               ema REAL NOT NULL,
               count INTEGER NOT NULL,
               updated REAL NOT NULL
           )"""
    )
    conn.commit()

class PB_EMARanker:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tags_dict": ("DICT", {}),      # {"tags": {tag: score}}
                "alpha": ("FLOAT", {"default": 0.2, "min": 0.01, "max": 1.0, "step": 0.01}),
                "top_k": ("INT", {"default": 16, "min": 1, "max": 256, "step": 1}),
            },
            "optional": {
                "feedback": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),  # multiply influence
            },
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
    RETURN_TYPES = ("LIST","DICT")
    RETURN_NAMES = ("ranked_tags","stats")
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_EMARanker"

    def run(self, tags_dict, alpha: float, top_k: int, feedback: float = 1.0, unique_id=None):
        tags = tags_dict.get("tags", {}) if isinstance(tags_dict, dict) else {}
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        _ensure_schema(conn)

        now = time.time()
        for tag, score in tags.items():
            row = conn.execute("SELECT ema, count FROM ema WHERE tag=?", (tag,)).fetchone()
            s = float(score) * float(feedback)
            if row is None:
                ema = s
                cnt = 1
                conn.execute("INSERT INTO ema (tag, ema, count, updated) VALUES (?,?,?,?)", (tag, ema, cnt, now))
            else:
                ema_prev, cnt = row
                ema = (1.0 - alpha) * ema_prev + alpha * s
                cnt = cnt + 1
                conn.execute("UPDATE ema SET ema=?, count=?, updated=? WHERE tag=?", (ema, cnt, now, tag))

        conn.commit()

        # Read back and produce ranking
        rows = conn.execute("SELECT tag, ema, count FROM ema ORDER BY ema DESC LIMIT ?", (int(top_k),)).fetchall()
        conn.close()
        ranked = [r[0] for r in rows]
        stats = {"rows": [{"tag": r[0], "ema": r[1], "count": r[2]} for r in rows]}
        return (ranked, stats)
