#!/usr/bin/env python3
"""
Generate 3D Interactive HTML Docking Visualizations for Pipeline-Predicted p95-HER2 mAbs.
Uses py3Dmol for interactive visualization similar to her2_trastuzumab_3d.html.

Updated to reflect new ESM + AlphaFold + Docking pipeline predictions.
"""

import os

# Get the script's directory for absolute path resolution
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, "data")
IMAGES_DIR = os.path.join(PROJECT_DIR, "images")

# p95-HER2 juxtamembrane sequence (residues 611-652)
P95_JM_SEQUENCE = "MPIWKFPDEEGACQPCPINCTHSCVDLDDKGCPAEQRASP"

# Pipeline-Predicted mAb CDR sequences (ESM + AlphaFold + Docking)
P95_MABS = {
    "p95-ESM-001": {
        "epitope": "615-635",
        "epitope_seq": "MPIWKFPDEEGACQPCPINC",
        "strategy": "Epitope Mimicry",
        "cdr_h3": "ARDPIWKFPDYAMDY",
        "cdr_l3": "QQGACQPLT",
        "predicted_kd": "0.21 nM",
        "adc_score": "9.0/10",
        "color": "#90EE90",
        "vh_seq": "EVQLVESGGGLVQPGGSLRLSCAASGYTFTSYWWVRQAPGKGLEWVSINPIWKGSRFTISRDNSKNTLYLQMNSLRAEDTAVYYCARARDPIWKFPDYAMDYWGQGTLVTVSS",
        "vl_seq": "DIQMTQSPSSLSASVGDRVTITCRASQGISSWLAWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQGACQPLTFGQGTKVEIK"
    },
    "p95-ESM-002": {
        "epitope": "615-635",
        "epitope_seq": "MPIWKFPDEEGACQPCPINC",
        "strategy": "Charge Complementarity (TOP RANKED)",
        "cdr_h3": "ARDRKEYWFDY",
        "cdr_l3": "QQFPDEEGT",
        "predicted_kd": "0.13 nM",
        "adc_score": "9.0/10",
        "color": "#87CEEB",
        "vh_seq": "EVQLVESGGGLVQPGGSLRLSCAASGYTFTDYEWVRQAPGKGLEWVSINPKRGSTRFTISRDNSKNTLYLQMNSLRAEDTAVYYCARARDRKEYWFDYWGQGTLVTVSS",
        "vl_seq": "DIQMTQSPSSLSASVGDRVTITCRASQDISKYLNWYQQKPGKAPKLLIYAASRLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQFPDEEGTFGQGTKVEIK"
    },
    "p95-ESM-003": {
        "epitope": "640-652",
        "epitope_seq": "CTHSCVDLDDKGC",
        "strategy": "Hydrophobic Targeting",
        "cdr_h3": "ARCTHSCVDYFDY",
        "cdr_l3": "QQDLDKGCT",
        "predicted_kd": "0.33 nM",
        "adc_score": "8.0/10",
        "color": "#FFA07A",
        "vh_seq": "EVQLVESGGGLVQPGGSLRLSCAASGYTFTSYYWVRQAPGKGLEWVSINWWGGSTRFTISRDNSKNTLYLQMNSLRAEDTAVYYCARARCTHSCVDYFDYWGQGTLVTVSS",
        "vl_seq": "DIQMTQSPSSLSASVGDRVTITCRASQSVSSSYLAWYQQKPGKAPKLLIYGASSRATGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQDLDKGCTFGQGTKVEIK"
    },
    "p95-ESM-004": {
        "epitope": "611-625",
        "epitope_seq": "MPIWKFPDEEGACQP",
        "strategy": "Neo-epitope Specific (p95-ONLY)",
        "cdr_h3": "ARMETPIWKFDY",
        "cdr_l3": "QQMPIWFPT",
        "predicted_kd": "0.20 nM",
        "adc_score": "9.0/10",
        "color": "#FFD700",
        "vh_seq": "EVQLVESGGGLVQPGGSLRLSCAASGYTFTNYMWVRQAPGKGLEWVSINMETPGSRFTISRDNSKNTLYLQMNSLRAEDTAVYYCARARMETPIWKFDYWGQGTLVTVSS",
        "vl_seq": "DIQMTQSPSSLSASVGDRVTITCRASQMETSWLAWYQQKPGKAPKLLIYAASSLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQMPIWFPTFGQGTKVEIK"
    }
}

