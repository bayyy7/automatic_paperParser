
# Research Paper (PDF) Parser into JSON File

This repository provides a simple implementation of how to parse academic papers (in PDF format) into XML format using GROBID and then convert these XML files into JSON format. This tool is useful for extracting structured information from research papers for data analysis or machine learning purposes.

## Features

- Converts PDF files of academic papers into XML format using GROBID.
- Parses XML files into structured JSON format.
- Extracts metadata such as title, authors, abstract, body content, and references.

## Prerequisites

- **Python**: Ensure you are using Python version 3.6 or above.
- **GROBID**: You will need access to the GROBID service for XML conversion. This can be done using their cloud server or by setting up a local instance.

## Step-by-Step Guide

### 1. Clone this Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/bayyy7/automatic_paperParser.git
```

### 2. Set Up Your Python Environment

Ensure you have Python installed (version 3.6 or higher). It's recommended to use a virtual environment to manage dependencies.

### 3. Access GROBID Service

To convert PDF files into XML, you need to use the GROBID service:

- **Cloud Option**: Open the [GROBID cloud server](https://kermitt2-grobid-crf.hf.space/).
- **Local Option**: Alternatively, you can set up GROBID locally by following the instructions in the [GROBID repository](https://github.com/kermitt2/grobid).

### 4. Convert PDF to XML with GROBID

Once you have access to GROBID:

1. Navigate to the GROBID homepage.
2. Select **TEI** from the navigation bar.
3. Choose **Process Fulltext Document** in the "Service to call" section.
4. Check the **Consolidate Header** option to improve metadata extraction.
5. Upload your PDF file and click **Submit**.

### 5. Download and Save the XML Result

After processing, download the resulting TEI XML file and place it in the `Dataset` folder of this repository. If you have multiple PDFs, repeat steps 4 and 5 for each file.

### 6. Run the Parser

With the XML files in place, run the `parser.py` script to convert the XML files into JSON format:

```bash
python parser.py
```

### 7. Check the JSON Output

The parsed JSON files will be saved in the `JSON_Parsed` folder. Each JSON file will have a structure similar to the original XML file but formatted for easy data manipulation.

## JSON Structure

The output JSON files follow a structure similar to the XML file, with specific sections:

- **teiHeader**: Contains the title, publication date, and authors of the paper.
- **profileDesc**: Contains the abstract of the paper.
- **body**: Includes all sections of the paper, from the introduction to the conclusion.
- **back**: Contains all references cited in the paper.

## Notes

- The results of the JSON parse may occasionally be incorrect or contain blank spaces due to variations in the paper's formatting by different authors or journals. You may need to modify the `parser.py` script to suit your specific requirements.

## Accessing Research Papers

For additional papers to process, you can find academic articles on these platforms:
- [Open Review](https://openreview.net)
- [ArXiv](https://arxiv.org)

## Created By

You can check all my great stuff and works in my repository. <br><br>
**Rizky Indrabayu**
