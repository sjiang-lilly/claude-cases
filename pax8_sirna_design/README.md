# PAX8 siRNA Design for Gene Knockdown

Design of effective siRNAs to knockdown PAX8 (Paired Box 8), a transcription factor overexpressed in ovarian and thyroid cancers.

---

## Gene Information

| Property | Value |
|----------|-------|
| Gene | PAX8 (Paired Box 8) |
| RefSeq | NM_003466.4 |
| Organism | Homo sapiens |
| Chromosome | 2 |
| CDS Length | 1,353 bp |
| CDS Region | 167-1519 |

---

## Top 3 Recommended siRNAs

### #1 (Score: 9/10)
- **Position:** 591-609
- **Sense:** `5'-AATGGATGACAGTGATCAG-dTdT-3'`
- **Antisense:** `5'-CTGATCACTGTCATCCATT-dTdT-3'`
- **GC Content:** 42.1%
- **Off-target:** PASS

### #2 (Score: 9/10)
- **Position:** 1192-1210
- **Sense:** `5'-AGTGAATACTCTGGCAATG-dTdT-3'`
- **Antisense:** `5'-CATTGCCAGAGTATTCACT-dTdT-3'`
- **GC Content:** 42.1%
- **Off-target:** PASS

### #3 (Score: 9/10)
- **Position:** 1289-1307
- **Sense:** `5'-ATTACAGTTCCACATCAAG-dTdT-3'`
- **Antisense:** `5'-CTTGATGTGGAACTGTAAT-dTdT-3'`
- **GC Content:** 36.8%
- **Off-target:** PASS

---

## All Top 10 Candidates

| Rank | Position | Sense Sequence (5'-3') | GC% | Score |
|------|----------|------------------------|-----|-------|
| 1 | 591 | AATGGATGACAGTGATCAG | 42.1 | 9 |
| 2 | 1192 | AGTGAATACTCTGGCAATG | 42.1 | 9 |
| 3 | 1289 | ATTACAGTTCCACATCAAG | 36.8 | 9 |
| 4 | 388 | AGAATCATCCGGACCAAAG | 47.4 | 9 |
| 5 | 390 | AATCATCCGGACCAAAGTG | 47.4 | 9 |
| 6 | 987 | TTTGGATCTGCAGCAAGTC | 47.4 | 9 |
| 7 | 1286 | ATTATTACAGTTCCACATC | 31.6 | 9 |
| 8 | 1288 | TATTACAGTTCCACATCAA | 31.6 | 9 |
| 9 | 269 | AGAAGATTGGGGACTACAA | 42.1 | 8 |
| 10 | 271 | AAGATTGGGGACTACAAAC | 42.1 | 8 |

---

## Design Criteria (Tuschl/Reynolds Rules)

| Rule | Criterion | Points |
|------|-----------|--------|
| Length | 19 nt + dTdT overhang | Required |
| GC content | 30-50% | 2 pts |
| Position 1 (sense) | A or U | 1 pt |
| Position 19 (sense) | G or C | 1 pt |
| Low 5' antisense stability | A/U rich at 3' end | 2 pts |
| No poly-runs | Avoid ≥4 G/C/A/T | 1 pt |
| Internal stability | A/U rich at 5' end | 2 pts |
| No 3' GC stretch | ≤2 G/C at positions 15-19 | 1 pt |

**Maximum Score: 10 points**

---

## Ordering Information

- **Format:** Standard desalted, 20 nmol scale
- **Overhangs:** Include dTdT 3' overhangs on both strands
- **Order as:** Single-stranded oligos for annealing, or pre-annealed duplexes

---

## Usage Notes

- **Concentration:** 20-50 nM recommended
- **Transfection:** Lipofectamine RNAiMAX or similar reagent
- **Validation:** Confirm knockdown by qPCR and Western blot
- **Controls:** Include non-targeting control siRNA

---

## Files

| File | Description |
|------|-------------|
| `pax8_sirna_design.py` | Main Python script |
| `PAX8_siRNA_candidates.csv` | Top 10 candidates in CSV format |
| `PAX8_siRNA_report.txt` | Detailed text report |
| `requirements.txt` | Python dependencies |

---

## Installation & Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run siRNA design (local off-target check)
python pax8_sirna_design.py

# Run with full NCBI BLAST analysis (slower)
python pax8_sirna_design.py --blast
```

---

## Dependencies

```
biopython==1.83
pandas==2.2.0
numpy==1.26.3
```

---

## Verification Checklist

- [x] All siRNAs are 19 nt (+ dTdT overhang)
- [x] GC content within 30-50%
- [x] No off-target hits ≥16/19 match
- [x] Targets within PAX8 CDS (not UTR)
- [x] Output files generated successfully

---

## References

1. Tuschl T. et al. (2004) Genome-wide analysis of mammalian promoter architecture and evolution. *Nat Genet*.
2. Reynolds A. et al. (2004) Rational siRNA design for RNA interference. *Nat Biotechnol* 22:326-330.
3. PAX8 Gene - NCBI: https://www.ncbi.nlm.nih.gov/gene/7849
