# Scientific Plan to Overcome HER2 ADC Resistance

## Executive Summary

HER2-targeted ADCs face resistance through two major mechanisms: (1) HER2 expression loss/downregulation and (2) structural alterations like p95-HER2 truncation. This scientific plan outlines strategies to address these challenges through next-generation ADC designs, combination approaches, and alternative targeting strategies.

---

## 1. Resistance Mechanisms Hierarchy

| Mechanism | Frequency | Severity | Addressable |
|-----------|-----------|----------|-------------|
| HER2 downregulation | 15-30% | High | Partially |
| p95-HER2 truncation | 20-30% | High | Requires new approach |
| MDR1 efflux (T-DM1) | 10-20% | Moderate | Yes (T-DXd) |
| Epitope mutations | <2% | Low | Yes (bispecifics) |

---

## 2. Strategy 1: Biparatopic/Bispecific ADCs

### Rationale
- Target multiple epitopes to reduce escape mutations
- Enhanced internalization through receptor clustering
- Zanidatamab demonstrates 70% internalization vs 25% for trastuzumab

### Implementation
```
Approach: Zanidatamab-based ADC (ZW49)
Targets: Domain II + Domain IV
Linker: Cleavable
Payload: Auristatin (MMAE derivative)
Status: Phase 1/2 clinical trials
```

### Expected Outcomes
- Overcome single-epitope resistance
- Higher payload delivery per receptor
- Efficacy in HER2-low tumors

---

## 3. Strategy 2: Bystander Effect Optimization

### Rationale
- T-DXd shows bystander killing of HER2-negative cells
- Addresses tumor heterogeneity
- Works even with reduced HER2 expression

### Implementation
```
Requirements:
- Membrane-permeable payload
- Cleavable linker (intracellular release)
- High DAR (>4)

Optimized Design:
- Payload: Topoisomerase I inhibitors (cell permeable)
- Linker: Enzyme-cleavable tetrapeptide
- DAR: 8 (like T-DXd)
```

### Clinical Evidence
- T-DXd approved for HER2-low breast cancer (IHC 1+ or 2+/ISH-)
- Demonstrates efficacy even with heterogeneous HER2 expression

---

## 4. Strategy 3: Combination Therapies

### 4.1 ADC + Immune Checkpoint Inhibitors

| Combination | Rationale | Clinical Stage |
|-------------|-----------|----------------|
| T-DXd + Pembrolizumab | Enhanced immune activation | Phase 3 |
| T-DM1 + Atezolizumab | ADCC synergy | Phase 2 |
| ADC + TIL therapy | Overcome immune suppression | Preclinical |

### 4.2 ADC + HER2 Degraders

| Approach | Mechanism | Status |
|----------|-----------|--------|
| ADC + HSP90 inhibitor | Destabilize HER2 | Phase 1 |
| ADC + PROTAC | Degrade intracellular HER2 | Preclinical |

### 4.3 ADC + HER3 Targeting

| Rationale | Approach |
|-----------|----------|
| HER2/HER3 dimerization drives resistance | Combine anti-HER2 ADC + anti-HER3 mAb |
| HER3 upregulation compensates for HER2 loss | Dual targeting strategy |

---

## 5. Strategy 4: Address p95-HER2

### Challenge
- p95-HER2 lacks extracellular domain
- No binding site for mAbs/ADCs
- Associated with aggressive disease

### Solutions

| Approach | Mechanism | Status |
|----------|-----------|--------|
| HER2 TKIs | Target intracellular kinase | Approved |
| T-cell engaging bispecifics | Target other TAAs | Preclinical |
| ADC cocktail | Combine with non-HER2 ADC | Concept |
| CAR-T therapy | Target intracellular epitopes | Phase 1 |

### Recommended Approach
For p95-HER2 positive tumors:
1. First-line: HER2 TKI (neratinib, tucatinib)
2. Alternative: Switch to non-HER2 ADC (TROP2, HER3)
3. Experimental: CAR-T or TCR-based approaches

---

## 6. Strategy 5: Novel Epitope Targeting

### Unexplored Epitopes

