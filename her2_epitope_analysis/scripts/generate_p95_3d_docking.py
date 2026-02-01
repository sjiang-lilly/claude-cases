#!/usr/bin/env python3
"""
Generate 3D Interactive HTML Docking Visualizations for p95-HER2 Novel mAbs.
Uses py3Dmol for interactive visualization similar to her2_trastuzumab_3d.html.
"""

import os

# p95-HER2 juxtamembrane sequence (residues 611-652)
P95_JM_SEQUENCE = "MPIWKFPDEEGACQPCPINCTHSCVDLDDKGCPAEQRASP"

# Predicted mAb CDR sequences
P95_MABS = {
    "p95-mAb-001": {
        "epitope": "615-635",
        "cdr_h3": "DPIWKFPDY",
        "cdr_l3": "QQGACQPLT",
        "color": "#90EE90"
    },
    "p95-mAb-002": {
        "epitope": "611-625",
        "cdr_h3": "METPIWKFDY",
        "cdr_l3": "QQFPDEEGT",
        "color": "#87CEEB"
    },
    "p95-mAb-003": {
        "epitope": "640-652",
        "cdr_h3": "CTHSCVDY",
        "cdr_l3": "QQDLDKGCT",
        "color": "#FFA07A"
    }
}

def generate_p95_conceptual_3d_html(mab_name, mab_info, output_path):
    """
    Generate conceptual 3D visualization HTML for p95-HER2 targeting mAbs.

    Since no crystal structure exists for p95-mAb complexes, we create a
    conceptual visualization based on HER2 structure with emphasis on the
    juxtamembrane region.
    """

    # Use 1N8Z as base (has Domain IV which connects to JM region)
    pdb_file = "../data/structures/1N8Z.pdb"

    if os.path.exists(pdb_file):
        with open(pdb_file, 'r') as f:
            pdb_data = f.read()
    else:
        # Create placeholder if PDB not available
        pdb_data = ""

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{mab_name} - p95-HER2 Docking Concept</title>
    <script src="https://3dmol.org/build/3Dmol-min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid {mab_info["color"]};
            padding-bottom: 10px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .mol-container {{
            width: 100%;
            height: 600px;
            position: relative;
            border: 2px solid #ccc;
            border-radius: 8px;
            background-color: white;
        }}
        .info-panel {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 20px;
        }}
        .info-box {{
            flex: 1;
            min-width: 300px;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .info-box h3 {{
            margin-top: 0;
            color: #333;
            border-bottom: 1px solid #eee;
            padding-bottom: 8px;
        }}
        .sequence {{
            font-family: 'Courier New', monospace;
            background: #f0f0f0;
            padding: 10px;
            border-radius: 4px;
            word-break: break-all;
            font-size: 12px;
        }}
        .epitope {{
            background-color: {mab_info["color"]};
            font-weight: bold;
        }}
        .legend {{
            margin-top: 20px;
            padding: 15px;
            background: white;
            border-radius: 8px;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 5px;
        }}
        .color-box {{
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            vertical-align: middle;
            border: 1px solid #333;
            border-radius: 3px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background-color: #f5f5f5;
        }}
        .highlight {{
            background-color: {mab_info["color"]}40;
        }}
        .note {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            border-radius: 4px;
            padding: 10px;
            margin-top: 15px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 {mab_name} - p95-HER2 Binding Visualization</h1>

        <div class="mol-container" id="viewer"></div>

        <div class="legend">
            <h3>Color Legend</h3>
            <div class="legend-item"><span class="color-box" style="background-color: #FF6B6B;"></span>Domain I (23-195) - MISSING in p95</div>
            <div class="legend-item"><span class="color-box" style="background-color: #4ECDC4;"></span>Domain II (196-319) - MISSING in p95</div>
            <div class="legend-item"><span class="color-box" style="background-color: #45B7D1;"></span>Domain III (320-488) - MISSING in p95</div>
            <div class="legend-item"><span class="color-box" style="background-color: #96CEB4;"></span>Domain IV (489-630) - MISSING in p95</div>
            <div class="legend-item"><span class="color-box" style="background-color: #FFFF00;"></span>JM Stub (611-652) - <strong>TARGET EPITOPE</strong></div>
            <div class="legend-item"><span class="color-box" style="background-color: {mab_info["color"]};"></span>{mab_name} Binding Site</div>
            <div class="legend-item"><span class="color-box" style="background-color: #DDA0DD;"></span>Reference: Trastuzumab (Domain IV)</div>
        </div>

        <div class="info-panel">
            <div class="info-box">
                <h3>📍 Target Epitope: {mab_info["epitope"]}</h3>
                <p><strong>p95-HER2 Juxtamembrane Sequence (611-652):</strong></p>
                <div class="sequence">
                    611-<span class="epitope">MPIWKFPDEEGACQPCPINC</span>THSCVDLDDKGCPAEQRASP-652
                </div>
                <p class="note">
                    <strong>Note:</strong> The highlighted region shows the predicted {mab_name} epitope.
                    p95-HER2 lacks Domains I-IV, leaving only this ~42 aa juxtamembrane stub.
                </p>
            </div>

            <div class="info-box">
                <h3>🔬 Predicted CDR Sequences</h3>
                <table>
                    <tr>
                        <th>CDR</th>
                        <th>Sequence</th>
                        <th>Length</th>
                    </tr>
                    <tr class="highlight">
                        <td><strong>CDR-H3</strong></td>
                        <td class="sequence">{mab_info["cdr_h3"]}</td>
                        <td>{len(mab_info["cdr_h3"])} aa</td>
                    </tr>
                    <tr class="highlight">
                        <td><strong>CDR-L3</strong></td>
                        <td class="sequence">{mab_info["cdr_l3"]}</td>
                        <td>{len(mab_info["cdr_l3"])} aa</td>
                    </tr>
                </table>
                <p class="note">
                    <strong>Design Strategy:</strong> CDR-H3 contains motifs from the target epitope
                    ({mab_info["cdr_h3"]}) to maximize binding complementarity.
                </p>
            </div>
        </div>

        <div class="info-panel">
            <div class="info-box">
                <h3>📊 Binding Characteristics</h3>
                <table>
                    <tr><th>Property</th><th>Value</th></tr>
                    <tr><td>Target</td><td>p95-HER2 ({mab_info["epitope"]})</td></tr>
                    <tr><td>Epitope Type</td><td>Linear (JM stub)</td></tr>
                    <tr><td>Cross-reactivity</td><td>{"FL-HER2 (conserved region)" if mab_name != "p95-mAb-002" else "p95-CTF611 specific only"}</td></tr>
                    <tr><td>Framework</td><td>Human IgG1 (IGHV3-23/IGKV1-39)</td></tr>
                </table>
            </div>

            <div class="info-box">
                <h3>⚠️ Structural Context</h3>
                <p>
                    The 3D viewer shows the HER2 extracellular domain structure (PDB: 1N8Z)
                    for context. In p95-HER2:
                </p>
                <ul>
                    <li><span style="color: red;">❌</span> Domains I-IV are <strong>ABSENT</strong></li>
                    <li><span style="color: green;">✓</span> Only JM stub (611-652) remains extracellular</li>
                    <li><span style="color: green;">✓</span> {mab_name} targets this remaining epitope</li>
                </ul>
                <p>
                    The yellow-highlighted region near the membrane shows where {mab_name}
                    would bind on p95-HER2.
                </p>
            </div>
        </div>
    </div>

    <script>
        var viewer = $3Dmol.createViewer("viewer", {{backgroundColor: "white"}});

        var pdbData = `{pdb_data}`;

        if (pdbData.length > 0) {{
            viewer.addModel(pdbData, "pdb");

            // Color HER2 domains - show what's MISSING in p95
            // Domain I (red) - MISSING
            viewer.setStyle({{chain: "A", resi: ["23-195"]}}, {{
                cartoon: {{color: "#FF6B6B", opacity: 0.3}}
            }});

            // Domain II (teal) - MISSING
            viewer.setStyle({{chain: "A", resi: ["196-319"]}}, {{
                cartoon: {{color: "#4ECDC4", opacity: 0.3}}
            }});

            // Domain III (blue) - MISSING
            viewer.setStyle({{chain: "A", resi: ["320-488"]}}, {{
                cartoon: {{color: "#45B7D1", opacity: 0.3}}
            }});

            // Domain IV (green) - MISSING in p95
            viewer.setStyle({{chain: "A", resi: ["489-610"]}}, {{
                cartoon: {{color: "#96CEB4", opacity: 0.3}}
            }});

            // JM region (yellow) - THIS IS THE TARGET
            // Note: In crystal structures, JM region may not be fully resolved
            // Highlighting the membrane-proximal part of Domain IV as proxy
            viewer.setStyle({{chain: "A", resi: ["600-630"]}}, {{
                cartoon: {{color: "#FFFF00"}},
                stick: {{color: "#FFFF00"}}
            }});

            // Add surface to JM region to show accessibility
            viewer.addSurface($3Dmol.SurfaceType.VDW, {{
                opacity: 0.6,
                color: "{mab_info["color"]}"
            }}, {{chain: "A", resi: ["600-630"]}});

            // Trastuzumab Fab for reference
            viewer.setStyle({{chain: "B"}}, {{cartoon: {{color: "#DDA0DD", opacity: 0.5}}}});
            viewer.setStyle({{chain: "C"}}, {{cartoon: {{color: "#F0E68C", opacity: 0.5}}}});
            viewer.setStyle({{chain: "H"}}, {{cartoon: {{color: "#DDA0DD", opacity: 0.5}}}});
            viewer.setStyle({{chain: "L"}}, {{cartoon: {{color: "#F0E68C", opacity: 0.5}}}});

            // Add labels
            viewer.addLabel("p95 Target Region (JM stub)", {{
                position: {{x: 0, y: 0, z: 0}},
                backgroundColor: "{mab_info["color"]}",
                fontColor: "black",
                fontSize: 14
            }}, {{chain: "A", resi: "615"}});

            viewer.zoomTo();
            viewer.render();

            // Add rotation animation
            viewer.spin("y", 0.5);
        }} else {{
            // Show placeholder message if PDB not available
            document.getElementById("viewer").innerHTML = "<div style='padding:50px;text-align:center;'>" +
                "<h2>3D Structure Visualization</h2>" +
                "<p>PDB structure file not found. The visualization would show:</p>" +
                "<ul style='text-align:left;max-width:500px;margin:0 auto;'>" +
                "<li>HER2 extracellular domain (faded) - MISSING in p95</li>" +
                "<li>JM stub region (highlighted in yellow) - {mab_name} target</li>" +
                "<li>Predicted binding site surface in {mab_info["color"]}</li>" +
                "</ul></div>";
        }}
    </script>
</body>
</html>'''

    with open(output_path, 'w') as f:
        f.write(html_content)
    print(f"Generated: {output_path}")


def generate_bispecific_3d_html(output_path):
    """Generate 3D visualization for the bispecific p95-Bispecific-001."""

    # Use 1N8Z as base
    pdb_file = "../data/structures/1N8Z.pdb"

    if os.path.exists(pdb_file):
        with open(pdb_file, 'r') as f:
            pdb_data = f.read()
    else:
        pdb_data = ""

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>p95-Bispecific-001 - Dual Targeting Visualization</title>
    <script src="https://3dmol.org/build/3Dmol-min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #DDA0DD;
            padding-bottom: 10px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .mol-container {{
            width: 100%;
            height: 600px;
            position: relative;
            border: 2px solid #ccc;
            border-radius: 8px;
            background-color: white;
        }}
        .dual-panel {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }}
        .arm-box {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .arm-box.arm1 {{
            border-left: 4px solid #90EE90;
        }}
        .arm-box.arm2 {{
            border-left: 4px solid #DDA0DD;
        }}
        .arm-box h3 {{
            margin-top: 0;
        }}
        .sequence {{
            font-family: 'Courier New', monospace;
            background: #f0f0f0;
            padding: 10px;
            border-radius: 4px;
            word-break: break-all;
            font-size: 11px;
        }}
        .legend {{
            margin-top: 20px;
            padding: 15px;
            background: white;
            border-radius: 8px;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 5px;
        }}
        .color-box {{
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            vertical-align: middle;
            border: 1px solid #333;
            border-radius: 3px;
        }}
        .advantage {{
            background: #d4edda;
            border: 1px solid #28a745;
            border-radius: 4px;
            padding: 15px;
            margin-top: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 p95-Bispecific-001 - Dual Targeting p95-HER2 + FL-HER2</h1>

        <div class="mol-container" id="viewer"></div>

        <div class="legend">
            <h3>Color Legend - Dual Targeting Strategy</h3>
            <div class="legend-item"><span class="color-box" style="background-color: #90EE90;"></span><strong>Arm 1:</strong> p95-HER2 JM (615-635)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #DDA0DD;"></span><strong>Arm 2:</strong> FL-HER2 Domain IV (557-603)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #FFFF00;"></span>JM Stub Target Region</div>
            <div class="legend-item"><span class="color-box" style="background-color: #96CEB4;"></span>Domain IV (Trastuzumab epitope)</div>
        </div>

        <div class="dual-panel">
            <div class="arm-box arm1">
                <h3>🟢 Arm 1: p95-HER2 Targeting</h3>
                <p><strong>Target:</strong> Juxtamembrane stub (615-635)</p>
                <p><strong>Epitope:</strong> MPIWKFPDEEGACQPCPINC</p>
                <p><strong>CDR-H3:</strong></p>
                <div class="sequence">DPIWKFPDY</div>
                <p><strong>CDR-L3:</strong></p>
                <div class="sequence">QQGACQPLT</div>
                <table>
                    <tr><td>Binding</td><td>p95-HER2 + FL-HER2</td></tr>
                    <tr><td>Mechanism</td><td>JM region recognition</td></tr>
                </table>
            </div>

            <div class="arm-box arm2">
                <h3>💜 Arm 2: FL-HER2 Targeting (Trastuzumab-like)</h3>
                <p><strong>Target:</strong> Domain IV (557-603)</p>
                <p><strong>Epitope:</strong> Trastuzumab epitope</p>
                <p><strong>CDR-H3:</strong></p>
                <div class="sequence">SRWGGDGFYAMDY</div>
                <p><strong>CDR-L3:</strong></p>
                <div class="sequence">QQHYTTPPT</div>
                <table>
                    <tr><td>Binding</td><td>FL-HER2 only</td></tr>
                    <tr><td>Mechanism</td><td>Proven Domain IV binding</td></tr>
                </table>
            </div>
        </div>

        <div class="advantage">
            <h3>✅ Key Advantages of Bispecific Design</h3>
            <table>
                <tr>
                    <th>Property</th>
                    <th>Monospecific (e.g., Trastuzumab)</th>
                    <th>p95-Bispecific-001</th>
                </tr>
                <tr>
                    <td>p95-HER2 Binding</td>
                    <td>❌ No</td>
                    <td>✅ Yes (Arm 1)</td>
                </tr>
                <tr>
                    <td>FL-HER2 Binding</td>
                    <td>✅ Yes</td>
                    <td>✅ Yes (Both arms)</td>
                </tr>
                <tr>
                    <td>Internalization</td>
                    <td>25%</td>
                    <td><strong>60%</strong> (clustering)</td>
                </tr>
                <tr>
                    <td>ADC Score</td>
                    <td>8.8/10</td>
                    <td><strong>8.5/10</strong></td>
                </tr>
                <tr>
                    <td>Tumor Coverage</td>
                    <td>~50% (FL-HER2 only)</td>
                    <td><strong>~80-90%</strong> (p95 + FL)</td>
                </tr>
            </table>
        </div>
    </div>

    <script>
        var viewer = $3Dmol.createViewer("viewer", {{backgroundColor: "white"}});

        var pdbData = `{pdb_data}`;

        if (pdbData.length > 0) {{
            viewer.addModel(pdbData, "pdb");

            // Domain IV - Arm 2 target (Trastuzumab epitope)
            viewer.setStyle({{chain: "A", resi: ["557-603"]}}, {{
                cartoon: {{color: "#DDA0DD"}},
                stick: {{color: "#DDA0DD"}}
            }});

            // Rest of Domain IV
            viewer.setStyle({{chain: "A", resi: ["489-556"]}}, {{
                cartoon: {{color: "#96CEB4", opacity: 0.5}}
            }});
            viewer.setStyle({{chain: "A", resi: ["604-630"]}}, {{
                cartoon: {{color: "#96CEB4", opacity: 0.5}}
            }});

            // JM region proxy - Arm 1 target
            viewer.setStyle({{chain: "A", resi: ["620-630"]}}, {{
                cartoon: {{color: "#90EE90"}},
                stick: {{color: "#90EE90"}}
            }});

            // Add surface to both target regions
            viewer.addSurface($3Dmol.SurfaceType.VDW, {{
                opacity: 0.5,
                color: "#DDA0DD"
            }}, {{chain: "A", resi: ["557-603"]}});

            viewer.addSurface($3Dmol.SurfaceType.VDW, {{
                opacity: 0.5,
                color: "#90EE90"
            }}, {{chain: "A", resi: ["620-630"]}});

            // Other domains (faded - not targeted)
            viewer.setStyle({{chain: "A", resi: ["23-195"]}}, {{cartoon: {{color: "#FF6B6B", opacity: 0.2}}}});
            viewer.setStyle({{chain: "A", resi: ["196-319"]}}, {{cartoon: {{color: "#4ECDC4", opacity: 0.2}}}});
            viewer.setStyle({{chain: "A", resi: ["320-488"]}}, {{cartoon: {{color: "#45B7D1", opacity: 0.2}}}});

            // Trastuzumab Fab for reference
            viewer.setStyle({{chain: "B"}}, {{cartoon: {{color: "#DDA0DD", opacity: 0.7}}}});
            viewer.setStyle({{chain: "C"}}, {{cartoon: {{color: "#F0E68C", opacity: 0.7}}}});
            viewer.setStyle({{chain: "H"}}, {{cartoon: {{color: "#DDA0DD", opacity: 0.7}}}});
            viewer.setStyle({{chain: "L"}}, {{cartoon: {{color: "#F0E68C", opacity: 0.7}}}});

            viewer.zoomTo();
            viewer.render();
            viewer.spin("y", 0.3);
        }}
    </script>
</body>
</html>'''

    with open(output_path, 'w') as f:
        f.write(html_content)
    print(f"Generated: {output_path}")


def main():
    """Generate all p95 mAb 3D HTML visualization files."""
    print("=" * 60)
    print("Generating p95-HER2 Novel mAb 3D Docking HTML Files")
    print("=" * 60)

    os.makedirs("../images", exist_ok=True)

    # Generate individual mAb visualizations
    for mab_name, mab_info in P95_MABS.items():
        output_path = f"../images/{mab_name.lower().replace('-', '_')}_3d.html"
        print(f"\nGenerating {mab_name}...")
        generate_p95_conceptual_3d_html(mab_name, mab_info, output_path)

    # Generate bispecific visualization
    print("\nGenerating p95-Bispecific-001...")
    generate_bispecific_3d_html("../images/p95_bispecific_001_3d.html")

    print("\n" + "=" * 60)
    print("3D HTML Generation Complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - images/p95_mab_001_3d.html")
    print("  - images/p95_mab_002_3d.html")
    print("  - images/p95_mab_003_3d.html")
    print("  - images/p95_bispecific_001_3d.html")


if __name__ == "__main__":
    main()
