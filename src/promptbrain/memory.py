"""
Brains-XDEV PromptBrain — SQLite Memory nodes (Write/Read)

Stores tag/caption/score tuples to a local SQLite DB for later retrieval and prompt suggestion.
This is the foundational storage layer for the PromptBrain system.

Migrated from BRAIN project with Brains-XDEV naming conventions.
"""
from typing import Any, Dict, Tuple, List
import os, sqlite3, json, time

print("[Brains-XDEV] memory nodes import")

# Database path in the promptbrain module directory
DB_PATH = os.path.join(os.path.dirname(__file__), "promptbrain.db")

def _ensure_schema(conn: sqlite3.Connection):
    """Ensure the memory table exists with proper schema."""
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

class BrainsXDEV_MemoryWrite:
    """
    Write memory entries to SQLite database for later retrieval.
    Stores tags (as JSON), caption, score, and context information.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "caption": ("STRING", {"default": ""}),
                "score": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "tags_dict": ("DICT", {}),
                "context": ("STRING", {"default": ""}),  # e.g., model, style, user
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_MemoryWrite"

    def run(self, caption: str, score: float, tags_dict=None, context="", 
            prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[str]:
        """Write a memory entry to the database."""
        try:
            # Default empty dict if not provided
            if tags_dict is None:
                tags_dict = {}
            
            # Ensure database directory exists
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            
            # Connect and ensure schema
            conn = sqlite3.connect(DB_PATH)
            _ensure_schema(conn)
            
            # Insert the memory entry
            conn.execute(
                "INSERT INTO memory (ts, tags_json, caption, score, context) VALUES (?,?,?,?,?)",
                (time.time(), json.dumps(tags_dict), caption, float(score), context)
            )
            conn.commit()
            conn.close()
            
            return (f"ok:memory_write:{unique_id}",)
            
        except Exception as e:
            return (f"error:memory_write:{str(e)}",)


class BrainsXDEV_MemoryRead:
    """
    Read memory entries from SQLite database with filtering and ranking.
    Returns captions and raw data for further processing.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "top_k": ("INT", {"default": 5, "min": 1, "max": 100, "step": 1}),
                "min_score": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
            "optional": {
                "like_text": ("STRING", {"default": ""}), # substring match in caption/context
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("LIST", "DICT")
    RETURN_NAMES = ("captions", "raw_rows")
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_MemoryRead"

    def run(self, top_k: int, min_score: float, like_text: str = "", 
            prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[List[str], Dict]:
        """Read memory entries from the database with filtering."""
        try:
            # Check if database exists
            if not os.path.exists(DB_PATH):
                return ([], {"rows": [], "status": "no_database"})
            
            # Connect and query
            conn = sqlite3.connect(DB_PATH)
            _ensure_schema(conn)
            
            # Build query with filters
            q = "SELECT id, ts, tags_json, caption, score, context FROM memory WHERE score >= ?"
            params = [float(min_score)]
            
            if like_text.strip():
                q += " AND (caption LIKE ? OR context LIKE ?)"
                params += [f"%{like_text}%", f"%{like_text}%"]
            
            q += " ORDER BY score DESC, ts DESC LIMIT ?"
            params += [int(top_k)]
            
            # Execute query
            rows = conn.execute(q, params).fetchall()
            conn.close()
            
            # Format results
            captions = [r[3] for r in rows if r[3]]  # Filter out empty captions
            raw = {
                "rows": [
                    {
                        "id": r[0], 
                        "ts": r[1], 
                        "tags": r[2], 
                        "caption": r[3], 
                        "score": r[4], 
                        "context": r[5]
                    } for r in rows
                ],
                "status": "success",
                "count": len(rows)
            }
            
            return (captions, raw)
            
        except Exception as e:
            return ([], {"rows": [], "status": f"error:{str(e)}"})