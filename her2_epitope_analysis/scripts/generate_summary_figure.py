#!/usr/bin/env python3
"""
Generate comprehensive project summary figure for HER2 Epitope Analysis.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

def create_project_summary():
    """Create comprehensive multi-panel summary figure."""

    fig = plt.figure(figsize=(20, 16))

    # Main title
    fig.suptitle('HER2 Epitope Analysis for ADC Binder Design\nFull-Length vs p95-HER2 Targeting Strategies',
                 fontsize=18, fontweight='bold', y=0.98)

    # Create 2x3 grid of subplots
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.25,
                          left=0.05, right=0.95, top=0.92, bottom=0.05)

    # ========== PANEL A: HER2 Full-Length Structure ==========
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 12)
    ax1.axis('off')
    ax1.set_title('A. HER2 Full-Length Structure', fontsize=12, fontweight='bold', loc='left')

    # Draw domains
    domains = [
        {"name": "Domain I\n(23-195)", "y": 9, "h": 1.5, "color": "#FF6B6B"},
        {"name": "Domain II\n(196-319)", "y": 7.2, "h": 1.5, "color": "#4ECDC4"},
        {"name": "Domain III\n(320-488)", "y": 5.4, "h": 1.5, "color": "#45B7D1"},
        {"name": "Domain IV\n(489-630)", "y": 3.6, "h": 1.5, "color": "#96CEB4"},
    ]
    for d in domains:
        ax1.add_patch(FancyBboxPatch((3, d["y"]), 4, d["h"], boxstyle="round,pad=0.05",
                                     facecolor=d["color"], edgecolor="black", linewidth=2))
        ax1.text(5, d["y"]+d["h"]/2, d["name"], ha='center', va='center', fontsize=9, fontweight='bold')

    # JM, TM, Kinase
    ax1.add_patch(FancyBboxPatch((3, 2.4), 4, 0.9, boxstyle="round,pad=0.02",
                                 facecolor="#FFE4B5", edgecolor="black", linewidth=1.5))
    ax1.text(5, 2.85, "JM (611-652)", ha='center', va='center', fontsize=8)

    ax1.axhline(y=2.2, xmin=0.3, xmax=0.7, color='brown', linewidth=4)
    ax1.text(5, 2.0, "Membrane", ha='center', va='center', fontsize=8)

    ax1.add_patch(FancyBboxPatch((3, 0.5), 4, 1.3, boxstyle="round,pad=0.05",
                                 facecolor="#DDA0DD", edgecolor="black", linewidth=2))
    ax1.text(5, 1.15, "Kinase\n(720-987)", ha='center', va='center', fontsize=9)

    ax1.text(5, 11.2, "Full-length HER2\n(185 kDa)", ha='center', va='center', fontsize=11, fontweight='bold')

    # ========== PANEL B: Approved mAbs ==========
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 12)
    ax2.axis('off')
    ax2.set_title('B. Approved mAbs & ADCs', fontsize=12, fontweight='bold', loc='left')

    # Simplified HER2
    ax2.add_patch(FancyBboxPatch((4, 8), 3, 1, boxstyle="round,pad=0.02",
                                 facecolor="#4ECDC4", edgecolor="black", linewidth=1.5))
    ax2.text(5.5, 8.5, "Dom II", ha='center', va='center', fontsize=8)

    ax2.add_patch(FancyBboxPatch((4, 5), 3, 1, boxstyle="round,pad=0.02",
                                 facecolor="#96CEB4", edgecolor="black", linewidth=1.5))
    ax2.text(5.5, 5.5, "Dom IV", ha='center', va='center', fontsize=8)

    ax2.add_patch(FancyBboxPatch((4, 2), 3, 2.5, boxstyle="round,pad=0.02",
                                 facecolor="#D3D3D3", edgecolor="black", linewidth=1.5))
    ax2.text(5.5, 3.25, "TM+Kinase", ha='center', va='center', fontsize=8)

    # Pertuzumab binding Domain II
    ax2.annotate('', xy=(7.2, 8.5), xytext=(9, 9.5),
                arrowprops=dict(arrowstyle='->', color='orange', lw=2))
    ax2.add_patch(FancyBboxPatch((9, 9), 2.5, 1.2, boxstyle="round,pad=0.05",
                                 facecolor="#FFA07A", edgecolor="black", linewidth=2))
    ax2.text(10.25, 9.6, "Pertuzumab", ha='center', va='center', fontsize=8, fontweight='bold')

    # Trastuzumab/ADCs binding Domain IV
    ax2.annotate('', xy=(7.2, 5.5), xytext=(9, 5.5),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2))
    ax2.add_patch(FancyBboxPatch((9, 4.5), 2.5, 2.5, boxstyle="round,pad=0.05",
                                 facecolor="#DDA0DD", edgecolor="black", linewidth=2))
    ax2.text(10.25, 6.2, "Trastuzumab", ha='center', va='center', fontsize=8, fontweight='bold')
    ax2.text(10.25, 5.5, "T-DM1 (ADC)", ha='center', va='center', fontsize=7)
    ax2.text(10.25, 4.9, "T-DXd (ADC)", ha='center', va='center', fontsize=7)

    # ADC details
    ax2.text(5.5, 11, "Approved HER2-targeting\nAntibodies & ADCs", ha='center', va='center',
             fontsize=10, fontweight='bold')
    ax2.text(1, 1.5, "T-DM1: Non-cleavable linker\nT-DXd: Cleavable linker, DAR=8",
             ha='left', va='center', fontsize=8, style='italic')

    # ========== PANEL C: p95-HER2 ==========
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 12)
    ax3.axis('off')
    ax3.set_title('C. p95-HER2 Truncated Form', fontsize=12, fontweight='bold', loc='left')

    # Missing ECD (dashed)
    ax3.add_patch(FancyBboxPatch((3, 4.5), 4, 6, boxstyle="round,pad=0.05",
                                 facecolor="white", edgecolor="red", linewidth=2, linestyle='--'))
    ax3.text(5, 7.5, "MISSING\nDomains I-IV", ha='center', va='center',
             fontsize=11, color='red', fontweight='bold')

    # Red X
    ax3.plot([3.5, 6.5], [5, 10], 'r-', linewidth=3, alpha=0.7)
    ax3.plot([3.5, 6.5], [10, 5], 'r-', linewidth=3, alpha=0.7)

    # Remaining JM stub
    ax3.add_patch(FancyBboxPatch((3, 3), 4, 1.2, boxstyle="round,pad=0.02",
                                 facecolor="#FFFF99", edgecolor="black", linewidth=2))
    ax3.text(5, 3.6, "JM Stub (611-652)\n~42 aa only", ha='center', va='center', fontsize=8, fontweight='bold')

    # TM + Kinase
    ax3.axhline(y=2.8, xmin=0.3, xmax=0.7, color='brown', linewidth=4)
    ax3.add_patch(FancyBboxPatch((3, 0.5), 4, 2, boxstyle="round,pad=0.05",
                                 facecolor="#DDA0DD", edgecolor="black", linewidth=2))
    ax3.text(5, 1.5, "Kinase\n(retained)", ha='center', va='center', fontsize=9)

    ax3.text(5, 11.2, "p95-HER2 (95 kDa)", ha='center', va='center',
             fontsize=11, fontweight='bold', color='red')
    ax3.text(5, 0.1, "NO Trastuzumab/ADC binding!", ha='center', va='center',
             fontsize=9, color='red', fontweight='bold')

    # ========== PANEL D: Novel mAbs for p95 ==========
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    ax4.axis('off')
    ax4.set_title('D. Predicted Novel mAbs for p95-HER2', fontsize=12, fontweight='bold', loc='left')

    # JM stub zoomed
    ax4.add_patch(FancyBboxPatch((2, 4), 6, 3, boxstyle="round,pad=0.05",
                                 facecolor="#FFFF99", edgecolor="black", linewidth=2))
    ax4.text(5, 5.5, "Juxtamembrane Stub\n(611-652)", ha='center', va='center', fontsize=10, fontweight='bold')

    # Membrane
    ax4.axhline(y=3.5, xmin=0.2, xmax=0.8, color='brown', linewidth=4)
    ax4.text(5, 3.2, "Membrane", ha='center', va='center', fontsize=8)

    # Predicted mAbs
    mabs = [
        {"name": "p95-mAb-001\n(615-635)", "x": 0.5, "y": 7, "color": "#90EE90", "score": "6.5"},
        {"name": "p95-mAb-002\n(Neo: 611-625)", "x": 0.5, "y": 5.5, "color": "#87CEEB", "score": "5.0"},
        {"name": "p95-Bispecific\n(JM+DomIV)", "x": 7, "y": 6.5, "color": "#DDA0DD", "score": "8.5"},
    ]
    for mab in mabs:
        ax4.add_patch(FancyBboxPatch((mab["x"], mab["y"]-0.5), 2.3, 1.2, boxstyle="round,pad=0.05",
                                     facecolor=mab["color"], edgecolor="black", linewidth=1.5))
        ax4.text(mab["x"]+1.15, mab["y"]+0.1, mab["name"], ha='center', va='center', fontsize=7, fontweight='bold')
        ax4.text(mab["x"]+1.15, mab["y"]-0.3, f"Score: {mab['score']}/10", ha='center', va='center', fontsize=7)

        # Arrow to binding site
        if mab["x"] < 3:
            ax4.annotate('', xy=(2, 5.5), xytext=(mab["x"]+2.3, mab["y"]),
                        arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))

    ax4.text(5, 9.2, "Bispecific approach\nmost promising (8.5/10)", ha='center', va='center',
             fontsize=9, color='purple', fontweight='bold')

    # ========== PANEL E: Internalization Comparison ==========
    ax5 = fig.add_subplot(gs[1, 1])

    epitopes = ['Domain IV\n(Trastuzumab)', 'Domain II\n(Pertuzumab)', 'Biparatopic\n(Zanidatamab)']
    internalization = [25, 15, 70]
    colors = ['#96CEB4', '#4ECDC4', '#DDA0DD']

    bars = ax5.bar(epitopes, internalization, color=colors, edgecolor='black', linewidth=2)
    ax5.set_ylabel('% Internalized at 4h', fontsize=11)
    ax5.set_title('E. Internalization Comparison', fontsize=12, fontweight='bold', loc='left')
    ax5.set_ylim(0, 100)

    for bar, val in zip(bars, internalization):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Highlight best
    ax5.annotate('Best for ADC!', xy=(2, 70), xytext=(2.3, 85),
                fontsize=10, fontweight='bold', color='purple',
                arrowprops=dict(arrowstyle='->', color='purple', lw=2))

    ax5.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    ax5.text(2.5, 52, 'Target: >50%', fontsize=8, color='gray')

    # ========== PANEL F: Resistance Mechanisms ==========
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_xlim(0, 10)
    ax6.set_ylim(0, 10)
    ax6.axis('off')
    ax6.set_title('F. Resistance Mechanisms & Solutions', fontsize=12, fontweight='bold', loc='left')

    # Flowchart boxes
    # Start
    ax6.add_patch(FancyBboxPatch((3, 8.5), 4, 1, boxstyle="round,pad=0.1",
                                 facecolor="#E6E6FA", edgecolor="black", linewidth=2))
    ax6.text(5, 9, "HER2+ Cancer", ha='center', va='center', fontsize=9, fontweight='bold')

    # Decision
    ax6.annotate('', xy=(5, 8.5), xytext=(5, 7.7),
                arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax6.add_patch(FancyBboxPatch((2.5, 6.5), 5, 1, boxstyle="round,pad=0.1",
                                 facecolor="#FFFACD", edgecolor="black", linewidth=2))
    ax6.text(5, 7, "HER2 Status?", ha='center', va='center', fontsize=9, fontweight='bold')

    # Branch 1: Full-length (green)
    ax6.annotate('', xy=(2.5, 7), xytext=(1, 5.2),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.5))
    ax6.add_patch(FancyBboxPatch((0, 4.2), 2.5, 1.5, boxstyle="round,pad=0.05",
                                 facecolor="#90EE90", edgecolor="green", linewidth=2))
    ax6.text(1.25, 5.2, "Full-length\n(70%)", ha='center', va='center', fontsize=8)
    ax6.text(1.25, 4.5, "ADCs work!", ha='center', va='center', fontsize=7, color='green', fontweight='bold')

    # Branch 2: Downregulated (orange)
    ax6.annotate('', xy=(5, 6.5), xytext=(5, 5.2),
                arrowprops=dict(arrowstyle='->', color='orange', lw=1.5))
    ax6.add_patch(FancyBboxPatch((3.5, 4.2), 3, 1.5, boxstyle="round,pad=0.05",
                                 facecolor="#FFD700", edgecolor="orange", linewidth=2))
    ax6.text(5, 5.2, "Downregulated\n(15-30%)", ha='center', va='center', fontsize=8)
    ax6.text(5, 4.5, "T-DXd bystander", ha='center', va='center', fontsize=7, color='orange')

    # Branch 3: p95-HER2 (red)
    ax6.annotate('', xy=(7.5, 7), xytext=(8.5, 5.2),
                arrowprops=dict(arrowstyle='->', color='red', lw=1.5))
    ax6.add_patch(FancyBboxPatch((7, 4.2), 2.8, 1.5, boxstyle="round,pad=0.05",
                                 facecolor="#FFB6C1", edgecolor="red", linewidth=2))
    ax6.text(8.4, 5.2, "p95-HER2\n(30-50%)", ha='center', va='center', fontsize=8)
    ax6.text(8.4, 4.5, "ADCs FAIL", ha='center', va='center', fontsize=7, color='red', fontweight='bold')

    # Solution for p95
    ax6.annotate('', xy=(8.4, 4.2), xytext=(8.4, 2.8),
                arrowprops=dict(arrowstyle='->', color='purple', lw=1.5))
    ax6.add_patch(FancyBboxPatch((6.5, 1.5), 3.3, 1.2, boxstyle="round,pad=0.05",
                                 facecolor="#DDA0DD", edgecolor="purple", linewidth=2))
    ax6.text(8.15, 2.1, "Solution:\nBispecific ADC\nor TKI", ha='center', va='center', fontsize=8, fontweight='bold')

    # Legend
    ax6.text(1, 2.5, "Patient Coverage:", ha='left', va='center', fontsize=8, fontweight='bold')
    ax6.text(1, 1.8, "• Full-length: ~70%", ha='left', va='center', fontsize=7, color='green')
    ax6.text(1, 1.3, "• Downregulated: 15-30%", ha='left', va='center', fontsize=7, color='orange')
    ax6.text(1, 0.8, "• p95-HER2: 30-50%", ha='left', va='center', fontsize=7, color='red')

    plt.tight_layout()
    return fig


def main():
    print("Generating HER2 Project Summary Figure...")
    fig = create_project_summary()
    output_path = "images/project_summary.png"
    fig.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved: {output_path}")
    print("\nFigure includes:")
    print("  A. HER2 Full-Length Structure (4 domains)")
    print("  B. Approved mAbs & ADCs (Trastuzumab, Pertuzumab, T-DM1, T-DXd)")
    print("  C. p95-HER2 Truncated Form (missing ECD)")
    print("  D. Predicted Novel mAbs for p95-HER2")
    print("  E. Internalization Comparison (25% vs 70%)")
    print("  F. Resistance Mechanisms & Solutions")


if __name__ == "__main__":
    main()
