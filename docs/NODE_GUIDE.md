# 🧠 Brains Node Guide

Complete reference for all BRAIN system nodes in ComfyUI.

## 📚 Table of Contents

- [Beginner-Friendly Nodes](#-beginner-friendly-nodes)
- [Advanced BRAIN Datatype Nodes](#-advanced-brain-datatype-nodes)
- [Node Categories](#-node-categories)
- [Common Workflows](#-common-workflows)

---

## 🌟 Beginner-Friendly Nodes

These nodes provide an intuitive interface for getting started with the BRAIN learning system.

### 🧠 Smart Memory Loader

**Purpose**: To load or create your AI's memory. It's the starting point of the learning workflow.

**Features**: 
- Automatically discovers existing brain files in your ComfyUI installation
- Creates fresh memory databases
- Makes backups of existing memory before loading to prevent data loss
- Simple file browser interface

**Inputs**:
- `database_path` (STRING) - Path to brain database file
- `auto_discover` (BOOLEAN) - Automatically find existing databases
- `create_backup` (BOOLEAN) - Backup before loading

**Output**: 
- `smart_memory` (BRAIN) - A BRAIN object ready to be used by other nodes

**Usage Example**:
```
1. Add "Smart Memory Loader" node
2. Leave path empty for auto-discovery
3. Enable "create_backup" for safety
4. Connect output to other BRAIN nodes
```

---

### ✨ Smart Prompt Helper

**Purpose**: To transform a simple, basic prompt idea into multiple detailed, high-quality prompts.

**Features**: 
- Uses knowledge stored in smart_memory to suggest relevant keywords
- Control creativity_level (0.0-1.0) to guide suggestions
- Set preferred_style to match your artistic direction
- Provides explanation of why it made its suggestions
- Generates 3 diverse prompt variations

**Inputs**:
- `smart_memory` (BRAIN) - Trained memory object
- `basic_prompt` (STRING) - Your simple prompt idea
- `creativity_level` (FLOAT) - 0.0-1.0, controls variation (default: 0.7)
- `preferred_style` (STRING) - Art style preference (optional)

**Outputs**: 
- `improved_prompt_1` (STRING) - First enhanced prompt
- `improved_prompt_2` (STRING) - Second enhanced prompt  
- `improved_prompt_3` (STRING) - Third enhanced prompt
- `explanation` (STRING) - Why these suggestions were made

**Usage Example**:
```
Input: "a cat"
creativity_level: 0.7
preferred_style: "photorealistic"

Output 1: "a photorealistic cat with detailed fur, professional lighting, 8k resolution"
Output 2: "close-up portrait of a majestic cat, studio photography, sharp focus"
Output 3: "hyper-realistic cat portrait, natural lighting, award-winning photograph"
```

---

### 🎓 Memory Teacher

**Purpose**: To teach the AI which prompts produce good or bad results. This is how the memory learns and improves.

**Features**: 
- Simple 1-5 star rating system (no confusing decimals!)
- Analyzes the prompt structure and keywords
- Associates ratings with optional art styles
- Updates smart_memory with new knowledge
- Provides learning report showing what was learned

**Inputs**:
- `smart_memory` (BRAIN) - Memory to teach
- `prompt_to_rate` (STRING) - The prompt that was used
- `quality_rating` (INT) - 1-5 star rating
  - ⭐ (1) - Poor quality
  - ⭐⭐ (2) - Below average
  - ⭐⭐⭐ (3) - Average
  - ⭐⭐⭐⭐ (4) - Good quality
  - ⭐⭐⭐⭐⭐ (5) - Excellent quality
- `art_style` (STRING) - Optional style category

**Outputs**: 
- `updated_memory` (BRAIN) - Memory with new learning
- `learning_report` (STRING) - Summary of what was learned

**Usage Example**:
```
Scenario: You generated an image and loved it!

prompt_to_rate: "cyberpunk city at night, neon lights, rain"
quality_rating: 5 (⭐⭐⭐⭐⭐)
art_style: "cyberpunk"

learning_report: "✅ Learned high-quality association:
- Keywords: cyberpunk, city, night, neon, lights, rain
- Style: cyberpunk
- Rating: 5.0 (Excellent)
- These keywords will be prioritized in future suggestions"
```

---

### 🤖 Auto Quality Rater

**Purpose**: To automatically score the quality of a generated image, saving you from manual rating.

**Features**: 
- Acts as an "AI art critic"
- Analyzes technical qualities (sharpness, exposure, composition)
- Analyzes artistic qualities (style, creativity, aesthetics)
- Produces automatic 1-10 score
- Can be connected to Memory Teacher for automated learning
- Provides detailed rating report explaining the score

**Inputs**:
- `generated_image` (IMAGE) - The image to analyze
- `image_description` (STRING) - Prompt or description (optional)
- `rating_mode` (LIST) - ["balanced", "technical_focus", "artistic_focus"]

**Outputs**: 
- `quality_score` (FLOAT) - 0.0-10.0 score
- `rating_report` (STRING) - Detailed breakdown of score

**Usage Example**:
```
rating_report: "
🤖 Auto Quality Rating: 8.5/10

Technical Analysis:
✅ Sharpness: 9/10 - Excellent detail
✅ Exposure: 8/10 - Well balanced
✅ Composition: 9/10 - Rule of thirds applied

Artistic Analysis:
✅ Style Consistency: 8/10 - Strong style
✅ Color Harmony: 9/10 - Complementary colors
✅ Creativity: 8/10 - Unique approach

Overall: High quality generation!"
```

---

### 📊 Memory Stats Dashboard

**Purpose**: To provide an easy-to-understand report on the AI's learning progress.

**Features**: 
- Acts like a "report card" for your AI's training
- Shows visual progress bars
- Displays learning trends over time
- Provides smart recommendations on how to improve training
- Shows most successful keywords and styles

**Inputs**:
- `smart_memory` (BRAIN) - Memory to analyze

**Outputs**: 
- `stats_report` (STRING) - Comprehensive statistics dashboard

**Usage Example**:
```
stats_report: "
📊 BRAIN Memory Statistics Dashboard

Training Progress:
━━━━━━━━━━━━━━━━━━━━ 75% Complete

Learning Summary:
📝 Total Prompts Learned: 342
⭐ Average Quality: 4.2/5.0
🎨 Styles Trained: 8 different styles
📈 Learning Trend: ↗️ Improving

Top Performing Keywords:
1. "detailed" - Avg: 4.8/5.0 (used 45 times)
2. "professional" - Avg: 4.6/5.0 (used 38 times)
3. "8k resolution" - Avg: 4.5/5.0 (used 52 times)

Best Style Category:
🏆 "photorealistic" - Avg: 4.7/5.0

💡 Recommendations:
✅ Continue training with "photorealistic" style
⚠️ Need more training in "abstract" style (only 3 examples)
✅ Your keyword vocabulary is growing well!"
```

---

## 🚀 Advanced BRAIN Datatype Nodes

These are the high-performance, technical nodes that form the core of the BRAIN system. They offer more detailed control and are designed for complex, automated workflows.

### BrainsXDEV_PromptBrainSource (BRAIN)

**Purpose**: The technical equivalent of the SmartMemoryLoader. It creates a BrainData object either from scratch or by loading a file.

**Features**: 
- Robust auto-discovery system scans ComfyUI installation
- Automatic backup system with timestamp
- Can convert older exported brain formats into current standard
- Thread-safe SQLite operations
- Validation and integrity checking

**Inputs**:
- `database_path` (STRING) - Absolute or relative path
  - Default: `"promptbrain.db"`
  - Can use auto-discovery: `"auto"`
- `create_if_missing` (BOOLEAN) - Create new if doesn't exist (default: True)
- `backup_on_load` (BOOLEAN) - Backup before loading (default: True)
- `validate_schema` (BOOLEAN) - Check database integrity (default: True)

**Output**: 
- `brain_data` (BRAIN) - BrainData object ready for use

**Technical Details**:
```python
# Database Schema:
# - learning_events: prompt, score, style, timestamp
# - keywords: word, frequency, avg_score
# - styles: name, count, avg_score
# - performance: metrics, trends
```

---

### BrainsXDEV_PromptBrainLearnDirect (BRAIN)

**Purpose**: The core learning engine. It takes a BrainData object, a prompt, and a score, and updates the object directly in memory.

**Features**:
- Direct in-memory learning (fast)
- Advanced keyword extraction with NLP
- Style category association
- Feature emphasis system
- Configurable learning rate
- Automatic score normalization

**Inputs**:
- `brain_data` (BRAIN) - BrainData object to update
- `prompt` (STRING) - Prompt to learn from
- `score` (FLOAT) - Quality score (0.0-10.0)
- `style_category` (STRING) - Optional style tag (default: "general")
- `feature_emphasis` (FLOAT) - Weight importance (0.0-2.0, default: 1.0)
- `learning_rate` (FLOAT) - How quickly to learn (0.1-2.0, default: 1.0)

**Outputs**: 
- `brain_data` (BRAIN) - Updated BrainData object
- `learning_status` (STRING) - Confirmation message

**Learning Rate Guide**:
- `0.1-0.5` - Conservative learning (slow adaptation)
- `0.5-1.0` - Normal learning (balanced)
- `1.0-2.0` - Aggressive learning (fast adaptation, may overfit)

**Usage Example**:
```python
# Learning from high-quality result:
prompt: "masterpiece, detailed landscape, golden hour lighting"
score: 9.5
style_category: "landscape"
learning_rate: 1.0

# Result: Keywords "masterpiece", "detailed", "golden hour" 
# are strongly associated with high quality in "landscape" style
```

---

### BrainsXDEV_PromptBrainSuggestDirect (BRAIN)

**Purpose**: Generates prompt suggestions by reading from an incoming BrainData object in memory.

**Features**:
- Real-time suggestion generation
- Uses learned keyword associations
- Respects style preferences
- Quality threshold filtering
- Creativity control (conservative to wild)
- Passes through brain_data for chaining

**Inputs**:
- `brain_data` (BRAIN) - Trained BrainData object
- `base_prompt` (STRING) - Starting prompt idea
- `suggestion_count` (INT) - Number of suggestions (1-3, default: 3)
- `creativity` (FLOAT) - Variation level (0.0-1.0, default: 0.7)
  - `0.0-0.3` - Conservative (safe, proven keywords)
  - `0.3-0.7` - Balanced (mix of proven + creative)
  - `0.7-1.0` - Experimental (bold, unique combinations)
- `target_style` (STRING) - Preferred style category
- `quality_threshold` (FLOAT) - Minimum keyword quality (0.0-10.0, default: 5.0)

**Outputs**: 
- `brain_data` (BRAIN) - Pass-through for chaining
- `suggestion_1` (STRING) - First enhanced prompt
- `suggestion_2` (STRING) - Second enhanced prompt
- `suggestion_3` (STRING) - Third enhanced prompt

**Creativity Examples**:
```
base_prompt: "portrait of a woman"
target_style: "photorealistic"

creativity: 0.2 (Conservative)
→ "professional portrait of a woman, studio lighting, sharp focus"

creativity: 0.7 (Balanced)
→ "stunning portrait of a woman, golden hour light, bokeh background, 8k"

creativity: 1.0 (Experimental)
→ "ethereal dreamlike portrait of a woman, surreal lighting, artistic composition, award-winning photography"
```

---

### BrainsXDEV_PromptBrainQualityScore (AI)

**Purpose**: A professional-grade AI analysis node for scoring image quality with a high degree of control.

**Features**: 
- Multiple analysis depth levels (fast, standard, deep)
- Different scoring models (balanced, artistic, technical)
- 10 distinct scoring criteria
- Advanced sharpness detection
- Color harmony analysis
- Composition rule checking
- Six separate output scores

**Inputs**:
- `image` (IMAGE) - Image to analyze
- `prompt` (STRING) - Original prompt (for semantic analysis)
- `analysis_depth` (LIST) - ["fast", "standard", "deep"]
  - Fast: ~0.5s, basic metrics
  - Standard: ~2s, full analysis
  - Deep: ~5s, advanced + ML models
- `scoring_model` (LIST) - ["balanced", "technical", "artistic"]
- `scoring_criteria` (MULTI-SELECT) - Which aspects to evaluate:
  - ✅ Sharpness
  - ✅ Exposure
  - ✅ Contrast
  - ✅ Color Harmony
  - ✅ Composition
  - ✅ Detail Level
  - ✅ Style Consistency
  - ✅ Creativity
  - ✅ Semantic Match
  - ✅ Overall Aesthetic

**Outputs**: 
- `overall_score` (FLOAT) - Final combined score (0.0-10.0)
- `letter_grade` (STRING) - A+ to F grade
- `technical_score` (FLOAT) - Technical quality (0.0-10.0)
- `artistic_score` (FLOAT) - Artistic quality (0.0-10.0)
- `semantic_score` (FLOAT) - Prompt matching (0.0-10.0)
- `detailed_report` (STRING) - Full analysis breakdown

**Letter Grade Scale**:
- `A+` (9.5-10.0) - Exceptional
- `A` (9.0-9.4) - Excellent
- `A-` (8.5-8.9) - Very Good
- `B+` (8.0-8.4) - Good
- `B` (7.5-7.9) - Above Average
- `B-` (7.0-7.4) - Average
- `C+` (6.5-6.9) - Below Average
- `C` (6.0-6.4) - Mediocre
- `D` (5.0-5.9) - Poor
- `F` (0.0-4.9) - Very Poor

**Usage Example**:
```
detailed_report: "
🎨 Quality Analysis Report

Overall Score: 8.7/10 (A-)
Letter Grade: A-

Technical Quality: 9.2/10
├─ Sharpness: 9.5/10 ✅ Excellent detail
├─ Exposure: 9.0/10 ✅ Well balanced
├─ Contrast: 8.8/10 ✅ Good dynamic range
└─ Color Accuracy: 9.5/10 ✅ True to life

Artistic Quality: 8.5/10
├─ Composition: 9.0/10 ✅ Rule of thirds
├─ Color Harmony: 8.5/10 ✅ Complementary
├─ Style Consistency: 8.0/10 ✅ Coherent
└─ Creativity: 8.5/10 ✅ Unique approach

Semantic Quality: 8.5/10
├─ Prompt Match: 9.0/10 ✅ Accurate to prompt
└─ Subject Clarity: 8.0/10 ✅ Clear subject

💡 Recommendations:
✅ Technical quality is exceptional
✅ Consider experimenting with more creative compositions
✅ Overall: High-quality professional result"
```

---

### BrainsXDEV_PromptBrainKSamplerDirect (AI-Optimized)

**Purpose**: An intelligent KSampler that automatically adjusts its parameters (steps, CFG, sampler, scheduler) based on the output from the PromptBrainQualityScore node.

**Features**: 
- Self-correcting generation loop
- Automatic parameter optimization
- Quality-based adjustment rules:
  - Low sharpness → Increase steps
  - Poor contrast → Adjust CFG
  - Weak colors → Change scheduler
  - Bad composition → Adjust sampler
- Learns optimal settings over time
- Maintains compatibility with standard KSampler

**Inputs**:
- `brain_data` (BRAIN) - For learning optimal parameters
- `model` (MODEL) - Stable Diffusion model
- `positive` (CONDITIONING) - Positive prompt
- `negative` (CONDITIONING) - Negative prompt
- `latent_image` (LATENT) - Starting latent
- `quality_analysis` (STRING) - Output from QualityScore node
- `seed` (INT) - Random seed
- `enable_optimization` (BOOLEAN) - Enable auto-adjust (default: True)
- `optimization_strength` (FLOAT) - How aggressively to adjust (0.0-1.0)

**Outputs**: 
- `brain_data` (BRAIN) - Updated with optimal parameters
- `samples` (LATENT) - Generated latent
- `optimization_report` (STRING) - Explanation of changes made

**Auto-Adjustment Examples**:
```
Scenario 1: Low Sharpness Detected
quality_analysis: "Sharpness: 5.5/10"
→ Steps: 20 → 35 (+15)
→ Report: "⚡ Increased steps to improve detail"

Scenario 2: Poor Contrast
quality_analysis: "Contrast: 4.0/10"
→ CFG: 7.0 → 8.5 (+1.5)
→ Report: "📊 Increased CFG for stronger contrast"

Scenario 3: Color Issues
quality_analysis: "Color Harmony: 5.0/10"
→ Scheduler: "normal" → "karras"
→ Report: "🎨 Changed scheduler for better color"

Scenario 4: High Quality (No Changes)
quality_analysis: "Overall: 9.2/10"
→ No changes made
→ Report: "✅ Parameters are optimal, no changes needed"
```

---

### BrainsXDEV_PromptBrainPerformanceDirect (BRAIN)

**Purpose**: Analyzes the performance and health of a BrainData object in real-time.

**Features**:
- Real-time database statistics
- Learning trend analysis
- Memory health checks
- Performance metrics
- Recommendation system

**Inputs**:
- `brain_data` (BRAIN) - BrainData to analyze

**Outputs**: 
- `brain_data` (BRAIN) - Pass-through
- `performance_report` (STRING) - Comprehensive statistics

**Report Example**:
```
performance_report: "
📊 BRAIN Performance Report

Database Health: ✅ Excellent
├─ Size: 2.4 MB
├─ Tables: All present
└─ Integrity: 100%

Learning Statistics:
├─ Total Learning Events: 847
├─ Unique Keywords: 342
├─ Style Categories: 12
└─ Date Range: 2024-09-15 to 2024-10-05

Quality Metrics:
├─ Average Score: 7.8/10
├─ Median Score: 8.2/10
├─ Score Range: 3.5 - 10.0
└─ Trend: ↗️ +0.3 improvement over last 100 events

Performance Indicators:
├─ Query Speed: 12ms (Fast)
├─ Learning Speed: 45ms (Fast)
├─ Memory Usage: 15 MB (Normal)
└─ Cache Hit Rate: 87% (Good)

Top Keywords (by avg score):
1. masterpiece - 9.2/10 (used 89 times)
2. detailed - 8.9/10 (used 156 times)
3. professional - 8.7/10 (used 94 times)

💡 Recommendations:
✅ Training data is well-balanced
✅ Performance is optimal
⚠️ Consider pruning old low-quality entries (<5.0)
✅ Ready for production use"
```

---

### BrainsXDEV_PromptBrainResetDirect (BRAIN)

**Purpose**: Safely resets or clears the data within a BrainData object.

**Features**: 
- Mandatory confirmation checkbox (prevents accidents)
- Multiple reset modes:
  - Complete reset (wipe everything)
  - Preserve styles (keep style data)
  - Preserve history (keep learning events)
  - Selective reset (keep high-quality entries)
- Built-in automatic backup before reset
- Detailed confirmation report

**Inputs**:
- `brain_data` (BRAIN) - BrainData to reset
- `confirm_reset` (BOOLEAN) - **MUST BE TRUE** to proceed
- `reset_mode` (LIST) - Reset strategy:
  - `"complete"` - Delete everything
  - `"preserve_styles"` - Keep style categories
  - `"preserve_history"` - Keep learning events
  - `"selective"` - Only remove low-quality data
- `quality_threshold` (FLOAT) - For selective mode (keep entries above this)
- `create_backup` (BOOLEAN) - Backup before reset (default: True)
- `backup_location` (STRING) - Where to save backup

**Outputs**: 
- `brain_data` (BRAIN) - New, reset BrainData object
- `reset_status` (STRING) - Detailed reset report

**Safety Features**:
```
⚠️ SAFETY CHECKPOINT ⚠️

confirm_reset: FALSE
→ "❌ Reset cancelled. Set confirm_reset to TRUE to proceed."

confirm_reset: TRUE
→ "✅ Creating backup: promptbrain_backup_2024-10-05_14-30-22.db"
→ "✅ Backup successful (2.4 MB saved)"
→ "🗑️ Performing complete reset..."
→ "✅ Reset complete. All data cleared."
→ "📊 New database initialized and ready."
```

**Reset Mode Examples**:
```
Mode: "complete"
→ Deletes everything, fresh start

Mode: "preserve_styles"  
→ Deletes: Learning events, keywords
→ Keeps: Style categories, style statistics
→ Use case: Start fresh but keep style knowledge

Mode: "preserve_history"
→ Deletes: Keyword associations, statistics
→ Keeps: All learning events (for analysis)
→ Use case: Reprocess learning with new algorithm

Mode: "selective" (threshold: 7.0)
→ Deletes: All entries with score < 7.0
→ Keeps: High-quality entries (score ≥ 7.0)
→ Use case: Remove poor training data
```

---

## 🗂️ Node Categories

### Brains-XDEV/PromptBrain
All BRAIN learning system nodes:
- PromptBrainSource
- PromptBrainLearnDirect
- PromptBrainSuggestDirect
- PromptBrainQualityScore
- PromptBrainKSamplerDirect
- PromptBrainPerformanceDirect
- PromptBrainResetDirect
- PromptBrainParameterOptimizer

### Brains-XDEV/AI
AI analysis and integration nodes:
- Florence2Adapter
- EnhancedWD14Tagger
- AnalyzeBrain

### Brains-XDEV/Utils
Utility and helper nodes:
- CleanupMemory
- ComfyUIStatusCheck

---

## 🔄 Common Workflows

### Basic Learning Loop
```
1. PromptBrainSource → Create/load memory
2. KSampler → Generate image
3. PromptBrainQualityScore → Rate quality
4. PromptBrainLearnDirect → Learn from result
5. Loop back to step 2 with improved knowledge
```

### Automated Quality Pipeline
```
1. PromptBrainSource → Load trained memory
2. PromptBrainSuggestDirect → Get enhanced prompts
3. KSampler → Generate from suggestions
4. PromptBrainQualityScore → Auto-score results
5. PromptBrainLearnDirect → Auto-learn
6. PromptBrainPerformanceDirect → Monitor progress
```

### Intelligent Generation
```
1. PromptBrainSource → Load memory
2. PromptBrainSuggestDirect → Get suggestions
3. PromptBrainKSamplerDirect → Generate with auto-optimization
4. PromptBrainQualityScore → Analyze result
5. Loop: KSampler auto-adjusts based on quality analysis
```

### Style Transfer Learning
```
1. LoadImage → Load reference image
2. Florence2Adapter → Extract style description
3. PromptBrainLearnDirect → Learn style (high score)
4. PromptBrainSuggestDirect → Generate style-aware prompts
5. KSampler → Generate in learned style
```

---

## 💡 Best Practices

### Learning Rate Guidelines
- **New memory**: Start with `learning_rate: 1.0`
- **Established memory**: Use `learning_rate: 0.5-0.7`
- **Fine-tuning**: Use `learning_rate: 0.3-0.5`
- **Production memory**: Use `learning_rate: 0.2-0.3`

### Quality Score Guidelines
- **0.0-4.0**: Poor quality, don't learn from this
- **4.0-6.0**: Below average, learn cautiously
- **6.0-8.0**: Good quality, standard learning
- **8.0-10.0**: Excellent quality, high learning rate

### Creativity Guidelines
- **Photography/Realism**: 0.2-0.5
- **Illustration/Art**: 0.5-0.8
- **Experimental/Abstract**: 0.7-1.0

### Database Maintenance
- Run PromptBrainPerformanceDirect weekly
- Backup before major changes
- Use selective reset to remove poor data (<5.0)
- Monitor database size (>50MB may need cleanup)

---

## 🔗 Related Documentation

- [README.md](../README.md) - Main project overview
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [workflows/INDEX.md](../workflows/INDEX.md) - Workflow examples
- [DEVELOPMENT.md](DEVELOPMENT.md) - Developer guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues

---

**Made with 🧠 for the ComfyUI community**