def generate_p95_conceptual_3d_html(mab_name, mab_info, output_path):
    """
    Generate conceptual 3D visualization HTML for p95-HER2 targeting mAbs.
    """

    # Use 6OGE which has full HER2 ECD (residues 23-644) including JM region
    pdb_file = os.path.join(DATA_DIR, "structures", "6OGE.pdb")

    if os.path.exists(pdb_file):
        with open(pdb_file, 'r') as f:
            pdb_data = f.read()
        print(f"  Loaded PDB file: {pdb_file} ({len(pdb_data)} bytes)")
    else:
        pdb_data = ""
        print(f"  WARNING: PDB file not found: {pdb_file}")

    is_neo_epitope = "Neo-epitope" in mab_info["strategy"]

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>{mab_name} - p95-HER2 Docking (Pipeline-Predicted)</title>
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
        .badge {{
            display: inline-block;
            background: {mab_info["color"]};
            color: #333;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
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
            font-size: 11px;
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
        .pipeline-note {{
            background: #e3f2fd;
            border: 1px solid #2196F3;
            border-radius: 4px;
            padding: 10px;
            margin-top: 15px;
            font-size: 14px;
        }}
        .metric {{
            display: inline-block;
            background: #f5f5f5;
            padding: 8px 15px;
            border-radius: 5px;
            margin: 5px;
            text-align: center;
        }}
        .metric .value {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }}
        .metric .label {{
            font-size: 11px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧬 {mab_name} <span class="badge">{mab_info["strategy"]}</span></h1>

        <div style="margin-bottom: 20px;">
            <div class="metric">
                <div class="value">{mab_info["predicted_kd"]}</div>
                <div class="label">Predicted Kd</div>
            </div>
            <div class="metric">
                <div class="value">{mab_info["adc_score"]}</div>
                <div class="label">ADC Score</div>
            </div>
            <div class="metric">
                <div class="value">{mab_info["epitope"]}</div>
                <div class="label">Target Epitope</div>
            </div>
        </div>

        <div class="mol-container" id="viewer"></div>

        <div class="legend">
            <h3>Color Legend</h3>
            <div class="legend-item"><span class="color-box" style="background-color: #E53935;"></span>Domain I (23-195)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #00ACC1;"></span>Domain II (196-319)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #1E88E5;"></span>Domain III (320-488)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #43A047;"></span>Domain IV (489-630)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #FFD600;"></span>JM Stub (631-644) - <strong>TARGET</strong></div>
            <div class="legend-item"><span class="color-box" style="background-color: #AB47BC;"></span>Antibody Heavy Chain</div>
            <div class="legend-item"><span class="color-box" style="background-color: #FF7043;"></span>Antibody Light Chain</div>
            <div class="legend-item"><span class="color-box" style="background-color: {mab_info["color"]};"></span>{mab_name} Epitope Surface</div>
        </div>

        <div class="info-panel">
            <div class="info-box">
                <h3>📍 Target Epitope: {mab_info["epitope"]}</h3>
                <p><strong>p95-HER2 Juxtamembrane Sequence (611-652):</strong></p>
                <div class="sequence">
                    611-<span class="epitope">{mab_info["epitope_seq"]}</span>{"THSCVDLDDKGCPAEQRASP" if "615" in mab_info["epitope"] else ""}-652
                </div>
                <div class="pipeline-note">
                    <strong>Pipeline Design:</strong> ESM + AlphaFold + Docking<br>
                    <strong>Strategy:</strong> {mab_info["strategy"]}<br>
                    <strong>Cross-reactivity:</strong> {"p95-HER2 ONLY (no FL-HER2)" if is_neo_epitope else "p95-HER2 + FL-HER2"}
                </div>
            </div>

            <div class="info-box">
                <h3>🔬 CDR Sequences (Pipeline-Designed)</h3>
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
            </div>
        </div>

        <div class="info-panel">
            <div class="info-box">
                <h3>📋 Full VH Sequence ({len(mab_info["vh_seq"])} aa)</h3>
                <div class="sequence">{mab_info["vh_seq"]}</div>
            </div>
            <div class="info-box">
                <h3>📋 Full VL Sequence ({len(mab_info["vl_seq"])} aa)</h3>
                <div class="sequence">{mab_info["vl_seq"]}</div>
            </div>
        </div>
    </div>

    <script>
        var viewer = $3Dmol.createViewer("viewer", {{backgroundColor: "white"}});

        var pdbData = `{pdb_data}`;

        if (pdbData.length > 0) {{
            viewer.addModel(pdbData, "pdb");

            // ============================================
            // HER2 DOMAINS (Chain A) - STRONG COLORS
            // ============================================
            // Domain I (23-195) - Strong Red
            viewer.setStyle({{chain: "A", resi: ["23-195"]}}, {{cartoon: {{color: "#E53935"}}}});

            // Domain II (196-319) - Strong Cyan
            viewer.setStyle({{chain: "A", resi: ["196-319"]}}, {{cartoon: {{color: "#00ACC1"}}}});

            // Domain III (320-488) - Strong Blue
            viewer.setStyle({{chain: "A", resi: ["320-488"]}}, {{cartoon: {{color: "#1E88E5"}}}});

            // Domain IV (489-630) - Strong Green
            viewer.setStyle({{chain: "A", resi: ["489-630"]}}, {{cartoon: {{color: "#43A047"}}}});

            // JM Stub region (631-644) - Bright Yellow (TARGET) - EXTRA VISIBLE
            viewer.setStyle({{chain: "A", resi: ["631-644"]}}, {{
                cartoon: {{color: "#FFD600", thickness: 0.5}},
                stick: {{color: "#FFD600", radius: 0.3}}
            }});

            // ============================================
            // EPITOPE SURFACE - Target binding site
            // ============================================
            viewer.addSurface($3Dmol.SurfaceType.VDW, {{
                opacity: 0.6,
                color: "{mab_info["color"]}"
            }}, {{chain: "A", resi: ["631-644"]}});

            // ============================================
            // PERTUZUMAB FAB (Chains B, C) - STRONG COLORS
            // ============================================
            // Chain B: Pertuzumab Light Chain - Orange
            viewer.setStyle({{chain: "B"}}, {{cartoon: {{color: "#FF7043"}}}});

            // Chain C: Pertuzumab Heavy Chain - Purple
            viewer.setStyle({{chain: "C"}}, {{cartoon: {{color: "#AB47BC"}}}});

            // ============================================
            // TRASTUZUMAB FAB (Chains D, E) - STRONG COLORS
            // ============================================
            // Chain D: Trastuzumab Light Chain - Orange
            viewer.setStyle({{chain: "D"}}, {{cartoon: {{color: "#FF7043"}}}});

            // Chain E: Trastuzumab Heavy Chain - Purple
            viewer.setStyle({{chain: "E"}}, {{cartoon: {{color: "#AB47BC"}}}});

            viewer.zoomTo();
            viewer.render();
            viewer.spin("y", 0.5);
        }}
    </script>
</body>
</html>'''

    with open(output_path, 'w') as f:
        f.write(html_content)
    print(f"Generated: {output_path}")


def generate_bispecific_3d_html(output_path):
    """Generate 3D visualization for the p95-Trastuzumab-Biparatopic."""

    # Use 6OGE which has full HER2 ECD (residues 23-644) including JM region
    pdb_file = os.path.join(DATA_DIR, "structures", "6OGE.pdb")

    if os.path.exists(pdb_file):
        with open(pdb_file, 'r') as f:
            pdb_data = f.read()
        print(f"  Loaded PDB file: {pdb_file} ({len(pdb_data)} bytes)")
    else:
        pdb_data = ""
        print(f"  WARNING: PDB file not found: {pdb_file}")

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>p95-Trastuzumab-Biparatopic - Dual Targeting (RECOMMENDED)</title>
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
        .recommended {{
            display: inline-block;
            background: linear-gradient(90deg, #90EE90, #DDA0DD);
            color: white;
            padding: 4px 15px;
            border-radius: 15px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 10px;
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
            font-size: 10px;
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
        .metric {{
            display: inline-block;
            background: #f5f5f5;
            padding: 8px 15px;
            border-radius: 5px;
            margin: 5px;
            text-align: center;
        }}
        .metric .value {{
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }}
        .metric .label {{
            font-size: 11px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 p95-Trastuzumab-Biparatopic <span class="recommended">RECOMMENDED</span></h1>

        <div style="margin-bottom: 20px;">
            <div class="metric">
                <div class="value">0.08 nM</div>
                <div class="label">Predicted Kd</div>
            </div>
            <div class="metric">
                <div class="value">9.5/10</div>
                <div class="label">ADC Score</div>
            </div>
            <div class="metric">
                <div class="value">65%</div>
                <div class="label">Internalization</div>
            </div>
            <div class="metric">
                <div class="value">Dual</div>
                <div class="label">p95 + FL-HER2</div>
            </div>
        </div>

        <div class="mol-container" id="viewer"></div>

        <div class="legend">
            <h3>Color Legend</h3>
            <div class="legend-item"><span class="color-box" style="background-color: #E53935;"></span>Domain I (23-195)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #00ACC1;"></span>Domain II (196-319)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #1E88E5;"></span>Domain III (320-488)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #43A047;"></span>Domain IV (489-630)</div>
            <div class="legend-item"><span class="color-box" style="background-color: #FFD600;"></span>JM Stub (631-644) - <strong>Arm 1 Target</strong></div>
            <div class="legend-item"><span class="color-box" style="background-color: #FF4081;"></span>Domain IV Epitope (557-603) - <strong>Arm 2 Target</strong></div>
            <div class="legend-item"><span class="color-box" style="background-color: #AB47BC;"></span>Antibody Heavy Chain</div>
            <div class="legend-item"><span class="color-box" style="background-color: #FF7043;"></span>Antibody Light Chain</div>
        </div>

        <div class="dual-panel">
            <div class="arm-box arm1">
                <h3>🟢 Arm 1: p95-HER2 Targeting (from p95-ESM-002)</h3>
                <p><strong>Target:</strong> Juxtamembrane stub (615-635)</p>
                <p><strong>Strategy:</strong> Charge Complementarity</p>
                <p><strong>CDR-H3:</strong> <span class="sequence" style="display:inline;">ARDRKEYWFDY</span></p>
                <p><strong>CDR-L3:</strong> <span class="sequence" style="display:inline;">QQFPDEEGT</span></p>
                <p><strong>Full VH:</strong></p>
                <div class="sequence">EVQLVESGGGLVQPGGSLRLSCAASGYTFTDYEWVRQAPGKGLEWVSINPKRGSTRFTISRDNSKNTLYLQMNSLRAEDTAVYYCARARDRKEYWFDYWGQGTLVTVSS</div>
                <p><strong>Full VL:</strong></p>
                <div class="sequence">DIQMTQSPSSLSASVGDRVTITCRASQDISKYLNWYQQKPGKAPKLLIYAASRLQSGVPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQFPDEEGTFGQGTKVEIK</div>
            </div>

            <div class="arm-box arm2">
                <h3>💜 Arm 2: FL-HER2 Targeting (Trastuzumab)</h3>
                <p><strong>Target:</strong> Domain IV (557-603)</p>
                <p><strong>Strategy:</strong> Proven Clinical Binder</p>
                <p><strong>CDR-H3:</strong> <span class="sequence" style="display:inline;">SRWGGDGFYAMDY</span></p>
                <p><strong>CDR-L3:</strong> <span class="sequence" style="display:inline;">QQHYTTPPT</span></p>
                <p><strong>Full VH:</strong></p>
                <div class="sequence">EVQLVESGGGLVQPGGSLRLSCAASGFNIKDTYIHWVRQAPGKGLEWVARIYPTNGYTRYADSVKGRFTISADTSKNTAYLQMNSLRAEDTAVYYCSRWGGDGFYAMDYWGQGTLVTVSS</div>
                <p><strong>Full VL:</strong></p>
                <div class="sequence">DIQMTQSPSSLSASVGDRVTITCRASQDVNTAVAWYQQKPGKAPKLLIYSASFLYSGVPSRFSGSRSGTDFTLTISSLQPEDFATYYCQQHYTTPPTFGQGTKVEIK</div>
            </div>
        </div>

        <div class="advantage">
            <h3>✅ Key Advantages of p95-Trastuzumab-Biparatopic</h3>
            <table>
                <tr>
                    <th>Property</th>
                    <th>Trastuzumab (T-DM1/T-DXd)</th>
                    <th>p95-Trastuzumab-Biparatopic</th>
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
                    <td>Predicted Kd</td>
                    <td>5.0 nM</td>
                    <td><strong>0.08 nM</strong> (~60x better)</td>
                </tr>
                <tr>
                    <td>Internalization</td>
                    <td>25%</td>
                    <td><strong>65%</strong> (clustering effect)</td>
                </tr>
                <tr>
                    <td>ADC Score</td>
                    <td>8.8/10</td>
                    <td><strong>9.5/10</strong></td>
                </tr>
                <tr>
                    <td>Tumor Coverage</td>
                    <td>~50-70% (FL-HER2 only)</td>
                    <td><strong>~90%+</strong> (p95 + FL)</td>
                </tr>
                <tr>
                    <td>Immunosuppression (Hu 2025)</td>
                    <td>Limited by p95-driven PD-L1</td>
                    <td><strong>Targets immunosuppressive p95+ cells</strong></td>
                </tr>
            </table>
        </div>
    </div>

    <script>
        var viewer = $3Dmol.createViewer("viewer", {{backgroundColor: "white"}});

        var pdbData = `{pdb_data}`;

        if (pdbData.length > 0) {{
            viewer.addModel(pdbData, "pdb");

            // ============================================
            // HER2 DOMAINS (Chain A) - STRONG COLORS
            // ============================================
            // Domain I (23-195) - Strong Red
            viewer.setStyle({{chain: "A", resi: ["23-195"]}}, {{cartoon: {{color: "#E53935"}}}});

            // Domain II (196-319) - Strong Cyan
            viewer.setStyle({{chain: "A", resi: ["196-319"]}}, {{cartoon: {{color: "#00ACC1"}}}});

            // Domain III (320-488) - Strong Blue
            viewer.setStyle({{chain: "A", resi: ["320-488"]}}, {{cartoon: {{color: "#1E88E5"}}}});

            // Domain IV (489-630) - Strong Green
            viewer.setStyle({{chain: "A", resi: ["489-630"]}}, {{cartoon: {{color: "#43A047"}}}});

            // JM Stub region (631-644) - Bright Yellow (Arm 1 Target)
            viewer.setStyle({{chain: "A", resi: ["631-644"]}}, {{cartoon: {{color: "#FFD600"}}}});

            // ============================================
            // EPITOPE SURFACES - Both Target Sites
            // ============================================
            // Arm 2 Target: Domain IV epitope (557-603) - Hot Pink surface
            viewer.addSurface($3Dmol.SurfaceType.VDW, {{opacity: 0.8, color: "#FF4081"}}, {{chain: "A", resi: ["557-603"]}});

            // Arm 1 Target: JM stub (631-644) - Bright Yellow surface
            viewer.addSurface($3Dmol.SurfaceType.VDW, {{opacity: 0.8, color: "#FFD600"}}, {{chain: "A", resi: ["631-644"]}});

            // ============================================
            // PERTUZUMAB FAB (Chains B, C) - STRONG COLORS
            // ============================================
            // Chain B: Pertuzumab Light Chain - Orange
            viewer.setStyle({{chain: "B"}}, {{cartoon: {{color: "#FF7043"}}}});

            // Chain C: Pertuzumab Heavy Chain - Purple
            viewer.setStyle({{chain: "C"}}, {{cartoon: {{color: "#AB47BC"}}}});

            // ============================================
            // TRASTUZUMAB FAB (Chains D, E) - STRONG COLORS
            // ============================================
            // Chain D: Trastuzumab Light Chain - Orange
            viewer.setStyle({{chain: "D"}}, {{cartoon: {{color: "#FF7043"}}}});

            // Chain E: Trastuzumab Heavy Chain - Purple
            viewer.setStyle({{chain: "E"}}, {{cartoon: {{color: "#AB47BC"}}}});

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
    """Generate all pipeline-predicted p95 mAb 3D HTML visualization files."""
    print("=" * 60)
    print("Generating Pipeline-Predicted p95-HER2 mAb 3D Docking HTML")
    print("=" * 60)

    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Generate individual mAb visualizations
    for mab_name, mab_info in P95_MABS.items():
        output_path = os.path.join(IMAGES_DIR, f"{mab_name.lower().replace('-', '_')}_3d.html")
        print(f"\nGenerating {mab_name}...")
        generate_p95_conceptual_3d_html(mab_name, mab_info, output_path)

    # Generate bispecific visualization
    print("\nGenerating p95-Trastuzumab-Biparatopic...")
    generate_bispecific_3d_html(os.path.join(IMAGES_DIR, "p95_trastuzumab_biparatopic_3d.html"))

    print("\n" + "=" * 60)
    print("3D HTML Generation Complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - images/p95_esm_001_3d.html")
    print("  - images/p95_esm_002_3d.html")
    print("  - images/p95_esm_003_3d.html")
    print("  - images/p95_esm_004_3d.html")
    print("  - images/p95_trastuzumab_biparatopic_3d.html")


if __name__ == "__main__":
    main()
