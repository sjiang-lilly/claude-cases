#!/usr/bin/env python3
"""
Generate docking visualization images for pipeline-predicted p95-HER2 targeting mAbs.
Shows ESM + AlphaFold + Docking pipeline predictions binding to the juxtamembrane epitope region.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
import numpy as np
import os

def draw_antibody_structure(ax, x, y, scale=1.0, color='#DDA0DD', label='', arm1_color=None, arm2_color=None):
    """Draw simplified antibody Y-shape structure."""
    # Fc region (bottom)
    fc_width = 0.8 * scale
    fc_height = 1.2 * scale
    ax.add_patch(FancyBboxPatch((x - fc_width/2, y), fc_width, fc_height,
                                boxstyle="round,pad=0.05", facecolor=color,
                                edgecolor='black', linewidth=1.5))

    # Hinge region
    ax.plot([x, x - 0.5*scale], [y + fc_height, y + fc_height + 0.3*scale], 'k-', linewidth=2)
    ax.plot([x, x + 0.5*scale], [y + fc_height, y + fc_height + 0.3*scale], 'k-', linewidth=2)

    # Fab arms
    arm1_c = arm1_color if arm1_color else color
    arm2_c = arm2_color if arm2_color else color

    # Left Fab arm
    fab_width = 0.6 * scale
    fab_height = 1.0 * scale
    ax.add_patch(FancyBboxPatch((x - 0.5*scale - fab_width/2, y + fc_height + 0.3*scale),
                                fab_width, fab_height, boxstyle="round,pad=0.05",
                                facecolor=arm1_c, edgecolor='black', linewidth=1.5))

    # Right Fab arm
    ax.add_patch(FancyBboxPatch((x + 0.5*scale - fab_width/2, y + fc_height + 0.3*scale),
                                fab_width, fab_height, boxstyle="round,pad=0.05",
                                facecolor=arm2_c, edgecolor='black', linewidth=1.5))

    # CDR loops at tips (binding sites)
    cdr_y = y + fc_height + 0.3*scale + fab_height
    ax.add_patch(Circle((x - 0.5*scale, cdr_y), 0.15*scale, facecolor='yellow',
                        edgecolor='black', linewidth=1))
    ax.add_patch(Circle((x + 0.5*scale, cdr_y), 0.15*scale, facecolor='yellow',
                        edgecolor='black', linewidth=1))

    if label:
        ax.text(x, y - 0.3*scale, label, ha='center', va='top', fontsize=9, fontweight='bold')

    return cdr_y

def create_p95_docking_figure():
    """Create comprehensive p95-HER2 docking visualization with pipeline-predicted mAbs."""
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('Pipeline-Predicted p95-HER2 Targeting mAbs: ESM + AlphaFold + Docking',
                 fontsize=18, fontweight='bold', y=0.98)

    gs = fig.add_gridspec(2, 3, hspace=0.35, wspace=0.3,
                          left=0.05, right=0.95, top=0.92, bottom=0.05)

    # ========== PANEL A: p95-ESM-001 (Epitope Mimicry) ==========
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 12)
    ax1.axis('off')
    ax1.set_title('A. p95-ESM-001 (Epitope Mimicry)\n→ JM Epitope (615-635)', fontsize=12, fontweight='bold', loc='left')

    # Draw p95-HER2 structure
    ax1.add_patch(FancyBboxPatch((3, 3), 4, 2.5, boxstyle="round,pad=0.05",
                                 facecolor='#FFFF99', edgecolor='black', linewidth=2))
    ax1.text(5, 4.25, "JM Stub\n(611-652)", ha='center', va='center', fontsize=10, fontweight='bold')

    # Epitope region highlighted
    ax1.add_patch(FancyBboxPatch((3.2, 4.2), 1.8, 1.0, boxstyle="round,pad=0.02",
                                 facecolor='#90EE90', edgecolor='green', linewidth=2))
    ax1.text(4.1, 4.7, "615-635", ha='center', va='center', fontsize=8, fontweight='bold', color='green')

    # Membrane
    ax1.axhline(y=2.5, xmin=0.2, xmax=0.8, color='brown', linewidth=6)
    ax1.text(5, 2.1, "Cell Membrane", ha='center', va='center', fontsize=9)

    # Draw antibody
    cdr_y = draw_antibody_structure(ax1, 4.1, 6.5, scale=0.8, color='#90EE90', label='p95-ESM-001')

    # Binding arrow
    ax1.annotate('', xy=(4.1, 5.2), xytext=(4.1, 6.5),
                arrowprops=dict(arrowstyle='->', color='green', lw=2))

    # Sequence box
    ax1.text(5, 11, "CDR-H3: ARDPIWKFPDYAMDY\nCDR-L3: QQGACQPLT\nStrategy: Epitope Mimicry", ha='center', va='center',
             fontsize=8, family='monospace', bbox=dict(boxstyle='round', facecolor='white', edgecolor='gray'))

    ax1.text(5, 0.5, "Kd: 0.21 nM | ADC Score: 9.0/10", ha='center', va='center', fontsize=9, style='italic', color='green', fontweight='bold')

    # ========== PANEL B: p95-ESM-002 (Charge Complementarity) - TOP ==========
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 12)
    ax2.axis('off')
    ax2.set_title('B. p95-ESM-002 (Charge Complementarity) ★TOP\n→ JM Epitope (615-635)', fontsize=12, fontweight='bold', loc='left')

    # Draw p95-HER2 structure
    ax2.add_patch(FancyBboxPatch((3, 3), 4, 2.5, boxstyle="round,pad=0.05",
                                 facecolor='#FFFF99', edgecolor='black', linewidth=2))
    ax2.text(5, 4.25, "JM Stub\n(611-652)", ha='center', va='center', fontsize=10, fontweight='bold')

    # Epitope with charge indicators
    ax2.add_patch(FancyBboxPatch((3.2, 4.2), 1.8, 1.0, boxstyle="round,pad=0.02",
                                 facecolor='#87CEEB', edgecolor='blue', linewidth=2))
    ax2.text(4.1, 4.7, "615-635", ha='center', va='center', fontsize=8, fontweight='bold', color='blue')

    # Charge indicators
    ax2.text(3.5, 4.0, "- - -", ha='center', va='center', fontsize=10, color='red', fontweight='bold')
    ax2.annotate('Glu/Asp\n(negative)', xy=(3.5, 3.8), xytext=(2.0, 3.2),
                fontsize=7, ha='center', color='red',
                arrowprops=dict(arrowstyle='->', color='red', lw=1))

    # Membrane
    ax2.axhline(y=2.5, xmin=0.2, xmax=0.8, color='brown', linewidth=6)
    ax2.text(5, 2.1, "Cell Membrane", ha='center', va='center', fontsize=9)

    # Draw antibody
    draw_antibody_structure(ax2, 4.1, 6.5, scale=0.8, color='#87CEEB', label='p95-ESM-002')

    # Binding arrow
    ax2.annotate('', xy=(4.1, 5.2), xytext=(4.1, 6.5),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))

    ax2.text(5, 11, "CDR-H3: ARDRKEYWFDY\nCDR-L3: QQFPDEEGT\nStrategy: Charge Complementarity", ha='center', va='center',
             fontsize=8, family='monospace', bbox=dict(boxstyle='round', facecolor='#E6F3FF', edgecolor='blue'))

    ax2.text(5, 0.5, "Kd: 0.13 nM | ADC Score: 9.0/10 | BEST SINGLE-ARM", ha='center', va='center',
             fontsize=9, style='italic', color='blue', fontweight='bold')

    # ========== PANEL C: p95-ESM-004 (Neo-epitope Specific) ==========
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 12)
    ax3.axis('off')
    ax3.set_title('C. p95-ESM-004 (Neo-epitope Specific)\n→ Met611 Neo-epitope (611-625)', fontsize=12, fontweight='bold', loc='left')

    # Draw p95-HER2 structure
    ax3.add_patch(FancyBboxPatch((3, 3), 4, 2.5, boxstyle="round,pad=0.05",
                                 facecolor='#FFFF99', edgecolor='black', linewidth=2))
    ax3.text(5, 4.25, "JM Stub\n(611-652)", ha='center', va='center', fontsize=10, fontweight='bold')

    # Neo-epitope at N-terminus (Met611)
    ax3.add_patch(FancyBboxPatch((3.0, 4.5), 1.5, 0.8, boxstyle="round,pad=0.02",
                                 facecolor='#FFB6C1', edgecolor='#FF1493', linewidth=2))
    ax3.text(3.75, 4.9, "M611", ha='center', va='center', fontsize=9, fontweight='bold', color='#FF1493')
    ax3.annotate('Neo-epitope\n(p95-SPECIFIC)', xy=(3.0, 5.3), xytext=(1.5, 6.5),
                fontsize=8, ha='center', color='#FF1493', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#FF1493', lw=1.5))

    # Membrane
    ax3.axhline(y=2.5, xmin=0.2, xmax=0.8, color='brown', linewidth=6)
    ax3.text(5, 2.1, "Cell Membrane", ha='center', va='center', fontsize=9)

    # Draw antibody
    draw_antibody_structure(ax3, 3.75, 6.5, scale=0.8, color='#FFB6C1', label='p95-ESM-004')

    # Binding arrow
    ax3.annotate('', xy=(3.75, 5.3), xytext=(3.75, 6.5),
                arrowprops=dict(arrowstyle='->', color='#FF1493', lw=2))

    ax3.text(5, 11, "CDR-H3: ARMETPIWKFDY\nCDR-L3: QQMPIWFPT\nStrategy: Neo-epitope Recognition", ha='center', va='center',
             fontsize=8, family='monospace', bbox=dict(boxstyle='round', facecolor='#FFE4E1', edgecolor='#FF1493'))

    ax3.text(5, 0.5, "Kd: 0.20 nM | ADC Score: 9.0/10 | NO FL-HER2 binding", ha='center', va='center',
             fontsize=9, style='italic', color='#FF1493', fontweight='bold')

    # ========== PANEL D: p95-Trastuzumab-Biparatopic (RECOMMENDED) ==========
    ax4 = fig.add_subplot(gs[1, 0:2])
    ax4.set_xlim(0, 16)
    ax4.set_ylim(0, 12)
    ax4.axis('off')
    ax4.set_title('D. p95-Trastuzumab-Biparatopic (RECOMMENDED): Dual Targeting (p95-JM + FL-HER2 Domain IV)',
                  fontsize=12, fontweight='bold', loc='left')

    # LEFT: p95-HER2
    ax4.text(4, 11, "p95-HER2+ Cell", ha='center', va='center', fontsize=11, fontweight='bold', color='red')

    ax4.add_patch(FancyBboxPatch((2, 3), 4, 2.5, boxstyle="round,pad=0.05",
                                 facecolor='#FFFF99', edgecolor='red', linewidth=2))
    ax4.text(4, 4.25, "JM Stub\n(611-652)", ha='center', va='center', fontsize=10, fontweight='bold')

    # p95 epitope
    ax4.add_patch(FancyBboxPatch((2.2, 4.2), 1.6, 0.9, boxstyle="round,pad=0.02",
                                 facecolor='#87CEEB', edgecolor='blue', linewidth=2))
    ax4.text(3, 4.65, "615-635", ha='center', va='center', fontsize=8, fontweight='bold', color='blue')

    ax4.axhline(y=2.5, xmin=0.1, xmax=0.45, color='brown', linewidth=6)
    ax4.text(4, 2.1, "Membrane", ha='center', va='center', fontsize=8)

    # RIGHT: Full-length HER2
    ax4.text(12, 11, "FL-HER2+ Cell", ha='center', va='center', fontsize=11, fontweight='bold', color='green')

    # Domain IV
    ax4.add_patch(FancyBboxPatch((10, 3), 4, 4, boxstyle="round,pad=0.05",
                                 facecolor='#96CEB4', edgecolor='black', linewidth=2))
    ax4.text(12, 5, "Domain IV\n(489-630)", ha='center', va='center', fontsize=10, fontweight='bold')

    # Trastuzumab epitope
    ax4.add_patch(FancyBboxPatch((11.5, 5.5), 1.6, 1.0, boxstyle="round,pad=0.02",
                                 facecolor='#DDA0DD', edgecolor='purple', linewidth=2))
    ax4.text(12.3, 6, "557-603", ha='center', va='center', fontsize=8, fontweight='bold', color='purple')

    ax4.axhline(y=2.5, xmin=0.6, xmax=0.9, color='brown', linewidth=6)
    ax4.text(12, 2.1, "Membrane", ha='center', va='center', fontsize=8)

    # BISPECIFIC ANTIBODY in center
    center_x = 8
    fc_y = 7

    # Fc region
    ax4.add_patch(FancyBboxPatch((center_x - 0.6, fc_y), 1.2, 1.5,
                                 boxstyle="round,pad=0.05", facecolor='#E6E6FA',
                                 edgecolor='black', linewidth=2))

    # Left arm (p95-targeting from ESM-002) - blue
    ax4.plot([center_x - 0.2, center_x - 1.5], [fc_y + 1.5, fc_y + 2.0], 'k-', linewidth=2)
    ax4.add_patch(FancyBboxPatch((center_x - 2.0, fc_y + 2.0), 1.0, 1.2,
                                 boxstyle="round,pad=0.05", facecolor='#87CEEB',
                                 edgecolor='blue', linewidth=2))
    ax4.add_patch(Circle((center_x - 1.5, fc_y + 3.2), 0.2, facecolor='yellow',
                         edgecolor='black', linewidth=1))
    ax4.text(center_x - 1.5, fc_y + 2.6, "p95\nESM-002", ha='center', va='center', fontsize=7, fontweight='bold')

    # Right arm (Domain IV-targeting - Trastuzumab) - purple
    ax4.plot([center_x + 0.2, center_x + 1.5], [fc_y + 1.5, fc_y + 2.0], 'k-', linewidth=2)
    ax4.add_patch(FancyBboxPatch((center_x + 1.0, fc_y + 2.0), 1.0, 1.2,
                                 boxstyle="round,pad=0.05", facecolor='#DDA0DD',
                                 edgecolor='purple', linewidth=2))
    ax4.add_patch(Circle((center_x + 1.5, fc_y + 3.2), 0.2, facecolor='yellow',
                         edgecolor='black', linewidth=1))
    ax4.text(center_x + 1.5, fc_y + 2.6, "Tras\nDomIV", ha='center', va='center', fontsize=7, fontweight='bold')

    # Label
    ax4.text(center_x, fc_y - 0.5, "p95-Trastuzumab-Biparatopic", ha='center', va='top',
             fontsize=10, fontweight='bold', color='purple')

    # Binding arrows
    ax4.annotate('', xy=(3, 5.1), xytext=(center_x - 1.5, fc_y + 3.2),
                arrowprops=dict(arrowstyle='->', color='blue', lw=2))
    ax4.annotate('', xy=(12.3, 6.5), xytext=(center_x + 1.5, fc_y + 3.2),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2))

    # Advantages box
    ax4.text(8, 0.8, "Kd: 0.08 nM | ADC Score: 9.5/10 | Internalization: 65%\nTargets BOTH p95+ and FL-HER2+ tumor cells | BEST OVERALL",
             ha='center', va='center', fontsize=10, fontweight='bold', color='purple',
             bbox=dict(boxstyle='round', facecolor='#E6E6FA', edgecolor='purple', linewidth=2))

    # ========== PANEL E: Comparison Table ==========
    ax5 = fig.add_subplot(gs[1, 2])
    ax5.set_xlim(0, 10)
    ax5.set_ylim(0, 12)
    ax5.axis('off')
    ax5.set_title('E. ADC Suitability Comparison\n(Pipeline-Predicted)', fontsize=12, fontweight='bold', loc='left')

    # Comparison bars - Updated with new pipeline predictions
    mabs = ['p95-Tras-Biparatopic', 'Zanidatamab', 'p95-ESM-002', 'p95-ESM-001', 'p95-ESM-004', 'p95-ESM-003']
    scores = [9.5, 9.5, 9.0, 9.0, 9.0, 8.0]
    p95_binding = [True, False, True, True, True, True]
    colors = ['#DDA0DD', '#E6E6FA', '#87CEEB', '#90EE90', '#FFB6C1', '#FFA07A']
    kd_values = ['0.08', '0.50', '0.13', '0.21', '0.20', '0.33']

    bar_height = 0.8
    y_positions = np.arange(len(mabs)) * 1.5 + 1.5

    for i, (mab, score, p95, color, kd) in enumerate(zip(mabs, scores, p95_binding, colors, kd_values)):
        # Bar
        bar_width = score * 0.85
        ax5.add_patch(FancyBboxPatch((1, y_positions[i]), bar_width, bar_height,
                                     boxstyle="round,pad=0.02", facecolor=color,
                                     edgecolor='black', linewidth=1))
        # Score label
        ax5.text(bar_width + 1.2, y_positions[i] + bar_height/2, f"{score}/10",
                ha='left', va='center', fontsize=9, fontweight='bold')
        # mAb name
        ax5.text(0.9, y_positions[i] + bar_height/2, mab, ha='right', va='center', fontsize=7)
        # p95 binding indicator
        if p95:
            ax5.text(9.5, y_positions[i] + bar_height/2, f"✓ {kd}nM", ha='center', va='center',
                    fontsize=7, color='green', fontweight='bold')
        else:
            ax5.text(9.5, y_positions[i] + bar_height/2, f"✗ {kd}nM", ha='center', va='center',
                    fontsize=7, color='gray')

    ax5.text(5, 11.5, "ADC Suitability Score", ha='center', va='center', fontsize=11, fontweight='bold')
    ax5.axvline(x=9, ymin=0.1, ymax=0.9, color='gray', linestyle='--', alpha=0.5)
    ax5.text(9.5, 0.5, "p95 | Kd", ha='center', va='center', fontsize=7, color='gray')

    plt.tight_layout()
    return fig

def create_epitope_binding_detail():
    """Create detailed epitope-binding visualization for pipeline-predicted mAbs."""
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    fig.suptitle('Pipeline-Predicted p95-HER2 mAbs: Epitope Binding Detail', fontsize=16, fontweight='bold')

    epitopes = [
        {"name": "p95-ESM-001", "region": "615-635", "seq": "MPIWKFPDEEGACQPCPINC",
         "cdr_h3": "ARDPIWKFPDYAMDY", "cdr_l3": "QQGACQPLT", "color": "#90EE90", "kd": "0.21", "strategy": "Epitope Mimicry"},
        {"name": "p95-ESM-002", "region": "615-635", "seq": "MPIWKFPDEEGACQPCPINC",
         "cdr_h3": "ARDRKEYWFDY", "cdr_l3": "QQFPDEEGT", "color": "#87CEEB", "kd": "0.13", "strategy": "Charge Complementarity"},
        {"name": "p95-ESM-003", "region": "640-652", "seq": "CTHSCVDLDDKGC",
         "cdr_h3": "ARCTHSCVDYFDY", "cdr_l3": "QQDLDKGCT", "color": "#FFA07A", "kd": "0.33", "strategy": "Hydrophobic Targeting"},
        {"name": "p95-ESM-004", "region": "611-625", "seq": "MPIWKFPDEEGACQP",
         "cdr_h3": "ARMETPIWKFDY", "cdr_l3": "QQMPIWFPT", "color": "#FFB6C1", "kd": "0.20", "strategy": "Neo-epitope Specific"}
    ]

    for ax, epi in zip(axes.flatten(), epitopes):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

        # Title
        ax.set_title(f'{epi["name"]} ({epi["strategy"]})\nEpitope: {epi["region"]}', fontsize=11, fontweight='bold')

        # Epitope sequence display
        ax.add_patch(FancyBboxPatch((1, 6), 8, 1.5, boxstyle="round,pad=0.1",
                                    facecolor='#FFFACD', edgecolor='black', linewidth=2))
        ax.text(5, 6.75, f'Epitope: {epi["seq"]}', ha='center', va='center',
               fontsize=8, family='monospace', fontweight='bold')

        # CDR-H3 binding representation
        ax.add_patch(FancyBboxPatch((1.5, 4), 7, 1.2, boxstyle="round,pad=0.1",
                                    facecolor=epi["color"], edgecolor='black', linewidth=2))
        ax.text(5, 4.6, f'CDR-H3: {epi["cdr_h3"]}', ha='center', va='center',
               fontsize=8, family='monospace', fontweight='bold')

        # CDR-L3 binding representation
        ax.add_patch(FancyBboxPatch((2, 2.5), 6, 1.0, boxstyle="round,pad=0.1",
                                    facecolor=epi["color"], edgecolor='black', linewidth=1.5, alpha=0.7))
        ax.text(5, 3, f'CDR-L3: {epi["cdr_l3"]}', ha='center', va='center',
               fontsize=8, family='monospace')

        # Binding interaction lines
        for i in range(5):
            x_pos = 2.5 + i * 1.2
            ax.plot([x_pos, x_pos], [5.2, 6], 'k--', linewidth=1, alpha=0.5)
            ax.plot([x_pos], [5.5], 'ro', markersize=4)

        # Binding affinity
        ax.text(5, 1.2, f"Predicted Kd: {epi['kd']} nM", ha='center', va='center',
               fontsize=11, fontweight='bold', color='darkblue')
        ax.text(5, 0.6, f"AlphaFold pLDDT > 84", ha='center', va='center',
               fontsize=9, style='italic', color='gray')

    plt.tight_layout()
    return fig

def create_mab_evaluation_figure():
    """Create p95 mAb ADC evaluation figure with pipeline predictions."""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_title('p95-HER2 Pipeline-Predicted mAb ADC Evaluation', fontsize=16, fontweight='bold')

    # Data for pipeline-predicted mAbs
    mabs = ['p95-Tras-\nBiparatopic', 'p95-ESM-002\n(TOP)', 'p95-ESM-001', 'p95-ESM-004', 'p95-ESM-003', 'Zanidatamab\n(Reference)', 'T-DXd\n(Reference)']
    scores = [9.5, 9.0, 9.0, 9.0, 8.0, 9.5, 8.8]
    kd_values = [0.08, 0.13, 0.21, 0.20, 0.33, 0.50, 5.0]
    internalization = [65, 50, 40, 55, 25, 70, 25]
    p95_binding = [True, True, True, True, True, False, False]

    colors = ['#DDA0DD', '#87CEEB', '#90EE90', '#FFB6C1', '#FFA07A', '#E6E6FA', '#96CEB4']

    x = np.arange(len(mabs))
    width = 0.25

    # Create grouped bars
    bars1 = ax.bar(x - width, scores, width, label='ADC Score (/10)', color=colors, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x, [k*10 for k in kd_values], width, label='Kd (nM × 10)', color='lightgray', edgecolor='black', linewidth=1)
    bars3 = ax.bar(x + width, [i/10 for i in internalization], width, label='Internalization (% / 10)', color='gold', edgecolor='black', linewidth=1)

    ax.set_ylabel('Score / Value', fontsize=12)
    ax.set_xlabel('Monoclonal Antibody', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(mabs, fontsize=9)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 12)

    # Add p95 binding indicators
    for i, (p95, score) in enumerate(zip(p95_binding, scores)):
        if p95:
            ax.text(i - width, score + 0.3, '✓p95', ha='center', va='bottom', fontsize=8, color='green', fontweight='bold')
        else:
            ax.text(i - width, score + 0.3, '✗p95', ha='center', va='bottom', fontsize=8, color='red')

    # Add value labels on bars
    for i, (bar, kd) in enumerate(zip(bars2, kd_values)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'{kd}nM',
                ha='center', va='bottom', fontsize=7, rotation=45)

    ax.axhline(y=9, color='green', linestyle='--', alpha=0.5, label='High ADC suitability threshold')
    ax.text(6.5, 9.2, 'High suitability threshold', fontsize=8, color='green')

    plt.tight_layout()
    return fig

def main():
    os.makedirs("../images", exist_ok=True)

    print("Generating pipeline-predicted p95-HER2 docking visualization images...")

    # Main docking figure
    fig1 = create_p95_docking_figure()
    fig1.savefig("../images/p95_mab_docking.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig1)
    print("Saved: images/p95_mab_docking.png")

    # Epitope binding detail
    fig2 = create_epitope_binding_detail()
    fig2.savefig("../images/p95_epitope_binding_detail.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig2)
    print("Saved: images/p95_epitope_binding_detail.png")

    # mAb evaluation figure
    fig3 = create_mab_evaluation_figure()
    fig3.savefig("../images/p95_mab_evaluation.png", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig3)
    print("Saved: images/p95_mab_evaluation.png")

    print("\nPipeline-predicted docking images generated successfully!")

if __name__ == "__main__":
    main()
