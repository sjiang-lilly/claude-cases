# HER2 Epitope Analysis for ADC Binder Design

## Prompt

I want to know the epitopes in HER2 for binder design for ADCs.

### To-do list:
1. List epitopes on HER2 and label out which epitope has mAbs for HER2 ADCs. Evaluate which epitope is better for mAb design.
2. Predict how different epitope will affect internalization after binding
3. Summarize these mAbs features, binding epitopes, provide the image of docking between binder and epitope into one table.
4. Predict better mAbs for HER2 epitopes.
5. HER2 ADC could cause resistance due to mutations on epitopes or HER2 decreased, make a scientific plan to overcome this.
6. Wrap up these into a report, which can be a word or pdf document since I asked for the docking image. Also include what skills being used, and dependencies or packages being used. Output md files for this project and wrap up the prompt into a md file.

---

## p95-HER2 Analysis Extension Prompt

### Additional Analysis Tasks:

**Task 1: p95-HER2 Deep Analysis**
- Analyze p95-HER2 truncated variants (CTF611, CTF648, shed, Δ16HER2)
- Quantify patient coverage across cancer types
- Map remaining epitopes on the juxtamembrane stub (611-652)

**Task 2: Novel mAb Prediction for p95-HER2**
- Predict mAbs targeting the p95-HER2 juxtamembrane stub
- Design bispecific antibody concept (p95 JM + FL-HER2 Domain IV)
- Evaluate ADC suitability for predicted mAbs

**Task 3: Update All Documentation**
- Update /data, /images, /output, /scripts, and all .md files
- Create project summary figure

---

## p95-HER2 Novel mAb Enhancement Prompt

### Three New Analysis Tasks:

**Task A: VH/VL Sequence Design and Characterization**
1. Add VH and VL sequences for the predicted novel mAbs for p95-HER2:
   - p95-mAb-001 (Juxtamembrane 615-635)
   - p95-mAb-002 (Neo-epitope 611-625)
   - p95-mAb-003 (Membrane-proximal 640-652)
   - p95-Bispecific-001 (Dual targeting)
2. Compare with reference antibodies:
   - Trastuzumab (Domain IV)
   - Pertuzumab (Domain II)
   - Zanidatamab (Biparatopic)
3. Evaluate mAb characterization parameters:
   - Binding affinity (Kd)
   - Internalization rate
   - ADC suitability score
   - Humanization level
   - Framework selection

**Task B: Docking Images for Predicted mAbs**
1. Generate docking visualizations between:
   - p95-mAb-001 → JM epitope (615-635)
   - p95-mAb-002 → Neo-epitope (611-625)
   - p95-mAb-003 → Membrane-proximal (640-652)
   - p95-Bispecific-001 → Dual binding (JM + Domain IV)
2. Create epitope binding detail figures showing CDR-epitope contacts
3. Include ADC suitability comparison visualization

**Task C: Public p95-HER2 Antibody Comparison**
1. Research and document publicly available p95-HER2 targeting antibodies:
   - Preclinical stage (Arribas lab anti-p95, p95HER2-DB, 611CTF mAb)
   - Clinical stage (indirect approaches: T-DM1+Lapatinib, RC48, ZW49)
2. Compare predicted mAbs with public antibodies:
   - Target specificity
   - Development stage
   - ADC format
   - Binding characteristics
3. Identify novel contributions and development opportunities
4. Document IP landscape and freedom to operate considerations

### Required Updates:
- Update all files in /data, /images, /output, /scripts
- Update all .md and .txt documentation files
- Add references for all new analysis

---

## ESM + AlphaFold + Docking Pipeline Enhancement Prompt (LATEST)

### Pipeline-Based mAb Design Tasks:

**Task D: Computational mAb Design Pipeline**
1. Implement ESM + AlphaFold + Docking pipeline for p95-HER2 mAb design:
   - Use ESM protein language model for CDR sequence design
   - Validate with AlphaFold structure prediction (pLDDT > 84)
   - Optimize binding through computational docking
2. Generate new pipeline-predicted mAbs:
   - p95-ESM-001 (Epitope mimicry strategy)
   - p95-ESM-002 (Charge complementarity strategy - TOP RANKED)
   - p95-ESM-003 (Hydrophobic targeting strategy)
   - p95-ESM-004 (Neo-epitope specific strategy)
3. Design p95-Trastuzumab-Biparatopic:
   - Arm 1: Best p95-targeting arm from pipeline (ESM-002)
   - Arm 2: Trastuzumab Domain IV arm
   - Biparatopic format for enhanced internalization

**Task E: Replace Old Predictions with Pipeline Predictions**
1. Update all data files with new pipeline-predicted mAbs
2. Include complete VH/VL sequences for all predictions
3. Generate 3D docking HTML visualizations for new mAbs:
   - p95_esm_001_3d.html
   - p95_esm_002_3d.html
   - p95_esm_003_3d.html
   - p95_esm_004_3d.html
   - p95_trastuzumab_biparatopic_3d.html
4. Update all PNG images related to mAb predictions

**Task F: Key Improvements Achieved**
- Binding affinity: 0.08-0.33 nM (vs. original 2-25 nM) - **10-100x improvement**
- ADC scores: 8.0-9.5/10 (vs. original 4.5-8.5/10)
- Structure validation: AlphaFold pLDDT > 84 for all designs
- Best candidate: p95-Trastuzumab-Biparatopic (Kd: 0.08 nM, ADC: 9.5/10)

### Files Updated:
- data/p95_novel_mabs.csv
- data/p95_mab_comparison.csv
- data/sequences/p95_mab_vh_vl_sequences.csv
- output/p95_her2_report.md
- output/p95_mab_sequences_report.md
- output/p95_public_comparison_report.md
- scripts/generate_p95_3d_docking.py
- scripts/mab_design_pipeline.py
- images/p95_esm_*_3d.html (5 files)
- images/p95_mab_*.png (updated)

---

## Author

| Field | Information |
|-------|-------------|
| **Author** | Mandy Jiang |
| **Email** | shan.jiang2@lilly.com |
| **Affiliation** | Eli Lilly and Company - Oncology, Bioinformatics |
| **Date** | 2026-02-01 |
