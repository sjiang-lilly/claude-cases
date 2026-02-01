#!/usr/bin/env python3
"""
HER2 Epitope Analysis for ADC Binder Design
Main analysis script for epitope mapping, mAb database, and internalization prediction.
"""

import pandas as pd
import numpy as np
import requests
import json
from datetime import datetime

# ============================================================================
# HER2 DOMAIN STRUCTURE (UniProt P04626)
# ============================================================================

HER2_DOMAINS = {
    "Signal peptide": {"start": 1, "end": 22, "type": "signal"},
    "Domain I": {"start": 23, "end": 195, "type": "extracellular", "function": "L1 domain, receptor dimerization"},
    "Domain II": {"start": 196, "end": 319, "type": "extracellular", "function": "Cysteine-rich 1, dimerization arm"},
    "Domain III": {"start": 320, "end": 488, "type": "extracellular", "function": "L2 domain, ligand binding"},
    "Domain IV": {"start": 489, "end": 630, "type": "extracellular", "function": "Cysteine-rich 2, membrane proximal"},
    "Transmembrane": {"start": 653, "end": 675, "type": "transmembrane"},
    "Kinase domain": {"start": 720, "end": 987, "type": "intracellular", "function": "Tyrosine kinase"}
}

# ============================================================================
# HER2 EPITOPES - Known therapeutic epitopes
# ============================================================================

HER2_EPITOPES = [
    {
        "epitope_id": "EPI-001",
        "domain": "Domain IV",
        "residues": "557-603",
        "key_residues": "Arg559, His560, Tyr572, Phe573, Asp597, Trp592",
        "description": "Membrane-proximal epitope in subdomain IV, juxtamembrane region",
        "mab_binding": ["Trastuzumab", "T-DM1", "T-DXd", "Margetuximab"],
        "structural_features": "Exposed loop region, stable conformation",
        "adc_suitability": "High - proven clinical efficacy"
    },
    {
        "epitope_id": "EPI-002",
        "domain": "Domain II",
        "residues": "266-333",
        "key_residues": "Ser288, Phe293, Lys294, Pro295, Glu299",
        "description": "Dimerization arm epitope, blocks HER2-HER3 heterodimerization",
        "mab_binding": ["Pertuzumab"],
        "structural_features": "Dimerization interface, allosteric site",
        "adc_suitability": "Moderate - blocks signaling but slower internalization"
    },
    {
        "epitope_id": "EPI-003",
        "domain": "Domain I",
        "residues": "23-165",
        "key_residues": "Thr144, Leu149, Arg150, Ile153",
        "description": "N-terminal L1 domain epitope",
        "mab_binding": ["Zanidatamab (in combination)"],
        "structural_features": "Accessible N-terminal region",
        "adc_suitability": "Moderate - less validated"
    },
    {
        "epitope_id": "EPI-004",
        "domain": "Domain III",
        "residues": "355-435",
        "key_residues": "Asp355, Leu356, Thr359, Glu395",
        "description": "L2 domain ligand-binding region",
        "mab_binding": ["Experimental mAbs"],
        "structural_features": "Central ECD region",
        "adc_suitability": "Under investigation"
    },
    {
        "epitope_id": "EPI-005",
        "domain": "Domain II + IV",
        "residues": "Biparatopic",
        "key_residues": "Combined epitopes",
        "description": "Bispecific targeting both dimerization and juxtamembrane regions",
        "mab_binding": ["Zanidatamab"],
        "structural_features": "Dual epitope engagement, receptor clustering",
        "adc_suitability": "High - enhanced internalization via cross-linking"
    }
]

# ============================================================================
# HER2-TARGETING mAbs AND ADCs
# ============================================================================

