"""
Brains-XDEV PromptBrain — EMA Tag Ranker

Maintains exponential moving averages per tag based on incoming scores and feedback.
Provides intelligent tag ranking based on historical performance.

Stores state in a local SQLite DB next to the node.
Migrated from BRAIN project with Brains-XDEV naming conventions.
"""
from typing import Any, Dict, Tuple, List
import os, sqlite3, time, json, math

print("[Brains-XDEV] ema_ranker import")

# Database path in the promptbrain module directory
DB_PATH = os.path.join(os.path.dirname(__file__), "promptbrain_ema.db")

def _ensure_schema(conn: sqlite3.Connection):
    """Ensure the EMA table exists with proper schema."""
    conn.execute(
        """CREATE TABLE IF NOT EXISTS ema (
               tag TEXT PRIMARY KEY,
               ema REAL NOT NULL,
               count INTEGER NOT NULL,
               updated REAL NOT NULL
           )"""
    )
    conn.commit()

class BrainsXDEV_EMARanker:
    """
    Exponential Moving Average tag ranker for intelligent prompt optimization.
    Learns from feedback to rank tags by their effectiveness over time.
    """
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Dict[str, Any]]:
        return {
            "required": {
                "tags_dict": ("DICT", {}),      # {"tags": {tag: score}}
                "alpha": ("FLOAT", {"default": 0.2, "min": 0.01, "max": 1.0, "step": 0.01}),
                "top_k": ("INT", {"default": 16, "min": 1, "max": 256, "step": 1}),
            },
            "optional": {
                "feedback": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01}),  # multiply influence
                "decay_days": ("INT", {"default": 30, "min": 1, "max": 365, "step": 1}),  # optional decay
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID"
            }
        }
    
    RETURN_TYPES = ("LIST", "DICT")
    RETURN_NAMES = ("ranked_tags", "stats")
    FUNCTION = "run"
    CATEGORY = "Brains-XDEV/PromptBrain"
    NODE_NAME = "BrainsXDEV_EMARanker"

    def run(self, tags_dict, alpha: float, top_k: int, feedback: float = 1.0, 
            decay_days: int = 30, prompt=None, extra_pnginfo=None, unique_id=None) -> Tuple[List[str], Dict]:
        """
        Update EMA scores for tags and return ranked results.
        """
        try:
            # Extract tags from input dict
            tags = tags_dict.get("tags", {}) if isinstance(tags_dict, dict) else {}
            
            if not tags:
                return ([], {"error": "no_tags", "stats": []})
            
            # Ensure database directory exists
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            
            # Connect to database
            conn = sqlite3.connect(DB_PATH)
            _ensure_schema(conn)

            now = time.time()
            decay_cutoff = now - (decay_days * 24 * 3600)  # Decay old entries
            
            # Update EMA for each tag
            updated_count = 0
            for tag, score in tags.items():
                if not isinstance(score, (int, float)):
                    continue
                    
                # Get existing EMA data
                row = conn.execute("SELECT ema, count, updated FROM ema WHERE tag=?", (tag,)).fetchone()
                
                # Apply feedback multiplier
                adjusted_score = float(score) * float(feedback)
                
                if row is None:
                    # New tag
                    ema = adjusted_score
                    cnt = 1
                    conn.execute(
                        "INSERT INTO ema (tag, ema, count, updated) VALUES (?,?,?,?)", 
                        (tag, ema, cnt, now)
                    )
                else:
                    # Update existing tag
                    ema_prev, cnt, last_updated = row
                    
                    # Apply time decay if entry is old
                    if last_updated < decay_cutoff:
                        ema_prev *= 0.9  # Decay factor for old entries
                    
                    # Update EMA
                    ema = (1.0 - alpha) * ema_prev + alpha * adjusted_score
                    cnt = cnt + 1
                    
                    conn.execute(
                        "UPDATE ema SET ema=?, count=?, updated=? WHERE tag=?", 
                        (ema, cnt, now, tag)
                    )
                
                updated_count += 1

            conn.commit()

            # Read back ranked results
            rows = conn.execute(
                "SELECT tag, ema, count, updated FROM ema ORDER BY ema DESC LIMIT ?", 
                (int(top_k),)
            ).fetchall()
            
            conn.close()
            
            # Format results
            ranked_tags = [r[0] for r in rows]
            stats = {
                "rows": [
                    {
                        "tag": r[0], 
                        "ema": round(r[1], 4), 
                        "count": r[2],
                        "last_updated": r[3]
                    } for r in rows
                ],
                "updated_count": updated_count,
                "total_tags": len(tags),
                "alpha": alpha,
                "feedback": feedback,
                "uid": unique_id
            }
            
            return (ranked_tags, stats)
            
        except Exception as e:
            error_msg = f"EMA ranker error: {str(e)}"
            print(f"[Brains-XDEV] {error_msg}")
            return ([], {"error": error_msg, "stats": []})