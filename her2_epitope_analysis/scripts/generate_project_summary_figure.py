#!/usr/bin/env python3
"""
Generate Publication-Quality HER2 Project Summary Figure.

Uses scientific-visualization skill best practices:
- Colorblind-friendly Okabe-Ito palette
- Publication-ready typography (Arial/Helvetica)
- Clean multi-panel layout with proper panel labels
- 300 DPI for raster output
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle, Polygon
from matplotlib.gridspec import GridSpec
import numpy as np
import os
import sys

# Add skills path for imports
sys.path.insert(0, os.path.expanduser('~/.claude/skills/scientific-visualization/scripts'))
sys.path.insert(0, os.path.expanduser('~/.claude/skills/scientific-visualization/assets'))

# Okabe-Ito colorblind-friendly palette
OKABE_ITO = {
    'orange': '#E69F00',
    'sky_blue': '#56B4E9',
    'bluish_green': '#009E73',
    'yellow': '#F0E442',
    'blue': '#0072B2',
    'vermillion': '#D55E00',
    'reddish_purple': '#CC79A7',
    'black': '#000000'
}

# Domain colors using Okabe-Ito
DOMAIN_COLORS = {
    'DomI': OKABE_ITO['orange'],
    'DomII': OKABE_ITO['sky_blue'],
    'DomIII': OKABE_ITO['bluish_green'],
    'DomIV': OKABE_ITO['reddish_purple'],
    'JM': OKABE_ITO['reddish_purple'],
    'TM': '#888888',
    'Kinase': OKABE_ITO['yellow'],
}


def apply_publication_style():
    """Apply publication-quality matplotlib settings."""
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'font.size': 8,
        'axes.labelsize': 9,
        'axes.titlesize': 10,
        'axes.linewidth': 0.8,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'xtick.labelsize': 7,
        'ytick.labelsize': 7,
        'xtick.major.width': 0.8,
        'ytick.major.width': 0.8,
        'legend.fontsize': 7,
        'legend.frameon': False,
        'figure.facecolor': 'white',
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.facecolor': 'white',
    })


def draw_her2_domain_structure(ax, x_center=0.5, y_base=0.1, width=0.25, title="Full-Length HER2"):
    """Draw HER2 domain structure schematically."""

    domain_height = 0.12
    gap = 0.02

    # Domain positions (bottom to top: Kinase -> TM -> DomIV -> DomIII -> DomII -> DomI)
    domains = [
        ('Kinase', 'Kinase\nDomain', DOMAIN_COLORS['Kinase'], 1.0),
        ('TM', 'TM', DOMAIN_COLORS['TM'], 0.3),
        ('DomIV', 'Domain IV\n(489-630)', DOMAIN_COLORS['DomIV'], 1.0),
        ('DomIII', 'Domain III\n(320-488)', DOMAIN_COLORS['DomIII'], 1.0),
        ('DomII', 'Domain II\n(196-319)', DOMAIN_COLORS['DomII'], 1.0),
        ('DomI', 'Domain I\n(23-195)', DOMAIN_COLORS['DomI'], 1.0),
    ]

    y_pos = y_base
    domain_boxes = {}

    for dom_id, label, color, width_frac in domains:
        box_width = width * width_frac
        x_pos = x_center - box_width/2

        rect = FancyBboxPatch(
            (x_pos, y_pos), box_width, domain_height,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor=color, edgecolor='black', linewidth=0.8,
            alpha=0.9, zorder=2
        )
        ax.add_patch(rect)

        # Label
        if dom_id == 'TM':
            ax.text(x_center, y_pos + domain_height/2, label,
                   fontsize=6, ha='center', va='center', fontweight='bold', zorder=3)
        else:
            ax.text(x_center, y_pos + domain_height/2, label,
                   fontsize=7, ha='center', va='center', fontweight='bold', zorder=3)

        domain_boxes[dom_id] = (x_pos, y_pos, box_width, domain_height)
        y_pos += domain_height + gap

    # Add membrane line
    membrane_y = y_base + domain_height + gap + domain_height/2
    ax.axhline(y=membrane_y, xmin=0.1, xmax=0.9, color='#666666',
               linestyle='--', linewidth=1, zorder=1)
    ax.text(0.92, membrane_y, 'Membrane', fontsize=6, va='center', color='#666666')

    # Title
    ax.text(x_center, y_pos + 0.02, title, fontsize=10, ha='center',
            va='bottom', fontweight='bold')

    return domain_boxes


def draw_p95_structure(ax, x_center=0.5, y_base=0.1, width=0.25):
    """Draw p95-HER2 truncated structure."""

    domain_height = 0.12
    gap = 0.02

    # p95 only has: Kinase, TM, and small JM stub
    domains = [
        ('Kinase', 'Kinase\n(Active)', DOMAIN_COLORS['Kinase'], 1.0),
        ('TM', 'TM', DOMAIN_COLORS['TM'], 0.3),
        ('JM', 'JM Stub\n(611-652)', DOMAIN_COLORS['JM'], 0.5),
    ]

    y_pos = y_base

    for dom_id, label, color, width_frac in domains:
        box_width = width * width_frac
        x_pos = x_center - box_width/2

        rect = FancyBboxPatch(
            (x_pos, y_pos), box_width, domain_height,
            boxstyle="round,pad=0.01,rounding_size=0.02",
            facecolor=color, edgecolor='black', linewidth=0.8,
            alpha=0.9, zorder=2
        )
        ax.add_patch(rect)

        fontsize = 6 if dom_id == 'TM' else 7
        ax.text(x_center, y_pos + domain_height/2, label,
               fontsize=fontsize, ha='center', va='center', fontweight='bold', zorder=3)

        y_pos += domain_height + gap

    # Draw "lost" ECD region with dashed outline
    lost_height = 4 * (domain_height + gap)
    lost_rect = FancyBboxPatch(
        (x_center - width/2, y_pos), width, lost_height,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        facecolor='white', edgecolor=OKABE_ITO['vermillion'],
        linewidth=1.5, linestyle='--', alpha=0.3, zorder=1
    )
    ax.add_patch(lost_rect)
    ax.text(x_center, y_pos + lost_height/2, 'ECD LOST\n(Domains I-IV)',
           fontsize=8, ha='center', va='center', color=OKABE_ITO['vermillion'],
           fontweight='bold', zorder=3)

    # Membrane line
    membrane_y = y_base + domain_height + gap + domain_height/2
    ax.axhline(y=membrane_y, xmin=0.1, xmax=0.9, color='#666666',
               linestyle='--', linewidth=1, zorder=1)

    # Title
    ax.text(x_center, y_pos + lost_height + 0.02, 'p95-HER2\n(Truncated)',
           fontsize=10, ha='center', va='bottom', fontweight='bold')


def draw_mab_binding(ax, domain_boxes, mab_name, target_domain, side='left', color=None):
    """Draw mAb binding to a domain."""

    x, y, w, h = domain_boxes[target_domain]

    if side == 'left':
        arrow_start_x = x - 0.12
        arrow_end_x = x - 0.02
        text_x = arrow_start_x - 0.02
        ha = 'right'
    else:
        arrow_start_x = x + w + 0.12
        arrow_end_x = x + w + 0.02
        text_x = arrow_start_x + 0.02
        ha = 'left'

    arrow_y = y + h/2

    # Arrow
    ax.annotate('', xy=(arrow_end_x, arrow_y), xytext=(arrow_start_x, arrow_y),
               arrowprops=dict(arrowstyle='->', color=color or OKABE_ITO['blue'],
                              lw=1.5, connectionstyle='arc3'))

    # Label
    ax.text(text_x, arrow_y, mab_name, fontsize=7, ha=ha, va='center',
           color=color or OKABE_ITO['blue'], fontweight='bold')


def draw_internalization_bar_chart(ax):
    """Draw internalization rate comparison bar chart."""

    categories = ['Domain IV\n(Trastuzumab)', 'Domain II\n(Pertuzumab)',
                  'Biparatopic\n(Zanidatamab)', 'p95-Bispecific\n(Predicted)']
    values = [25, 15, 70, 60]
    colors = [OKABE_ITO['reddish_purple'], OKABE_ITO['sky_blue'],
              OKABE_ITO['bluish_green'], OKABE_ITO['orange']]

    bars = ax.bar(range(len(categories)), values, color=colors, edgecolor='black', linewidth=0.8)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
               f'{val}%', ha='center', va='bottom', fontsize=7, fontweight='bold')

    ax.set_xticks(range(len(categories)))
    ax.set_xticklabels(categories, fontsize=7)
    ax.set_ylabel('Internalization Rate (%)', fontsize=8)
    ax.set_ylim(0, 85)
    ax.set_title('Epitope-Dependent Internalization', fontsize=9, fontweight='bold')

    # Add reference line for "good ADC threshold"
    ax.axhline(y=50, color='gray', linestyle=':', linewidth=1, alpha=0.7)
    ax.text(3.5, 52, 'ADC threshold', fontsize=6, color='gray', ha='right')


def draw_biparatopic_concept(ax):
    """Draw biparatopic ADC concept schematic."""

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Draw tumor cell
    cell = FancyBboxPatch((0.1, 0.05), 0.8, 0.45,
                          boxstyle="round,pad=0.02,rounding_size=0.05",
                          facecolor='#FFFDE7', edgecolor='#666666',
                          linewidth=1, alpha=0.7, zorder=1)
    ax.add_patch(cell)
    ax.text(0.5, 0.02, 'Tumor Cell', fontsize=8, ha='center', fontweight='bold')

    # Draw FL-HER2 receptors (left side)
    for x_pos in [0.22, 0.35]:
        # ECD stack
        rect = Rectangle((x_pos-0.025, 0.35), 0.05, 0.25,
                         facecolor=OKABE_ITO['sky_blue'], edgecolor='black',
                         linewidth=0.5, zorder=2)
        ax.add_patch(rect)
        ax.text(x_pos, 0.47, 'FL', fontsize=6, ha='center', va='center', fontweight='bold')

    # Draw p95-HER2 receptors (right side)
    for x_pos in [0.60, 0.73]:
        # Small JM stub
        rect = Rectangle((x_pos-0.02, 0.35), 0.04, 0.10,
                         facecolor=OKABE_ITO['reddish_purple'], edgecolor='black',
                         linewidth=0.5, zorder=2)
        ax.add_patch(rect)
        ax.text(x_pos, 0.40, 'p95', fontsize=5, ha='center', va='center', fontweight='bold')

    # Draw bispecific antibody (Y-shape connecting both)
    # Central Fc region
    fc_rect = FancyBboxPatch((0.42, 0.68), 0.12, 0.08,
                             boxstyle="round,pad=0.01",
                             facecolor='#DDA0DD', edgecolor='black',
                             linewidth=0.8, zorder=3)
    ax.add_patch(fc_rect)
    ax.text(0.48, 0.72, 'Fc', fontsize=6, ha='center', va='center', fontweight='bold')

    # Arms to FL-HER2
    ax.plot([0.42, 0.285], [0.72, 0.72], color=OKABE_ITO['blue'], linewidth=2, zorder=2)
    ax.plot([0.285, 0.285], [0.72, 0.60], color=OKABE_ITO['blue'], linewidth=2, zorder=2)
    ax.add_patch(Circle((0.285, 0.60), 0.02, facecolor=OKABE_ITO['blue'],
                        edgecolor='black', linewidth=0.5, zorder=3))

    # Arms to p95-HER2
    ax.plot([0.54, 0.665], [0.72, 0.72], color=OKABE_ITO['vermillion'], linewidth=2, zorder=2)
    ax.plot([0.665, 0.665], [0.72, 0.45], color=OKABE_ITO['vermillion'], linewidth=2, zorder=2)
    ax.add_patch(Circle((0.665, 0.45), 0.02, facecolor=OKABE_ITO['vermillion'],
                        edgecolor='black', linewidth=0.5, zorder=3))

    # Payload (DXd)
    ax.add_patch(Circle((0.48, 0.82), 0.025, facecolor=OKABE_ITO['vermillion'],
                        edgecolor='black', linewidth=0.5, zorder=4))
    ax.text(0.48, 0.88, 'DXd', fontsize=6, ha='center', color=OKABE_ITO['vermillion'],
           fontweight='bold')

    # Labels
    ax.text(0.285, 0.95, 'p95-Bispecific-001', fontsize=9, ha='center',
           fontweight='bold', color=OKABE_ITO['blue'])

    # Legend box
    legend_text = (
        "Targets both:\n"
        "  FL-HER2 (Domain IV)\n"
        "  p95-HER2 (JM stub)\n"
        "ADC Score: 8.5/10"
    )
    ax.text(0.95, 0.25, legend_text, fontsize=6, ha='right', va='center',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9',
                    edgecolor=OKABE_ITO['bluish_green'], linewidth=0.8))


def draw_key_statistics(ax):
    """Draw key statistics panel."""

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, 'Key Findings', fontsize=10, ha='center',
           fontweight='bold', va='top')

    # Statistics
    stats = [
        ('p95-HER2 Prevalence', '30-50%', 'of HER2+ breast cancer'),
        ('Trastuzumab Resistant', '20-50%', 'express p95-HER2'),
        ('US Patient Population', '~50,000', 'patients/year'),
        ('Clinical Development', '0', 'p95-specific ADCs'),
    ]

    y_pos = 0.80
    for title, value, subtitle in stats:
        ax.text(0.5, y_pos, title, fontsize=8, ha='center', fontweight='bold')
        ax.text(0.5, y_pos - 0.08, value, fontsize=14, ha='center',
               fontweight='bold', color=OKABE_ITO['blue'])
        ax.text(0.5, y_pos - 0.15, subtitle, fontsize=7, ha='center', color='#666666')
        y_pos -= 0.23

    # Highlight box
    highlight = FancyBboxPatch((0.05, 0.02), 0.9, 0.12,
                               boxstyle="round,pad=0.02",
                               facecolor='#FFF3E0', edgecolor=OKABE_ITO['orange'],
                               linewidth=1, zorder=1)
    ax.add_patch(highlight)
    ax.text(0.5, 0.08, 'First-in-class p95-HER2 ADC opportunity',
           fontsize=8, ha='center', va='center', fontweight='bold',
           color=OKABE_ITO['vermillion'])


def create_summary_figure():
    """Create the complete publication-quality summary figure."""

    apply_publication_style()

    # Create figure with GridSpec layout
    fig = plt.figure(figsize=(11, 8))
    gs = GridSpec(2, 3, figure=fig, height_ratios=[1.2, 1],
                  width_ratios=[1, 1, 0.8], hspace=0.35, wspace=0.3)

    # Panel A: Full-length HER2 structure
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.set_xlim(0, 1)
    ax_a.set_ylim(0, 1)
    ax_a.axis('off')
    domain_boxes = draw_her2_domain_structure(ax_a, x_center=0.5, y_base=0.08)

    # Add mAb binding annotations
    draw_mab_binding(ax_a, domain_boxes, 'Trastuzumab\n(T-DM1, T-DXd)', 'DomIV',
                    side='left', color=OKABE_ITO['vermillion'])
    draw_mab_binding(ax_a, domain_boxes, 'Pertuzumab', 'DomII',
                    side='left', color=OKABE_ITO['blue'])

    # Panel label
    ax_a.text(-0.05, 1.02, 'A', fontsize=12, fontweight='bold',
             transform=ax_a.transAxes, va='bottom')
    ax_a.text(0.5, 1.0, 'Full-Length HER2 with mAb Binding Sites',
             fontsize=9, ha='center', transform=ax_a.transAxes, style='italic')

    # Panel B: p95-HER2 structure
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.set_xlim(0, 1)
    ax_b.set_ylim(0, 1)
    ax_b.axis('off')
    draw_p95_structure(ax_b, x_center=0.5, y_base=0.08)

    # Add "No binding" annotations
    ax_b.text(0.12, 0.60, 'X Trastuzumab', fontsize=7, ha='left',
             color=OKABE_ITO['vermillion'], fontweight='bold')
    ax_b.text(0.12, 0.55, 'X Pertuzumab', fontsize=7, ha='left',
             color=OKABE_ITO['vermillion'], fontweight='bold')

    # New target annotation
    ax_b.annotate('', xy=(0.68, 0.36), xytext=(0.85, 0.36),
                 arrowprops=dict(arrowstyle='->', color=OKABE_ITO['bluish_green'], lw=2))
    ax_b.text(0.87, 0.36, 'Novel\nTarget', fontsize=7, ha='left', va='center',
             color=OKABE_ITO['bluish_green'], fontweight='bold')

    ax_b.text(-0.05, 1.02, 'B', fontsize=12, fontweight='bold',
             transform=ax_b.transAxes, va='bottom')
    ax_b.text(0.5, 1.0, 'p95-HER2 Truncation (Resistance)',
             fontsize=9, ha='center', transform=ax_b.transAxes, style='italic')

    # Panel C: Key statistics
    ax_c = fig.add_subplot(gs[0, 2])
    draw_key_statistics(ax_c)
    ax_c.text(-0.05, 1.02, 'C', fontsize=12, fontweight='bold',
             transform=ax_c.transAxes, va='bottom')

    # Panel D: Internalization bar chart
    ax_d = fig.add_subplot(gs[1, 0])
    draw_internalization_bar_chart(ax_d)
    ax_d.text(-0.15, 1.05, 'D', fontsize=12, fontweight='bold',
             transform=ax_d.transAxes, va='bottom')

    # Panel E: Biparatopic ADC concept
    ax_e = fig.add_subplot(gs[1, 1:])
    draw_biparatopic_concept(ax_e)
    ax_e.text(-0.02, 1.02, 'E', fontsize=12, fontweight='bold',
             transform=ax_e.transAxes, va='bottom')
    ax_e.text(0.5, 1.0, 'Biparatopic ADC Strategy: Overcoming Resistance',
             fontsize=9, ha='center', transform=ax_e.transAxes, style='italic')

    # Main title
    fig.suptitle('HER2 Epitope Analysis for ADC Binder Design:\n'
                'p95-HER2 as a Novel Target for Overcoming Trastuzumab Resistance',
                fontsize=12, fontweight='bold', y=0.98)

    # Citation
    fig.text(0.99, 0.01, 'Jiang S. (2026) Eli Lilly - Oncology Bioinformatics',
            fontsize=6, ha='right', va='bottom', style='italic', color='gray')

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=DOMAIN_COLORS['DomI'], edgecolor='black',
                      linewidth=0.5, label='Domain I'),
        mpatches.Patch(facecolor=DOMAIN_COLORS['DomII'], edgecolor='black',
                      linewidth=0.5, label='Domain II'),
        mpatches.Patch(facecolor=DOMAIN_COLORS['DomIII'], edgecolor='black',
                      linewidth=0.5, label='Domain III'),
        mpatches.Patch(facecolor=DOMAIN_COLORS['DomIV'], edgecolor='black',
                      linewidth=0.5, label='Domain IV/JM'),
        mpatches.Patch(facecolor=DOMAIN_COLORS['Kinase'], edgecolor='black',
                      linewidth=0.5, label='Kinase'),
    ]
    fig.legend(handles=legend_elements, loc='lower left', ncol=5,
              fontsize=7, frameon=False, bbox_to_anchor=(0.01, 0.01))

    return fig


def main():
    """Generate and save the summary figure."""

    output_dir = os.path.join(os.path.dirname(__file__), '..', 'images')
    os.makedirs(output_dir, exist_ok=True)

    print("Generating publication-quality HER2 Project Summary Figure...")
    print("Using scientific-visualization standards:")
    print("  - Okabe-Ito colorblind-friendly palette")
    print("  - Arial/Helvetica fonts")
    print("  - 300 DPI output")

    fig = create_summary_figure()

    # Save as PNG (300 DPI)
    png_path = os.path.join(output_dir, 'project_summary.png')
    fig.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {png_path}")

    # Save as PDF (vector)
    pdf_path = os.path.join(output_dir, 'project_summary.pdf')
    fig.savefig(pdf_path, format='pdf', bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f"Saved: {pdf_path}")

    plt.close(fig)

    print("\nFigure panels:")
    print("  A: Full-length HER2 structure with approved mAb binding sites")
    print("  B: p95-HER2 truncation showing lost ECD and novel JM target")
    print("  C: Key statistics and clinical opportunity")
    print("  D: Internalization rate comparison (bar chart)")
    print("  E: Biparatopic ADC strategy for dual FL-HER2/p95 targeting")


if __name__ == "__main__":
    main()
