"""
PDF Parsing Functionality
"""

import re
import json
import os
import hashlib
import fitz  # PyMuPDF
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
from config.constants import TOPIC_KEYWORDS


class PDFParser:
    """Handles PDF parsing and caching"""
    
    def __init__(self, cache_prefix: str = "quiz_cache_"):
        self.cache_prefix = cache_prefix
    
    def parse_pdf(self, pdf_filename: str) -> List[Dict]:
        """Parse PDF file and extract questions"""
        # Try cache first
        cache_key = self._get_file_hash(pdf_filename)
        cache_file = f"{self.cache_prefix}{cache_key}.json"
        
        cached_questions = self._load_from_cache(cache_file)
        if cached_questions:
            return cached_questions
        
        # Parse PDF if not cached
        questions = self._extract_questions_from_pdf(pdf_filename)
        
        # Cache the results
        self._save_to_cache(cache_file, questions)
        
        return questions
    
    def _extract_questions_from_pdf(self, pdf_filename: str) -> List[Dict]:
        """Extract questions from PDF file"""
        questions = []
        
        try:
            doc = fitz.open(pdf_filename)
            
            # Extract text from all pages in parallel
            with ThreadPoolExecutor(max_workers=4) as executor:
                page_texts = list(executor.map(lambda page: page.get_text(), doc))
            
            doc.close()
            full_text = "\n".join(page_texts)
            
            # Enhanced regex pattern
            pattern = re.compile(
                r"Question #(\d+)\n(.*?)\n((?:[A-E]\. .*?\n)+)(?:Most Voted\n)?Correct Answer: ([A-E]+)(?:\nExplanation:\s*(.*?)(?=\n\n|\nQuestion #|\Z))?",
                re.DOTALL
            )
            
            for match in pattern.finditer(full_text):
                question_num = int(match.group(1))
                question_text = match.group(2).strip()
                options_block = match.group(3)
                correct_letters = match.group(4).strip()
                explanation = match.group(5).strip() if match.group(5) else ""
                
                # Parse options
                options = self._parse_options(options_block)
                
                # Parse correct answers
                correct_indices = [ord(letter) - ord('A') for letter in correct_letters 
                                 if ord('A') <= ord(letter) <= ord('E')]
                
                # Categorize question
                topic = self._detect_topic(question_text)
                difficulty = self._detect_difficulty(question_text, len(options))
                
                questions.append({
                    "id": question_num,
                    "question": question_text,
                    "options": options,
                    "correct_answers": correct_indices,
                    "explanation": explanation,
                    "topic": topic,
                    "difficulty": difficulty,
                    "times_answered": 0,
                    "times_correct": 0
                })
        
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return []
        
        return questions
    
    def _parse_options(self, options_block: str) -> List[str]:
        """Parse answer options from text block"""
        option_pattern = re.compile(r"([A-E])\. (.*?)(?=\n[A-E]\. |\n*$)", re.DOTALL)
        options = []
        
        for letter, text in option_pattern.findall(options_block):
            clean_text = text.replace("Most Voted", "").strip()
            options.append(clean_text)
        
        return options
    
    def _detect_topic(self, question_text: str) -> str:
        """Detect question topic based on keywords"""
        question_lower = question_text.lower()
        
        for topic, keywords in TOPIC_KEYWORDS.items():
            if any(word.lower() in question_lower for word in keywords):
                return topic
        
        return "General"
    
    def _detect_difficulty(self, question_text: str, num_options: int) -> str:
        """Detect question difficulty"""
        if len(question_text) > 200 or "EXCEPT" in question_text or "NOT" in question_text:
            return "Hard"
        elif len(question_text) > 100 or num_options > 4:
            return "Medium"
        else:
            return "Easy"
    
    def _get_file_hash(self, filename: str) -> str:
        """Get MD5 hash of file for caching"""
        hash_md5 = hashlib.md5()
        try:
            with open(filename, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()[:8]
        except:
            return "default"
    
    def _load_from_cache(self, cache_file: str) -> List[Dict]:
        """Load questions from cache"""
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                if cached_data.get('version') == '2.0':
                    return cached_data['questions']
        except:
            pass
        
        return None
    
    def _save_to_cache(self, cache_file: str, questions: List[Dict]) -> None:
        """Save questions to cache"""
        try:
            from datetime import datetime
            cache_data = {
                'version': '2.0',
                'timestamp': datetime.now().isoformat(),
                'questions': questions
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")