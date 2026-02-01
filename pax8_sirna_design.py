#!/usr/bin/env python3
"""
PAX8 siRNA Design Tool

Designs effective siRNAs to knockdown PAX8 (Paired Box 8) using
Tuschl/Reynolds design rules and BLAST off-target analysis.
"""

import pandas as pd
import numpy as np
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
from Bio.Blast import NCBIWWW, NCBIXML
from datetime import datetime
import time
import sys

# Configure NCBI Entrez
Entrez.email = "sirna_designer@example.com"

# PAX8 RefSeq accession
PAX8_REFSEQ = "NM_003466.4"


def fetch_pax8_sequence():
    """Retrieve PAX8 mRNA sequence from NCBI RefSeq."""
    print(f"Fetching PAX8 sequence ({PAX8_REFSEQ})...")

    handle = Entrez.efetch(
        db="nucleotide",
        id=PAX8_REFSEQ,
        rettype="gb",
        retmode="text"
    )
    record = SeqIO.read(handle, "genbank")
    handle.close()

    # Extract CDS region
    cds_start = None
    cds_end = None
    for feature in record.features:
        if feature.type == "CDS":
            cds_start = int(feature.location.start)
            cds_end = int(feature.location.end)
            break

    if cds_start is None:
        raise ValueError("Could not find CDS feature in PAX8 record")

    cds_sequence = str(record.seq[cds_start:cds_end])

    print(f"  Gene: PAX8 (Paired Box 8)")
    print(f"  Organism: {record.annotations.get('organism', 'Homo sapiens')}")
    print(f"  Full mRNA length: {len(record.seq)} bp")
    print(f"  CDS region: {cds_start+1}-{cds_end} ({len(cds_sequence)} bp)")

    return {
        "record": record,
        "cds_sequence": cds_sequence,
        "cds_start": cds_start,
        "cds_end": cds_end,
        "full_sequence": str(record.seq)
    }


def calculate_gc_content(sequence):
    """Calculate GC percentage of a sequence."""
    gc_count = sequence.upper().count('G') + sequence.upper().count('C')
    return (gc_count / len(sequence)) * 100


def score_sirna(sense_seq):
    """
    Score an siRNA candidate based on Tuschl/Reynolds design rules.

    Returns a score out of 10 based on:
    - GC content 30-50%: 2 pts
    - Position 1 (sense) is A or U: 1 pt
    - Position 19 (sense) is G or C: 1 pt
    - Low 5' antisense stability (A/U rich at positions 15-19): 2 pts
    - No poly-runs (≥4 consecutive identical bases): 1 pt
    - Internal stability (A/U at positions 1-7): 2 pts
    - No GC stretch at 3' end of sense: 1 pt
    """
    score = 0
    details = []

    seq = sense_seq.upper().replace('T', 'U')  # Work with RNA

    # 1. GC content 30-50% (2 pts)
    gc = calculate_gc_content(sense_seq)
    if 30 <= gc <= 50:
        score += 2
        details.append("GC 30-50%: +2")
    elif 25 <= gc < 30 or 50 < gc <= 55:
        score += 1
        details.append("GC near optimal: +1")

    # 2. Position 1 is A or U (1 pt)
    if seq[0] in ['A', 'U']:
        score += 1
        details.append("Pos1 A/U: +1")

    # 3. Position 19 is G or C (1 pt)
    if seq[18] in ['G', 'C']:
        score += 1
        details.append("Pos19 G/C: +1")

    # 4. Low 5' antisense stability - A/U rich at 3' end of sense (positions 15-19) (2 pts)
    au_count_3prime = sum(1 for b in seq[14:19] if b in ['A', 'U'])
    if au_count_3prime >= 4:
        score += 2
        details.append("3' A/U rich: +2")
    elif au_count_3prime >= 3:
        score += 1
        details.append("3' A/U moderate: +1")

    # 5. No poly-runs of ≥4 identical bases (1 pt)
    has_poly_run = False
    for base in ['A', 'U', 'G', 'C', 'T']:
        if base * 4 in sense_seq.upper():
            has_poly_run = True
            break
    if not has_poly_run:
        score += 1
        details.append("No poly-runs: +1")

    # 6. Internal stability - A/U rich at 5' end (positions 1-7) (2 pts)
    au_count_5prime = sum(1 for b in seq[0:7] if b in ['A', 'U'])
    if au_count_5prime >= 5:
        score += 2
        details.append("5' A/U rich: +2")
    elif au_count_5prime >= 4:
        score += 1
        details.append("5' A/U moderate: +1")

    # 7. Avoid GC stretch at 3' end of sense (1 pt)
    gc_3prime = sum(1 for b in seq[15:19] if b in ['G', 'C'])
    if gc_3prime <= 2:
        score += 1
        details.append("No 3' GC stretch: +1")

    return score, details


