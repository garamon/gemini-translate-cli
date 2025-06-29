# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`gemini-translate` is a Python CLI tool that translates text or web content using Google's Gemini API. It can read text from stdin or accept a URL as an argument, outputting the translation to stdout. The tool is designed for Unix-style piping operations and is particularly useful on macOS with pbpaste for quick clipboard translations.

### Key Features
- Text translation from stdin
- Web page URL translation with automatic content extraction
- Multi-language support (default: Japanese)
- Multiple Gemini model support via environment variable
- Unix philosophy compliance for easy piping and scripting

## Development Setup

### Environment Requirements

- Python 3.13 (specified in `.python-version`)
- `GTR_API_KEY` environment variable must be set with a valid Gemini API key
- `GTR_MODEL` (optional) - Gemini model to use (default: "gemini-2.5-pro")

### Package Management

This project uses `uv` as the package manager. Common commands:

```bash
# Install dependencies
uv sync

# Run the CLI tool after installation
gtr

# Install in development mode
uv pip install -e .

# Install as global tool
uv tool install .
```

### Development Commands

Use the `justfile` for common tasks:

```bash
# Run linter with auto-fix
just lint
# or directly: uv run ruff check --fix .

# Format code
just format
# or directly: uv run ruff format .
```

## Architecture

### Key Components

- **Main Entry Point**: `src/gemini_translate/cli.py:main()` - Handles CLI arguments and orchestrates translation
- **CLI Command**: `gtr` - Registered in `pyproject.toml` as the command-line interface
- **Translation Function**: `translate_text()` - Handles both text and URL translation with optimized prompts
- **Setup Function**: `setup_gemini()` - Initializes Gemini API with model selection

### Translation Flow

1. **Input Sources**:
   - Standard input: `pbpaste | gtr` or `echo "text" | gtr`
   - URL argument: `gtr https://example.com`

2. **Processing**:
   - Uses `google.generativeai` to create a Gemini model instance
   - Applies different prompts for text vs URL translation:
     - Text: Ensures complete translation without abbreviation (lines 35-43)
     - URL: Extracts main content and ignores navigation/ads (lines 26-33)

3. **Output**: Translated text to stdout, errors to stderr

### Error Handling

- Missing API key: Exits with clear instructions
- Empty input: Specific error message
- API errors: Displays error and exits with code 1
- No retry logic implemented

### Usage Examples

```bash
# Translate from clipboard (macOS)
pbpaste | gtr

# Translate to specific language
echo "Hello" | gtr -t Spanish

# Translate a web page
gtr https://example.com/article.html

# Translate URL to specific language
gtr https://example.com -t English

# Using different model
GTR_MODEL="gemini-2.5-flash" gtr https://example.com

# Chaining with other commands
curl -s https://example.com/api.json | jq .description | gtr
```

## Project Structure

```
gemini-translate/
├── src/
│   └── gemini_translate/
│       ├── __init__.py         # Package init (empty)
│       └── cli.py              # Main CLI implementation (93 lines)
├── .vscode/                    # VSCode configuration
│   ├── extensions.json         # Recommended extensions
│   └── settings.json           # Python/Ruff settings
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Dependency lock file
├── justfile                    # Development commands
├── README.md                   # User documentation (Japanese)
├── CLAUDE.md                   # This file
├── .gitignore                  # Git ignore rules
└── .python-version             # Python 3.13 requirement
```

## Configuration Details

### pyproject.toml
- Project name: `gemini-translate`
- Version: `0.1.0`
- Command entry point: `gtr`
- Dependencies: `google-generativeai>=0.8.5`
- Dev dependencies: `ruff>=0.12.1`
- Ruff configuration with various linting rules enabled

### Environment Variables
- `GTR_API_KEY` (required): Google Gemini API key
- `GTR_MODEL` (optional): Model selection, defaults to "gemini-2.5-pro"

## Development Notes

- The tool requires internet access for both API calls and URL fetching
- Error messages are written to stderr, translations to stdout
- The tool exits with code 1 on any error
- No test files currently exist in the project
- The project follows Python packaging best practices
- Ruff is configured for both linting and formatting
- VSCode settings are pre-configured for Python development

## Recent Session Changes

- Unified command name to `gtr` throughout the project
- Changed environment variables from `TR_GEMINI_*` to `GTR_*`
- Added URL translation capability with separate prompts
- Updated default model to `gemini-2.5-pro`
- Added `uv tool install .` installation method
- Removed test directory structure
- Fixed various inconsistencies in documentation