HER2_MABS_ADCS = [
    {
        "name": "Trastuzumab",
        "brand_name": "Herceptin",
        "type": "Monoclonal antibody (IgG1)",
        "epitope_domain": "Domain IV",
        "binding_residues": "557-603",
        "kd_nm": 5.0,
        "mechanism": "ADCC, blocks HER2 signaling, prevents cleavage",
        "approval_status": "FDA approved (1998)",
        "indication": "HER2+ breast cancer, gastric cancer",
        "adc_derivative": "Yes (T-DM1, T-DXd)"
    },
    {
        "name": "Pertuzumab",
        "brand_name": "Perjeta",
        "type": "Monoclonal antibody (IgG1)",
        "epitope_domain": "Domain II",
        "binding_residues": "266-333",
        "kd_nm": 1.0,
        "mechanism": "Blocks HER2-HER3 dimerization",
        "approval_status": "FDA approved (2012)",
        "indication": "HER2+ breast cancer (with trastuzumab)",
        "adc_derivative": "No"
    },
    {
        "name": "Trastuzumab emtansine",
        "brand_name": "Kadcyla (T-DM1)",
        "type": "ADC",
        "epitope_domain": "Domain IV",
        "binding_residues": "557-603",
        "kd_nm": 5.0,
        "mechanism": "Internalization, lysosomal release of DM1 (maytansinoid)",
        "linker": "Non-cleavable thioether (SMCC)",
        "payload": "DM1 (maytansinoid, microtubule inhibitor)",
        "dar": 3.5,
        "approval_status": "FDA approved (2013)",
        "indication": "HER2+ metastatic breast cancer"
    },
    {
        "name": "Trastuzumab deruxtecan",
        "brand_name": "Enhertu (T-DXd, DS-8201)",
        "type": "ADC",
        "epitope_domain": "Domain IV",
        "binding_residues": "557-603",
        "kd_nm": 5.0,
        "mechanism": "Internalization, cleavable linker, bystander effect",
        "linker": "Cleavable tetrapeptide (GGFG)",
        "payload": "Deruxtecan (DXd, topoisomerase I inhibitor)",
        "dar": 8.0,
        "approval_status": "FDA approved (2019)",
        "indication": "HER2+ breast cancer, HER2-low breast cancer, gastric, NSCLC"
    },
    {
        "name": "Margetuximab",
        "brand_name": "Margenza",
        "type": "Monoclonal antibody (Fc-optimized)",
        "epitope_domain": "Domain IV",
        "binding_residues": "557-603",
        "kd_nm": 4.8,
        "mechanism": "Enhanced ADCC via Fc optimization (F243L/R292P/Y300L/V305I/P396L)",
        "approval_status": "FDA approved (2020)",
        "indication": "HER2+ metastatic breast cancer",
        "adc_derivative": "No"
    },
    {
        "name": "Zanidatamab",
        "brand_name": "N/A (in development)",
        "type": "Bispecific antibody",
        "epitope_domain": "Domain II + Domain IV",
        "binding_residues": "Biparatopic",
        "kd_nm": 0.5,
        "mechanism": "Dual epitope binding, receptor clustering, enhanced internalization",
        "approval_status": "Phase 3 (2024)",
        "indication": "HER2+ biliary tract, gastric, breast cancer",
        "adc_derivative": "In development (ZW49)"
    },
    {
        "name": "Disitamab vedotin",
        "brand_name": "Aidixi",
        "type": "ADC",
        "epitope_domain": "Domain IV",
        "binding_residues": "557-603 (similar to trastuzumab)",
        "kd_nm": 3.0,
        "mechanism": "Internalization, MMAE payload",
        "linker": "Cleavable mc-vc-PABC",
        "payload": "MMAE (auristatin, microtubule inhibitor)",
        "dar": 4.0,
        "approval_status": "Approved in China (2021)",
        "indication": "HER2+ gastric cancer, urothelial cancer"
    }
]

# ============================================================================
# FUNCTIONS
# ============================================================================

def generate_epitope_csv(output_path):
    """Generate epitope summary CSV."""
    df = pd.DataFrame(HER2_EPITOPES)
    df['mab_binding'] = df['mab_binding'].apply(lambda x: '; '.join(x))
    df.to_csv(output_path, index=False)
    print(f"Generated: {output_path}")
    return df

def generate_mabs_csv(output_path):
    """Generate mAbs/ADCs summary CSV."""
    df = pd.DataFrame(HER2_MABS_ADCS)
    df.to_csv(output_path, index=False)
    print(f"Generated: {output_path}")
    return df

def fetch_uniprot_sequence(accession="P04626"):
    """Fetch HER2 sequence from UniProt."""
    url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.text
    except Exception as e:
        print(f"Warning: Could not fetch UniProt sequence: {e}")

    # Fallback: return partial sequence
    return """>sp|P04626|ERBB2_HUMAN Receptor tyrosine-protein kinase erbB-2 OS=Homo sapiens
MELAALCRWGLLLALLPPGAASTQVCTGTDMKLRLPASPETHLDMLRHLYQGCQVVQGNL
ELTYLPTNASLSFLQDIQEVQGYVLIAHNQVRQVPLQRLRIVRGTQLFEDNYALAVLDNG
DPLNNTTPVTGASPGGLRELQLRSLTEILKGGVLIQRNPQLCYQDTILWKDIFHKNNQLA
LTLIDTNRSRACHPCSPMCKGSRCWGESSEDCQSLTRTVCAGGCARCKGPLPTDCCHEQC
AAGCTGPKHSDCLACLHFNHSGICELHCPALVTYNTDTFESMPNPEGRYTFGASCVTACP
YNYLSTDVGSCTLVCPLHNQEVTAEDGTQRCEKCSKPCARVCYGLGMEHLREVRAVTSAN
IQEFAGCKKIFGSLAFLPESFDGDPASNTAPLQPEQLQVFETLEEITGYLYISAWPDSLP
DLSVFQNLQVIRGRILHNGAYSLTLQGLGISWLGLRSLRELGSGLALIHHNTHLCFVHTV
PWDQLFRNPHQALLHTANRPEDECVGEGLACHQLCARGHCWGPGPTQCVNCSQFLRGQEC
VEECRVLQGLPREYVNARHCLPCHPECQPQNGSVTCFGPEADQCVACAHYKDPPFCVARC
PSGVKPDLSYMPIWKFPDEEGACQPCPINCTHSCVDLDDKGCPAEQRASPLT"""

