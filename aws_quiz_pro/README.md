# AWS Quiz Pro

A comprehensive AWS certification quiz application with advanced features for practice and exam simulation.

## Features

- 📝 **Practice Mode**: Study with customizable filters and hints
- 🎯 **Exam Mode**: Simulate real AWS certification exams (65 questions, timed)
- 📊 **Statistics**: Track your progress with detailed analytics and charts
- 📋 **Review System**: Review wrong answers and all questions with detailed explanations
- ⚙️ **Customization**: Configure appearance, question order, timers, and more
- 💾 **Persistence**: Automatic caching and progress tracking

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aws_quiz_pro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

Or with a specific PDF file:
```bash
python main.py path/to/your/quiz.pdf
```

## Directory Structure
```
aws_quiz_pro/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── config/                 # Configuration management
│   ├── settings.py
│   └── constants.py
├── core/                   # Business logic
│   ├── quiz_manager.py
│   ├── pdf_parser.py
│   └── statistics.py
├── ui/                     # User interface
│   ├── main_window.py
│   ├── quiz_tab.py
│   ├── review_tab.py
│   ├── stats_tab.py
│   ├── settings_tab.py
│   └── dialogs.py
└── utils/                  # Utilities
    ├── file_utils.py
    └── ui_helpers.py
```

## Usage

### Loading Questions

1. Click "📁 Load PDF" button
2. Select your AWS quiz PDF file
3. Wait for questions to be parsed and cached

### Taking a Quiz

**Practice Mode:**
- Select difficulty filter (optional)
- Choose question order (Random, Sequential, or Reverse)
- Click "🚀 Start Quiz"
- Answer questions with hints available
- Review explanations for wrong answers

**Exam Mode:**
- Select "Exam (65 Questions)" from mode dropdown
- Click "🚀 Start Quiz"
- Complete 65 random questions within time limit
- No hints or explanations during exam
- Get pass/fail result (70% required)

### Question Ordering

Three ordering options available:
- **Random**: Questions in random order (default for exams)
- **Sequential (First to Last)**: Original PDF order (Q1, Q2, Q3...)
- **Reverse (Last to First)**: Reverse PDF order (Q100, Q99, Q98...)

### Reviewing Answers

- **Review Wrong**: See only incorrect answers with explanations
- **Review All**: Browse all answered questions with collapsible details
- Color-coded options show your answer vs correct answer

### Statistics

View detailed statistics including:
- Total quizzes taken
- Average and best scores
- Exam pass rate
- Performance trends over time
- Score distribution charts

### Settings

Customize:
- Appearance mode (Dark/Light)
- Default question order
- Show explanations
- Timer settings
- Exam time limit

## PDF Format

The application expects PDF files with questions in the following format:
```
Question #1
What is AWS EC2?
A. A storage service
B. A compute service
C. A database service
D. A networking service
Correct Answer: B
Explanation: EC2 is Amazon's compute service...

Question #2
...
```

## Data Files

- `quiz_config.json`: Application settings
- `quiz_stats.json`: Quiz history and statistics
- `quiz_cache_*.json`: Cached parsed questions (auto-generated)

## Keyboard Shortcuts

- Use mouse to navigate interface
- Click on question headers in review to expand/collapse

## Tips

1. **Cache**: Questions are cached after first load for faster subsequent loads
2. **Progress**: All quiz attempts are saved to statistics
3. **Review**: Use review features to focus on weak areas
4. **Exam Prep**: Take multiple practice quizzes before attempting exam mode
5. **Order**: Try different question orders to avoid memorizing positions

## Troubleshooting

**Questions not loading:**
- Ensure PDF follows expected format
- Check console for error messages
- Try clearing cache files

**Statistics not showing:**
- Complete at least one quiz
- Check that `quiz_stats.json` is writable

**Charts not displaying:**
- Ensure matplotlib is installed correctly
- Check that you have completed multiple quizzes

## Contributing

Contributions are welcome! Please ensure code follows the existing structure and includes appropriate documentation.

## License

[Your License Here]

## Support

For issues or questions, please open an issue on the repository.