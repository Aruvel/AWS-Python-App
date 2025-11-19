"""
Application Constants
"""

# Application Info
APP_TITLE = "🎯 AWS Quiz Pro"
APP_VERSION = "2.0.0"

# Window Settings
DEFAULT_GEOMETRY = "1200x800"
MIN_WIDTH = 1000
MIN_HEIGHT = 700

# File Settings
CONFIG_FILE = "quiz_config.json"
STATS_FILE = "quiz_stats.json"
CACHE_PREFIX = "quiz_cache_"

# Quiz Settings
EXAM_QUESTION_COUNT = 65
EXAM_PASSING_SCORE = 70
PRACTICE_PASSING_SCORE = 80

# File Extensions
PDF_EXTENSIONS = [("PDF files", "*.pdf"), ("All files", "*.*")]
CSV_EXTENSIONS = [("CSV files", "*.csv"), ("All files", "*.*")]

# Topics and Keywords
TOPIC_KEYWORDS = {
    "Security": ["security", "IAM", "encryption", "firewall", "VPC", "SSL", "TLS"],
    "Storage": ["S3", "EBS", "storage", "bucket", "volume", "snapshot"],
    "Compute": ["EC2", "Lambda", "compute", "instance", "server", "container"],
    "Database": ["RDS", "DynamoDB", "database", "SQL", "NoSQL"],
    "Networking": ["VPC", "subnet", "route", "gateway", "load balancer", "CDN"],
    "Monitoring": ["CloudWatch", "monitoring", "logs", "metrics", "alarms"],
    "Management": ["billing", "cost", "support", "compliance", "governance"]
}

# UI Labels
EMOJI = {
    "correct": "✅",
    "incorrect": "❌",
    "hint": "💡",
    "time": "⏰",
    "stats": "📊",
    "review": "📋",
    "settings": "⚙️",
    "trophy": "🏆",
    "check": "✓",
    "cross": "✗"
}