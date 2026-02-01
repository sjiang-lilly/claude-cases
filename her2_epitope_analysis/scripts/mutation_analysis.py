#!/usr/bin/env python3
"""
HER2 Mutation and Resistance Analysis

Analyzes mutations that affect ADC efficacy and cause resistance.
"""

import pandas as pd

# ============================================================================
# HER2 MUTATIONS AFFECTING ADC EFFICACY
# ============================================================================

HER2_MUTATIONS = [
    # Epitope mutations (Domain IV - Trastuzumab binding site)
    {
        "mutation": "S310F",
        "domain": "Domain II",
        "residue_position": 310,
        "frequency_percent": 0.8,
        "cancer_types": "Breast, Gastric, Bladder",
        "affects_epitope": "Pertuzumab (reduced)",
        "resistance_mechanism": "Reduced pertuzumab binding, altered dimerization",
        "adc_impact": "Minimal (does not affect T-DM1/T-DXd)",
        "clinical_significance": "May reduce pertuzumab efficacy"
    },
    {
        "mutation": "L755S",
        "domain": "Kinase domain",
        "residue_position": 755,
        "frequency_percent": 2.1,
        "cancer_types": "Breast, NSCLC",
        "affects_epitope": "No (intracellular)",
        "resistance_mechanism": "Lapatinib/neratinib resistance, HER2 activation",
        "adc_impact": "None (ADC binding unaffected)",
        "clinical_significance": "TKI resistance, ADC remains effective"
    },
    {
        "mutation": "V777L",
        "domain": "Kinase domain",
        "residue_position": 777,
        "frequency_percent": 1.5,
        "cancer_types": "Breast, Colorectal",
        "affects_epitope": "No (intracellular)",
        "resistance_mechanism": "Increased kinase activity",
        "adc_impact": "None (ADC binding unaffected)",
        "clinical_significance": "Activating mutation, ADC effective"
    },
    {
        "mutation": "T798M",
        "domain": "Kinase domain",
        "residue_position": 798,
        "frequency_percent": 0.5,
        "cancer_types": "Breast (acquired)",
        "affects_epitope": "No (intracellular)",
        "resistance_mechanism": "Gatekeeper mutation, TKI resistance",
        "adc_impact": "None (ADC binding unaffected)",
        "clinical_significance": "TKI resistance, ADC alternative"
    },
    {
        "mutation": "D769H/Y",
        "domain": "Kinase domain",
        "residue_position": 769,
        "frequency_percent": 1.2,
        "cancer_types": "Breast, NSCLC",
        "affects_epitope": "No (intracellular)",
        "resistance_mechanism": "Altered kinase activity",
        "adc_impact": "None (ADC binding unaffected)",
        "clinical_significance": "May affect TKI sensitivity"
    },
    {
        "mutation": "R678Q",
        "domain": "Juxtamembrane",
        "residue_position": 678,
        "frequency_percent": 0.3,
        "cancer_types": "Breast",
        "affects_epitope": "Potentially (near Domain IV)",
        "resistance_mechanism": "Unknown mechanism",
        "adc_impact": "Under investigation",
        "clinical_significance": "Rare, significance unclear"
    },
    # Expression-related resistance
    {
        "mutation": "HER2 loss/downregulation",
        "domain": "N/A",
        "residue_position": "N/A",
        "frequency_percent": 15.0,
        "cancer_types": "All HER2+ cancers (post-treatment)",
        "affects_epitope": "Complete loss",
        "resistance_mechanism": "Reduced target expression, antigen escape",
        "adc_impact": "Major - loss of target",
        "clinical_significance": "Major resistance mechanism"
    },
    {
        "mutation": "p95-HER2 (truncated)",
        "domain": "N-terminal truncation",
        "residue_position": "611-start",
        "frequency_percent": 20.0,
        "cancer_types": "Breast (aggressive)",
        "affects_epitope": "Loss of ECD (Domains I-IV)",
        "resistance_mechanism": "Loss of extracellular domain, no mAb binding",
        "adc_impact": "Major - no binding site",
        "clinical_significance": "Trastuzumab resistant, poor prognosis"
    },
    # Splice variants
    {
        "mutation": "HER2 splice variants",
        "domain": "Various",
        "residue_position": "N/A",
        "frequency_percent": 5.0,
        "cancer_types": "Breast",
        "affects_epitope": "Variable",
        "resistance_mechanism": "Altered protein structure",
        "adc_impact": "Variable - epitope dependent",
        "clinical_significance": "May affect therapy response"
    }
]

