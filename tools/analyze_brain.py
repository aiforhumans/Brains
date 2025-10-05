#!/usr/bin/env python3
"""
PromptBrain Data Analyzer
Comprehensive analysis tool for PromptBrain learning data
"""

import json
import os
import time
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import re

class PromptBrainAnalyzer:
    def __init__(self, brain_path=None, images_path=None):
        self.brain_path = brain_path or self._find_brain_file()
        self.images_path = images_path or self._find_images_folder()
        self.brain_data = None
        self.analysis_results = {}
        
    def _find_brain_file(self):
        """Find the prompt_brain.json file"""
        possible_paths = [
            Path("c:/comfy/ComfyUI_windows_portable/ComfyUI/user/prompt_brain.json"),
            Path("../../../user/prompt_brain.json"),
            Path("prompt_brain.json")
        ]
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def _find_images_folder(self):
        """Find the prompt_brain_images folder"""
        possible_paths = [
            Path("c:/comfy/ComfyUI_windows_portable/ComfyUI/user/prompt_brain_images"),
            Path("../../../user/prompt_brain_images"),
            Path("prompt_brain_images")
        ]
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def load_brain_data(self):
        """Load and parse brain data"""
        if not self.brain_path or not self.brain_path.exists():
            print("âŒ Brain file not found!")
            return False
            
        try:
            with open(self.brain_path, 'r', encoding='utf-8') as f:
                self.brain_data = json.load(f)
            print(f"âœ… Loaded brain data from: {self.brain_path}")
            return True
        except Exception as e:
            print(f"âŒ Error loading brain data: {e}")
            return False
    
    def analyze_dataset_size(self):
        """Analyze the overall dataset size and composition"""
        if not self.brain_data:
            return
            
        tags = self.brain_data.get('tags', {})
        co_occurrence = self.brain_data.get('co', {})
        history = self.brain_data.get('history', [])
        styles = self.brain_data.get('styles', {})
        features = self.brain_data.get('features', {})
        tag_styles = self.brain_data.get('tag_styles', {})
        
        # Calculate file size
        file_size = 0
        if self.brain_path and self.brain_path.exists():
            file_size = self.brain_path.stat().st_size
        
        analysis = {
            'total_tags': len(tags),
            'co_occurrence_pairs': len(co_occurrence),
            'history_entries': len(history),
            'styles_defined': len(styles),
            'features_defined': len(features),
            'tag_style_mappings': len(tag_styles),
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'estimated_learning_sessions': len(history)
        }
        
        self.analysis_results['dataset_size'] = analysis
        return analysis
    
    def analyze_tag_patterns(self):
        """Analyze tag usage patterns and frequencies"""
        if not self.brain_data:
            return
            
        tags = self.brain_data.get('tags', {})
        
        # Categorize tags
        categories = {
            'character': [],
            'avoid': [],
            'style': [],
            'composition': [],
            'technical': [],
            'other': []
        }
        
        tag_frequencies = {}
        tag_scores = {}
        recent_tags = []
        
        current_time = time.time()
        
        for tag_name, tag_data in tags.items():
            count = tag_data.get('count', 0)
            score = tag_data.get('score', 0)
            last_used = tag_data.get('last', 0)
            
            tag_frequencies[tag_name] = count
            tag_scores[tag_name] = score
            
            # Check if used recently (within last 24 hours)
            if current_time - last_used < 86400:
                recent_tags.append(tag_name)
            
            # Categorize tags
            if tag_name.startswith('avoid:'):
                categories['avoid'].append(tag_name)
            elif any(keyword in tag_name.lower() for keyword in ['hair', 'eyes', 'skin', 'face', 'body', 'girl', 'woman']):
                categories['character'].append(tag_name)
            elif any(keyword in tag_name.lower() for keyword in ['shot', 'close-up', 'portrait', 'angle', 'view']):
                categories['composition'].append(tag_name)
            elif any(keyword in tag_name.lower() for keyword in ['realistic', 'photo', 'quality', 'details']):
                categories['technical'].append(tag_name)
            elif any(keyword in tag_name.lower() for keyword in ['elegant', 'soft', 'natural', 'style']):
                categories['style'].append(tag_name)
            else:
                categories['other'].append(tag_name)
        
        # Top tags by frequency and score
        top_frequent = sorted(tag_frequencies.items(), key=lambda x: x[1], reverse=True)[:20]
        top_scored = sorted(tag_scores.items(), key=lambda x: x[1], reverse=True)[:20]
        
        analysis = {
            'tag_categories': {cat: len(tags) for cat, tags in categories.items()},
            'top_frequent_tags': top_frequent,
            'top_scored_tags': top_scored,
            'recent_tags_count': len(recent_tags),
            'recent_tags': recent_tags[:10],  # Show first 10
            'avoid_tags_count': len(categories['avoid']),
            'character_tags_count': len(categories['character'])
        }
        
        self.analysis_results['tag_patterns'] = analysis
        return analysis
    
    def analyze_co_occurrence(self):
        """Analyze tag co-occurrence patterns"""
        if not self.brain_data:
            return
            
        co_data = self.brain_data.get('co', {})
        
        # Parse co-occurrence data
        tag_relationships = defaultdict(list)
        strongest_pairs = []
        
        for pair, count in co_data.items():
            if '|' in pair:
                tag1, tag2 = pair.split('|', 1)
                tag_relationships[tag1].append((tag2, count))
                tag_relationships[tag2].append((tag1, count))
                strongest_pairs.append((pair, count))
        
        # Sort by strength
        strongest_pairs.sort(key=lambda x: x[1], reverse=True)
        
        # Find tags with most relationships
        relationship_counts = {tag: len(relationships) for tag, relationships in tag_relationships.items()}
        most_connected = sorted(relationship_counts.items(), key=lambda x: x[1], reverse=True)[:15]
        
        analysis = {
            'total_relationships': len(co_data),
            'strongest_pairs': strongest_pairs[:20],
            'most_connected_tags': most_connected,
            'average_connections_per_tag': round(len(co_data) / len(relationship_counts), 2) if relationship_counts else 0
        }
        
        self.analysis_results['co_occurrence'] = analysis
        return analysis
    
    def analyze_learning_progression(self):
        """Analyze learning progression from history and timestamps"""
        if not self.brain_data:
            return
            
        tags = self.brain_data.get('tags', {})
        
        # Extract timestamps
        timestamps = []
        for tag_data in tags.values():
            last_time = tag_data.get('last', 0)
            if last_time > 0:
                timestamps.append(last_time)
        
        if not timestamps:
            return {'error': 'No timestamp data available'}
        
        timestamps.sort()
        
        # Calculate learning period
        first_use = min(timestamps)
        last_use = max(timestamps)
        learning_span_days = (last_use - first_use) / 86400
        
        # Activity analysis
        current_time = time.time()
        recent_activity = sum(1 for t in timestamps if current_time - t < 86400)  # Last 24h
        week_activity = sum(1 for t in timestamps if current_time - t < 604800)   # Last week
        
        analysis = {
            'learning_span_days': round(learning_span_days, 2),
            'total_learning_events': len(timestamps),
            'first_learning_date': datetime.fromtimestamp(first_use).strftime('%Y-%m-%d %H:%M:%S'),
            'last_learning_date': datetime.fromtimestamp(last_use).strftime('%Y-%m-%d %H:%M:%S'),
            'recent_activity_24h': recent_activity,
            'recent_activity_week': week_activity,
            'average_daily_learning': round(len(timestamps) / max(learning_span_days, 1), 2)
        }
        
        self.analysis_results['learning_progression'] = analysis
        return analysis
    
    def analyze_generated_images(self):
        """Analyze generated images and their scores"""
        if not self.images_path or not self.images_path.exists():
            return {'error': 'Images folder not found'}
        
        image_files = list(self.images_path.glob("brain_*.png"))
        json_files = list(self.images_path.glob("brain_*.json"))
        
        scores = []
        image_data = []
        
        for img_file in image_files:
            # Extract score from filename
            score_match = re.search(r'score([0-9]+\.?[0-9]*)', img_file.name)
            if score_match:
                score_str = score_match.group(1)
                try:
                    score = float(score_str)
                    scores.append(score)
                    
                    # Get file timestamp
                    timestamp = img_file.stat().st_mtime
                    
                    image_data.append({
                        'filename': img_file.name,
                        'score': score,
                        'timestamp': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                        'size_mb': round(img_file.stat().st_size / (1024 * 1024), 2)
                    })
                except ValueError:
                    continue  # Skip files with invalid scores
        
        # Sort by timestamp (most recent first)
        image_data.sort(key=lambda x: x['timestamp'], reverse=True)
        
        analysis = {
            'total_images': len(image_files),
            'total_metadata_files': len(json_files),
            'score_range': (min(scores), max(scores)) if scores else (0, 0),
            'average_score': round(sum(scores) / len(scores), 2) if scores else 0,
            'recent_images': image_data[:10],
            'total_storage_mb': round(sum(img.stat().st_size for img in image_files) / (1024 * 1024), 2)
        }
        
        self.analysis_results['generated_images'] = analysis
        return analysis
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "="*80)
        print("ðŸ§  PROMPTBRAIN COMPREHENSIVE ANALYSIS REPORT")
        print("="*80)
        
        if not self.load_brain_data():
            return
        
        # Run all analyses
        print("\nðŸ“Š Analyzing dataset size...")
        size_analysis = self.analyze_dataset_size()
        
        print("ðŸ·ï¸  Analyzing tag patterns...")
        tag_analysis = self.analyze_tag_patterns()
        
        print("ðŸ”— Analyzing co-occurrence patterns...")
        co_analysis = self.analyze_co_occurrence()
        
        print("ðŸ“ˆ Analyzing learning progression...")
        learning_analysis = self.analyze_learning_progression()
        
        print("ðŸ–¼ï¸  Analyzing generated images...")
        image_analysis = self.analyze_generated_images()
        
        # Print comprehensive report
        self._print_detailed_report()
    
    def _print_detailed_report(self):
        """Print detailed analysis report"""
        print("\n" + "="*80)
        print("ðŸ“‹ DETAILED ANALYSIS RESULTS")
        print("="*80)
        
        # Dataset Overview
        if 'dataset_size' in self.analysis_results:
            data = self.analysis_results['dataset_size']
            print(f"\nðŸ“Š DATASET SIZE & COMPOSITION")
            print(f"   Total Tags: {data['total_tags']:,}")
            print(f"   Co-occurrence Pairs: {data['co_occurrence_pairs']:,}")
            print(f"   File Size: {data['file_size_mb']} MB")
            print(f"   Styles Defined: {data['styles_defined']}")
            print(f"   Features Defined: {data['features_defined']}")
        
        # Tag Patterns
        if 'tag_patterns' in self.analysis_results:
            data = self.analysis_results['tag_patterns']
            print(f"\nðŸ·ï¸  TAG USAGE PATTERNS")
            print(f"   Character Tags: {data['character_tags_count']}")
            print(f"   Avoid Tags: {data['avoid_tags_count']}")
            print(f"   Recent Activity (24h): {data['recent_tags_count']} tags")
            
            print(f"\n   ðŸ“ˆ TOP FREQUENT TAGS:")
            for i, (tag, count) in enumerate(data['top_frequent_tags'][:10], 1):
                print(f"      {i:2d}. {tag[:30]:<30} ({count:,} uses)")
        
        # Co-occurrence Analysis
        if 'co_occurrence' in self.analysis_results:
            data = self.analysis_results['co_occurrence']
            print(f"\nðŸ”— CO-OCCURRENCE ANALYSIS")
            print(f"   Total Relationships: {data['total_relationships']:,}")
            print(f"   Avg Connections/Tag: {data['average_connections_per_tag']}")
            
            print(f"\n   ðŸ’ª STRONGEST TAG PAIRS:")
            for i, (pair, count) in enumerate(data['strongest_pairs'][:8], 1):
                tag1, tag2 = pair.split('|', 1)
                print(f"      {i}. {tag1[:20]} + {tag2[:20]} ({count} times)")
        
        # Learning Progression
        if 'learning_progression' in self.analysis_results:
            data = self.analysis_results['learning_progression']
            if 'error' not in data:
                print(f"\nðŸ“ˆ LEARNING PROGRESSION")
                print(f"   Learning Span: {data['learning_span_days']:.1f} days")
                print(f"   Total Learning Events: {data['total_learning_events']:,}")
                print(f"   Average Daily Learning: {data['average_daily_learning']:.1f} events/day")
                print(f"   Recent Activity (24h): {data['recent_activity_24h']} events")
                print(f"   First Learning: {data['first_learning_date']}")
                print(f"   Last Learning: {data['last_learning_date']}")
        
        # Generated Images
        if 'generated_images' in self.analysis_results:
            data = self.analysis_results['generated_images']
            if 'error' not in data:
                print(f"\nðŸ–¼ï¸  GENERATED IMAGES ANALYSIS")
                print(f"   Total Images: {data['total_images']}")
                print(f"   Score Range: {data['score_range'][0]:.1f} - {data['score_range'][1]:.1f}")
                print(f"   Average Score: {data['average_score']:.2f}")
                print(f"   Storage Used: {data['total_storage_mb']:.1f} MB")
                
                if data['recent_images']:
                    print(f"\n   ðŸŽ¨ RECENT GENERATIONS:")
                    for img in data['recent_images'][:5]:
                        print(f"      â€¢ {img['filename']} (Score: {img['score']:.1f}) - {img['timestamp']}")
        
        # Performance Assessment
        self._print_performance_assessment()
        
        # Recommendations
        self._print_recommendations()
    
    def _print_performance_assessment(self):
        """Print performance assessment"""
        print(f"\nâš¡ PERFORMANCE ASSESSMENT")
        
        if 'dataset_size' in self.analysis_results:
            data = self.analysis_results['dataset_size']
            total_tags = data['total_tags']
            file_size = data['file_size_mb']
            
            if total_tags > 1000:
                print(f"   ðŸ”´ Large Dataset: {total_tags:,} tags (Performance optimizations ACTIVE)")
            elif total_tags > 500:
                print(f"   ðŸŸ¡ Medium Dataset: {total_tags:,} tags (Some optimizations active)")
            else:
                print(f"   ðŸŸ¢ Manageable Dataset: {total_tags:,} tags (Standard performance)")
            
            if file_size > 10:
                print(f"   âš ï¸  Large File Size: {file_size:.1f} MB")
            else:
                print(f"   âœ… Reasonable File Size: {file_size:.1f} MB")
    
    def _print_recommendations(self):
        """Print optimization recommendations"""
        print(f"\nðŸ’¡ OPTIMIZATION RECOMMENDATIONS")
        
        if 'dataset_size' in self.analysis_results:
            data = self.analysis_results['dataset_size']
            total_tags = data['total_tags']
            
            if total_tags > 1000:
                print(f"   â€¢ Use PromptBrainPerformance node to monitor performance")
                print(f"   â€¢ Consider periodic cleanup of low-value tags")
                print(f"   â€¢ Performance optimizations are automatically active")
            
            if total_tags > 500:
                print(f"   â€¢ Score caching is active for better performance")
                print(f"   â€¢ Compressed saves are enabled")
        
        if 'tag_patterns' in self.analysis_results:
            data = self.analysis_results['tag_patterns']
            avoid_count = data['avoid_tags_count']
            
            if avoid_count > 50:
                print(f"   â€¢ High number of avoid tags ({avoid_count}) - consider consolidation")
        
        if 'generated_images' in self.analysis_results:
            data = self.analysis_results['generated_images']
            if 'error' not in data and data['total_storage_mb'] > 100:
                print(f"   â€¢ Image storage is {data['total_storage_mb']:.1f} MB - consider cleanup")
        
        print(f"   â€¢ Restart ComfyUI to ensure optimizations are active")
        print(f"   â€¢ Use style steering features for better prompt control")

def main():
    """Main function"""
    analyzer = PromptBrainAnalyzer()
    analyzer.generate_report()

if __name__ == "__main__":
    main()
