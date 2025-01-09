#!/usr/bin/env python3
"""
VCF Analysis Script
Parses and filters VCF file to extract variant information for reporting.
"""

import json
import pysam

def parse_vcf(vcf_path):
    """Parse VCF file and extract relevant variant information."""
    variants = []
    
    try:
        # Open VCF file using pysam
        vcf_in = pysam.VariantFile(vcf_path)
        
        # Process each record
        for record in vcf_in:
            # Extract quality and depth, defaulting to 0 if missing
            qual = record.qual if record.qual is not None else 0
            dp = record.info.get('DP', 0)
            
            # Filter low quality variants
            if qual < 30 or dp < 10:
                continue
            
            # Extract allele frequency, default to 0 if missing
            af = record.info.get('AF', [0])[0] if 'AF' in record.info else 0
            
            # Create variant dictionary with required fields
            variant = {
                'chrom': record.chrom,
                'pos': record.pos,
                'ref': record.ref,
                'alt': str(record.alts[0]) if record.alts else '',
                'af': af,
                'dp': dp,
                'qual': qual
            }
            variants.append(variant)
            
    except Exception as e:
        print(f"Error processing VCF file: {str(e)}")
        raise
    
    finally:
        # Ensure file is closed
        if 'vcf_in' in locals():
            vcf_in.close()
    
    return variants

def compute_statistics(variants):
    """Compute summary statistics from variants data."""
    # Initialize counters and collectors
    snps = 0
    indels = 0
    af_values = []
    dp_values = []
    chrom_counts = {}
    
    # Process each variant
    for v in variants:
        # Count SNPs vs indels
        if len(v['ref']) == 1 and len(v['alt']) == 1:
            snps += 1
        else:
            indels += 1
            
        # Collect values for distributions
        af_values.append(v['af'])
        dp_values.append(v['dp'])
        
        # Count variants per chromosome
        chrom = v['chrom']
        chrom_counts[chrom] = chrom_counts.get(chrom, 0) + 1
    
    # Calculate percentages
    total = len(variants)
    snp_percent = (snps / total * 100) if total > 0 else 0
    indel_percent = (indels / total * 100) if total > 0 else 0
    
    # Find most common chromosome
    most_common_chrom = max(chrom_counts.items(), key=lambda x: x[1])[0] if chrom_counts else None
    
    # Create histogram ranges for allele frequencies
    af_hist = {'0.0-0.1': 0, '0.1-0.2': 0, '0.2-0.3': 0, '0.3-0.4': 0,
               '0.4-0.5': 0, '0.5-0.6': 0, '0.6-0.7': 0, '0.7-0.8': 0,
               '0.8-0.9': 0, '0.9-1.0': 0}
    
    for af in af_values:
        if af <= 1.0:  # Ensure AF is valid
            bin_idx = min(int(af * 10), 9)  # Handle edge case of AF = 1.0
            bin_key = f"{bin_idx/10:.1f}-{(bin_idx+1)/10:.1f}"
            af_hist[bin_key] += 1
    
    return {
        'total_variants': total,
        'snp_count': snps,
        'indel_count': indels,
        'snp_percentage': snp_percent,
        'indel_percentage': indel_percent,
        'most_common_chromosome': most_common_chrom,
        'af_histogram': af_hist,
        'af_values': af_values,
        'dp_values': dp_values,
        'chromosome_counts': chrom_counts
    }

def main():
    """Main function to process VCF file and save results."""
    vcf_path = 'Tyler_Houchin_nucleus_dna_download_vcf_NU-JYOC-5394.vcf'
    
    try:
        print("Starting VCF analysis...")
        variants = parse_vcf(vcf_path)
        print(f"Successfully processed {len(variants)} variants")
        
        # Save first 1000 variants to JSON for table (for better performance)
        print("Saving limited variants data for table...")
        limited_variants = variants[:1000]  # Only save first 1000 variants
        with open('variants.json', 'w') as f:
            json.dump(limited_variants, f, indent=2)
        print(f"Saved {len(limited_variants)} variants to variants.json")
        
        # Compute and save statistics
        print("Computing summary statistics...")
        stats = compute_statistics(variants)
        
        # Save analysis results to JSON
        with open('analysis_results.json', 'w') as f:
            json.dump(stats, f, indent=2)
        print("Saved analysis results to analysis_results.json")
        
        # Print summary to console
        print("\nSummary Statistics:")
        print(f"Total Variants: {stats['total_variants']:,}")
        print(f"SNPs: {stats['snp_count']:,} ({stats['snp_percentage']:.1f}%)")
        print(f"Indels: {stats['indel_count']:,} ({stats['indel_percentage']:.1f}%)")
        print(f"Most Common Chromosome: {stats['most_common_chromosome']}")
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        raise

if __name__ == '__main__':
    main()
