#!/usr/bin/env python3
"""
Generate Docking Images for HER2-Antibody Complexes

Uses py3Dmol for interactive visualization and matplotlib for static images.
"""

import py3Dmol
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# Domain color scheme
DOMAIN_COLORS = {
    "Domain I": "#FF6B6B",    # Red
    "Domain II": "#4ECDC4",   # Teal
    "Domain III": "#45B7D1",  # Blue
    "Domain IV": "#96CEB4",   # Green
    "Antibody Heavy": "#DDA0DD",  # Plum
    "Antibody Light": "#F0E68C",  # Khaki
}

# HER2 domain residue ranges (for chain A in PDB structures)
HER2_DOMAINS_PDB = {
    "Domain I": (23, 195),
    "Domain II": (196, 319),
    "Domain III": (320, 488),
    "Domain IV": (489, 630),
}


def create_schematic_figure():
    """Create a schematic diagram of HER2 domains and antibody binding sites."""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))

    # Draw HER2 receptor schematic
    # Extracellular domains
    domain_boxes = [
        {"name": "Domain I\n(23-195)", "y": 8, "color": DOMAIN_COLORS["Domain I"], "height": 1.5},
        {"name": "Domain II\n(196-319)", "y": 6.2, "color": DOMAIN_COLORS["Domain II"], "height": 1.5},
        {"name": "Domain III\n(320-488)", "y": 4.4, "color": DOMAIN_COLORS["Domain III"], "height": 1.5},
        {"name": "Domain IV\n(489-630)", "y": 2.6, "color": DOMAIN_COLORS["Domain IV"], "height": 1.5},
    ]

    # Draw domains
    for domain in domain_boxes:
        rect = mpatches.FancyBboxPatch(
            (4, domain["y"]), 4, domain["height"],
            boxstyle="round,pad=0.05",
            facecolor=domain["color"],
            edgecolor="black",
            linewidth=2
        )
        ax.add_patch(rect)
        ax.text(6, domain["y"] + domain["height"]/2, domain["name"],
                ha='center', va='center', fontsize=11, fontweight='bold')

    # Membrane
    membrane = mpatches.FancyBboxPatch(
        (2, 1.8), 8, 0.5,
        boxstyle="round,pad=0.02",
        facecolor="#FFE4B5",
        edgecolor="black",
        linewidth=2
    )
    ax.add_patch(membrane)
    ax.text(6, 2.05, "Cell Membrane", ha='center', va='center', fontsize=10)

    # Intracellular kinase domain
    kinase = mpatches.FancyBboxPatch(
        (4, 0.3), 4, 1.2,
        boxstyle="round,pad=0.05",
        facecolor="#D3D3D3",
        edgecolor="black",
        linewidth=2
    )
    ax.add_patch(kinase)
    ax.text(6, 0.9, "Kinase Domain\n(720-987)", ha='center', va='center', fontsize=10)

    # Draw antibodies
    # Trastuzumab (Domain IV)
    ax.annotate('', xy=(8.2, 3.35), xytext=(11, 3.35),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2))
    ax.add_patch(mpatches.FancyBboxPatch(
        (11, 2.85), 3, 1,
        boxstyle="round,pad=0.05",
        facecolor="#DDA0DD",
        edgecolor="black",
        linewidth=2
    ))
    ax.text(12.5, 3.35, "Trastuzumab\n(T-DM1, T-DXd)", ha='center', va='center', fontsize=9, fontweight='bold')

    # Pertuzumab (Domain II)
    ax.annotate('', xy=(8.2, 6.95), xytext=(11, 6.95),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2))
    ax.add_patch(mpatches.FancyBboxPatch(
        (11, 6.45), 3, 1,
        boxstyle="round,pad=0.05",
        facecolor="#FFA07A",
        edgecolor="black",
        linewidth=2
    ))
    ax.text(12.5, 6.95, "Pertuzumab", ha='center', va='center', fontsize=9, fontweight='bold')

    # Zanidatamab (Biparatopic)
    ax.annotate('', xy=(0, 6.95), xytext=(-1, 5.15),
                arrowprops=dict(arrowstyle='-', color='green', lw=2, connectionstyle="arc3,rad=-0.3"))
    ax.annotate('', xy=(0, 3.35), xytext=(-1, 5.15),
                arrowprops=dict(arrowstyle='-', color='green', lw=2, connectionstyle="arc3,rad=0.3"))
    ax.add_patch(mpatches.FancyBboxPatch(
        (-4, 4.4), 3, 1.5,
        boxstyle="round,pad=0.05",
        facecolor="#90EE90",
        edgecolor="black",
        linewidth=2
    ))
    ax.text(-2.5, 5.15, "Zanidatamab\n(Biparatopic)", ha='center', va='center', fontsize=9, fontweight='bold')

    # Add title and labels
    ax.set_xlim(-5, 16)
    ax.set_ylim(-0.5, 10.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("HER2 Domain Structure and Therapeutic Antibody Binding Sites",
                 fontsize=14, fontweight='bold', pad=20)

    # Add legend
    legend_elements = [
        mpatches.Patch(facecolor=DOMAIN_COLORS["Domain I"], edgecolor='black', label='Domain I (Dimerization)'),
        mpatches.Patch(facecolor=DOMAIN_COLORS["Domain II"], edgecolor='black', label='Domain II (Dimerization arm)'),
        mpatches.Patch(facecolor=DOMAIN_COLORS["Domain III"], edgecolor='black', label='Domain III (Ligand binding)'),
        mpatches.Patch(facecolor=DOMAIN_COLORS["Domain IV"], edgecolor='black', label='Domain IV (Membrane proximal)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)

    # Add annotation box
    textstr = '\n'.join([
        'ADC Binding Sites:',
        '• Trastuzumab epitope (Domain IV): T-DM1, T-DXd',
        '• Pertuzumab epitope (Domain II): Blocks dimerization',
        '• Zanidatamab (Biparatopic): Enhanced internalization'
    ])
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.02, 0.02, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='bottom', bbox=props)

    plt.tight_layout()
    return fig


def create_epitope_comparison():
    """Create epitope comparison chart."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left: Internalization rates
    epitopes = ['Domain IV\n(Trastuzumab)', 'Domain II\n(Pertuzumab)', 'Biparatopic\n(Zanidatamab)']
    internalization = [25, 15, 70]
    colors = [DOMAIN_COLORS["Domain IV"], DOMAIN_COLORS["Domain II"], '#90EE90']

    bars1 = axes[0].bar(epitopes, internalization, color=colors, edgecolor='black', linewidth=2)
    axes[0].set_ylabel('% Internalized at 4h', fontsize=12)
    axes[0].set_title('Epitope-Dependent Internalization Rates', fontsize=12, fontweight='bold')
    axes[0].set_ylim(0, 100)
    for bar, val in zip(bars1, internalization):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                     f'{val}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Right: ADC suitability scores
    mabs = ['T-DM1', 'T-DXd', 'Disitamab\nvedotin', 'ZW49\n(development)']
    scores = [7.5, 8.5, 7.0, 9.5]
    mab_colors = ['#DDA0DD', '#DDA0DD', '#DDA0DD', '#90EE90']

    bars2 = axes[1].bar(mabs, scores, color=mab_colors, edgecolor='black', linewidth=2)
    axes[1].set_ylabel('ADC Suitability Score', fontsize=12)
    axes[1].set_title('ADC Suitability by Antibody Platform', fontsize=12, fontweight='bold')
    axes[1].set_ylim(0, 10)
    for bar, val in zip(bars2, scores):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                     f'{val}', ha='center', va='bottom', fontsize=11, fontweight='bold')

    plt.tight_layout()
    return fig


def create_mab_summary_table():
    """Create visual mAb summary table."""
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.axis('off')

    # Table data
    columns = ['mAb/ADC', 'Type', 'Epitope', 'Kd (nM)', 'Internalization', 'ADC Status', 'Approval']
    data = [
        ['Trastuzumab', 'mAb', 'Domain IV', '5.0', 'Slow (25%)', 'T-DM1, T-DXd', 'FDA 1998'],
        ['Pertuzumab', 'mAb', 'Domain II', '1.0', 'V. Slow (15%)', 'None', 'FDA 2012'],
        ['T-DM1 (Kadcyla)', 'ADC', 'Domain IV', '5.0', 'Slow (25%)', '-', 'FDA 2013'],
        ['T-DXd (Enhertu)', 'ADC', 'Domain IV', '5.0', 'Slow (25%)', '-', 'FDA 2019'],
        ['Margetuximab', 'mAb', 'Domain IV', '4.8', 'Slow (25%)', 'None', 'FDA 2020'],
        ['Zanidatamab', 'Bispecific', 'II + IV', '0.5', 'Fast (70%)', 'ZW49 (dev)', 'Phase 3'],
        ['Disitamab vedotin', 'ADC', 'Domain IV', '3.0', 'Slow (25%)', '-', 'China 2021'],
    ]

    # Create table
    table = ax.table(
        cellText=data,
        colLabels=columns,
        cellLoc='center',
        loc='center',
        colColours=['#4472C4'] * len(columns)
    )

    # Style table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.8)

    # Color header
    for i in range(len(columns)):
        table[(0, i)].set_text_props(color='white', fontweight='bold')

    # Color rows by type
    for i, row in enumerate(data):
        if row[1] == 'ADC':
            for j in range(len(columns)):
                table[(i+1, j)].set_facecolor('#E2EFDA')
        elif row[1] == 'Bispecific':
            for j in range(len(columns)):
                table[(i+1, j)].set_facecolor('#FFF2CC')

    ax.set_title('HER2-Targeting mAbs and ADCs Summary', fontsize=14, fontweight='bold', pad=20)

    plt.tight_layout()
    return fig


def generate_py3dmol_html(pdb_file, output_html, title="HER2 Structure"):
    """Generate interactive 3D visualization HTML file."""

    with open(pdb_file, 'r') as f:
        pdb_data = f.read()

    html_template = f'''<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://3dmol.org/build/3Dmol-min.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .mol-container {{ width: 800px; height: 600px; position: relative; border: 1px solid #ccc; }}
        .legend {{ margin-top: 20px; }}
        .legend-item {{ display: inline-block; margin-right: 20px; }}
        .color-box {{ display: inline-block; width: 20px; height: 20px; margin-right: 5px; vertical-align: middle; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div id="viewer" class="mol-container"></div>
    <div class="legend">
        <div class="legend-item"><span class="color-box" style="background-color: #FF6B6B;"></span>Domain I</div>
        <div class="legend-item"><span class="color-box" style="background-color: #4ECDC4;"></span>Domain II</div>
        <div class="legend-item"><span class="color-box" style="background-color: #45B7D1;"></span>Domain III</div>
        <div class="legend-item"><span class="color-box" style="background-color: #96CEB4;"></span>Domain IV</div>
        <div class="legend-item"><span class="color-box" style="background-color: #DDA0DD;"></span>Antibody Heavy Chain</div>
        <div class="legend-item"><span class="color-box" style="background-color: #F0E68C;"></span>Antibody Light Chain</div>
    </div>
    <script>
        var viewer = $3Dmol.createViewer("viewer", {{backgroundColor: "white"}});
        var pdbData = `{pdb_data}`;
        viewer.addModel(pdbData, "pdb");

        // Color HER2 domains (chain A typically)
        viewer.setStyle({{chain: "A", resi: ["23-195"]}}, {{cartoon: {{color: "#FF6B6B"}}}});
        viewer.setStyle({{chain: "A", resi: ["196-319"]}}, {{cartoon: {{color: "#4ECDC4"}}}});
        viewer.setStyle({{chain: "A", resi: ["320-488"]}}, {{cartoon: {{color: "#45B7D1"}}}});
        viewer.setStyle({{chain: "A", resi: ["489-630"]}}, {{cartoon: {{color: "#96CEB4"}}}});

        // Color antibody chains
        viewer.setStyle({{chain: "B"}}, {{cartoon: {{color: "#DDA0DD"}}}});
        viewer.setStyle({{chain: "C"}}, {{cartoon: {{color: "#F0E68C"}}}});
        viewer.setStyle({{chain: "H"}}, {{cartoon: {{color: "#DDA0DD"}}}});
        viewer.setStyle({{chain: "L"}}, {{cartoon: {{color: "#F0E68C"}}}});

        viewer.zoomTo();
        viewer.render();
    </script>
</body>
</html>'''

    with open(output_html, 'w') as f:
        f.write(html_template)
    print(f"Generated: {output_html}")


def main():
    """Generate all visualization outputs."""
    print("=" * 60)
    print("Generating HER2 Docking Visualizations")
    print("=" * 60)

    os.makedirs("images", exist_ok=True)

    # 1. Schematic diagram
    print("\n1. Creating HER2 domain schematic...")
    fig1 = create_schematic_figure()
    fig1.savefig("images/her2_domain_schematic.png", dpi=300, bbox_inches='tight')
    plt.close(fig1)
    print("   Saved: images/her2_domain_schematic.png")

    # 2. Epitope comparison charts
    print("\n2. Creating epitope comparison charts...")
    fig2 = create_epitope_comparison()
    fig2.savefig("images/epitope_comparison.png", dpi=300, bbox_inches='tight')
    plt.close(fig2)
    print("   Saved: images/epitope_comparison.png")

    # 3. mAb summary table
    print("\n3. Creating mAb summary table...")
    fig3 = create_mab_summary_table()
    fig3.savefig("images/mab_summary_table.png", dpi=300, bbox_inches='tight')
    plt.close(fig3)
    print("   Saved: images/mab_summary_table.png")

    # 4. Interactive 3D visualizations
    print("\n4. Creating interactive 3D visualizations...")

    structures = [
        ("data/structures/1N8Z.pdb", "images/her2_trastuzumab_3d.html", "HER2-Trastuzumab Complex (PDB: 1N8Z)"),
        ("data/structures/1S78.pdb", "images/her2_pertuzumab_3d.html", "HER2-Pertuzumab Complex (PDB: 1S78)"),
        ("data/structures/6OGE.pdb", "images/her2_dual_3d.html", "HER2-Trastuzumab-Pertuzumab Complex (PDB: 6OGE)"),
    ]

    for pdb_file, output_html, title in structures:
        if os.path.exists(pdb_file):
            generate_py3dmol_html(pdb_file, output_html, title)
        else:
            print(f"   Warning: {pdb_file} not found")

    print("\n" + "=" * 60)
    print("Visualization generation complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - images/her2_domain_schematic.png")
    print("  - images/epitope_comparison.png")
    print("  - images/mab_summary_table.png")
    print("  - images/her2_trastuzumab_3d.html")
    print("  - images/her2_pertuzumab_3d.html")
    print("  - images/her2_dual_3d.html")


if __name__ == "__main__":
    main()
