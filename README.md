# Adobe India Hackathon 2025 – Connecting the Dots 🧠📄

Welcome to my submission for the **Adobe India Hackathon 2025** under the "Connecting the Dots" challenge. This repository contains solutions to both:

- 🧩 Challenge 1a: **PDF Processing & Outline Extraction**
- 🔍 Challenge 1b: **Multi-Collection PDF Analysis**

---

## 🚀 Challenge Overview

> In a world flooded with documents, what wins is not more content — it's context.

The goal is to transform static PDFs into intelligent companions that understand structure, highlight insights, and serve as responsive research tools.

---

## 🧠 Round-wise Breakdown

### ✅ Round 1 – Structure & Extraction
Build the foundation:
- Parse raw PDFs using PyMuPDF.
- Extract document `title` and heading hierarchy (H1, H2, H3 only).
- Output structured JSON outlines for downstream processing.

### ✅ Round 2 – Contextual Intelligence
Leverage insights:
- Analyze multiple PDFs as a collection.
- Match content to user-defined personas and tasks.
- Extract and rank relevant sections using TF-IDF and cosine similarity.
- Generate a unified JSON summary for each collection.

---

## 📂 Project Structure

```bash
Adobe-India-Hackathon25/
├── Challenge_1a/
│   ├── process_pdfs.py              # PDF heading extractor (H1–H3)
│   ├── sample_dataset/
│   │   ├── pdfs/                    # Input PDFs for 1a
│   │   └── outputs/                 # Extracted outlines (file01.json, ...)
├── Challenge_1b/
│   ├── process_collections.py       # Persona-aware multi-doc analysis
│   ├── Collection 1/
│   ├── Collection 2/
│   └── Collection 3/                # Each has PDFs, input.json, and output.json
