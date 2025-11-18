# services/pdf_parser.py
"""
Parallel PDF parser with caching (PyMuPDF)
"""

import fitz
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor
from core.models import Question
from pathlib import Path
import re


class PDFParser:

    def __init__(self, cache_dir="cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def _hash_file(self, path: str) -> str:
        md5 = hashlib.md5()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                md5.update(chunk)
        return md5.hexdigest()[:10]

    def load(self, path: str):
        cache_key = self._hash_file(path)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if cache_file.exists():
            with open(cache_file) as f:
                raw = json.load(f)
            return [Question(**q) for q in raw]

        questions = self._parse_pdf(path)

        with open(cache_file, "w") as f:
            json.dump([q.dict() for q in questions], f, indent=2)

        return questions

    def _parse_pdf(self, path: str):
        doc = fitz.open(path)
        with ThreadPoolExecutor(max_workers=4) as ex:
            pages = list(ex.map(lambda p: p.get_text(), doc))

        text = "\n".join(pages)
        doc.close()

        pattern = re.compile(
            r"Question #(\d+)\n(.*?)\n((?:[A-E]\..*?\n)+)Correct Answer: ([A-E]+)",
            re.DOTALL,
        )

        results = []
        for m in pattern.finditer(text):
            qid = int(m.group(1))
            body = m.group(2).strip()
            opts_block = m.group(3)
            ans_letters = m.group(4)

            opts = re.findall(r"[A-E]\. (.*?)(?=\n[A-E]\.|$)", opts_block, flags=re.DOTALL)
            correct_idx = {ord(c) - 65 for c in ans_letters}

            results.append(
                Question(
                    id=qid,
                    question=body,
                    options=[o.strip() for o in opts],
                    correct_answers=correct_idx,
                )
            )

        return results
