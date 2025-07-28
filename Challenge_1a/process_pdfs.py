import fitz
import json
import os

INPUT_DIR = "sample_dataset/pdfs"
OUTPUT_DIR = "sample_dataset/outputs"
def extract_title_and_outline_from_pdf(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    all_lines = []  # (page, text, font_size, y_top)
    font_counter = {}

    for pno in range(len(doc)):
        page = doc.load_page(pno)
        blocks = page.get_text("dict")["blocks"]
        spans = []
        for b in blocks:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    txt = s["text"].strip()
                    if not txt:
                        continue
                    y_top = round(s["bbox"][1], 1)
                    x_left = round(s["bbox"][0], 1)
                    size = round(s["size"], 1)
                    spans.append((y_top, x_left, txt, size))
                    font_counter[size] = font_counter.get(size, 0) + 1

        spans.sort(key=lambda x: (x[0], x[1]))
        merged = []
        current_y = None
        cur_texts = []
        cur_sizes = []
        for y, x, t, s in spans:
            if current_y is None:
                current_y = y
                cur_texts = [t]
                cur_sizes = [s]
                continue
            if abs(y - current_y) < 2:
                cur_texts.append(t)
                cur_sizes.append(s)
            else:
                merged.append((" ".join(cur_texts).strip(), max(cur_sizes), current_y))
                current_y = y
                cur_texts = [t]
                cur_sizes = [s]
        if cur_texts:
            merged.append((" ".join(cur_texts).strip(), max(cur_sizes), current_y))

        for text, size, y in merged:
            all_lines.append((pno, text.strip(), size, y))

    if not all_lines:
        return {"title": "", "outline": []}

    # Get the top 3 most frequent font sizes (used for H1–H3)
    font_freq_sorted = sorted(font_counter.items(), key=lambda x: (-x[0], -x[1]))[:3]
    font_sizes = [size for size, _ in font_freq_sorted]
    level_map = {}
    if len(font_sizes) >= 1: level_map[font_sizes[0]] = "H1"
    if len(font_sizes) >= 2: level_map[font_sizes[1]] = "H2"
    if len(font_sizes) >= 3: level_map[font_sizes[2]] = "H3"

    # Improved title detection: longest H1 from page 0
    title = ""
    for pno, text, size, y in all_lines:
        if pno == 0 and level_map.get(size) == "H1":
            if len(text) > len(title):
                title = text.strip()

    outline = []
    seen = set()
    for pno, text, size, y in all_lines:
        if len(text) < 4 or len(text) > 150:
            continue
        if text == title:
            continue
        level = level_map.get(size)
        if not level:
            continue
        if text in seen:
            continue
        seen.add(text)
        outline.append({
            "level": level,
            "text": text.strip(),
            "page": pno
        })

    return {"title": title, "outline": outline}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for fname in os.listdir(INPUT_DIR):
        if fname.lower().endswith(".pdf"):
            in_path = os.path.join(INPUT_DIR, fname)
            result = extract_title_and_outline_from_pdf(in_path)
            out_name = os.path.splitext(fname)[0] + ".json"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)
            print(f"Processed {fname} -> {out_name}")

if __name__ == "__main__":
    main()
