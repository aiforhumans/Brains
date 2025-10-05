# 🎨 Workflow Gallery & Documentation

Complete guide to all 16 workflows included in comfyui-Brains.

## � Quick Navigation

- [Basic Templates](#-basic-templates-5-workflows) - Getting started workflows
- [Advanced Automation](#-advanced-automation-7-workflows) - Production workflows
- [Experimental](#-experimental-workflows-4-workflows) - Creative experiments
- [Legacy Workflows](#-legacy-workflows) - Previous versions
- [Usage Tips](#-usage-tips) - Best practices

---

## 🌱 Basic Templates (5 workflows)

Quick-start workflows for learning the BRAIN learning system.

### 1. Simple Learning Loop
**File**: `basic/simple_learning.json` *(coming soon)*  
**Purpose**: Introduction to BRAIN learning cycle  
**Complexity**: ⭐ Beginner

**What it does:**
- Create a BRAIN database
- Generate an image
- Learn from the prompt and result
- Get AI suggestions for improvement

**Key Nodes:**
- PromptBrainSource (create database)
- PromptBrainLearnDirect (learn patterns)
- PromptBrainSuggestDirect (get suggestions)

**Use Case**: First workflow to understand BRAIN learning basics

---

### 2. Quality Analysis
**File**: `basic/quality_analysis.json` *(coming soon)*  
**Purpose**: Learn quality scoring system  
**Complexity**: ⭐⭐ Intermediate

**What it does:**
- Generate images with different settings
- Score quality (technical/artistic/semantic)
- Analyze performance trends
- Identify best parameters

**Key Nodes:**
- PromptBrainQualityScore (multi-dimensional scoring)
- PromptBrainPerformanceDirect (trend analysis)

**Use Case**: Optimize generation settings based on quality metrics

---

### 3. PromptBrain Source
**File**: `01_promptbrain_source.json` ✅  
**Purpose**: Create/load BRAIN databases  
**Complexity**: ⭐ Beginner

**What it does:**
- Create new BRAIN databases
- Load existing databases
- Initialize learning system
- Manage database paths

**Key Nodes:**
- PromptBrainSource (load/create)

**Use Case**: Starting point for any BRAIN workflow

---

### 4. PromptBrain Learn
**File**: `02_promptbrain_learn.json` ✅  
**Purpose**: Learn from prompts with quality scoring  
**Complexity**: ⭐⭐ Intermediate

**What it does:**
- Learn from prompts
- Track quality scores
- Build learning history
- Associate styles with prompts

**Key Nodes:**
- PromptBrainLearnDirect (with quality scoring)

**Use Case**: Build up BRAIN knowledge from successful generations

---

### 5. Memory Read/Write
**File**: `memory_read_write.json` ✅  
**Purpose**: Understand BRAIN data persistence  
**Complexity**: ⭐ Beginner

**What it does:**
- SQLite database operations
- Data persistence demonstration
- Memory management basics

**Use Case**: Understand how BRAIN data is stored

---

## 🚀 Advanced Automation (7 workflows)

Production-ready professional workflows for serious creative work.

### 1. Quality Analysis Pipeline
**File**: `advanced/quality_analysis_pipeline.json` ✅  
**Nodes**: 25+ | **Complexity**: ⭐⭐⭐⭐ Advanced

**What it does:**
- Multi-stage iterative learning
- Automatic quality feedback loops
- Parameter optimization per iteration
- Comprehensive performance reporting

**Key Features:**
- 3-generation evolution cycle
- Quality-driven parameter adjustment
- Automated best-practice learning
- Full analytics dashboard

**Use Case**: High-quality iterative refinement for professional results

---

### 2. Style Transfer Learning
**File**: `advanced/style_transfer_learning.json` ✅  
**Nodes**: 28 | **Links**: 46 | **Complexity**: ⭐⭐⭐⭐ Advanced

**What it does:**
- Extract style from reference images
- Learn style characteristics with Florence2
- Apply learned style to new generations
- Validate style consistency

**Key Features:**
- Florence2 detailed caption analysis
- Style-category learning integration
- Quality scoring for style matching
- Reference image comparison

**Use Case**: Consistent style application across multiple generations

---

### 3. Parameter Optimization
**File**: `advanced/parameter_optimization.json` ✅  
**Nodes**: 30+ | **Complexity**: ⭐⭐⭐⭐⭐ Expert

**What it does:**
- AI-driven parameter search
- Quality-based optimization
- Multi-dimensional testing (steps/CFG/sampler)
- Statistical analysis of results

**Key Features:**
- PromptBrainParameterOptimizer node
- Automatic best-parameter detection
- Quality trend visualization
- Performance reporting

**Use Case**: Find optimal generation settings for specific prompts/styles

---

### 4. Iterative Learning Loop
**File**: `advanced/iterative_learning_loop.json` ✅  
**Nodes**: 22 | **Complexity**: ⭐⭐⭐ Intermediate

**What it does:**
- Continuous learning from results
- Automatic suggestion improvement
- Multi-iteration refinement
- Learning history tracking

**Use Case**: Long-running learning sessions for specific subjects

---

### 5. Professional Portrait Studio
**File**: `advanced/professional_portrait_studio.json` ✅  
**Nodes**: 25 | **Links**: 39 | **Complexity**: ⭐⭐⭐⭐ Advanced

**What it does:**
- Studio portrait photography workflow
- Professional lighting and pose prompts
- Quality refinement iteration
- Technical quality optimization

**Key Features:**
- Portrait-specific prompt learning
- Florence2 facial analysis
- Technical quality focus (sharpness, exposure, composition)
- Professional output standards

**Use Case**: High-end portrait photography with AI assistance

---

### 6. Fashion Photography
**File**: `advanced/fashion_photography.json` ✅  
**Nodes**: 33 | **Links**: 48 | **Complexity**: ⭐⭐⭐⭐⭐ Expert

**What it does:**
- Editorial fashion photography workflow
- 3-generation evolution system
- Pose and clothing analysis
- Editorial style consistency

**Key Features:**
- Multi-generation refinement
- Style category: "Fashion Editorial"
- Artistic quality prioritization
- Clothing and pose learning

**Use Case**: Editorial fashion shoots with consistent styling

---

### 7. Artistic Figure Studies
**File**: `advanced/artistic_figure_studies.json` ✅  
**Nodes**: 31 | **Links**: 45 | **Complexity**: ⭐⭐⭐⭐ Advanced

**What it does:**
- Academic figure drawing approach
- Anatomy and form analysis
- Artistic composition learning
- Traditional art style application

**Key Features:**
- Classical art style learning
- Anatomical correctness focus
- Composition analysis
- Academic quality standards

**Use Case**: Academic figure drawing and classical art studies

---

## 🧪 Experimental Workflows (4 workflows)

Creative and experimental concepts pushing ComfyUI limits.

### 1. Ouroboros Engine
**File**: `experimental/ouroboros_engine.json` ✅  
**Nodes**: 32 | **Links**: 55 | **Complexity**: ⭐⭐⭐⭐⭐ Extreme

**Concept**: Self-consuming recursive evolution system

**What it does:**
- Generate image → Learn from it → Feed back as reference → Repeat
- Recursive style evolution
- Self-referential learning loops
- Emergent pattern discovery

**Key Features:**
- 3 recursive generations
- Each generation learns from previous
- Img2Img feedback loop
- Style drift analysis

**Use Case**: Discover emergent artistic styles through recursive evolution

**⚠️ Warning**: Can produce highly abstract/unpredictable results. Requires 16GB+ VRAM.

---

### 2. Schizophrenic Tribunal
**File**: `experimental/schizophrenic_tribunal.json` ✅  
**Nodes**: 35 | **Links**: 48 | **Complexity**: ⭐⭐⭐⭐⭐ Extreme

**Concept**: Multi-personality AI competition system

**What it does:**
- 3 independent BRAIN personalities compete
- Different creativity settings (conservative/moderate/wild)
- Quality-based winner selection
- Cross-pollination learning

**Key Features:**
- Brain A (creativity: 0.3) - Conservative
- Brain B (creativity: 0.7) - Balanced
- Brain C (creativity: 1.0) - Experimental
- Competition scoring system

**Use Case**: Explore prompt space with diverse AI perspectives

**⚠️ Warning**: Computationally expensive. Best run overnight.

---

### 3. Corrupted Oracle
**File**: `experimental/corrupted_oracle.json` ✅  
**Nodes**: 22 | **Links**: 35 | **Complexity**: ⭐⭐⭐⭐ Advanced

**Concept**: Adversarial quality degradation system

**What it does:**
- Start with high-quality generation
- Deliberately corrupt parameters
- Learn what makes quality drop
- Understand quality boundaries

**Key Features:**
- Adversarial parameter selection
- Quality degradation tracking
- Failure mode analysis
- Boundary condition discovery

**Use Case**: Research into quality failure modes and boundaries

**⚠️ Warning**: Designed to produce low-quality results for research purposes.

---

### 4. Temporal Paradox
**File**: `experimental/temporal_paradox.json` ✅  
**Nodes**: 28 | **Links**: 45 | **Complexity**: ⭐⭐⭐⭐⭐ Extreme

**Concept**: Time-loop causality violation system

**What it does:**
- Future generation influences past learning
- Causality-violating feedback loops
- Temporal quality bootstrapping
- Non-linear learning evolution

**Key Features:**
- 3-stage temporal loop
- Future-to-past learning propagation
- Quality bootstrapping from "future"
- Causal loop analysis

**Use Case**: Explore non-traditional learning architectures

**⚠️ Warning**: Highly experimental. Results may be nonsensical or brilliant.

---

## 📦 Legacy Workflows

Older workflows from development phase:

### Debug & Testing
- `debug_all_nodes.json` ✅ - Comprehensive node testing
- `florence2_adapter_debug.json` ✅ - Florence2 debugging
  - Features: Florence2, Quality Score, Memory, BRAIN datatype
  - Extensive debug outputs and troubleshooting notes
  
- `iterative_learning_loop.json` ✅ - Manual feedback loop workflow
  - Generate → Analyze → Learn → Suggest → Iterate
  - Quality scoring, pattern learning, prompt adaptation
  - See `ITERATIVE_LOOP_GUIDE.md` for detailed instructions
  
- `complete_learning_pipeline.json` - Full learning cycle *(coming soon)*
- `quality_analysis_pipeline.json` - Multi-stage analysis *(coming soon)*

## 📊 Quick Start

1. **Beginners**: Start with `01_promptbrain_source.json`
2. **AI Features**: Try `florence2_adapter_debug.json`
3. **Learning**: Use `02_promptbrain_learn.json`
4. **Storage**: Test `memory_read_write.json`
5. **Advanced**: Explore complete demos

## 🔧 Debug Features

Each workflow includes:
- ShowText nodes for string outputs
- Show any [Crystools] for data inspection
- Note nodes with documentation
- Console logging markers
- Error handling displays

## 📝 Workflow Naming Convention

- `##_` prefix = numbered sequence
- `_debug` suffix = extra debugging nodes
- `_simple` suffix = minimal version
- No suffix = standard template

## 💡 Usage Tips

- Load workflow in ComfyUI
- Read Note nodes for instructions
- Check console for [Brains-XDEV] logs
- Review debug nodes after execution
- Modify parameters as needed

---

**Status**: Templates in progress  
**Updated**: October 2025  
**Version**: 1.0.0
