# Plan: p95-HER2 Analysis and Novel mAb Prediction

## Background

p95-HER2 is a truncated form of HER2 lacking most or all of the extracellular domain (ECD). It results from:
1. Alternative translation initiation at Met611
2. Proteolytic shedding of the ECD by ADAM10/17
3. Alternative splicing

p95-HER2 retains the transmembrane and intracellular kinase domains but lacks the trastuzumab/pertuzumab binding sites.

---

## Plan Overview

| Step | Task | Estimated Time |
|------|------|----------------|
| 1 | p95-HER2 deep analysis | 5 min |
| 2 | Patient coverage research | 3 min |
| 3 | Identify remaining epitopes on p95-HER2 | 5 min |
| 4 | Predict novel mAbs for p95-HER2 | 5 min |
| 5 | Generate docking images | 5 min |
| 6 | Evaluate mAbs for ADC suitability | 3 min |
| 7 | Update report and documentation | 4 min |
| **Total** | | **~30 min** |

---

## Step 1: p95-HER2 Deep Analysis

### What to research:
- Molecular structure of p95-HER2 variants
- Cleavage sites and remaining residues
- Signaling differences vs full-length HER2
- Association with aggressive disease

### p95-HER2 Variants:
| Variant | Start Residue | Missing Domains | Retained |
|---------|---------------|-----------------|----------|
| p95-CTF611 | Met611 | Domain I-IV | Stub + TM + Kinase |
| p95-CTF648 | Met648 | Domain I-IV | TM + Kinase |
| p95-shed | ~650 | Domain I-IV (shed) | TM + Kinase |

---

## Step 2: Patient Coverage

### Data to collect:
- Frequency of p95-HER2 in HER2+ breast cancer
- Frequency by cancer type
- Co-occurrence with full-length HER2
- Prognostic significance

### Expected findings:
- 20-30% of HER2+ breast cancers express p95-HER2
- Associated with poor prognosis
- Often co-expressed with full-length HER2

---

## Step 3: Identify Remaining Epitopes

### p95-HER2 structure analysis:
- Residues 611-687: Juxtamembrane region (short stub)
- Residues 653-675: Transmembrane domain
- Residues 676-1255: Intracellular domain

### Potential epitope regions:
1. **Juxtamembrane stub (611-652)**: ~40 aa extracellular
2. **Membrane-proximal region**: Limited accessibility
3. **Neo-epitope at truncation site**: Exposed new terminus

---

## Step 4: Predict Novel mAbs

### Strategy:
Design mAbs targeting the remaining extracellular stub of p95-HER2:
- Target: Residues 611-652 (juxtamembrane region)
- Neo-epitope: Exposed Met611 N-terminus

### Predicted mAbs:
| mAb ID | Target | Epitope | Rationale |
|--------|--------|---------|-----------|
| p95-mAb-1 | Juxtamembrane | 615-635 | Exposed loop |
| p95-mAb-2 | Neo-epitope | 611-625 | New N-terminus |
| p95-mAb-3 | Membrane-proximal | 640-652 | Near TM |

---

## Step 5: Docking Images

### Generate:
1. p95-HER2 structure model (homology from full-length)
2. Predicted mAb binding sites
3. Comparison with full-length HER2

---

## Step 6: ADC Suitability Evaluation

### Criteria:
| Feature | Assessment |
|---------|------------|
| Epitope accessibility | Limited (short stub) |
| Internalization | Unknown (may differ from full-length) |
| Expression level | Often co-expressed with FL-HER2 |
| Stability | Membrane-associated |

### Challenges:
- Very short extracellular region (~40 aa)
- May require bispecific approach (p95 + FL-HER2)
- Limited clinical validation

---

## Step 7: Update Documentation

### Files to create/update:
1. `data/p95_her2_analysis.csv` - p95 variant data
2. `data/p95_novel_mabs.csv` - Predicted mAbs
3. `images/p95_her2_structure.png` - Structure diagram
4. `images/p95_mab_docking.png` - Docking visualization
5. `output/p95_her2_report.md` - Detailed report
6. Update main report with p95 section

---

## Output Files (New)

| File | Description |
|------|-------------|
| `data/p95_her2_analysis.csv` | p95-HER2 variants and frequencies |
| `data/p95_novel_mabs.csv` | Predicted mAbs with features |
| `data/p95_patient_coverage.csv` | Patient frequency data |
| `images/p95_her2_structure.png` | p95 structure schematic |
| `images/p95_mab_docking.png` | Predicted mAb binding |
| `output/p95_her2_report.md` | Comprehensive p95 analysis |

---

## Key Questions to Address

1. What epitopes remain accessible on p95-HER2?
2. Can existing mAbs be modified to target p95?
3. What is the patient coverage for p95-targeting therapy?
4. How does p95-HER2 internalization differ from full-length?
5. Are bispecific (FL + p95) approaches more promising?

---

Proceed with this plan?
