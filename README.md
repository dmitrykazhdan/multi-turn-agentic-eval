# Multi-Turn Agentic Evaluation Framework

A comprehensive evaluation framework for conversational AI agents using τ²-bench, with extended analytics and visualization capabilities.

## Project Structure

### Core Components

- **`tau2_eval/`** - Basic τ²-bench model evaluation runner
  - `main.py` - Entry point for running model comparisons
  - `tau2_runner.py` - Core evaluation logic with environment setup

- **`tau2_ext/`** - Extended analytics and visualization framework
  - `main.py` - Analysis script for processing simulation results
  - `data_processing/` - Data preparation and enrichment modules
  - `metrics/` - Comprehensive metric calculation (4 main metrics)
  - `visualisations/` - Modular plotting framework with domain separation

- **`tests/`** - Test suite for framework validation
  - `test_tau2_setup.py` - Environment and τ²-bench installation verification
  - `test_litellm_calls.py` - API connectivity and LLM inference testing
  - `test_tau2_mock_task.py` - Basic τ²-bench functionality validation
  - `test_tool_schema_loader.py` - Tool schema loading verification

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- τ²-bench installation (see below)
- API keys for xAI (Grok) and OpenAI

### 2. Environment Setup

```bash
# Clone this repository
git clone https://github.com/dmitrykazhdan/multi-turn-agentic-eval.git
cd multi-turn-agentic-eval

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp env.example .env
# Edit .env with your API keys:
# XAI_API_KEY=your_grok_api_key_here
# OPENAI_API_KEY=your_openai_api_key_here
```

### 3. τ²-bench Installation

```bash
# Clone τ²-bench to the same parent directory
cd ..
git clone https://github.com/sierra-research/tau2-bench.git
cd tau2-bench

# Install τ²-bench
pip install -e .

# Verify installation
tau2 --help
```

### 4. Verify Setup

```bash
# Run setup verification
python tests/test_tau2_setup.py
python tests/test_litellm_calls.py
```

## Usage

### Basic Model Evaluation

Run τ²-bench evaluations with model comparisons:

```bash
# Run basic evaluation (default: Grok-3 on telecom/retail domains)
python tau2_eval/main.py

# Or run directly with custom parameters
python tau2_eval/tau2_runner.py
```

### Extended Analytics

Process simulation results with comprehensive metrics and visualizations:

```bash
# Analyze simulation files
python tau2_ext/main.py --input-dir /path/to/simulation/results --output-dir analytics_results

# The analysis includes:
# - Per-tool Precision/Recall/F1/Omission metrics
# - Tool Criticality Index (TCI)
# - Sequence Compliance (nPED + Position Deviation)
# - Complexity-weighted and bucketed pass@1
```

## Key Features

### Extended Metrics (τ²-ext)

1. **Per-Tool Precision/Recall/F1/Omission** - Tool usage accuracy analysis
2. **Tool Criticality Index (TCI)** - Impact of tool correctness on overall success
3. **Sequence Compliance** - Plan execution order and deviation analysis
4. **Complexity-Weighted pass@1** - Performance across task complexity levels

### Visualization Framework

- **Domain-separated plots** - Separate analysis per domain
- **Modular architecture** - Individual visualizers for each metric type
- **Timestamped outputs** - Organized result storage
- **Interactive and static plots** - Both display and file saving options

### Data Processing

- **Conversation enrichment** - Extract features from raw simulation logs
- **Dynamic tool schema loading** - Domain-specific tool argument validation
- **Task loader** - Ground truth tool expectation management

## Output Structure

```
analytics_results/
├── figures_YYYYMMDD_HHMMSS/
│   ├── tci_by_domain.png
│   ├── precision_recall_by_domain.png
│   ├── nped_by_domain.png
│   └── bucket_pass1_by_domain.png
├── per_tool_prf.csv
├── tool_criticality.csv
├── sequence_compliance.csv
├── bucket_pass1.csv
└── summary.txt
```

## Testing Order

1. **Environment Setup**: `python tests/test_tau2_setup.py`
2. **API Connectivity**: `python tests/test_litellm_calls.py`
3. **Basic Functionality**: `python tests/test_tau2_mock_task.py`
4. **Extended Features**: `python tests/test_tool_schema_loader.py`

## Configuration

- **API Keys**: Configure in `.env` file (xAI for Grok, OpenAI for comparison models)
- **τ²-bench Path**: Defaults to `../tau2-bench`, configurable via `--tau2-path`
- **Domains**: Supports `telecom`, `retail`, and other τ²-bench domains
- **Concurrency**: Configurable via `--max-concurrency` parameter

## Dependencies

Key dependencies include:
- `litellm` - Multi-provider LLM access
- `pandas` - Data manipulation
- `matplotlib` - Visualization
- `scipy` - Statistical analysis
- `python-dotenv` - Environment management

See `requirements.txt` for complete list.

## License

MIT License