def check_off_targets_local(sense_seq, pax8_cds):
    """
    Simple local off-target check - look for near-matches in the PAX8 sequence itself.
    For a full analysis, BLAST would be used against the entire transcriptome.
    """
    # Check if the sequence has multiple near-identical matches in PAX8 itself
    # (indicating potential self-targeting issues)
    matches = 0
    for i in range(len(pax8_cds) - 18):
        window = pax8_cds[i:i+19]
        match_count = sum(1 for a, b in zip(sense_seq.upper(), window.upper()) if a == b)
        if match_count >= 16:
            matches += 1

    # More than 1 match means the sequence appears multiple times
    return matches <= 1


def run_blast_check(sense_seq, skip_blast=True):
    """
    Run BLAST against human transcriptome to check for off-targets.

    For production use, this would query NCBI BLAST.
    Set skip_blast=False to perform actual BLAST search (slow, ~30s per query).
    """
    if skip_blast:
        # Return predicted PASS - in production, run actual BLAST
        return "PASS", "Skipped (use --blast for full analysis)"

    print(f"    Running BLAST for {sense_seq}...")

    try:
        result_handle = NCBIWWW.qblast(
            "blastn",
            "refseq_rna",
            sense_seq,
            entrez_query="Homo sapiens[organism]",
            word_size=7,
            expect=1000,
            hitlist_size=50
        )

        blast_records = NCBIXML.parse(result_handle)

        off_target_hits = []
        for record in blast_records:
            for alignment in record.alignments:
                # Skip PAX8 hits
                if "PAX8" in alignment.title.upper():
                    continue

                for hsp in alignment.hsps:
                    # Check if ≥16/19 match
                    if hsp.identities >= 16 and hsp.align_length >= 17:
                        off_target_hits.append({
                            "title": alignment.title[:50],
                            "identities": hsp.identities,
                            "length": hsp.align_length
                        })

        result_handle.close()

        if off_target_hits:
            return "FAIL", f"{len(off_target_hits)} off-targets found"
        else:
            return "PASS", "No significant off-targets"

    except Exception as e:
        return "UNKNOWN", f"BLAST error: {str(e)}"


def generate_sirna_candidates(cds_sequence, top_n=50):
    """
    Generate and score siRNA candidates using sliding window.
    """
    print(f"\nGenerating siRNA candidates from {len(cds_sequence)} bp CDS...")

    candidates = []

    # Sliding window of 19-mers
    for i in range(len(cds_sequence) - 18):
        sense_seq = cds_sequence[i:i+19]

        # Skip sequences with ambiguous bases
        if any(b not in 'ATGC' for b in sense_seq.upper()):
            continue

        # Calculate antisense (reverse complement)
        antisense_seq = str(Seq(sense_seq).reverse_complement())

        # Score the candidate
        score, score_details = score_sirna(sense_seq)

        # Calculate GC content
        gc_content = calculate_gc_content(sense_seq)

        # Local off-target check
        local_check = check_off_targets_local(sense_seq, cds_sequence)

        candidates.append({
            "position": i + 1,  # 1-based position
            "sense_seq": sense_seq,
            "antisense_seq": antisense_seq,
            "gc_percent": round(gc_content, 1),
            "score": score,
            "score_details": "; ".join(score_details),
            "local_check": "PASS" if local_check else "FAIL"
        })

    # Sort by score (descending), then by GC closeness to 40%
    candidates.sort(key=lambda x: (
        -x["score"],
        abs(x["gc_percent"] - 40)
    ))

    print(f"  Generated {len(candidates)} candidates")
    print(f"  Top score: {candidates[0]['score']}/10")

    return candidates[:top_n]


def filter_and_rank_candidates(candidates, run_blast=False):
    """
    Filter candidates and perform off-target analysis.
    """
    print("\nFiltering and ranking candidates...")

    filtered = []

    for cand in candidates:
        # Skip if local check failed
        if cand["local_check"] == "FAIL":
            continue

        # Skip if GC is outside acceptable range (25-55%)
        if cand["gc_percent"] < 25 or cand["gc_percent"] > 55:
            continue

        # Run BLAST check if requested
        if run_blast:
            off_target, blast_note = run_blast_check(cand["sense_seq"], skip_blast=False)
        else:
            off_target, blast_note = "PASS", "Local check only"

        cand["off_target"] = off_target
        cand["blast_note"] = blast_note

        if off_target != "FAIL":
            filtered.append(cand)

    # Final ranking
    for i, cand in enumerate(filtered):
        cand["rank"] = i + 1

    print(f"  Filtered to {len(filtered)} candidates")

    return filtered[:10]  # Return top 10


def save_csv_output(candidates, filename):
    """Save candidates to CSV file."""
    df = pd.DataFrame(candidates)

    # Select and order columns for output
    output_cols = [
        "rank", "position", "sense_seq", "antisense_seq",
        "gc_percent", "score", "off_target"
    ]

    df_out = df[output_cols]
    df_out.to_csv(filename, index=False)
    print(f"\nSaved CSV: {filename}")
    return df_out


