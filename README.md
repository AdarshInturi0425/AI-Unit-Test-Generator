# 🤖 AI-Unit-Test-Generator

An autonomous agent that generates and self-heals Python unit tests using **Google Gemini 3 Flash**.

This tool demonstrates advanced AI integration, feedback loops, and production-ready error handling patterns.

---

## ✨ Features

### 🧪 Automatic Test Generation
Analyzes any Python file and generates a complete `unittest` suite with comprehensive test cases.

### 🔧 Self-Healing Loop
If tests fail, the AI:
1. Analyzes the test failure
2. Identifies the bug in your source code
3. Automatically fixes it
4. Re-runs tests to verify the fix

### 🛡️ Resilient API Integration
- Built-in exponential backoff for handling 503 "Overloaded" errors
- Automatic retry logic (up to 3 attempts with exponential delays)
- Graceful degradation if API is temporarily unavailable

### ⚡ Production-Ready Code
- Error capture and detailed logging
- Subprocess-based test execution with stderr tracking
- Clean separation of concerns (Engine → Factory → Controller pattern)

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install google-genai
```

### 2. Set Your API Key
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### 3. Generate Tests & Heal Code
```bash
python3 main.py calculator.py
```

**Output:**
```
🧠 AI is analyzing calculator.py...
✅ Success! Generated: tests/test_calculator.py
🧪 Running generated tests: tests/test_calculator.py...
✅ ALL TESTS PASSED!
🎉 Code is already healthy. Work complete!
```

---

## 📁 Project Architecture

```
AI-Unit-Test-Generator/
├── main.py                 # Orchestrator (entry point)
├── src/
│   ├── ai_engine.py       # Gemini API integration (test generation + code healing)
│   └── generator.py       # Test factory (file I/O + unittest execution)
├── tests/                 # Auto-generated test files
├── calculator.py          # Sample code for demonstration
├── requirements.txt       # Dependencies
├── .gitignore            # Git exclusions
└── README.md             # This file
```

### 🧠 Core Components

**AITestEngine** (`src/ai_engine.py`)
- Interfaces with Google Gemini 3 Flash
- `generate_test_code()` - Creates unittest files from source code
- `heal_code()` - Analyzes errors and fixes source code
- Built-in retry logic with exponential backoff

**TestFactory** (`src/generator.py`)
- `create_test_file()` - Reads source, generates tests, saves to `/tests`
- `run_tests()` - Executes tests via subprocess, captures errors
- Returns both exit codes and error messages for the healing loop

**Main Controller** (`main.py`)
- Argument parsing and pipeline orchestration
- Implements try-heal-retry feedback loop
- Exits cleanly when code is healthy

---

## 🔄 How It Works: The Self-Healing Loop

```
1. Generate Tests
   ↓
2. Run Tests
   ├─ PASS → ✅ Work Complete!
   └─ FAIL → Capture Error
             ↓
3. Analyze Failure
   ↓
4. AI Fixes Code
   ↓
5. Re-Run Tests
   └─ ✅ PASS → Work Complete!
```

### Real-World Example

Given buggy code where `divide()` returns `a + b` instead of `a / b`:

```python
# calculator.py (buggy)
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a + b  # ❌ BUG!
```

**Running the tool:**
```bash
python3 main.py calculator.py
```

**The self-healing process:**
1. ✅ Tests generated successfully
2. ❌ Tests fail: `AssertionError: 12 != 5` (expecting 5, got 12)
3. 🔧 AI analyzes the error message
4. 🧠 AI realizes divide should return `a / b`
5. ✨ Code automatically fixed
6. 🧪 Tests re-run and pass

---

## 🛠️ Extending: Test Multiple Files

Want to generate tests for an entire directory? Use this pattern:

```python
import glob
import os

def run_bulk_generation(directory):
    python_files = glob.glob(f"{directory}/**/*.py", recursive=True)
    
    for file in python_files:
        if "test_" in file:
            continue  # Skip test files
        
        print(f"🔎 Scanning: {file}")
        # Run your existing main() logic here
```

---

## 📊 Technical Details

### API Configuration
- **Model:** `gemini-3-flash-preview`
- **SDK:** `google-genai` (modern, v0.3.0+)
- **Retry Strategy:** 3 attempts with 2-10 second delays
- **Rate Limit Handling:** Automatic backoff for 429 and 503 errors

### Test Execution
- Uses Python's built-in `unittest` module
- Tests saved to `/tests/test_<original_filename>.py`
- Subprocess-based execution for isolation
- Stderr captured for error analysis

### Error Handling
- API overload (503) → Automatic retry with exponential backoff
- Rate limit (429) → Automatic retry with exponential backoff
- Code generation failures → Clear error messages
- Self-healing failures → Falls back to original code

---

## 🔒 Security

⚠️ **API Key Management**
- Never commit your `.env` file (it's in `.gitignore`)
- Use `export GEMINI_API_KEY="..."` or a `.env` file with a loader
- Regenerate API keys if accidentally exposed

---

## 📚 What This Demonstrates

✅ **API Integration**
- Modern SDK usage (google-genai)
- Error handling and retry logic
- Production-grade resilience

✅ **Software Architecture**
- Factory pattern for test creation
- Dependency injection (AITestEngine passed to TestFactory)
- Separation of concerns (Engine → Factory → Controller)
- Feedback loops and error-driven workflows

✅ **AI/ML Fundamentals**
- Prompt engineering (strict rules for consistent output)
- Feedback loops (error messages drive AI decisions)
- Autonomous error correction

✅ **Python Best Practices**
- Subprocess management
- File I/O and error handling
- Clean CLI interface

---

## 🚀 Next Steps

1. **Get a Gemini API Key:** https://ai.google.dev/
2. **Clone and test:** `python3 main.py calculator.py`
3. **Experiment:** Try breaking the calculator code and watch it auto-heal
4. **Scale:** Adapt the pattern to your own projects

---

## 💡 Key Insights from Building This

1. **Modern APIs change fast** - Query live model availability instead of trusting docs
2. **Error messages are data** - Use them to drive intelligent fixes
3. **Retry logic saves lives** - Transient failures are inevitable; handle them gracefully
4. **Feedback loops enable autonomy** - Test failures can trigger automated corrections

---

## 📄 License

MIT - Feel free to use and modify for your own projects

---

**Built with:** Python 3, Google Gemini 3 Flash, unittest module

**Demonstrates:** AI integration, feedback loops, production-ready error handling