# ============================================================================
# RESISTANCE MECHANISMS SUMMARY
# ============================================================================

RESISTANCE_MECHANISMS = """
## HER2 ADC Resistance Mechanisms

### 1. Target-Related Resistance

| Mechanism | Frequency | Impact | Solution |
|-----------|-----------|--------|----------|
| HER2 downregulation | 15-30% | Loss of target | Bispecific ADCs, combination therapy |
| p95-HER2 truncation | 20-30% | No ECD binding | TKIs, intracellular targeting |
| Epitope mutations | <2% | Reduced binding | Alternative epitope targeting |
| HER2 splice variants | 5% | Variable | Epitope mapping, bispecifics |

### 2. Drug Resistance Mechanisms

| Mechanism | Affected ADCs | Solution |
|-----------|--------------|----------|
| MDR1/P-gp efflux | T-DM1, Disitamab | T-DXd (not P-gp substrate) |
| Altered lysosomal pH | All ADCs | Linker optimization |
| Payload metabolism | All ADCs | Novel payloads |
| DNA repair upregulation | T-DXd | Combination with PARP inhibitors |

### 3. Tumor Microenvironment

| Factor | Effect | Strategy |
|--------|--------|----------|
| Hypoxia | Reduced efficacy | Hypoxia-activated prodrugs |
| Stromal barriers | Poor penetration | Smaller formats, bispecifics |
| Immune suppression | Reduced ADCC | Fc optimization, immunotherapy |

### 4. Key Clinical Observations

**T-DM1 Resistance:**
- MDR1 upregulation common
- HER2 downregulation
- Lysosomal drug sequestration

**T-DXd Advantages:**
- Bystander effect (works with heterogeneous HER2)
- Not MDR1 substrate
- Higher DAR compensates for lower HER2

**Bispecific ADC Potential:**
- Zanidatamab-based ADCs in development
- Target multiple epitopes
- Enhanced internalization overcomes slow uptake
"""


def generate_mutation_csv(output_path):
    """Generate mutation data CSV."""
    df = pd.DataFrame(HER2_MUTATIONS)
    df.to_csv(output_path, index=False)
    print(f"Generated: {output_path}")
    return df


def print_mutation_summary():
    """Print mutation analysis summary."""
    print("=" * 70)
    print("HER2 Mutation and Resistance Analysis")
    print("=" * 70)

    print("\n1. Point Mutations in HER2:")
    print("-" * 50)
    print(f"{'Mutation':<20} {'Domain':<15} {'Freq %':<10} {'ADC Impact':<20}")
    print("-" * 70)

    for mut in HER2_MUTATIONS:
        if mut['domain'] != 'N/A' and 'loss' not in mut['mutation'].lower():
            print(f"{mut['mutation']:<20} {mut['domain']:<15} "
                  f"{mut['frequency_percent']:<10} {mut['adc_impact']:<20}")

    print("\n2. Major Resistance Mechanisms:")
    print("-" * 50)
    major = [m for m in HER2_MUTATIONS if 'Major' in m['adc_impact'] or m['frequency_percent'] >= 10]
    for mut in major:
        print(f"\n• {mut['mutation']}:")
        print(f"  Frequency: {mut['frequency_percent']}%")
        print(f"  Mechanism: {mut['resistance_mechanism']}")
        print(f"  ADC Impact: {mut['adc_impact']}")

    print("\n3. Key Findings:")
    print("-" * 50)
    print("• Most HER2 point mutations do NOT affect ADC binding")
    print("• Kinase domain mutations confer TKI resistance but ADCs remain effective")
    print("• HER2 loss/downregulation is the MAJOR resistance mechanism (15-30%)")
    print("• p95-HER2 (truncated) lacks ECD - complete loss of mAb/ADC binding")
    print("• T-DXd bystander effect partially overcomes HER2 heterogeneity")


def main():
    # Generate CSV
    df = generate_mutation_csv("data/mutations/her2_mutations_resistance.csv")

    # Print summary
    print_mutation_summary()

    # Save resistance mechanisms document
    with open("data/mutations/resistance_mechanisms.md", "w") as f:
        f.write(RESISTANCE_MECHANISMS)
    print("\nSaved: data/mutations/resistance_mechanisms.md")

    return df


if __name__ == "__main__":
    main()