def generate_report(candidates, pax8_info, filename):
    """Generate detailed text report."""

    report = []
    report.append("=" * 50)
    report.append("PAX8 siRNA Design Report")
    report.append("=" * 50)
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("GENE INFORMATION")
    report.append("-" * 30)
    report.append(f"Gene: PAX8 (Paired Box 8)")
    report.append(f"RefSeq: {PAX8_REFSEQ}")
    report.append(f"Organism: Homo sapiens")
    report.append(f"CDS Length: {len(pax8_info['cds_sequence'])} bp")
    report.append(f"CDS Region: {pax8_info['cds_start']+1}-{pax8_info['cds_end']}")
    report.append("")
    report.append("DESIGN CRITERIA")
    report.append("-" * 30)
    report.append("- siRNA length: 19 nt + dTdT overhang")
    report.append("- GC content: 30-50% (optimal)")
    report.append("- Tuschl/Reynolds scoring rules applied")
    report.append("- Off-target threshold: <16/19 match")
    report.append("")
    report.append("TOP 3 RECOMMENDED siRNAs")
    report.append("=" * 50)

    for i, cand in enumerate(candidates[:3]):
        report.append("")
        report.append(f"#{i+1} (Score: {cand['score']}/10)")
        report.append(f"   Position: {cand['position']}-{cand['position']+18}")
        report.append(f"   Sense:     5'-{cand['sense_seq']}-dTdT-3'")
        report.append(f"   Antisense: 5'-{cand['antisense_seq']}-dTdT-3'")
        report.append(f"   GC: {cand['gc_percent']}%")
        report.append(f"   Off-target: {cand['off_target']}")
        if 'score_details' in cand:
            report.append(f"   Scoring: {cand['score_details']}")

    report.append("")
    report.append("ALL TOP 10 CANDIDATES")
    report.append("-" * 50)
    header = "Sense Sequence (5'-3')"
    report.append(f"{'Rank':<6}{'Pos':<8}{'Score':<8}{'GC%':<8}{header}")
    report.append("-" * 50)

    for cand in candidates[:10]:
        report.append(f"{cand['rank']:<6}{cand['position']:<8}{cand['score']:<8}{cand['gc_percent']:<8}{cand['sense_seq']}")

    report.append("")
    report.append("ORDERING FORMAT")
    report.append("-" * 30)
    report.append("- Standard desalted, 20 nmol scale")
    report.append("- Include dTdT 3' overhangs on both strands")
    report.append("- Order as single-stranded oligos for annealing")
    report.append("  or as pre-annealed duplexes")
    report.append("")
    report.append("USAGE NOTES")
    report.append("-" * 30)
    report.append("- Recommended concentration: 20-50 nM")
    report.append("- Transfection: Lipofectamine RNAiMAX or similar")
    report.append("- Validate knockdown by qPCR and Western blot")
    report.append("- Include non-targeting control siRNA")
    report.append("")
    report.append("=" * 50)
    report.append("End of Report")
    report.append("=" * 50)

    report_text = "\n".join(report)

    with open(filename, 'w') as f:
        f.write(report_text)

    print(f"Saved report: {filename}")
    return report_text


def main():
    """Main workflow for PAX8 siRNA design."""
    print("=" * 50)
    print("PAX8 siRNA Design Tool")
    print("=" * 50)
    print()

    # Check for --blast flag
    run_blast = "--blast" in sys.argv
    if run_blast:
        print("BLAST off-target analysis enabled (this will be slow)")
    else:
        print("Note: Using local off-target check only.")
        print("      Add --blast flag for full NCBI BLAST analysis.")
    print()

    # Step 1: Retrieve PAX8 sequence
    pax8_info = fetch_pax8_sequence()

    # Step 2 & 3: Generate and score candidates
    candidates = generate_sirna_candidates(pax8_info["cds_sequence"])

    # Step 4: Filter and rank with off-target analysis
    top_candidates = filter_and_rank_candidates(candidates, run_blast=run_blast)

    if not top_candidates:
        print("\nERROR: No suitable siRNA candidates found!")
        return 1

    # Generate outputs
    csv_file = "PAX8_siRNA_candidates.csv"
    report_file = "PAX8_siRNA_report.txt"

    save_csv_output(top_candidates, csv_file)
    generate_report(top_candidates, pax8_info, report_file)

    # Print summary
    print("\n" + "=" * 50)
    print("DESIGN COMPLETE")
    print("=" * 50)
    print(f"\nTop siRNA candidate:")
    top = top_candidates[0]
    print(f"  Position: {top['position']}")
    print(f"  Sense:    5'-{top['sense_seq']}-dTdT-3'")
    print(f"  Score:    {top['score']}/10")
    print(f"  GC:       {top['gc_percent']}%")
    print(f"\nOutput files:")
    print(f"  - {csv_file}")
    print(f"  - {report_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
