# Challenge 1b: Multi-Collection PDF Analysis

## Overview
Each collection contains a real-world scenario, a user persona, and several PDFs. The system processes these documents to extract, rank, and refine the most relevant content sections for that scenario.

## Project Structure
```
Challenge_1b/
├── process_collections.py          # Main script to process all collections
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                       # South of France guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/                       # Acrobat tutorials
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
└── README.md
```

## ⚙️ How It Works

1. **Persona & Task Understanding**  
   Reads the `persona` and `job_to_be_done` fields from the input JSON to understand the user intent.

2. **Outline Extraction**  
   For each PDF, extracts top-level headings using Challenge 1a’s outline extractor (`H1`, `H2`, `H3` only). The outlines are cached under each collection’s `Outlines/` folder to avoid redundant computation.

3. **Ranking Logic**  
   Computes semantic similarity between the persona task and each heading using **TF-IDF vectorization** + **cosine similarity**. The top 5 most relevant headings are selected per document collection.

4. **Content Extraction**  
   Retrieves the **first meaningful paragraph** from the page containing each top-ranked heading using PyMuPDF.

5. **Structured Output**  
   Combines all results into a final `challenge1b_output.json`, including:
   - Metadata (persona, task, timestamp, input docs)
   - Top-ranked sections with page numbers
   - Refined textual snippets from those pages

### Input JSON Structure
```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [{"filename": "doc.pdf", "title": "Title"}],
  "persona": {"role": "User Persona"},
  "job_to_be_done": {"task": "Use case description"}
}
```

### Output JSON Structure
```json
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

## Key Features
- Persona-based content analysis
- Importance ranking of extracted sections
- Multi-collection document processing
- Structured JSON output with metadata

---

## 📦 Dependencies

To run the `process_collections.py` script, make sure the following Python packages are installed:

```bash
pip install PyMuPDF scikit-learn

