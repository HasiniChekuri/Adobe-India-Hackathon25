import os
import sys
import json
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF
from datetime import UTC

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import
from Challenge_1a.process_pdfs import extract_title_and_outline_from_pdf

TOP_N = 5
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_outline_from_cache_or_extract(json_dir, pdf_path):
    os.makedirs(json_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    json_path = os.path.join(json_dir, f"{base}.json")

    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f).get("outline", [])
    else:
        result = extract_title_and_outline_from_pdf(pdf_path)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return result.get("outline", [])

def extract_refined_text(pdf_path, page_no):
    doc = fitz.open(pdf_path)
    if page_no < 0 or page_no >= len(doc):
        return ""
    page = doc[page_no]
    text = page.get_text("text")
    for para in text.split("\n\n"):
        para = para.strip()
        if para:
            return para
    return text.strip()

def rank_headings_by_persona(headings, persona_text):
    if not headings:
        return []
    texts = [h["text"] for h in headings]
    corpus = [persona_text] + texts
    tfidf = TfidfVectorizer(stop_words="english").fit_transform(corpus)
    scores = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
    ranked = sorted(zip(headings, scores), key=lambda x: x[1], reverse=True)
    return ranked[:TOP_N]

def process_collection(collection_path):
    input_json = os.path.join(collection_path, "challenge1b_input.json")
    output_json = os.path.join(collection_path, "challenge1b_output.json")
    pdf_dir = os.path.join(collection_path, "PDFs")
    json_outline_dir = os.path.join(collection_path, "Outlines")

    if not os.path.exists(input_json):
        print(f"❌ Missing: {input_json}")
        return

    with open(input_json, "r", encoding="utf-8") as f:
        config = json.load(f)

    persona_text = f"{config['persona']['role']} {config['job_to_be_done']['task']}"
    extracted_sections = []
    subsection_analysis = []

    for doc in config["documents"]:
        filename = doc["filename"]
        pdf_path = os.path.join(pdf_dir, filename)
        if not os.path.exists(pdf_path):
            print(f"⚠️ PDF missing: {filename}")
            continue

        headings = get_outline_from_cache_or_extract(json_outline_dir, pdf_path)
        ranked = rank_headings_by_persona(headings, persona_text)

        for rank, (heading, _) in enumerate(ranked, start=1):
            page = heading["page"]
            section = {
                "document": filename,
                "section_title": heading["text"],
                "importance_rank": rank,
                "page_number": page
            }
            refined = {
                "document": filename,
                "refined_text": extract_refined_text(pdf_path, page),
                "page_number": page
            }
            extracted_sections.append(section)
            subsection_analysis.append(refined)

    output_data = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in config["documents"]],
            "persona": config["persona"]["role"],
            "job_to_be_done": config["job_to_be_done"]["task"],
            "processing_timestamp": datetime.datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Processed: {os.path.basename(collection_path)}")

def main():
    for folder in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, folder)
        if os.path.isdir(full_path) and folder.lower().startswith("collection"):
            process_collection(full_path)

if __name__ == "__main__":
    main()
