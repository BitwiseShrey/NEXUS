"""
NEXUS Capstone Phase-I Report - Chapter Sections Content
Contains all detailed academic text, algorithms, data tables, and figures.
"""

import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from scripts.build_full_capstone_report import (
    add_para, add_bullet, add_numbered_item, add_subitem,
    add_chapter_heading, add_section_heading, add_subsection_heading,
    add_figure_image, add_code_block, set_cell_background, set_cell_margins, set_table_borders,
    COLOR_BLACK, COLOR_RED, HEX_LIGHT_GRAY, HEX_BORDER
)


def build_preliminaries(doc):
    # ================= PAGE 1: TITLE PAGE =================
    add_para(doc, "A PROPOSED DESIGN AND IMPLEMENTATION", bold=True, font_size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=40, space_after=14)
    add_para(doc, "DSN4091-CAPSTONE PROJECT PHASE-I", bold=True, font_size=15, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_para(doc, "Phase – I Report", bold=False, italic=True, font_size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=30)

    add_para(doc, "Submitted by", italic=True, font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)
    add_para(doc, "SHREYANSH UTTAM (21BAI10xxx)", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=26)

    add_para(doc, "in partial fulfillment for the award of the degree\nof", italic=True, font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    add_para(doc, "BACHELOR OF TECHNOLOGY", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_para(doc, "in", italic=True, font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_para(doc, "COMPUTER SCIENCE AND ENGINEERING\n(ARTIFICIAL INTELLIGENCE AND MACHINE LEARNING)", bold=True, font_size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=36)

    # University Name & Location
    add_para(doc, "SCHOOL OF COMPUTING SCIENCE AND ENGINEERING", bold=True, font_size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
    add_para(doc, "VIT BHOPAL UNIVERSITY SEHORE,\nMADHYA PRADESH - 466114", bold=True, font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)
    add_para(doc, "September 2026", bold=False, font_size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

    doc.add_page_break()

    # ================= PAGE 2: BONAFIDE CERTIFICATE =================
    add_para(doc, "VIT BHOPAL UNIVERSITY, KOTHRIKALAN, SEHORE\nMADHYA PRADESH – 466114", bold=True, font_size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=18)
    add_para(doc, "BONAFIDE CERTIFICATE", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=24)

    cert_text = (
        'Certified that this project report titled “A PROPOSED DESIGN AND IMPLEMENTATION FOR '
        'AI-POWERED SUPPLY CHAIN INTELLIGENCE, RISK PREDICTION & OPTIMIZATION PLATFORM - NEXUS” '
        'is the bonafide work of “SHREYANSH UTTAM (21BAI10xxx)” who carried out the project work '
        '(DSN4091- Capstone Project Phase-I) under my supervision.'
    )
    add_para(doc, cert_text, font_size=12, space_after=16, line_spacing=1.3)

    cert_text_2 = (
        'Certified further that to the best of my knowledge the work reported at this time does not form '
        'part of any other project/research work based on which a degree or award was conferred on an '
        'earlier occasion on this or any other candidate.'
    )
    add_para(doc, cert_text_2, font_size=12, space_after=50, line_spacing=1.3)

    # Signature Table
    sig_table = doc.add_table(rows=2, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2 = sig_table.cell(0, 0), sig_table.cell(0, 1)
    c1.width = Inches(3.2)
    c2.width = Inches(3.2)

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p1.add_run("PROGRAM CHAIR\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p1.add_run("Dr Pradeep Kumar Mishra\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p1.add_run("Senior Assistant Professor (Gr-2),\nSchool of Computing Science Engineering and\nArtificial Intelligence\nVIT BHOPAL UNIVERSITY")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)

    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p2.add_run("PROJECT GUIDE\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r = p2.add_run("Dr. XXX,\n")
    r.bold = True
    r.font.name = "Times New Roman"
    r.font.color.rgb = COLOR_RED
    r = p2.add_run("Assistant Professor (Gr-2) or other designation\nSchool of Computing Science Engineering and\nArtificial Intelligence\nVIT BHOPAL UNIVERSITY")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)

    add_para(doc, "", space_after=40)
    add_para(doc, "The DSN4091-Capstone Project Phase-I Viva Voce Examination is held on ____________", font_size=11, space_before=20)

    doc.add_page_break()

    # ================= PAGE 3: ACKNOWLEDGEMENT =================
    add_para(doc, "ACKNOWLEDGEMENT", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=20, space_after=24)

    add_para(doc, "First and foremost, we would like to thank the Lord Almighty for his presence and immense blessings throughout the project work.", space_after=14, line_spacing=1.3)
    
    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_guide.paragraph_format.space_after = Pt(14)
    p_guide.paragraph_format.line_spacing = 1.3
    r = p_guide.add_run("We would like to thank our internal guide ")
    r.font.name = "Times New Roman"
    r = p_guide.add_run("Dr. XX")
    r.bold = True
    r.font.color.rgb = COLOR_RED
    r.font.name = "Times New Roman"
    r = p_guide.add_run(", for continually guiding and actively participating in our project, and giving valuable suggestions to complete the project works.")
    r.font.name = "Times New Roman"

    add_para(doc, "We wish to express our heartfelt gratitude to Dr. Pradeep Kumar Mishra, PC-Lead, School of Computing Science Engineering and Artificial Intelligence for much of his valuable support and encouragement in carrying out this work.", space_after=14, line_spacing=1.3)

    add_para(doc, "We wish to express our heartfelt gratitude to Dr Pon Harshavardhanan, Dean, School of Computing Science Engineering and Artificial Intelligence for much of his valuable support and encouragement in carrying out this work.", space_after=14, line_spacing=1.3)

    add_para(doc, "We would like to thank all the technical and teaching staff of the School of Computing Science Engineering and Artificial Intelligence, who extended directly or indirectly all support.", space_after=14, line_spacing=1.3)

    add_para(doc, "Last, but not least, we are deeply indebted to our parents who have been the greatest support while we worked day and night for the project to make it a success.", space_after=14, line_spacing=1.3)

    doc.add_page_break()

    # ================= PAGE 4: LIST OF FIGURES =================
    add_para(doc, "LIST OF FIGURES", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=20)

    fig_table = doc.add_table(rows=9, cols=3)
    fig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(fig_table, HEX_BORDER)

    headers = ["FIGURE NO.", "TITLE", "PAGE NO."]
    widths = [Inches(1.5), Inches(3.8), Inches(1.1)]

    for c_idx, h_text in enumerate(headers):
        cell = fig_table.cell(0, c_idx)
        cell.width = widths[c_idx]
        set_cell_background(cell, "E2E8F0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    fig_data = [
        ("1.0", "System Architectural Design & End-to-End Pipeline", "14"),
        ("2.0", "Closed-Loop Decision Intelligence Workflow", "15"),
        ("3.0", "Relational Schema and Digital Twin Entity-Relationship Diagram", "16"),
        ("4.0", "Executive Overview Control Room Dashboard Interface", "17"),
        ("5.0", "Digital Twin Geospatial Network Map Across Indian Corridors", "18"),
        ("6.0", "Scenario Simulation & Non-Destructive State Shock Control Flow", "22"),
        ("7.0", "Machine Learning Demand Forecasting Benchmarks", "26"),
        ("8.0", "Operational Cost Optimization Waterfall Under Disruption", "27")
    ]

    for row_idx, (f_num, f_title, f_page) in enumerate(fig_data, start=1):
        row = fig_table.rows[row_idx]
        for c_idx, val in enumerate([f_num, f_title, f_page]):
            cell = row.cells[c_idx]
            cell.width = widths[c_idx]
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx != 1 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)

    doc.add_page_break()

    # ================= PAGE 5: ABSTRACT =================
    add_para(doc, "ABSTRACT", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=18)

    abstract_p1 = (
        "Modern multi-echelon enterprise supply chains operate under conditions of persistent volatility, "
        "characterized by frequent supplier disruptions, transit delays, freight bottlenecks, and sharp demand surges. "
        "Conventional Enterprise Resource Planning (ERP) systems and Business Intelligence (BI) dashboards suffer "
        "from significant operational latency because they function predominantly as passive, descriptive reporting "
        "tools. They record historical failures rather than anticipating risk, diagnosing upstream failure cascades, "
        "or mathematically prescribing cost-effective counteractions. Consequently, supply chain managers frequently "
        "resort to manual, sub-optimal heuristics that amplify Bullwhip effects, incur massive stockout penalties, "
        "and severely compromise end-to-end service levels."
    )
    add_para(doc, abstract_p1, font_size=11.5, space_after=10, line_spacing=1.2)

    abstract_p2 = (
        "This project addresses these critical industry challenges through the design, implementation, and empirical "
        "validation of NEXUS — an AI-powered supply chain intelligence, predictive risk management, and multi-echelon "
        "linear optimization platform. Built upon an authentic Indian national logistics topology comprising 83 nodes "
        "(20 Suppliers, 8 Manufacturing Plants, 10 Central Warehouses, 15 Feeder Hubs, and 30 Regional Demand Zones) "
        "interconnected across 160 multimodal freight corridors, NEXUS implements a closed-loop decision workflow: "
        "Monitor → Predict → Analyze Impact → Simulate → Optimize → Recommend. The system unifies real-world empirical "
        "data foundations (Walmart Store Sales 421,570 records and DataCo Global Logistics 35,000 records) with "
        "machine learning algorithms, including lag-engineered XGBoost demand regressors (reducing RMSE by 29.5% over "
        "naive persistence), supervised supplier disruption classifiers (achieving 0.757 F1-score across unseen vendors), "
        "and unsupervised Isolation Forest anomaly detectors."
    )
    add_para(doc, abstract_p2, font_size=11.5, space_after=10, line_spacing=1.2)

    abstract_p3 = (
        "To translate predictive risk intelligence into operational execution, NEXUS features a NetworkX graph impact "
        "engine that calculates multi-tier inventory runways and flags catastrophic failure cascades. An in-memory "
        "scenario engine enables non-destructive 'what-if' shock simulation across 5 operational disruption archetypes. "
        "When shocks are detected, a mathematical optimization engine formulated in Google OR-Tools solves a 530-variable "
        "multi-echelon linear program in 0.011 seconds. Empirical benchmark experiments on an 80% capacity loss shock "
        "demonstrate that NEXUS slashes operational disruption costs by 53.89% (saving INR 22,542,319), completely "
        "eliminates 74,967 units of unmet shortages, and elevates network service levels from 51.24% to 100.00% compared "
        "to standard baseline heuristics. The platform delivers an enterprise-grade FastAPI REST backend and a responsive "
        "React 19 dark control-room dashboard featuring interactive Leaflet GIS mapping, Recharts telemetry, and "
        "plain-language executive decision directives."
    )
    add_para(doc, abstract_p3, font_size=11.5, space_after=12, line_spacing=1.2)

    doc.add_page_break()

    # ================= PAGES 6-8: TABLE OF CONTENTS =================
    add_para(doc, "TABLE OF CONTENTS", bold=True, font_size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=18)

    toc_table = doc.add_table(rows=1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_table, HEX_BORDER)

    toc_headers = ["CHAPTER NO.", "TITLE", "PAGE NO."]
    toc_widths = [Inches(1.4), Inches(4.0), Inches(1.0)]

    for c_idx, h_text in enumerate(toc_headers):
        cell = toc_table.cell(0, c_idx)
        cell.width = toc_widths[c_idx]
        set_cell_background(cell, "E2E8F0")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h_text)
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

    toc_rows = [
        ("", "List of Figures", "iv"),
        ("", "Abstract", "v"),
        ("1", "CHAPTER-1: PROJECT DESCRIPTION AND OUTLINE", "1"),
        ("", "1.1 Introduction", "1"),
        ("", "1.2 Motivation for the work", "1-2"),
        ("", "1.3 Problem Statement", "2"),
        ("", "1.4 Objective of the work", "2-3"),
        ("", "1.5 Summary", "3"),
        ("2", "CHAPTER-2: RELATED WORK INVESTIGATION", "4"),
        ("", "2.1 Existing Approaches/Methods", "4-5"),
        ("", "2.2 Pros and cons of the stated Approaches/Methods", "5-6"),
        ("3", "CHAPTER-3: REQUIREMENT ARTIFACTS", "7"),
        ("", "3.1 Introduction", "7"),
        ("", "3.2 Hardware and Software requirements", "7-8"),
        ("", "3.3 Specific Project requirements", "8"),
        ("", "    3.3.1 Data Requirements", "8"),
        ("", "    3.3.2 Functionality Requirements", "9"),
        ("", "    3.3.3 Performance Requirements", "9"),
        ("", "    3.3.4 Security Requirements", "9"),
        ("", "    3.3.5 Looks and Feel Requirements", "9-10"),
        ("", "3.4 Summary", "10"),
        ("4", "CHAPTER-4: DESIGN METHODOLOGY AND ITS NOVELTY", "11"),
        ("", "4.1 Methodology and goal", "11"),
        ("", "4.2 Functional modules design and analysis", "12-13"),
        ("", "4.3 Software Architectural designs", "13-15"),
        ("", "4.4 User Interface designs", "15-17"),
        ("", "4.5 Summary", "17"),
        ("5", "CHAPTER-5: TECHNICAL IMPLEMENTATION & ANALYSIS", "18"),
        ("", "5.1 Outline", "18-19"),
        ("", "5.2 Technical coding and code solutions", "19-20"),
        ("", "5.3 Prototype submission", "20-21"),
        ("", "5.4 Summary", "21-22"),
        ("6", "CHAPTER-6: PROJECT OUTCOME AND APPLICABILITY", "23"),
        ("", "6.1 Key implementations outline of the System", "23-24"),
        ("", "6.2 Significant project outcomes", "24-25"),
        ("", "6.3 Project applicability on Real-world applications", "25-26"),
        ("", "6.4 Inference", "26-27"),
        ("7", "CHAPTER-7: CONCLUSIONS AND RECOMMENDATION", "28"),
        ("", "7.1 Outline", "28-29"),
        ("", "7.2 Limitation/Constraints of the System", "29-30"),
        ("", "7.3 Future Enhancements", "30-31"),
        ("", "7.4 Inference", "31"),
        ("", "APPENDIX A – Screen Shots", "32-35"),
        ("", "APPENDIX B – Coding", "36-47"),
        ("", "REFERENCES", "48")
    ]

    for c_num, title, page in toc_rows:
        row = toc_table.add_row()
        for idx, val in enumerate([c_num, title, page]):
            cell = row.cells[idx]
            cell.width = toc_widths[idx]
            set_cell_margins(cell, 40, 40, 80, 80)
            p = cell.paragraphs[0]
            if idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(10)
            if "CHAPTER" in val or "APPENDIX" in val or "REFERENCES" in val:
                r.bold = True

    doc.add_page_break()


print("Preliminaries module loaded.")