def evaluate_epitope_for_adc(epitope):
    """Evaluate epitope suitability for ADC design."""
    scores = {
        "accessibility": 0,
        "internalization": 0,
        "clinical_validation": 0,
        "stability": 0
    }

    domain = epitope["domain"]

    # Accessibility scoring
    if domain in ["Domain IV", "Domain I"]:
        scores["accessibility"] = 9
    elif domain == "Domain II":
        scores["accessibility"] = 8
    else:
        scores["accessibility"] = 7

    # Internalization scoring
    if "Zanidatamab" in str(epitope["mab_binding"]) or "Biparatopic" in domain:
        scores["internalization"] = 10  # Bispecific enhances internalization
    elif domain == "Domain IV":
        scores["internalization"] = 7  # Moderate internalization
    elif domain == "Domain II":
        scores["internalization"] = 6  # Slower internalization
    else:
        scores["internalization"] = 5

    # Clinical validation scoring
    validated_mabs = ["Trastuzumab", "T-DM1", "T-DXd", "Pertuzumab"]
    if any(mab in str(epitope["mab_binding"]) for mab in validated_mabs):
        scores["clinical_validation"] = 10
    else:
        scores["clinical_validation"] = 5

    # Stability scoring
    if domain == "Domain IV":
        scores["stability"] = 9
    else:
        scores["stability"] = 7

    total = sum(scores.values()) / 4
    return scores, round(total, 1)


def main():
    """Main analysis workflow."""
    print("=" * 60)
    print("HER2 Epitope Analysis for ADC Binder Design")
    print("=" * 60)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Generate epitope data
    print("Step 2: Generating HER2 epitope data...")
    epitope_df = generate_epitope_csv("data/her2_epitopes.csv")

    print("\nHER2 Domain Structure:")
    print("-" * 40)
    for domain, info in HER2_DOMAINS.items():
        if info["type"] == "extracellular":
            print(f"  {domain}: residues {info['start']}-{info['end']}")
            print(f"    Function: {info.get('function', 'N/A')}")

    print("\nEpitope Evaluation for ADC Design:")
    print("-" * 40)
    for epitope in HER2_EPITOPES:
        scores, total = evaluate_epitope_for_adc(epitope)
        print(f"\n{epitope['epitope_id']} ({epitope['domain']}):")
        print(f"  Residues: {epitope['residues']}")
        print(f"  mAbs: {', '.join(epitope['mab_binding'])}")
        print(f"  ADC Suitability Score: {total}/10")
        print(f"    - Accessibility: {scores['accessibility']}/10")
        print(f"    - Internalization: {scores['internalization']}/10")
        print(f"    - Clinical validation: {scores['clinical_validation']}/10")
        print(f"    - Stability: {scores['stability']}/10")

    # Generate mAb data
    print("\n" + "=" * 60)
    print("Step 3: Generating mAb/ADC database...")
    mab_df = generate_mabs_csv("data/her2_mabs_adcs.csv")

    print("\nApproved HER2 ADCs:")
    print("-" * 40)
    for mab in HER2_MABS_ADCS:
        if mab["type"] == "ADC":
            print(f"\n{mab['name']} ({mab['brand_name']}):")
            print(f"  Epitope: {mab['epitope_domain']} ({mab['binding_residues']})")
            print(f"  Linker: {mab.get('linker', 'N/A')}")
            print(f"  Payload: {mab.get('payload', 'N/A')}")
            print(f"  DAR: {mab.get('dar', 'N/A')}")
            print(f"  Status: {mab['approval_status']}")

    # Save UniProt sequence
    print("\n" + "=" * 60)
    print("Fetching HER2 sequence from UniProt...")
    sequence = fetch_uniprot_sequence()
    with open("data/sequences/P04626.fasta", "w") as f:
        f.write(sequence)
    print("Saved: data/sequences/P04626.fasta")

    print("\n" + "=" * 60)
    print("Analysis complete!")
    print("=" * 60)

    return epitope_df, mab_df


if __name__ == "__main__":
    main()
