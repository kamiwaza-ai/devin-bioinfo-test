# Devin's Guide to VCF Analysis and Interactive Report Generation

This document outlines the steps Devin (our AI software engineer) will follow to analyze the provided VCF file and build an interactive report in a simple webpage format. The instructions are junior engineer-friendly and include repetitive patterns with small variations for practice.

## Overview
### Goal:
1. **Analyze the VCF file** for genetic variants of interest, focusing on essential fields like variant type, allele frequency, and read depth.
2. **Generate summary statistics** and provide a visual representation of the data.
3. **Create an interactive HTML-based report** to display the results.

### Input:
- VCF file: `Tyler_Houchin_nucleus_dna_download_vcf_NU-JYOC-5394.vcf.gz`  
  **Download URL:** [VCF File](https://drive.google.com/file/d/1pShDcHLHdktMZtwH5bVBw1ymO99YXq1m/view?usp=sharing)

### Output:
- A single HTML file with:
  - Summary statistics (e.g., number of variants, common filters applied, etc.).
  - Visualizations (e.g., histograms for allele frequency, variant types).
  - An interactive table of key variant data (sortable and filterable).

---

## Step 1: Preprocessing the VCF File
### Instructions:
1. **Download and decompress the file:**
   ```bash
   wget <VCF URL> -O Tyler_Houchin_nucleus_dna_download_vcf_NU-JYOC-5394.vcf.gz
   gunzip Tyler_Houchin_nucleus_dna_download_vcf_NU-JYOC-5394.vcf.gz
   ```
2. Use a library like `PyVCF` or `pysam` to parse the VCF file in Python.
3. Extract essential fields for each variant:
   - Chromosome (`CHROM`)
   - Position (`POS`)
   - Reference allele (`REF`)
   - Alternate allele(s) (`ALT`)
   - Allele Frequency (`AF`)
   - Read Depth (`DP`)
   - Quality (`QUAL`)

---

## Step 2: Analyze the Data
### Key Tasks:
1. **Filter the data:**
   - Remove low-quality variants (`QUAL < 30`).
   - Filter out variants with low read depth (`DP < 10`).

2. **Summarize the data:**
   - Total number of variants.
   - Breakdown by variant type (e.g., SNPs, indels).
   - Distribution of allele frequencies (create a histogram).
   - Distribution of read depths.

3. **Generate statistics:**
   - Percentage of variants passing filters.
   - Most common chromosomes with variants.
   - Average and median quality scores for variants.

---

## Step 3: Build the Interactive Report
### File Structure:
- `index.html` - Contains the HTML structure and JavaScript for interactivity.
- `styles.css` - Optional styling for the report.

### Content Requirements:
1. **Summary Section:**
   - Display key metrics like the total number of variants, percentage of high-quality variants, and a pie chart of variant types.

2. **Visualizations:**
   - **Histogram of Allele Frequencies:** Show the distribution of allele frequencies across all variants.
   - **Bar Chart of Variant Types:** Count of SNPs vs. indels.

3. **Interactive Table:**
   - Display a table of variants with the following columns:
     - Chromosome, Position, Reference, Alternate, Allele Frequency, Read Depth, Quality
   - Make the table sortable and filterable (use a JavaScript library like [DataTables](https://datatables.net/) if needed).

---

## Example of "What Good Looks Like"
### Example Output Metrics:
- **Total Variants:** 120,000
- **Filtered Variants:** 90,000
- **Most Common Chromosome:** Chr1
- **Variant Type Breakdown:**
  - SNPs: 80%
  - Indels: 20%
- **Allele Frequency Distribution:**
  - Histogram ranges: 0-0.1, 0.1-0.2, ..., 0.9-1.0

### Example Code for Key Steps
#### Parsing the VCF File:
```python
import vcf

# Open VCF file
vcf_reader = vcf.Reader(open('Tyler_Houchin_nucleus_dna_download_vcf_NU-JYOC-5394.vcf', 'r'))

# Extract key information
variants = []
for record in vcf_reader:
    variant = {
        "chrom": record.CHROM,
        "pos": record.POS,
        "ref": record.REF,
        "alt": str(record.ALT[0]),
        "af": record.INFO.get('AF', [0])[0],  # Use default 0 if AF is missing
        "dp": record.INFO.get('DP', 0),
        "qual": record.QUAL,
    }
    variants.append(variant)
```

#### Generating the Report:
```html
<!DOCTYPE html>
<html>
<head>
    <title>VCF Analysis Report</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>VCF Analysis Report</h1>
    <section id="summary">
        <h2>Summary Statistics</h2>
        <ul>
            <li>Total Variants: 120,000</li>
            <li>Filtered Variants: 90,000</li>
            <li>Most Common Chromosome: Chr1</li>
        </ul>
    </section>
    <section id="visualizations">
        <h2>Visualizations</h2>
        <div id="allele-frequency-histogram"></div>
        <div id="variant-type-chart"></div>
    </section>
    <section id="variant-table">
        <h2>Variant Table</h2>
        <table id="variants">
            <thead>
                <tr>
                    <th>Chromosome</th>
                    <th>Position</th>
                    <th>Reference</th>
                    <th>Alternate</th>
                    <th>Allele Frequency</th>
                    <th>Read Depth</th>
                    <th>Quality</th>
                </tr>
            </thead>
            <tbody>
                <!-- Rows inserted dynamically -->
            </tbody>
        </table>
    </section>
    <script src="scripts.js"></script>
</body>
</html>
```

---

## Notes for Devin
- Follow best practices for file parsing and handle potential errors (e.g., missing fields in the VCF).
- Use consistent formatting for output data.
- Comment your code liberally to make it easier for others to follow.

Once complete, the HTML report should provide a user-friendly summary and allow for exploration of the genetic data!


