"""
PromptBrain — SQLite Memory nodes (Write/Read)
Stores tag/caption/score tuples to a local SQLite DB for later retrieval and prompt suggestion.
"""
from typing import Any, Dict, Tuple, List
import os, sqlite3, json, time

DB_PATH = os.path.join(os.path.dirname(__file__), "promptbrain.db")

def _ensure_schema(conn: sqlite3.Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS memory (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               ts REAL NOT NULL,
               tags_json TEXT,
               caption TEXT,
               score REAL,
               context TEXT
           )"""
    )
    conn.commit()

class PB_MemoryWrite:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "tags_dict": ("DICT", {}),
                "caption": ("STRING", {"default": ""}),
                "score": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "context": ("STRING", {"default": ""}),  # e.g., model, style, user
            },
            "optional": {},
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_MemoryWrite"

    def run(self, tags_dict, caption: str, score: float, context: str, unique_id=None):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        _ensure_schema(conn)
        conn.execute("INSERT INTO memory (ts, tags_json, caption, score, context) VALUES (?,?,?,?,?)",
                     (time.time(), json.dumps(tags_dict), caption, float(score), context))
        conn.commit()
        conn.close()
        return (f"ok:{unique_id}",)

class PB_MemoryRead:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "top_k": ("INT", {"default": 5, "min": 1, "max": 100, "step": 1}),
                "min_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "like_text": ("STRING", {"default": ""}), # substring match in caption/context
            },
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
    RETURN_TYPES = ("LIST","DICT")
    RETURN_NAMES = ("captions","raw_rows")
    FUNCTION = "run"
    CATEGORY = "XDev/PromptBrain"
    NODE_NAME = "PB_MemoryRead"

    def run(self, top_k: int, min_score: float, like_text: str = "", unique_id=None):
        if not os.path.exists(DB_PATH):
            return ([], {"rows": []})
        conn = sqlite3.connect(DB_PATH)
        _ensure_schema(conn)
        q = "SELECT id, ts, tags_json, caption, score, context FROM memory WHERE score >= ?"
        params = [float(min_score)]
        if like_text:
            q += " AND (caption LIKE ? OR context LIKE ?)"
            params += [f"%{like_text}%", f"%{like_text}%"]
        q += " ORDER BY score DESC, ts DESC LIMIT ?"
        params += [int(top_k)]
        rows = conn.execute(q, params).fetchall()
        conn.close()
        captions = [r[3] for r in rows]
        raw = {"rows":[{"id":r[0], "ts":r[1], "tags":r[2], "caption":r[3], "score":r[4], "context":r[5]} for r in rows]}
        return (captions, raw)
