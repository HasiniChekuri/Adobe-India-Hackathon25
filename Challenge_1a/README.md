# 📘 Challenge 1A - PDF Outline Extraction

This module is part of the *Adobe India Hackathon 2025 - "Connecting the Dots" Challenge*, submitted by Team Code Warriors.  
The goal is to extract meaningful structure from PDFs — *titles* and *headings (H1, H2, H3)* — using efficient and rule-based logic.  

---

## 🎯 Objective

Transform unstructured PDF documents into structured outlines with hierarchical headings and titles using a lightweight, offline Python solution.

---

### Build Command
```bash
docker build --platform linux/amd64 -t <reponame.someidentifier> .
```

### Run Command
```bash
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/repoidentifier/:/app/output --network none <reponame.someidentifier>
```

## Solution Structure
```
Challenge_1a/
├── sample_dataset/
│   ├── outputs/         # JSON files provided as outputs.
│   ├── pdfs/            # Input PDF files
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Sample processing script
└── README.md           # This file
```


### Sample Docker Configuration
```dockerfile
FROM --platform=linux/amd64 python:3.10
WORKDIR /app
COPY process_pdfs.py .
CMD ["python", "process_pdfs.py"]
```

### Performance Considerations
- **Memory Management**: Efficient handling of large PDFs
- **Processing Speed**: Optimize for sub-10-second execution
- **Resource Usage**: Stay within 16GB RAM constraint
- **CPU Utilization**: Efficient use of 8 CPU cores


### Validation Checklist
- ✅ All PDFs in input directory are processed
- ✅ JSON output files are generated for each PDF
- ✅ Output format matches required structure
- ✅ **Output conforms to schema** in `sample_dataset/schema/output_schema.json`
- ✅ Processing completes within 10 seconds for 50-page PDFs
- ✅ Solution works without internet access
- ✅ Memory usage stays within 16GB limit
- ✅ Compatible with AMD64 architecture

---

### Local Testing
```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-processor .

# Test with sample data
docker run --rm -v $(pwd)/sample_dataset/pdfs:/app/input:ro -v $(pwd)/sample_dataset/outputs:/app/output --network none pdf-processor
```
