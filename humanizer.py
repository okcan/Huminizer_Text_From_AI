import re
import random
import spacy
import nltk
import textstat
from nltk.corpus import wordnet

# İndirilmeyen NLTK veri setlerini indir
nltk.download('wordnet')
nltk.download('omw-1.4')

# spaCy modeli
nlp = spacy.load("en_core_web_sm")

# Regex tabanlı sadeleştirmeler
RE_RULES = {
    r"\butilize\b": "use",
    r"\bmoreover\b": "also",
    r"\bfurthermore\b": "also",
    r"\bin order to\b": "to",
    r"\bsubsequently\b": "then",
    r"\bthus\b": "so",
    r"\btherefore\b": "so",
    r"\badditionally\b": "also",
    r"\bprior to\b": "before",
    r"\bassist\b": "help",
    r"\bcommence\b": "start",
    r"\bterminate\b": "end",
    r"\bendeavor\b": "try",
    r"\bpertaining to\b": "about",
    r"\bnotwithstanding\b": "despite",
    r"\bfacilitate\b": "make easier",
    r"\bnecessitate\b": "require",
    r"\bwith regard to\b": "about",
    r"\bsubstantial\b": "significant",
    r"\boptimize\b": "improve",
    # AI-kalıpları
    r"It is important to note that": "",
    r"As per our analysis": "We think",
    r"It can be observed that": "",
    r"In conclusion": "So",
    r"This clearly shows that": "This shows",
}

def apply_regex(text: str) -> str:
    for patt, rep in RE_RULES.items():
        text = re.sub(patt, rep, text, flags=re.IGNORECASE)
    return text

def synonym_replace(token):
    """Basit: sadece sıfat, zarf, fiiller için eşanlamlı dene."""
    wn_pos = None
    if token.pos_ in ('ADJ','ADV','VERB','NOUN'):
        wn_pos = {'ADJ':'a','ADV':'r','VERB':'v','NOUN':'n'}[token.pos_]
    if not wn_pos:
        return token.text
    syns = wordnet.synsets(token.text, pos=wn_pos)
    if not syns:
        return token.text
    # Rastgele bir lemma seç
    lemmas = [l.name().replace('_',' ') for s in syns for l in s.lemmas() if l.name().lower()!=token.text.lower()]
    return random.choice(lemmas) if lemmas else token.text

def humanize_sentence(sent: str) -> str:
    # Regex’le sadeleştir
    sent = apply_regex(sent)
    # spaCy ile token’la, eşanlamlı değiştir
    doc = nlp(sent)
    new_tokens = []
    for tok in doc:
        # %25 ihtimalle eşanlamlı değiştir (fazla değil, az dokunuş için)
        if random.random() < 0.25:
            new_tokens.append(synonym_replace(tok))
        else:
            new_tokens.append(tok.text)
    # Tokenleri tekrar birleştir
    out = spacy.tokens.Doc(doc.vocab, words=new_tokens).text
    return out

def humanize_text(text: str) -> str:
    doc = nlp(text)
    sentences = [s.text.strip() for s in doc.sents]
    humanized = [humanize_sentence(s) for s in sentences]
    return " ".join(humanized)

def report_readability(original: str, transformed: str):
    o_score = textstat.flesch_reading_ease(original)
    t_score = textstat.flesch_reading_ease(transformed)
    print(f"\n🔍 Readability (Flesch) → Before: {o_score:.1f}, After: {t_score:.1f}\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Advanced AI→Human Text Converter")
    parser.add_argument("input", help="Input .txt file path")
    parser.add_argument("output", help="Output .txt file path")
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        ai_text = f.read()

    print("== Converting... ==")
    transformed = humanize_text(ai_text)
    report_readability(ai_text, transformed)

    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(transformed)

    print(f"✅ Done! Saved to {args.output}")

if __name__ == "__main__":
    main()
