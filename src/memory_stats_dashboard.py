"""
Memory Stats Dashboard — See what your Smart Memory has learned

A beginner-friendly wrapper for BrainsXDEV_PromptBrainPerformanceDirect that shows
learning progress in an easy-to-read format.

How it works:
1. Connect your Smart Memory
2. Get a beautiful dashboard showing:
   - How many prompts you've rated
   - What art styles you prefer
   - Learning progress over time
   - Quality score trends

Example workflow:
- Smart Memory Loader → Memory Stats Dashboard → stats report
- Check progress after rating batches of prompts
- See which styles you rate highest
"""
from typing import Tuple

# Import the advanced node we're wrapping
try:
    from .brain_datatype import BrainsXDEV_PromptBrainPerformanceDirect, BrainData
except ImportError:
    print("[Brains-XDEV] Warning: brain_datatype not found for Memory Stats Dashboard")
    BrainsXDEV_PromptBrainPerformanceDirect = None
    BrainData = None


class BrainsXDEV_MemoryStatsDashboard:
    """
    Beginner-friendly learning progress dashboard
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "smart_memory": ("BRAIN", {
                    "tooltip": "The Smart Memory to analyze (from Smart Memory Loader)"
                }),
            },
            "optional": {
                "show_details": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Show detailed statistics vs. just a summary"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("stats_report",)
    FUNCTION = "show_stats"
    CATEGORY = "Brains-XDEV/Beginner"
    NODE_NAME = "BrainsXDEV_MemoryStatsDashboard"
    DESCRIPTION = "View your Smart Memory learning progress and statistics"
    
    def show_stats(self, smart_memory, show_details: bool = True) -> Tuple:
        """
        Display Smart Memory statistics dashboard
        
        Args:
            smart_memory: BRAIN data from Smart Memory Loader
            show_details: Show detailed stats or just summary
            
        Returns:
            (stats_report,) tuple
        """
        
        # Check if advanced node is available
        if BrainsXDEV_PromptBrainPerformanceDirect is None:
            error_msg = "❌ Memory Stats Dashboard unavailable. Check brain_datatype.py installation."
            return (error_msg,)
        
        # Validate inputs
        if smart_memory is None:
            error_msg = "❌ No Smart Memory provided. Connect a Smart Memory Loader."
            return (error_msg,)
        
        try:
            # Use the advanced PromptBrainPerformanceDirect node
            performance_node = BrainsXDEV_PromptBrainPerformanceDirect()
            
            # Get performance analysis
            result = performance_node.analyze_direct(
                brain_data=smart_memory,
                show_detailed_stats=show_details
            )
            
            # Unpack result (brain_data, performance_report)
            _, raw_report = result
            
            # Get raw stats for additional beginner-friendly formatting
            stats = smart_memory.get_performance_stats()
            
            # Create beginner-friendly dashboard
            dashboard = f"""📊 SMART MEMORY DASHBOARD
{'=' * 60}

🎓 LEARNING PROGRESS

Total Prompts Rated: {stats['total_history']:,}
Unique Tags Learned: {stats['total_tags']:,}
Tag Relationships: {stats['total_cooccurrence']:,}

Average Rating: {stats['average_score']:.2f}/1.0 ({stats['average_score'] * 10:.1f}/10)

"""
            
            # Add learning progress bar
            if stats['total_history'] > 0:
                learning_level = min(stats['total_history'] // 10, 10)
                progress_bar = "🟩" * learning_level + "⬜" * (10 - learning_level)
                dashboard += f"Learning Level: {progress_bar} {learning_level}/10\n\n"
            
            # Add learning milestones
            dashboard += "🏆 MILESTONES:\n"
            milestones = [
                (10, "Beginner", "Started learning!"),
                (50, "Apprentice", "Building knowledge base"),
                (100, "Skilled", "Solid understanding"),
                (250, "Expert", "Deep pattern recognition"),
                (500, "Master", "Comprehensive knowledge"),
            ]
            
            for threshold, title, desc in milestones:
                if stats['total_history'] >= threshold:
                    dashboard += f"✅ {title}: {desc}\n"
                else:
                    dashboard += f"⬜ {title}: Reach {threshold} ratings ({stats['total_history']}/{threshold})\n"
            
            dashboard += "\n"
            
            # Add quality insights
            dashboard += "💡 INSIGHTS:\n\n"
            
            if stats['total_history'] == 0:
                dashboard += "• You haven't rated any prompts yet!\n"
                dashboard += "• Connect a Memory Teacher node to start learning.\n"
            elif stats['total_history'] < 10:
                dashboard += f"• Great start! You've rated {stats['total_history']} prompts.\n"
                dashboard += "• Rate at least 10 prompts for basic pattern recognition.\n"
            elif stats['total_history'] < 50:
                dashboard += f"• Building knowledge! {stats['total_history']} prompts rated.\n"
                dashboard += "• Your Smart Memory is learning your preferences.\n"
            elif stats['total_history'] < 100:
                dashboard += f"• Solid progress! {stats['total_history']} prompts in memory.\n"
                dashboard += "• Suggestions should be getting more accurate.\n"
            else:
                dashboard += f"• Excellent! {stats['total_history']} prompts learned.\n"
                dashboard += "• Your Smart Memory has deep pattern recognition.\n"
            
            dashboard += "\n"
            
            # Add average rating insights
            if stats['average_score'] < 0.3:
                dashboard += "• Average rating is low - try rating some better prompts!\n"
            elif stats['average_score'] < 0.5:
                dashboard += "• Average rating is moderate - good balanced dataset.\n"
            elif stats['average_score'] < 0.7:
                dashboard += "• Average rating is good - you have high standards!\n"
            else:
                dashboard += "• Average rating is excellent - strong quality focus!\n"
            
            dashboard += "\n"
            
            # Add recommendations
            dashboard += "📋 RECOMMENDATIONS:\n\n"
            
            if stats['total_history'] < 20:
                dashboard += "1. Rate more prompts to improve suggestions (target: 20+)\n"
            if stats['total_tags'] < 50:
                dashboard += "1. Try diverse prompts to learn more tag varieties\n"
            if stats['average_score'] > 0.8:
                dashboard += "1. Consider rating some lower-quality prompts for balance\n"
            if stats['total_history'] >= 100:
                dashboard += "1. Your memory is well-trained! Keep refining with new styles.\n"
            
            dashboard += "\n"
            
            # Add raw technical report if detailed
            if show_details:
                dashboard += "=" * 60 + "\n"
                dashboard += "🔧 TECHNICAL DETAILS\n\n"
                dashboard += raw_report
            
            print(f"[Brains-XDEV] 📊 Memory Stats: {stats['total_history']} ratings, {stats['total_tags']} tags")
            
            return (dashboard,)
            
        except Exception as e:
            error_msg = f"❌ Error getting stats: {str(e)}"
            print(f"[Brains-XDEV] {error_msg}")
            import traceback
            traceback.print_exc()
            return (error_msg,)


# Export for registration
NODE_CLASS_MAPPINGS = {
    "BrainsXDEV_MemoryStatsDashboard": BrainsXDEV_MemoryStatsDashboard,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BrainsXDEV_MemoryStatsDashboard": "Brains-XDEV • Memory Stats Dashboard (beginner)",
}
