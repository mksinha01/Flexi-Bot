# Contributing to FlexiBot

First off, thank you for considering contributing to FlexiBot! It's people like you that make FlexiBot such a great tool for PDF document interaction.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for FlexiBot. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**
- Check the existing issues to see if the bug has already been reported
- Ensure you're using the latest version
- Check that your issue isn't related to AWS credentials or configuration

**How Do I Submit A Bug Report?**
Use the bug report template and include:
- A clear and descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)
- PDF file characteristics (if relevant)
- Error logs or screenshots

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:
- A clear and descriptive title
- A detailed description of the proposed feature
- Use cases where this enhancement would be useful
- Whether it should work with Claude, Llama 3, or both

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these beginner-friendly issues:
- Issues labeled `good first issue` - should only require a few lines of code
- Issues labeled `help wanted` - should be a bit more involved than beginner issues

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure your code follows the existing style
4. Make sure your code lints without errors
5. Issue that pull request!

## Development Environment Setup

### Prerequisites
- Python 3.8 or higher
- AWS account with Bedrock access
- AWS CLI configured with appropriate credentials

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mksinha01/Flexi-Bot.git
   cd Flexi-Bot
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure AWS credentials:**
   Make sure your AWS CLI is configured with access to Bedrock services.

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Running Tests

Currently, the project uses manual testing. We welcome contributions to add automated testing:

```bash
# Manual testing checklist:
# 1. Upload a sample PDF
# 2. Test with different AI models
# 3. Ask questions and verify responses
# 4. Test different use cases (medical, legal, books, etc.)
```

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and modular

## Project Structure

```
FlexiBot/
├── app.py                    # Main Streamlit application
├── claude2.py               # Claude 2 model integration
├── llama3.py                # Llama 3 model integration
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore patterns
├── CONTRIBUTING.md         # This file
└── .github/                # GitHub templates
    ├── ISSUE_TEMPLATE/     # Issue templates
    └── pull_request_template.md
```

## Working with AI Models

### Adding New Models
When adding support for new AI models:
1. Create a new file following the pattern `<model_name>.py`
2. Implement the same interface as existing models
3. Update the main app.py to include the new model option
4. Test thoroughly with various PDF types

### Model-Specific Guidelines
- **Claude**: Best for detailed analysis and medical documents
- **Llama 3**: Good for general purpose document Q&A
- Ensure prompts are optimized for each model's strengths

## Documentation

- Update README.md if you change functionality
- Add inline comments for complex logic
- Update this CONTRIBUTING.md if you change development processes

## Community

- Be respectful and constructive in discussions
- Help others by answering questions in issues
- Share interesting use cases and examples

## Questions?

Don't hesitate to ask questions by creating an issue. We're here to help!

Thank you for contributing to FlexiBot! 🤖📄