| Domain | Current Use | ADC Potential |
|--------|-------------|---------------|
| Domain I | Limited | Moderate (accessible) |
| Domain III | None | Under investigation |
| ECD/membrane junction | None | High (stable) |

### Next-Generation Antibody Discovery
1. Screen for novel Domain I/III binders
2. Prioritize epitopes with fast internalization
3. Validate against p95-HER2 negative tumors
4. Develop as biparatopic combinations

---

## 7. Strategy 6: Alternative Payload Strategies

### Overcome MDR1-Mediated Resistance

| Current Payload | MDR1 Substrate | Alternative |
|-----------------|----------------|-------------|
| DM1 (T-DM1) | Yes | DXd (T-DXd) - No |
| MMAE | Yes | MMAF (charged) |
| Calicheamicin | Partial | PBDs |

### Novel Payloads Under Development

| Payload Class | Example | Advantage |
|---------------|---------|-----------|
| Topoisomerase I | DXd, SN-38 | Not MDR1 substrate |
| PBD dimers | Talirine | DNA crosslinker |
| Bcl-xL inhibitors | ABBV-155 | Novel MOA |
| STING agonists | Novel | Immune activation |

---

## 8. Implementation Roadmap

### Phase 1: Immediate (0-12 months)
- [ ] Implement T-DXd as standard after T-DM1 failure
- [ ] Screen patients for p95-HER2 status
- [ ] Enroll in ZW49 (biparatopic ADC) trials
- [ ] Monitor HER2 expression longitudinally

### Phase 2: Near-term (1-3 years)
- [ ] Develop combination protocols (ADC + ICI)
- [ ] Validate novel epitope antibodies
- [ ] Clinical trials of biparatopic ADCs
- [ ] HER2-low treatment protocols

### Phase 3: Long-term (3-5 years)
- [ ] Next-gen ADCs with novel payloads
- [ ] Personalized ADC selection based on biomarkers
- [ ] CAR-T/TCR approaches for p95-HER2
- [ ] ADC combinations in first-line setting

---

## 9. Biomarker Strategy

### Predictive Biomarkers for ADC Response

| Biomarker | Method | Clinical Use |
|-----------|--------|--------------|
| HER2 IHC/FISH | Standard | Patient selection |
| HER2 mRNA | qPCR | Predict response |
| p95-HER2 | Specific IHC | Exclude from mAb/ADC |
| MDR1 expression | IHC | Predict T-DM1 resistance |
| ctDNA HER2 | Liquid biopsy | Monitor dynamics |

### Recommended Testing Protocol
1. Baseline: HER2 IHC/FISH, p95-HER2 status
2. Progression: Re-biopsy for HER2 status, MDR1
3. Longitudinal: ctDNA monitoring for HER2 amplification

---

## 10. Conclusions and Recommendations

### Key Takeaways
1. **HER2 loss is the major resistance mechanism** - not epitope mutations
2. **Biparatopic ADCs** offer the best solution for enhanced internalization
3. **T-DXd bystander effect** addresses tumor heterogeneity
4. **p95-HER2** requires alternative approaches (TKIs, non-HER2 targets)
5. **Combination therapies** are the future of ADC treatment

### Priority Actions
1. Adopt T-DXd for HER2-low patients
2. Implement longitudinal HER2 monitoring
3. Pursue biparatopic ADC clinical trials
4. Develop p95-HER2 screening protocols
5. Investigate ADC + immunotherapy combinations

---

## References

1. Modi S, et al. Trastuzumab deruxtecan in previously treated HER2-low advanced breast cancer. N Engl J Med. 2022.
2. Weisser NE, et al. Zanidatamab, a novel biparatopic HER2 antibody. Nat Commun. 2023.
3. Li BT, et al. Trastuzumab deruxtecan in HER2-mutant non-small-cell lung cancer. N Engl J Med. 2022.
4. Hunter FW, et al. Mechanisms of resistance to antibody-drug conjugates. Cancer Res. 2020.
5. Scaltriti M, et al. Expression of p95HER2, a truncated form of the HER2 receptor. JNCI. 2007.
