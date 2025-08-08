from pathlib import Path
import re

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\u00A0", " ", text)
    text = re.sub(r"\n+", " ", text)    
    return text.strip()

def chunk_text(text: str, max_words: int = 700, overlap: int = 120):
    text = clean_text(text)
    words = text.split()
    if not words:
        return []
    if len(words) <= max_words:
        return [text]
    step = max(1, max_words - overlap)
    chunks = []
    for i in range(0, len(words), step):
        ch = " ".join(words[i:i+max_words]).strip()
        if len(ch.split()) >= 50:
            chunks.append(ch)
    return chunks or [text]

def load_clean_chunks(art_dir: str, max_words: int, overlap: int):
    base_path = Path(__file__).parent / art_dir 

    records = []
    for p in base_path.iterdir():  
        if p.is_file() and p.suffix.lower() == ".txt":
            title = re.sub(r"[_-]+", " ", p.stem.strip("_- ")) or p.stem
            txt = p.read_text(encoding="utf-8", errors="ignore")
            txt = clean_text(txt)
            if not txt:
                continue
            chunks = chunk_text(txt, max_words=max_words, overlap=overlap)
            for j, ch in enumerate(chunks):
                records.append({
                    "title": title,
                    "chunk": ch,
                    "chunk_id": j
                })
    return records