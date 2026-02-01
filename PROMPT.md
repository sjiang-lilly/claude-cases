# siRNA Design for PAX8 Gene Knockdown

## Summary
Design effective siRNAs to knockdown PAX8 (Paired Box 8), a transcription factor overexpressed in ovarian and thyroid cancers. The workflow retrieves the PAX8 mRNA sequence, applies established siRNA design rules (Tuschl/Reynolds criteria), scores candidates, and performs off-target analysis.

---

## Skills Used

| Skill | Purpose |
|-------|---------|
| `scientific-skills:biopython` | Sequence retrieval, manipulation, BLAST |
| `scientific-skills:gene-database` | Query NCBI Gene for PAX8 info |
| `scientific-skills:pandas` | Data manipulation and CSV output |

---

## Dependencies

```bash
# requirements.txt
biopython==1.83
pandas==2.2.0
numpy==1.26.3
```

**Installation:**
```bash
pip install biopython==1.83 pandas==2.2.0 numpy==1.26.3
```

---

## Workflow

### Step 1: Retrieve PAX8 Sequence
- Source: NCBI RefSeq (NM_003466.4)
- Extract: CDS region (1,359 bp)
- Gene: PAX8, Chromosome 2

### Step 2: siRNA Design Rules

| Rule | Criterion | Weight |
|------|-----------|--------|
| Length | 19 nt + dTdT overhang | Required |
| GC content | 30-50% | 2 pts |
| Position 1 (sense) | A or U | 1 pt |
| Position 19 (sense) | G or C | 1 pt |
| Low 5' antisense stability | A/U rich | 2 pts |
| No poly-runs | Avoid ≥4 G/C/A/T | 1 pt |
| No off-targets | BLAST <16/19 match | Required |

### Step 3: Candidate Generation
- Sliding window: 19-mer across CDS
- Score each by design rules (max 10 pts)
- Rank and select top 10

### Step 4: Off-target Check
- BLAST against human transcriptome
- Filter: reject if ≥16/19 match to non-PAX8

---

## Output

### File: `PAX8_siRNA_candidates.csv`

| Column | Description |
|--------|-------------|
| rank | Overall ranking (1-10) |
| position | Start position in mRNA |
| sense_seq | Sense strand 5'-3' |
| antisense_seq | Antisense strand 5'-3' |
| gc_percent | GC content (%) |
| score | Design score (0-10) |
| off_target | BLAST result (PASS/FAIL) |

### File: `PAX8_siRNA_report.txt`

```
=====================================
PAX8 siRNA Design Report
=====================================
Gene: PAX8 (Paired Box 8)
RefSeq: NM_003466.4
Organism: Homo sapiens

TOP 3 RECOMMENDED siRNAs:

#1 (Score: 9.5/10)
   Position: 456-474
   Sense:     5'-NNNNNNNNNNNNNNNNNN-dTdT-3'
   Antisense: 5'-NNNNNNNNNNNNNNNNNN-dTdT-3'
   GC: 42%
   Off-target: PASS

#2 (Score: 9.0/10)
   ...

ORDERING FORMAT:
- Standard desalted, 20 nmol scale
- Include dTdT 3' overhangs
=====================================
```

---

## Verification Checklist
- [ ] All siRNAs are 19 nt (+ dTdT overhang)
- [ ] GC content within 30-50%
- [ ] No off-target hits ≥16/19 match
- [ ] Targets within PAX8 CDS (not UTR)
- [ ] Output files generated successfully
