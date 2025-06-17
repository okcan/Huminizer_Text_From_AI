  # 🧠 AI-to-Human Text Converter

This tool transforms AI-generated or overly academic text into more natural, readable, and human-like language. It uses regex rules, synonym substitution, and readability improvements to “humanize” text intelligently.

---

## 🚀 Features

- ✂️ Simplifies complex academic or formal expressions (`utilize → use`)
- 🔄 Replaces some words with synonyms to add variation
- 📊 Reports Flesch Reading Ease scores before and after
- 🧠 Sentence-level processing with spaCy NLP
- 📁 CLI-based input/output for easy batch processing

---

## 📦 Requirements

- Python 3.7 or higher

### Required Python packages

You can install the required packages using:

```bash
pip install -r requirements.txt

Contents of requirements.txt:

```bash
spacy
nltk
textstat
Additionally, download the necessary datasets:

```bash
python -m nltk.downloader wordnet omw-1.4
python -m spacy download en_core_web_sm

⚙️ Installation
Clone the repository and set up the environment:

```bash
git clone https://github.com/your-username/ai-to-human-text.git
cd ai-to-human-text
pip install -r requirements.txt
python -m nltk.downloader wordnet omw-1.4
python -m spacy download en_core_web_sm

🛠️ Usage
Run the script from the command line:

```bash
python humanizer.py input.txt output.txt

## 🤝 Contributions Welcome
Pull requests are welcome!

You can contribute by:

Adding new regex patterns

Improving synonym replacement logic

Supporting multilingual input

Creating a web-based interface or editor plugin
