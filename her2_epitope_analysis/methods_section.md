# Methods

## Data Sources and Retrieval

HER2 (ERBB2) protein sequence was retrieved from UniProt (accession P04626). The full-length human HER2 precursor consists of 1,255 amino acids, including a 22-residue signal peptide. Crystal structures of HER2 extracellular domain in complex with therapeutic antibodies were obtained from the RCSB Protein Data Bank:

- **1N8Z**: HER2 ECD in complex with trastuzumab Fab (2.5 Å resolution)
- **1S78**: HER2 ECD in complex with pertuzumab Fab (2.6 Å resolution)
- **6OGE**: HER2 ECD in complex with both trastuzumab and pertuzumab Fabs (3.2 Å resolution)

Mutation data was compiled from the COSMIC database (Catalogue of Somatic Mutations in Cancer) and supplemented with data from ClinVar and published literature.

## Epitope Mapping and Domain Analysis

HER2 extracellular domain was divided into four subdomains based on crystallographic analysis:

- **Domain I** (residues 23-195): L1 domain involved in receptor dimerization
- **Domain II** (residues 196-319): Cysteine-rich domain containing the dimerization arm
- **Domain III** (residues 320-488): L2 domain with ligand-binding characteristics
- **Domain IV** (residues 489-630): Membrane-proximal cysteine-rich domain

Epitope regions were mapped using published structural data from antibody-HER2 complex crystallography. Key contact residues were identified using a distance cutoff of 4.5 Å between antibody and HER2 atoms.

## Antibody-Antigen Complex Analysis

Structural analysis of mAb-HER2 complexes was performed using the following approach:

1. PDB structures were parsed using BioPython's PDB module
2. Interface residues were identified based on solvent-accessible surface area changes
3. Binding epitopes were defined as HER2 residues with >1 Å² buried surface area
4. Structural visualizations were generated using py3Dmol for interactive 3D views

## Internalization Rate Prediction

Epitope-dependent internalization rates were predicted based on:

1. **Published experimental data**: Flow cytometry and confocal microscopy studies measuring antibody internalization kinetics
2. **Receptor clustering analysis**: Biparatopic antibodies induce clustering, enhancing internalization
3. **Recycling rate estimation**: Based on HER2 trafficking literature

ADC suitability scores (0-10 scale) were calculated using weighted criteria:
- Accessibility (25%)
- Internalization rate (30%)
- Clinical validation (25%)
- Structural stability (20%)

## Mutation Analysis

Somatic mutations in ERBB2 were retrieved from COSMIC database v98. Mutations were classified by:

1. **Domain location**: Extracellular (I-IV), transmembrane, or kinase domain
2. **Frequency**: Percentage across all cancer types in COSMIC
3. **Epitope impact**: Potential to affect antibody binding based on structural proximity
4. **Clinical significance**: Known association with drug resistance

## p95-HER2 Truncation Analysis

p95-HER2 variants were characterized based on published literature (Scaltriti et al., 2007; Arribas et al., 2011). The analysis included:

1. **Variant identification**: Four major variants characterized:
   - p95-CTF611: Alternative translation initiation at Met611
   - p95-CTF648: Alternative translation initiation at Met648
   - p95-shed: Proteolytic shedding by ADAM10/17
   - Δ16HER2: Alternative splicing (exon 16 skip)

2. **Patient coverage**: Frequency data compiled from 5 major studies across breast (30-50%), gastric (22%), and ovarian (18%) cancers

3. **Epitope mapping**: Remaining extracellular residues (611-652, ~42 aa juxtamembrane stub) were analyzed for antibody accessibility

## Novel mAb Prediction for p95-HER2

Predicted mAbs targeting p95-HER2 were designed based on:

1. **Epitope selection**: Three regions identified:
   - Juxtamembrane (615-635): Exposed loop region
   - Neo-epitope (611-625): Unique N-terminus of p95-CTF611
   - Membrane-proximal (640-652): Close to transmembrane domain

2. **Binding prediction**: Estimated Kd values based on epitope accessibility and structural features

3. **ADC suitability scoring**: Same weighted criteria as full-length HER2 analysis

## Bispecific Antibody Design

The p95-Bispecific-001 concept was designed to target both:
- p95-HER2 juxtamembrane region (residues 615-635)
- Full-length HER2 Domain IV (residues 557-603)

This approach enables targeting of heterogeneous tumors expressing both p95 and full-length HER2, with predicted enhanced internalization (60% at 4h) due to receptor clustering.

## Molecular Visualization

Protein structures were visualized using:

- **py3Dmol**: Interactive 3D visualization in HTML format
- **matplotlib**: Static publication-quality figures

Domain coloring scheme:
- Domain I: Red (#FF6B6B)
- Domain II: Teal (#4ECDC4)
- Domain III: Blue (#45B7D1)
- Domain IV: Green (#96CEB4)
- Antibody heavy chain: Plum (#DDA0DD)
- Antibody light chain: Khaki (#F0E68C)

## Computational Environment

Analysis was performed using:
- Python 3.x
- BioPython 1.83 (sequence and structure handling)
- pandas 2.2.0 (data manipulation)
- numpy 1.26.3 (numerical operations)
- py3Dmol 2.1.0 (molecular visualization)
- matplotlib 3.8.2 (plotting)
- python-docx 1.1.0 (report generation)

## Data Availability

All data, code, and analysis outputs are available at:
https://github.com/sjiang-lilly/claude-cases/her2_epitope_analysis

## References

1. Cho HS, Mason K, Ramyar KX, et al. Structure of the extracellular region of HER2 alone and in complex with the Herceptin Fab. Nature. 2003;421(6924):756-760.

2. Franklin MC, Carey KD, Vajdos FF, et al. Insights into ErbB signaling from the structure of the ErbB2-pertuzumab complex. Cancer Cell. 2004;5(4):317-328.

3. Tate JG, Bamford S, Jubb HC, et al. COSMIC: the Catalogue Of Somatic Mutations In Cancer. Nucleic Acids Res. 2019;47(D1):D941-D947.

4. Austin CD, De Mazière AM, Schwartzberg PL, et al. Endocytosis and sorting of ErbB2 and the site of action of cancer therapeutics trastuzumab and geldanamycin. Mol Biol Cell. 2004;15(12):5268-5282.

5. Lewis Phillips GD, Li G, Dugger DL, et al. Targeting HER2-positive breast cancer with trastuzumab-DM1, an antibody-cytotoxic drug conjugate. Cancer Res. 2008;68(22):9280-9290.

### p95-HER2 References

6. Scaltriti M, Rojo F, Ocaña A, et al. Expression of p95HER2, a truncated form of the HER2 receptor, and response to anti-HER2 therapies in breast cancer. J Natl Cancer Inst. 2007;99(8):628-638.

7. Arribas J, Baselga J, Pedersen K, Parra-Palau JL. p95HER2 and breast cancer. Cancer Res. 2011;71(5):1515-1519.

8. Sáez R, Molina MA, Ramsey EE, et al. p95HER-2 predicts worse outcome in patients with HER-2-positive breast cancer. Clin Cancer Res. 2006;12(2):424-431.

9. Pedersen K, Angelini PD, Laos S, et al. A naturally occurring HER2 carboxy-terminal fragment promotes mammary tumor growth and metastasis. Mol Cell Biol. 2009;29(12):3319-3331.

10. Parra-Palau JL, Morancho B, Peg V, et al. Effect of p95HER2/611CTF on the response to trastuzumab and chemotherapy. J Natl Cancer Inst. 2014;106(11):dju291.
