"""
NEXUS — AI-Powered Supply Chain Intelligence, Risk Prediction & Optimization Platform
Complete Faculty-Review-Ready Presentation Generator
Output: NEXUS_Project_Review_Presentation.pptx (+ PDF Export)
Presenter: Shreyansh Uttam | B.Tech CSE (AI & ML) | VIT Bhopal University
"""

import os
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT_DIR / "NEXUS_Presentation_Assets"
PPTX_OUTPUT = ROOT_DIR / "NEXUS_Project_Review_Presentation.pptx"
PDF_OUTPUT = ROOT_DIR / "NEXUS_Project_Review_Presentation.pdf"

# Palette definitions
BG_COLOR = RGBColor(11, 19, 43)       # #0B132B Deep Navy
PANEL_BG = RGBColor(17, 29, 74)       # #111D4A Slate Navy
PANEL_BORDER = RGBColor(30, 58, 138)  # #1E3A8A Dark Blue
CYAN = RGBColor(56, 189, 248)         # #38BDF8 Bright Cyan
TEAL = RGBColor(6, 182, 212)          # #06B6D4 Vibrant Teal
WHITE = RGBColor(255, 255, 255)       # Crisp White
SLATE = RGBColor(148, 163, 184)       # #94A3B8 Light Slate
LIGHT_CYAN = RGBColor(186, 230, 253)  # #BAE6FD Soft Cyan
EMERALD = RGBColor(16, 185, 129)      # #10B981 Success
AMBER = RGBColor(245, 158, 11)        # #F59E0B Warning
CRIMSON = RGBColor(239, 68, 68)       # #EF4444 Danger
ROW_ALT = RGBColor(23, 37, 84)        # #172554 Table alternate row
DARK_ACCENT = RGBColor(15, 23, 42)    # #0F172A

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOR

def add_header(slide, slide_num, category, title, lede):
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.38), Inches(11.5), Inches(0.32))
    tf_cat = cat_box.text_frame
    tf_cat.word_wrap = True
    tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = f"[ {slide_num:02d} / 23  •  {category.upper()} ]"
    p_cat.font.name = "Segoe UI"
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = CYAN

    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.7), Inches(0.55))
    tf_title = title_box.text_frame
    tf_title.word_wrap = True
    tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
    p_title = tf_title.paragraphs[0]
    p_title.text = title
    p_title.font.name = "Segoe UI"
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE

    lede_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.24), Inches(11.7), Inches(0.4))
    tf_lede = lede_box.text_frame
    tf_lede.word_wrap = True
    tf_lede.margin_left = tf_lede.margin_top = tf_lede.margin_right = tf_lede.margin_bottom = 0
    p_lede = tf_lede.paragraphs[0]
    p_lede.text = lede
    p_lede.font.name = "Segoe UI"
    p_lede.font.size = Pt(11)
    p_lede.font.color.rgb = SLATE

def add_footer(slide, slide_num):
    footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.733), Inches(0.3))
    tf = footer_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = f"NEXUS — AI-Powered Supply Chain Intelligence, Risk Prediction & Optimization  |  Shreyansh Uttam (VIT Bhopal)  |  Slide {slide_num} of 23"
    p.font.name = "Segoe UI"
    p.font.size = Pt(8.5)
    p.font.color.rgb = RGBColor(100, 116, 139)

def add_card(slide, left, top, width, height, title=None, fill_color=PANEL_BG, border_color=PANEL_BORDER, border_width=Pt(1)):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = border_color
    shape.line.width = border_width
    
    if title:
        tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.12), width - Inches(0.36), Inches(0.32))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CYAN
    return shape

def add_speaker_notes(slide, notes_text):
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text.strip()

def add_formatted_bullets(text_frame, items, font_size=9.5, space_after=5):
    for i, item in enumerate(items):
        if i == 0 and len(text_frame.paragraphs) > 0:
            p = text_frame.paragraphs[0]
        else:
            p = text_frame.add_paragraph()
        p.font.name = "Segoe UI"
        p.font.size = Pt(font_size)
        p.space_after = Pt(space_after)
        
        if isinstance(item, tuple):
            prefix, text = item
            run1 = p.add_run()
            run1.text = "• " + prefix + ": "
            run1.font.bold = True
            run1.font.color.rgb = WHITE
            run2 = p.add_run()
            run2.text = text
            run2.font.color.rgb = SLATE
        else:
            run = p.add_run()
            run.text = "• " + item
            run.font.color.rgb = SLATE

def create_table(slide, left, top, width, height, headers, rows, col_widths=None):
    num_rows = len(rows) + 1
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(num_rows, num_cols, left, top, width, height)
    table = table_shape.table
    
    if col_widths and len(col_widths) == num_cols:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w

    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PANEL_BORDER
        cell.text_frame.word_wrap = True
        cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
        cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.05)
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = "Segoe UI"
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    for r_idx, row in enumerate(rows):
        bg = ROW_ALT if r_idx % 2 == 1 else PANEL_BG
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.text_frame.word_wrap = True
            cell.text_frame.margin_left = cell.text_frame.margin_right = Inches(0.08)
            cell.text_frame.margin_top = cell.text_frame.margin_bottom = Inches(0.04)
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = "Segoe UI"
            p.font.size = Pt(8.5)
            p.font.color.rgb = WHITE if c_idx == 0 or "NEXUS" in str(val) or "Winner" in str(val) or "100" in str(val) else SLATE
            if "Winner" in str(val) or "100.0" in str(val) or "-53.19%" in str(val) or "-100%" in str(val):
                p.font.bold = True
                p.font.color.rgb = EMERALD
    return table_shape

# =============================================================
# SLIDE BUILDERS (1 TO 23)
# =============================================================

def build_slide_01(prs):
    """Slide 1: Title Slide"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)

    # Accent decorative glow box
    card = add_card(slide, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.8), fill_color=DARK_ACCENT, border_color=TEAL, border_width=Pt(1.5))

    # Brand Title
    tb_title = slide.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(10.9), Inches(1.2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p1 = tf_title.paragraphs[0]
    p1.text = "NEXUS"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(54)
    p1.font.bold = True
    p1.font.color.rgb = CYAN

    p2 = tf_title.add_paragraph()
    p2.text = "AI-Powered Supply Chain Intelligence, Risk Prediction & Optimization Platform"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(4)

    # Subtitle / Closed-loop tag
    tb_loop = slide.shapes.add_textbox(Inches(1.2), Inches(2.7), Inches(10.9), Inches(0.6))
    tf_loop = tb_loop.text_frame
    p_loop = tf_loop.paragraphs[0]
    p_loop.text = "MONITOR   →   PREDICT   →   ANALYZE IMPACT   →   SIMULATE   →   OPTIMIZE   →   RECOMMEND"
    p_loop.font.name = "Segoe UI"
    p_loop.font.size = Pt(11)
    p_loop.font.bold = True
    p_loop.font.color.rgb = TEAL

    # Presenter Card
    p_box = add_card(slide, Inches(1.2), Inches(3.6), Inches(5.5), Inches(2.5), title="PROJECT PRESENTATION & DEFENSE", fill_color=PANEL_BG, border_color=PANEL_BORDER)
    tb_pres = slide.shapes.add_textbox(Inches(1.4), Inches(4.1), Inches(5.1), Inches(1.8))
    tf_pres = tb_pres.text_frame
    tf_pres.word_wrap = True
    bullets = [
        ("Candidate", "Shreyansh Uttam (22BCE10738)"),
        ("Program", "B.Tech Computer Science & Engineering (AI & ML)"),
        ("School", "School of Computing Science and Engineering (SCSE)"),
        ("Institution", "VIT Bhopal University, Madhya Pradesh"),
        ("Focus Area", "Operations Research, Machine Learning & Digital Twins")
    ]
    add_formatted_bullets(tf_pres, bullets, font_size=10, space_after=4)

    # Architecture Snapshot Thumbnail on the right
    arch_img = ASSETS_DIR / "12_decision_intelligence_loop.png"
    if arch_img.exists():
        slide.shapes.add_picture(str(arch_img), Inches(7.0), Inches(3.6), Inches(5.1), Inches(2.5))

    add_footer(slide, 1)
    add_speaker_notes(slide, """
Good morning, respected faculty members. My name is Shreyansh Uttam, and I am presenting NEXUS—an AI-powered supply chain intelligence, risk prediction, and optimization platform. 

In this presentation, I will walk you through the complete engineering lifecycle of NEXUS: from empirical data grounding and our multi-echelon digital twin to predictive machine learning, graph impact propagation, non-destructive simulation, Google OR-Tools optimization, and our interactive React control room. The core innovation of NEXUS is closing the loop from sensing an upstream disruption to computing mathematically optimal reallocation directives in under 10 milliseconds.
""")

def build_slide_02(prs):
    """Slide 2: The Supply Chain Problem"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 2, "PROBLEM STATEMENT & MOTIVATION", 
               "The Supply Chain Fragility Problem", 
               "Modern multi-echelon supply networks suffer from fragmented data, delayed analysis, and rigid static contracts.")

    # Left Card: Traditional Legacy Workflow
    add_card(slide, Inches(0.8), Inches(1.75), Inches(5.6), Inches(4.9), title="TRADITIONAL DECISION BOTTLENECKS", fill_color=PANEL_BG, border_color=CRIMSON)
    tb_left = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.3))
    tf_left = tb_left.text_frame
    tf_left.word_wrap = True

    bullets_left = [
        ("The Traditional Workflow", "Raw Data → Spreadsheets / Static ERP Reports → Manual Human Analysis → Delayed Decisions."),
        ("Demand Uncertainty & Bullwhip Effect", "Small shifts in consumer velocity amplify upstream into massive order swings, causing stockouts or inventory glut."),
        ("Multi-Tier Blindspots", "Enterprises lack visibility past Tier-1 suppliers; Tier-2 subassembly failures trigger sudden production halts."),
        ("Rigid Single-Sourcing", "Fixed contracts prevent dynamic rerouting; when a primary vendor collapses, downstream facilities face immediate stockouts."),
        ("High Contractual Penalties", "Unmitigated stockouts accumulate steep contractual SLA breach fees (e.g. INR 350 per unmet unit)."),
        ("Disconnected Systems", "Forecasting, inventory, and logistics exist in separate silos without an automated closed-loop feedback engine.")
    ]
    add_formatted_bullets(tf_left, bullets_left, font_size=9.5, space_after=6)

    # Right Card: Visual Impact & The Core Need
    add_card(slide, Inches(6.7), Inches(1.75), Inches(5.833), Inches(4.9), title="DISRUPTION CASCADE & THE CORE NEED", fill_color=PANEL_BG, border_color=PANEL_BORDER)
    
    img_cascade = ASSETS_DIR / "slide_impact_propagation.png"
    if img_cascade.exists():
        slide.shapes.add_picture(str(img_cascade), Inches(6.9), Inches(2.2), Inches(5.4), Inches(2.6))

    tb_callout = slide.shapes.add_textbox(Inches(6.9), Inches(4.9), Inches(5.4), Inches(1.6))
    tf_callout = tb_callout.text_frame
    tf_callout.word_wrap = True
    p = tf_callout.paragraphs[0]
    p.text = "THE ENGINEERING NEED:"
    p.font.name = "Segoe UI"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p_body = tf_callout.add_paragraph()
    p_body.text = "A unified decision intelligence platform that transitions supply chain management from reactive firefighting to automated, mathematically proven mitigation before stockouts materialize."
    p_body.font.name = "Segoe UI"
    p_body.font.size = Pt(9.5)
    p_body.font.color.rgb = WHITE
    p_body.space_before = Pt(3)

    add_footer(slide, 2)
    add_speaker_notes(slide, """
To understand why NEXUS was built, consider the traditional enterprise workflow. Today, when a supplier experiences an unscheduled shutdown or a highway corridor is blocked, data trickles through disconnected spreadsheets and legacy ERP reports. Planners spend days manually analyzing spreadsheets. By the time a decision is made, downstream assembly lines have halted and massive contractual SLA penalties have already accrued.

Furthermore, traditional supply chains rely on rigid single-sourcing contracts. Even when the broader national network has surplus capacity, downstream warehouses cannot dynamically pivot. As shown in the diagram on the right, an 80% failure at a single Tier-1 supplier cascades across production units, depletes warehouse safety stock, and starves metropolitan demand zones. The goal of NEXUS is to replace this delayed manual process with an automated, closed-loop decision system.
""")

def build_slide_03(prs):
    """Slide 3: The NEXUS Solution"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 3, "CORE VALUE PROPOSITION", 
               "From Monitoring to Decision — The Closed Loop", 
               "NEXUS unifies monitoring, machine learning, graph analysis, simulation, and optimization into a single automated pipeline.")

    # Flow graphic in top half
    img_loop = ASSETS_DIR / "slide_closed_loop_flow.png"
    if img_loop.exists():
        slide.shapes.add_picture(str(img_loop), Inches(0.8), Inches(1.75), Inches(11.733), Inches(2.35))

    # 6 Stage description cards below
    stages = [
        ("1. MONITOR", "Digital Twin State", "Real-time telemetry across 83 nodes, tracking inventory valuation and corridor transit status.", CYAN),
        ("2. PREDICT", "Predictive Analytics", "XGBoost Regressor for multi-step demand and XGBoost Classifier for supplier failure probability.", TEAL),
        ("3. ANALYZE IMPACT", "Graph Propagation", "NetworkX directed graph BFS tracing downstream dependency paths and stock runway days.", RGBColor(129, 140, 248)),
        ("4. SIMULATE", "What-If Stress Testing", "Non-destructive in-memory state shock cloning supporting 5 distinct operational disruption modes.", AMBER),
        ("5. OPTIMIZE", "Google OR-Tools", "Global multi-echelon linear program minimizing procurement, freight, holding, and penalty costs.", EMERALD),
        ("6. RECOMMEND", "Actionable Directives", "Automated synthesis of plain-language executive directives with LP Plan Robustness scoring.", CYAN)
    ]

    card_w = Inches(1.85)
    gap = Inches(0.12)
    start_x = Inches(0.8)

    for idx, (title, sub, desc, border_c) in enumerate(stages):
        x = start_x + idx * (card_w + gap)
        add_card(slide, x, Inches(4.3), card_w, Inches(2.6), fill_color=PANEL_BG, border_color=border_c)
        
        tb = slide.shapes.add_textbox(x + Inches(0.1), Inches(4.4), card_w - Inches(0.2), Inches(2.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = border_c
        
        p2 = tf.add_paragraph()
        p2.text = sub
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(8.5)
        p2.font.bold = True
        p2.font.color.rgb = WHITE
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(8)
        p3.font.color.rgb = SLATE
        p3.space_before = Pt(4)

    add_footer(slide, 3)
    add_speaker_notes(slide, """
This slide represents the core architectural identity of NEXUS: the closed-loop decision cycle. 

Most existing academic projects stop at machine learning predictions without determining operational actions. NEXUS connects the entire loop across six automated stages. First, we continuously MONITOR the digital twin network. Second, we PREDICT future demand and supplier failure probability using supervised ML. Third, we ANALYZE IMPACT using graph traversal to calculate exact warehouse runway days. Fourth, we SIMULATE the operational shock in memory. Fifth, we OPTIMIZE global sourcing and routing allocations using Google OR-Tools. And sixth, we RECOMMEND plain-language, executable directives. Every stage feeds directly into the next, ensuring real-time decision intelligence.
""")

def build_slide_04(prs):
    """Slide 4: System Overview"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 4, "SYSTEM ARCHITECTURE", 
               "How NEXUS Works — End-to-End Architecture", 
               "A decoupled, seven-layer engineering architecture connecting empirical datasets, ML pipelines, optimization, and React UI.")

    # Left: Architecture Diagram
    img_arch = ASSETS_DIR / "11_system_architecture_diagram.png"
    if img_arch.exists():
        slide.shapes.add_picture(str(img_arch), Inches(0.8), Inches(1.75), Inches(5.6), Inches(4.9))

    # Right: 7 Architecture Layers Breakdown
    add_card(slide, Inches(6.6), Inches(1.75), Inches(5.933), Inches(4.9), title="SEVEN-LAYER DECOUPLED STACK", fill_color=PANEL_BG, border_color=PANEL_BORDER)
    tb_arch = slide.shapes.add_textbox(Inches(6.8), Inches(2.15), Inches(5.5), Inches(4.4))
    tf_arch = tb_arch.text_frame
    tf_arch.word_wrap = True

    layers = [
        ("Layer 1: Ingestion & Provenance", "Walmart sales (421k rows), DataCo shipments (35k rows), and Indian hub geodesy."),
        ("Layer 2: Preprocessing & Validation", "Strict Pydantic v2 schemas, Parquet serialization, and 14-lag feature engineering."),
        ("Layer 3: Relational Persistence", "SQLite 3 database (14 tables, 50k orders, 500 inventory items, PostgreSQL DDL ready)."),
        ("Layer 4: Machine Learning & Analytics", "XGBoost Regressor, XGBoost Risk Classifier, and Isolation Forest anomaly detector."),
        ("Layer 5: Graph & Simulation Engine", "NetworkX multi-echelon directed graph (BFS cascade) and in-memory copy-on-write ScenarioEngine."),
        ("Layer 6: Operations Research", "Google OR-Tools GLOP linear solver enforcing multi-echelon flow, capacity, and demand satisfaction."),
        ("Layer 7: Presentation & Control Room", "FastAPI (20 REST endpoints) driving a modern React 19 TypeScript control room.")
    ]
    add_formatted_bullets(tf_arch, layers, font_size=9, space_after=4.5)

    add_footer(slide, 4)
    add_speaker_notes(slide, """
Here is the complete end-to-end system architecture of NEXUS, designed as a 7-layer decoupled enterprise stack. 

At the bottom, our ingestion layer ingests real empirical data from Walmart and DataCo, validated strictly by Pydantic v2 schemas into our SQLite database. The persistence layer manages 14 relational tables. The Intelligence Layer executes our three machine learning models. 

These model outputs pass directly into the Graph and Simulation Layer, which models the supply chain as a multi-echelon directed graph in NetworkX. During a shock, the ScenarioEngine forks an in-memory clone of the network state. The Operations Research layer then executes a linear program using Google OR-Tools to solve global allocation. Finally, the FastAPI backend exposes 20 RESTful endpoints to our React 19 frontend.
""")

def build_slide_05(prs):
    """Slide 5: Datasets"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 5, "DATA FOUNDATION", 
               "Data Foundation — Empirical vs Simulated Data", 
               "NEXUS combines real-world empirical time-series and shipment records with a calibrated synthetic digital twin.")

    # Table of Datasets
    headers = ["Dataset Source", "Nature of Data", "Verified Volume / Scope", "Target Analytical Purpose in NEXUS"]
    rows = [
        ["Walmart Store Sales", "Public Empirical\n(Kaggle Research)", "421,570 weekly historical records\n45 stores, 81 depts, 2.5+ years horizon", "Multi-step weekly demand forecasting,\nautoregressive lags, calendar seasonality"],
        ["DataCo Global Supply Chain", "Public Empirical\n(Mendeley Data CC BY 4.0)", "35,000+ representative shipments\n180,519 order corpus, real transit delays", "Supervised supplier disruption risk,\nlead-time variability, delivery failure modeling"],
        ["Indian Logistics Digital Twin", "Calibrated Synthetic\n(Reproducible Topology)", "83 facility nodes, 160 corridors,\n50,000 orders, 500 inventory items", "Multi-echelon network topology, geodesy,\nimpact propagation, OR-Tools optimization"]
    ]
    create_table(slide, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.6), headers, rows, 
                 col_widths=[Inches(2.4), Inches(2.0), Inches(3.6), Inches(3.733)])

    # Bottom Two Panels: Real vs Synthetic distinction
    add_card(slide, Inches(0.8), Inches(4.7), Inches(5.7), Inches(2.1), title="EMPIRICAL GROUNDING (REAL DATA)", fill_color=PANEL_BG, border_color=EMERALD)
    tb_real = slide.shapes.add_textbox(Inches(1.0), Inches(5.1), Inches(5.3), Inches(1.6))
    tf_real = tb_real.text_frame
    tf_real.word_wrap = True
    bullets_real = [
        ("Real Sales Volatility", "Captures genuine retail demand spikes, holiday surges, and trend seasonality that synthetic sine-waves cannot reproduce."),
        ("Real Delivery Delays", "Trained on authentic international freight delay distributions where actual transit days exceeded scheduled days.")
    ]
    add_formatted_bullets(tf_real, bullets_real, font_size=9, space_after=4)

    add_card(slide, Inches(6.833), Inches(4.7), Inches(5.7), Inches(2.1), title="ACADEMIC HONESTY (SIMULATED TWIN)", fill_color=PANEL_BG, border_color=AMBER)
    tb_synth = slide.shapes.add_textbox(Inches(7.033), Inches(5.1), Inches(5.3), Inches(1.6))
    tf_synth = tb_synth.text_frame
    tf_synth.word_wrap = True
    bullets_synth = [
        ("Simulated Indian Topology", "Real corporate facility BOMs and internal supplier networks are strictly confidential."),
        ("Calibrated Distributions", "NEXUS maps empirical Walmart and DataCo distributions onto realistic Indian hubs (Delhi, Mumbai, Pune, Sanand, Bengaluru).")
    ]
    add_formatted_bullets(tf_synth, bullets_synth, font_size=9, space_after=4)

    add_footer(slide, 5)
    add_speaker_notes(slide, """
A critical question in any AI project review is data provenance: where does the data come from? In supply chain management, real corporate operational databases are proprietary and legally confidential. Therefore, NEXUS employs a hybrid data strategy with strict academic honesty. 

We do not fabricate numbers. For demand forecasting, we use Walmart's empirical dataset of 421,570 weekly sales records from Kaggle, capturing real calendar seasonality and holiday spikes. For supplier risk modeling, we utilize the DataCo Global Supply Chain dataset from Mendeley, containing over 35,000 empirical shipments with actual lead-time delays and delivery failures. We then calibrate these statistical distributions onto an 83-node Indian logistics digital twin. As clearly labeled on the right, the network topology is a calibrated synthetic twin, ensuring full reproducibility while maintaining realistic industrial complexity.
""")

def build_slide_06(prs):
    """Slide 6: Data Pipeline"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 6, "DATA PIPELINE & FEATURE ENGINEERING", 
               "From Raw Data to Decision-Ready Intelligence", 
               "Systematic feature engineering, temporal shift guards, and in-memory state representations.")

    # 4 Pipeline Cards
    pipeline_cards = [
        ("1. DEMAND TIME-SERIES ENGINEERING", [
            ("Autoregressive Lags", "Lags t-1, t-2, t-4, t-8 capturing cyclical ordering patterns."),
            ("Rolling Window Stats", "4-week and 8-week moving averages (μ) and 4-week rolling volatility (σ)."),
            ("Temporal Guard", "All rolling metrics strictly shifted by 1 period (shift(1)) to prevent lookahead data leakage."),
            ("Calendar Seasonality", "Deterministic trend index, ISO week of year, month, and holiday flags.")
        ], CYAN),
        ("2. SUPPLIER RISK FEATURE EXTRACTION", [
            ("Lead-Time Volatility", "Standard deviation of delivery lead-time (primary collapse predictor)."),
            ("Operational Metrics", "Historical delay frequency, average late days, and on-time fulfillment rate."),
            ("Capacity Strain", "Plant capacity utilization ratio and quality assurance defect rate."),
            ("Stochastic Shock", "Latent operational stress modeling unannounced industrial failures.")
        ], TEAL),
        ("3. SPATIAL GEODESY & CORRIDORS", [
            ("Geocoded Facilities", "83 exact geographic coordinates across canonical Indian logistics corridors."),
            ("Highway Tortuosity", "Haversine distance multiplied by 1.22x tortuosity factor for authentic road transit km."),
            ("Multimodal Modes", "Differentiated transit speeds and costs for National Expressways vs Dedicated Rail Freight."),
            ("Corridor Capacity", "Throughput bottlenecks and maximum lane vehicle volumes.")
        ], RGBColor(129, 140, 248)),
        ("4. OPERATIONAL RUNWAY & SHOCK STATE", [
            ("Stock Runway Metric", "Runway (Days) = Current Inventory / Daily Consumption Burn Rate."),
            ("Buffer Depletion", "Pinpoints exact calendar day of catastrophic warehouse stockout."),
            ("In-Memory State Cloning", "Deep copy of SimulationState instantiates non-destructive shock test."),
            ("Allocation Feasibility", "Calculates net gross capacity surplus/deficit across all network echelons.")
        ], EMERALD)
    ]

    card_w = Inches(5.6)
    card_h = Inches(2.35)

    positions = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.8), Inches(1.8)),
        (Inches(0.8), Inches(4.45)),
        (Inches(6.8), Inches(4.45))
    ]

    for idx, (title, bullets, border_c) in enumerate(pipeline_cards):
        x, y = positions[idx]
        add_card(slide, x, y, card_w, card_h, title=title, fill_color=PANEL_BG, border_color=border_c)
        tb = slide.shapes.add_textbox(x + Inches(0.18), y + Inches(0.45), card_w - Inches(0.36), card_h - Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        add_formatted_bullets(tf, bullets, font_size=8.5, space_after=3.5)

    add_footer(slide, 6)
    add_speaker_notes(slide, """
Raw supply chain data cannot be fed directly into decision algorithms. This slide illustrates our feature engineering pipeline across four critical dimensions. 

For demand forecasting, we construct 14 autoregressive and calendar features. To ensure rigorous academic methodology, all rolling window statistics are strictly shifted by one time period to eliminate lookahead data leakage. For supplier risk, we extract operational variance metrics, notably lead-time standard deviation and historical delay frequency. For spatial corridors, we geocode 83 facilities and apply a 1.22 highway tortuosity factor to convert geodesic distances into realistic road transit kilometers. Finally, we compute warehouse stock runway by dividing current inventory by daily burn rate, allowing us to predict exact stockout dates before they occur.
""")

def build_slide_07(prs):
    """Slide 7: Digital Supply Chain Twin"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 7, "DIGITAL TWIN TOPOLOGY", 
               "The NEXUS Digital Twin — Calibrated Multi-Echelon Network", 
               "An 83-node, 160-corridor digital representation spanning five operational supply chain tiers.")

    # Top diagram: 5 Echelons Summary
    img_topo = ASSETS_DIR / "slide_network_topology.png"
    if img_topo.exists():
        slide.shapes.add_picture(str(img_topo), Inches(0.8), Inches(1.75), Inches(11.733), Inches(2.2))

    # Bottom Left: Map screenshot
    img_map = ASSETS_DIR / "02_digital_twin_network.png"
    if img_map.exists():
        slide.shapes.add_picture(str(img_map), Inches(0.8), Inches(4.15), Inches(5.6), Inches(2.75))

    # Bottom Right: Verified Topology Breakdown
    add_card(slide, Inches(6.6), Inches(4.15), Inches(5.933), Inches(2.75), title="VERIFIED DIGITAL TWIN METRICS", fill_color=PANEL_BG, border_color=CYAN)
    tb_metrics = slide.shapes.add_textbox(Inches(6.8), Inches(4.55), Inches(5.5), Inches(2.2))
    tf_metrics = tb_metrics.text_frame
    tf_metrics.word_wrap = True

    metrics = [
        ("Total Facilities", "83 geocoded nodes across canonical Indian logistics corridors."),
        ("20 Suppliers", "Tier-1 & Tier-2 automotive, metallurgy, polymer, and precision parts."),
        ("8 Production Units", "OEM manufacturing & assembly plants (Sanand, Pune, Gurgaon, Sriperumbudur)."),
        ("10 Central Warehouses", "Regional distribution centers tracking 500 SKUs with INR 45.92M valuation."),
        ("15 Distribution Hubs", "Intermediate multimodal transshipment and sorting facilities."),
        ("30 Demand Zones", "Tier-1/Tier-2 consumption centers representing 153.6k units of demand."),
        ("160 Corridors", "Active freight transit lanes calibrated with authentic transit hours.")
    ]
    add_formatted_bullets(tf_metrics, metrics, font_size=8.5, space_after=2.5)

    add_footer(slide, 7)
    add_speaker_notes(slide, """
Here we see the NEXUS Digital Twin network. The network models an authentic multi-echelon supply chain across India, comprising exactly 83 facility nodes and 160 multimodal corridors. 

The echelons represent five distinct functional tiers: 20 raw material and component suppliers, 8 manufacturing and assembly plants located in industrial clusters like Sanand and Pune, 10 central distribution warehouses tracking 500 SKUs with a total inventory valuation of 45.9 million rupees, 15 sorting hubs, and 30 consumer demand zones representing over 153,000 units of periodic demand. The digital twin maintains complete telemetry on stock levels, daily burn rates, operational capacities, and unit transit costs.
""")

def build_slide_08(prs):
    """Slide 8: Machine Learning Layer"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 8, "INTELLIGENCE LAYER", 
               "Intelligence Layer — Forecasting, Risk & Anomaly Detection", 
               "Three specialized analytical models addressing distinct operational supply chain failure modes.")

    # 3 Parallel Columns
    models = [
        ("1. DEMAND FORECASTING", "XGBoost Regressor", CYAN, [
            ("Objective", "Predict multi-step demand velocity over a 4-week horizon to prevent bullwhip distortion."),
            ("Input Vector", "14 engineered features: autoregressive lags (t-1 to t-8), rolling mean/std (4W/8W), calendar seasonality."),
            ("Algorithm", "Gradient Boosted Trees (150 estimators, max depth 4, learning rate 0.05, subsample 0.85)."),
            ("Output", "Weekly expected demand quantity with multi-horizon confidence intervals.")
        ]),
        ("2. SUPPLIER DISRUPTION RISK", "XGBoost Classifier", TEAL, [
            ("Objective", "Predict the probability of vendor SLA breach or operational failure before stockouts occur."),
            ("Input Vector", "8 operational variance metrics: lead-time std dev, nominal lead-time, delay frequency, OTR, quality score."),
            ("Algorithm", "Supervised classification with scale_pos_weight=1.5 and tree depth 3."),
            ("Output", "Disruption probability score [0.0, 1.0], risk tier (Low/Med/High/Critical), and explainable feature weights.")
        ]),
        ("3. OPERATIONAL ANOMALY DETECTION", "Isolation Forest", RGBColor(129, 140, 248), [
            ("Objective", "Unsupervised real-time detection of sudden demand surges and unprecedented transit delays."),
            ("Input Vector", "Continuous transaction streams: order quantities, delivery deviations, and velocity spikes."),
            ("Algorithm", "Isolation Forest (100 estimators, contamination rate α = 0.03)."),
            ("Output", "Normalized anomaly score and classification taxonomy (UNUSUAL_DEMAND_SPIKE, TRANSIT_DELAY_OUTLIER).")
        ])
    ]

    col_w = Inches(3.75)
    gap = Inches(0.24)
    start_x = Inches(0.8)

    for idx, (title, sub, border_c, bullets) in enumerate(models):
        x = start_x + idx * (col_w + gap)
        add_card(slide, x, Inches(1.8), col_w, Inches(4.9), title=title, fill_color=PANEL_BG, border_color=border_c)
        
        # Sub-header badge
        tb_sub = slide.shapes.add_textbox(x + Inches(0.18), Inches(2.2), col_w - Inches(0.36), Inches(0.3))
        tf_sub = tb_sub.text_frame
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = f"Architecture: {sub}"
        p_sub.font.name = "Segoe UI"
        p_sub.font.size = Pt(9.5)
        p_sub.font.bold = True
        p_sub.font.color.rgb = WHITE

        tb = slide.shapes.add_textbox(x + Inches(0.18), Inches(2.6), col_w - Inches(0.36), Inches(3.9))
        tf = tb.text_frame
        tf.word_wrap = True
        add_formatted_bullets(tf, bullets, font_size=8.5, space_after=6)

    add_footer(slide, 8)
    add_speaker_notes(slide, """
The Intelligence Layer contains three specialized machine learning models, each targeted at a specific vulnerability. 

First, the Demand Forecasting model uses an XGBoost Regressor trained on 14 lag and calendar features to forecast future demand velocity across a multi-step horizon. Second, our Supplier Risk Prediction model uses an XGBoost Classifier with positive class weighting to predict the probability of vendor failure before catastrophic stockouts occur. Third, we implement an unsupervised Isolation Forest anomaly detector with a 3% contamination threshold that continuously scans transaction volumes and transit logs to flag sudden demand surges or unprecedented lead-time deviations in real time.
""")

def build_slide_09(prs):
    """Slide 9: Model Comparison"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 9, "MODEL BENCHMARKING & EVALUATION", 
               "Empirical Model Evaluation & Benchmark Comparison", 
               "Rigorous out-of-sample benchmarking against industry baseline algorithms on strictly held-out test data.")

    # Left: Demand Forecasting Table & Chart
    add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), title="DEMAND FORECASTING BENCHMARK", fill_color=PANEL_BG, border_color=CYAN)
    
    headers_fc = ["Model Architecture", "MAE", "RMSE", "sMAPE", "Rank"]
    rows_fc = [
        ["Naive Persistence", "110,961.63", "136,255.10", "7.20%", "2"],
        ["Moving Avg (4-Week)", "135,495.41", "153,446.84", "8.42%", "3"],
        ["Moving Avg (8-Week)", "194,063.88", "210,775.27", "11.80%", "4"],
        ["XGBoost Regressor (NEXUS)", "68,553.14", "96,042.50", "4.35%", "1 (Winner)"]
    ]
    create_table(slide, Inches(1.0), Inches(2.2), Inches(5.2), Inches(1.8), headers_fc, rows_fc,
                 col_widths=[Inches(1.8), Inches(0.9), Inches(0.9), Inches(0.8), Inches(0.8)])

    img_fc = ASSETS_DIR / "slide_forecast_benchmark.png"
    if img_fc.exists():
        slide.shapes.add_picture(str(img_fc), Inches(1.0), Inches(4.1), Inches(5.2), Inches(2.45))

    # Right: Supplier Risk Table & Chart
    add_card(slide, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.9), title="SUPPLIER RISK OUT-OF-SAMPLE BENCHMARK", fill_color=PANEL_BG, border_color=TEAL)

    headers_risk = ["Model Architecture", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    rows_risk = [
        ["Logistic Regression Baseline", "0.7531", "0.7349", "0.7439", "0.7401"],
        ["XGBoost Classifier (NEXUS)", "0.7442", "0.7711", "0.7574", "0.6988"]
    ]
    create_table(slide, Inches(7.0), Inches(2.2), Inches(5.333), Inches(1.3), headers_risk, rows_risk,
                 col_widths=[Inches(2.133), Inches(0.8), Inches(0.8), Inches(0.8), Inches(0.8)])

    img_risk = ASSETS_DIR / "slide_risk_benchmark.png"
    if img_risk.exists():
        slide.shapes.add_picture(str(img_risk), Inches(7.0), Inches(3.6), Inches(5.333), Inches(2.95))

    add_footer(slide, 9)
    add_speaker_notes(slide, """
This slide demonstrates the empirical evaluation of our models. 

For demand forecasting, we evaluated our XGBoost Regressor against standard industry baselines: Naive persistence and Moving Averages. The results show that XGBoost reduces RMSE by 29.5% compared to the Naive baseline and lowers sMAPE down to 4.35%. 

For supplier risk, we addressed a critical academic pitfall discovered during our Phase 2 audit: previous iterations had data leakage that created artificial 1.0 accuracy. We resolved this by implementing an independent latent stress data generator and evaluated the model using GroupShuffleSplit across 40 vendors. The 10 test vendors were completely unseen during training. XGBoost achieved an F1-score of 0.7574 with a high recall of 77.1%, which is critical in supply chains because missing a vendor failure is far more costly than a false alarm. Feature importance analysis proves that lead-time variability and nominal lead time account for over 42% of predictive risk.
""")

def build_slide_10(prs):
    """Slide 10: Decision Matrix"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 10, "DECISION INTELLIGENCE", 
               "The NEXUS Decision Matrix — From Signal to Action", 
               "Prediction alone does not make decisions; NEXUS pairs signals with downstream impact and mathematical optimization.")

    # Decision Matrix Table
    headers_dm = ["Operational Signal", "Detection Mechanism", "Downstream Network Impact", "NEXUS Prescriptive Decision"]
    rows_dm = [
        ["Demand Spike / Surge", "XGBoost Regressor\n(multi-step forecast)", "Depletes warehouse safety buffer;\nstockout risk within 14 days", "Dynamically scale production quotas &\nincrease supplier procurement allocations"],
        ["Supplier Capacity Loss", "Supervised Risk Classifier\n+ ScenarioEngine", "Upstream component starvation;\nTier-1 assembly line halt", "Shift sourcing allocation to qualified secondary\nvendors (e.g. SUP_005, SUP_009)"],
        ["Route Delay / Blockage", "NetworkX Graph Centrality\n& Geodesy Engine", "Transit time extended by 2-5 days;\nlate delivery SLA penalties", "Reroute freight via alternative multimodal\nrail/expressway corridors"],
        ["Inventory Runway Depletion", "Runway Calculus\n(Stock / Daily Burn Rate)", "Imminent stockout (< 7 days runway)\nat regional central warehouse", "Trigger rapid inter-warehouse safety stock\ntransfers via rail corridors"],
        ["Multi-Node System Shock", "Scenario Simulation Engine\n(copy-on-write state)", "Cascading multi-tier deficit across\nmultiple metropolitan demand zones", "Execute Google OR-Tools multi-echelon linear\nprogram to find global cost-optimal allocation"]
    ]
    create_table(slide, Inches(0.8), Inches(1.8), Inches(11.733), Inches(3.4), headers_dm, rows_dm,
                 col_widths=[Inches(2.2), Inches(2.4), Inches(3.2), Inches(3.933)])

    # Bottom Principle Card
    add_card(slide, Inches(0.8), Inches(5.35), Inches(11.733), Inches(1.5), title="THE NEXUS DECISION PRINCIPLE", fill_color=DARK_ACCENT, border_color=TEAL)
    tb_prin = slide.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.333), Inches(0.9))
    tf_prin = tb_prin.text_frame
    tf_prin.word_wrap = True
    p = tf_prin.paragraphs[0]
    p.text = "Prediction is only an input, not a solution."
    p.font.name = "Segoe UI"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = CYAN

    p2 = tf_prin.add_paragraph()
    p2.text = "A prediction of 80% supplier risk does not tell a manager how many units to reroute, which alternative vendor has capacity, or what the freight cost tradeoff will be. NEXUS bridges this gap by combining Prediction + Network Impact + Scenario Simulation + Mathematical Optimization into concrete, actionable decisions."
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = WHITE
    p2.space_before = Pt(3)

    add_footer(slide, 10)
    add_speaker_notes(slide, """
A central question faculty often ask is: 'Why is this an engineering decision system rather than just a machine learning project?' This slide answers that directly. Prediction alone does not make a business decision. 

A prediction of 80% supplier risk does not tell a manager how many units to reroute, which alternative supplier has surplus capacity, or what the transportation cost trade-off will be. The NEXUS Decision Matrix connects every incoming signal—whether it is a demand surge, a supplier failure, or a highway blockage—to its downstream network impact, runs a simulation to test the constraint boundaries, and then executes mathematical optimization to output the exact procurement and routing decisions.
""")

def build_slide_11(prs):
    """Slide 11: Impact Propagation"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 11, "NETWORK GRAPH ANALYSIS", 
               "Impact Propagation — What Happens When a Node Fails?", 
               "NetworkX directed graph traversal (BFS) traces the ripple effect of upstream shocks across all downstream tiers.")

    # Left: Cascade diagram
    img_cascade = ASSETS_DIR / "slide_impact_propagation.png"
    if img_cascade.exists():
        slide.shapes.add_picture(str(img_cascade), Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.9))

    # Right: Impact Mechanics
    add_card(slide, Inches(7.0), Inches(1.8), Inches(5.533), Inches(4.9), title="GRAPH TRAVERSAL & RUNWAY CALCULUS", fill_color=PANEL_BG, border_color=PANEL_BORDER)
    tb_imp = slide.shapes.add_textbox(Inches(7.2), Inches(2.2), Inches(5.1), Inches(4.3))
    tf_imp = tb_imp.text_frame
    tf_imp.word_wrap = True

    mechanics = [
        ("Multi-Tier Graph Traversal", "NetworkX directed graph executes Breadth-First Search (BFS) starting from the disrupted supplier node down to final demand zones."),
        ("Component Dependency Mapping", "Directly maps disrupted supplier parts to downstream Bill-of-Materials (PROD_ITEM_003 automotive subassembly)."),
        ("Warehouse Runway Calculus", "Runway Days = Current Stock / Daily Burn Rate. For Western Warehouse (WH_01): 1,420 units / 280 units/day = 5.07 Days Runway."),
        ("Pinpointing Stockout Dates", "Pinpoints exact day of stockout: WH_01 depletes completely on Day 6 without intervention."),
        ("Service Level Degradation", "Network-wide on-time fulfillment projected to plummet from 98.0% baseline down to 54.57%."),
        ("Exposed Demand Volume", "69,843.2 units of unmet demand exposed across 5 metropolitan consumption zones (Mumbai, Pune, Delhi NCR, Jaipur, Ahmedabad)."),
        ("Automated Mitigation Search", "Graph engine immediately queries active secondary suppliers with matching product categories and surplus capacity.")
    ]
    add_formatted_bullets(tf_imp, mechanics, font_size=8.5, space_after=4.5)

    add_footer(slide, 11)
    add_speaker_notes(slide, """
When a disruption strikes, its damage is rarely confined to the immediate node; it ripples downstream. In NEXUS, we use NetworkX directed graph traversal to trace this propagation. 

In our flagship scenario, when supplier SUP_001 in Pune loses 80% capacity, our BFS engine traces the failure downstream to the assembly plant in Sanand, and then to two central warehouses: WH_01 in the West and WH_02 in the North. Our stock runway algorithm calculates that WH_01 has only 5.07 days of buffer stock remaining before a total stockout occurs on Day 6. This allows the system to determine the exact downstream shortage—in this case, 69,843 units across five demand zones—before the physical stockout ever takes place.
""")

def build_slide_12(prs):
    """Slide 12: Scenario Simulation"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 12, "WHAT-IF SIMULATION", 
               "Scenario Simulation — Non-Destructive In-Memory Testing", 
               "Evaluating operational network resilience across five parameterized disruption scenarios without persistent DB modification.")

    # Left: Scenario Simulation Screenshot
    img_sim = ASSETS_DIR / "06_scenario_simulation.png"
    if img_sim.exists():
        slide.shapes.add_picture(str(img_sim), Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.9))

    # Right: 5 Disruption Scenarios & Copy-on-Write
    add_card(slide, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.9), title="FIVE VERIFIED DISRUPTION SCENARIOS", fill_color=PANEL_BG, border_color=AMBER)
    tb_scen = slide.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_scen = tb_scen.text_frame
    tf_scen.word_wrap = True

    scenarios = [
        ("1. Supplier Capacity Loss", "Parameterized capacity cut (10% to 90%) and shock duration (1 to 60 days) to simulate plant fires, boiler failures, or strikes."),
        ("2. Route Transit Delay", "Corridor blockage or severe speed reduction (1.5x to 4.0x transit days) modeling highway washouts or rail freight congestion."),
        ("3. Extreme Demand Surge", "Regional demand spikes (+20% to +100%) across targeted metropolitan consumer zones."),
        ("4. Warehouse Shutdown", "Complete temporary facility closure due to regional quarantine or localized power grid failure."),
        ("5. Multi-Node System Shock", "Simultaneous compound disruption affecting multiple suppliers and freight corridors concurrently."),
        ("Copy-on-Write In-Memory State", "SimulationState deepcopy clones all 83 nodes and 160 routes in RAM. Planners test catastrophic shocks with zero risk of database corruption.")
    ]
    add_formatted_bullets(tf_scen, scenarios, font_size=8.5, space_after=5)

    add_footer(slide, 12)
    add_speaker_notes(slide, """
Before committing expensive operational changes, supply chain managers must be able to ask 'what-if' questions. NEXUS features a dedicated Scenario Simulation engine supporting five parameterized stress scenarios: supplier failure, route blockage, demand surges, warehouse shutdowns, and compound multi-hazard shocks. 

Crucially, the simulation operates non-destructively. Using copy-on-write state cloning, the engine creates an ephemeral in-memory clone of the digital twin. This means an operator can simulate a catastrophic 90% capacity loss across multiple nodes, inspect the resulting network balance and shortage projections, and trigger optimization without corrupting the production database.
""")

def build_slide_13(prs):
    """Slide 13: Optimization Engine"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 13, "OPERATIONS RESEARCH", 
               "Optimization Engine — Google OR-Tools Linear Solver", 
               "Formulating multi-echelon supply chain allocation as a mathematically rigorous linear program solved in milliseconds.")

    # Left: Mathematical LP Formulation
    add_card(slide, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), title="MATHEMATICAL LP FORMULATION (GLOP)", fill_color=PANEL_BG, border_color=EMERALD)
    tb_lp = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_lp = tb_lp.text_frame
    tf_lp.word_wrap = True

    lp_points = [
        ("Objective Function", "Minimize Total Cost Z = Procurement + Freight + Holding + Shortage Penalties + Risk Penalties."),
        ("Procurement Cost", "Sum of units procured multiplied by vendor unit price: Σ (C_proc × X_sw)."),
        ("Freight Transportation", "Sum of freight shipped multiplied by route transit cost: Σ (C_freight × X_route)."),
        ("Shortage SLA Penalties", "Strict industrial contract penalty of INR 350 per unmet demand unit: Σ (INR 350 × S_z)."),
        ("Constraint 1 (Supplier Capacity)", "Total outflow from supplier s cannot exceed remaining simulated capacity: Σ_w X_sw ≤ Cap_s."),
        ("Constraint 2 (Flow Conservation)", "Warehouse inflow + existing inventory = outflow to demand zones + final stock."),
        ("Constraint 3 (Demand Satisfaction)", "Zone fulfillment + shortage = total zone demand: Σ_w Y_wz + S_z = D_z."),
        ("Constraint 4 (Non-Negativity)", "All decision variables X_sw, Y_wz, S_z ≥ 0.")
    ]
    add_formatted_bullets(tf_lp, lp_points, font_size=8.5, space_after=3.5)

    # Right: Optimization UI Screenshot & Performance
    img_opt = ASSETS_DIR / "07_optimization_engine.png"
    if img_opt.exists():
        slide.shapes.add_picture(str(img_opt), Inches(6.8), Inches(1.8), Inches(5.733), Inches(3.1))

    # Solver metrics card below image
    add_card(slide, Inches(6.8), Inches(5.05), Inches(5.733), Inches(1.65), title="SOLVER PERFORMANCE & GUARANTEES", fill_color=DARK_ACCENT, border_color=TEAL)
    tb_perf = slide.shapes.add_textbox(Inches(7.0), Inches(5.4), Inches(5.333), Inches(1.2))
    tf_perf = tb_perf.text_frame
    tf_perf.word_wrap = True
    perf_bullets = [
        ("Solver Algorithm", "Google OR-Tools GLOP (Simplex-based Linear Programming)."),
        ("Global Optimality", "Mathematical guarantee of global cost minimum across all feasible network flows."),
        ("Execution Speed", "Solves the complete 83-node, 160-corridor network in under 10 milliseconds (0.0094s).")
    ]
    add_formatted_bullets(tf_perf, perf_bullets, font_size=8.5, space_after=2.5)

    add_footer(slide, 13)
    add_speaker_notes(slide, """
Once a disruption is simulated, how do we find the best response? NEXUS formulates the problem as a global multi-echelon linear program solved using Google OR-Tools GLOP solver. 

The objective function minimizes total operational cost: procurement costs, multimodal transportation costs, holding costs, risk penalties, and contractual shortage penalties, which are set at 350 rupees per unit. The solver enforces strict physical constraints: supplier capacity boundaries, warehouse conservation of flow, and demand fulfillment. Rather than relying on trial-and-error or greedy heuristics, Google OR-Tools evaluates all feasible sourcing and routing permutations simultaneously, returning the mathematically optimal allocation in less than 10 milliseconds.
""")

def build_slide_14(prs):
    """Slide 14: Flagship Successful Model Run"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 14, "VERIFIED DEMONSTRATION", 
               "Flagship Demonstration — 80% Disruption of Supplier SUP_001", 
               "An end-to-end, reproducible validation of the complete NEXUS pipeline under severe operational stress.")

    # Left: Disruption Parameters & Cascade
    add_card(slide, Inches(0.8), Inches(1.8), Inches(5.7), Inches(4.9), title="THE DISRUPTION INJECTION & DILEMMA", fill_color=PANEL_BG, border_color=CRIMSON)
    tb_dis = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_dis = tb_dis.text_frame
    tf_dis.word_wrap = True

    dis_bullets = [
        ("Target Vendor", "SUP_001 (Tata AutoComp Components, Pune Chakan Industrial Hub)."),
        ("Primary Product", "PROD_ITEM_003 (Tier-1 critical automotive subassembly)."),
        ("Normal Capacity", "12,000 units per operational period."),
        ("Injected Shock", "80% Capacity Loss (12,000 → 2,400 units/period) for a 10-day duration."),
        ("Simulated Trigger", "Unscheduled boiler explosion and localized plant strike."),
        ("Downstream Crisis", "Western Warehouse (WH_01) stock of 1,420 units vs 280 units/day burn rate causes complete stockout on Day 6."),
        ("Unmitigated Shortage", "69,843.2 units of unmet demand across Mumbai, Pune, Delhi NCR, Jaipur, and Ahmedabad."),
        ("Unmitigated Penalties", "INR 350 × 69,843.2 = INR 24,445,120.00 in contractual stockout penalties.")
    ]
    add_formatted_bullets(tf_dis, dis_bullets, font_size=8.5, space_after=4)

    # Right: Impact Screen & The Strategic Insight
    img_imp_screen = ASSETS_DIR / "05_impact_analysis.png"
    if img_imp_screen.exists():
        slide.shapes.add_picture(str(img_imp_screen), Inches(6.8), Inches(1.8), Inches(5.733), Inches(3.0))

    add_card(slide, Inches(6.8), Inches(4.95), Inches(5.733), Inches(1.75), title="THE SYSTEM CAPACITY REALITY", fill_color=DARK_ACCENT, border_color=CYAN)
    tb_real = slide.shapes.add_textbox(Inches(7.0), Inches(5.35), Inches(5.333), Inches(1.25))
    tf_real = tb_real.text_frame
    tf_real.word_wrap = True
    real_bullets = [
        ("Total Network Demand", "153,600.0 units across all 30 demand zones."),
        ("Remaining Network Capacity", "314,350.2 units available across secondary suppliers post-shock."),
        ("Net Capacity Surplus", "+160,750.2 units available across the broader network."),
        ("Core Takeaway", "The physical network retains sufficient capacity to absorb the shock, but rigid static allocations create localized failure.")
    ]
    add_formatted_bullets(tf_real, real_bullets, font_size=8.5, space_after=2)

    add_footer(slide, 14)
    add_speaker_notes(slide, """
To validate the platform, we executed our verified flagship demonstration scenario. We inject an 80% capacity reduction into supplier SUP_001, Tata AutoComp Components in Pune, for a 10-day duration. This reduces their periodic throughput from 12,000 units down to 2,400. 

In unoptimized operations, this causes Western Warehouse WH_01 to run out of stock on Day 6, creating an aggregate shortage of 69,843 units across five major cities and incurring 24.45 million rupees in stockout penalties. However, our simulation reveals a crucial insight: the network as a whole actually has 314,000 units of available capacity across other suppliers. The failure occurs solely because traditional contracts are statically bound. This provides the exact opportunity for NEXUS optimization.
""")

def build_slide_15(prs):
    """Slide 15: Baseline vs NEXUS Results"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 15, "EXPERIMENTAL RESULTS", 
               "Baseline vs Optimized Decision — Verified Outcome", 
               "Google OR-Tools multi-echelon reallocation achieves a 53.19% operational cost reduction and restores 100% service level.")

    # Left: High-res comparison chart
    img_comp = ASSETS_DIR / "slide_optimization_comparison.png"
    if img_comp.exists():
        slide.shapes.add_picture(str(img_comp), Inches(0.8), Inches(1.8), Inches(6.2), Inches(4.9))

    # Right: Verified Benchmark Table
    add_card(slide, Inches(7.2), Inches(1.8), Inches(5.333), Inches(4.9), title="VERIFIED NUMERICAL BENCHMARK", fill_color=PANEL_BG, border_color=EMERALD)
    
    headers_res = ["Operational Metric", "Baseline Heuristic", "NEXUS (OR-Tools)"]
    rows_res = [
        ["Total Operational Cost", "INR 41,215,184.70", "INR 19,291,240.54"],
        ["Cost Reduction %", "0.0% (Baseline)", "-53.19% (Saved ₹21.92M)"],
        ["Procurement Cost", "INR 12,410,250.00", "INR 15,820,140.54"],
        ["Freight Transit Cost", "INR 1,845,220.00", "INR 3,471,100.00"],
        ["Shortage Penalty Cost", "INR 24,445,120.00", "INR 0.00 (-100%)"],
        ["Holding Cost", "INR 2,514,594.70", "INR 0.00 (Cross-dock)"],
        ["Unmet Shortages", "69,843.2 units", "0.0 units (Fulfilled)"],
        ["Network Service Level", "54.57%", "100.00% (+45.43 pp)"],
        ["Solver Runtime", "N/A (Rule-based)", "0.0094 seconds"]
    ]
    create_table(slide, Inches(7.35), Inches(2.2), Inches(5.033), Inches(3.6), headers_res, rows_res,
                 col_widths=[Inches(1.833), Inches(1.6), Inches(1.6)])

    # Bottom academic disclaimer inside card
    tb_note = slide.shapes.add_textbox(Inches(7.35), Inches(5.9), Inches(5.033), Inches(0.7))
    tf_note = tb_note.text_frame
    tf_note.word_wrap = True
    p = tf_note.paragraphs[0]
    p.text = "ACADEMIC DISCLAIMER: SIMULATED SCENARIO OUTCOME"
    p.font.name = "Segoe UI"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p2 = tf_note.add_paragraph()
    p2.text = "These results represent mathematical model performance under this specific stress scenario and are not a universal guarantee for all possible disruption topologies."
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(7.5)
    p2.font.color.rgb = SLATE

    add_footer(slide, 15)
    add_speaker_notes(slide, """
This is one of the most important slides in the presentation: the quantitative comparison between the unoptimized baseline and NEXUS optimization. 

Under the baseline heuristic, the company incurs over 41.2 million rupees in total costs, of which 24.45 million are pure stockout penalties, resulting in a disastrous service level of only 54.57%. NEXUS completely transforms this outcome. The linear program proactively increases procurement spending by 3.4 million and freight spending by 1.6 million to reroute goods from secondary qualified suppliers in Jamshedpur and Pantnagar. 

By spending 5.04 million in proactive logistics, NEXUS eliminates all 24.45 million rupees of stockout penalties. The net result is a 53.19% total operational cost reduction—saving nearly 22 million rupees—while restoring service level from 54.57% to a perfect 100%.
""")

def build_slide_16(prs):
    """Slide 16: Recommendation Engine"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 16, "RECOMMENDATION & ACTION", 
               "Recommendation Engine — From Optimization to Action", 
               "Converting mathematical LP allocations into plain-language executive directives and simulated ERP dispatch.")

    # Left: Recommendation Center Screenshot
    img_rec = ASSETS_DIR / "08_recommendation_center.png"
    if img_rec.exists():
        slide.shapes.add_picture(str(img_rec), Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.9))

    # Right: Real Synthesized Directives
    add_card(slide, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.9), title="SYNTHESIZED MITIGATION DIRECTIVES", fill_color=PANEL_BG, border_color=CYAN)
    tb_rec = slide.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_rec = tb_rec.text_frame
    tf_rec.word_wrap = True

    rec_items = [
        ("Directives ID", "REC_AUTO_MITIGATION_SUP001 (Action: REALLOCATE_AND_REROUTE)."),
        ("Executive Rationale", "'Tata AutoComp Components (SUP_001) faces severe capacity degradation. Without intervention, baseline operations cause 69,843 units of shortage. NEXUS has formulated an optimal reallocation plan.'"),
        ("Action Directive 1", "Shift 18.5% (25,000 units) of raw material procurement to SUP_005 (Tata Steel, Jamshedpur)."),
        ("Action Directive 2", "Shift 12.0% (16,200 units) of component buffering to SUP_009 (Kumaon Polymer, Pantnagar)."),
        ("Action Directive 3", "Rebalance safety stock at WH_01 by dispatching 1,800 units from WH_04 via North-South Rail Freight Corridor."),
        ("Plan Robustness Index", "0.98 / 1.00 (derived from LP solver status = OPTIMAL and 100% shortage mitigation)."),
        ("Simulated ERP/WMS Dispatch", "Dispatched to mock WMS/ERP queue for operator demonstration (strictly labeled as simulation).")
    ]
    add_formatted_bullets(tf_rec, rec_items, font_size=8.5, space_after=4.5)

    add_footer(slide, 16)
    add_speaker_notes(slide, """
Mathematical output from an optimization solver consists of hundreds of continuous flow decision variables, which an executive cannot easily interpret. The NEXUS Recommendation Engine converts these mathematical tensors into plain-language business directives. 

For our scenario, it generates three specific action items: shifting 25,000 units to SUP_005 in Jamshedpur, shifting 16,200 units to SUP_009 in Pantnagar, and rebalancing safety stock between Western and Northern warehouses. Furthermore, following our Phase 2 audit, we replaced arbitrary 'confidence scores' with a mathematically derived Plan Robustness Index of 0.98 based on solver optimality and shortage mitigation. Finally, the 'Simulate ERP Dispatch' button clearly demonstrates how these directives would be handed off to enterprise ERP systems like SAP or Oracle in production.
""")

def build_slide_17(prs):
    """Slide 17: Frontend Control Room"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 17, "USER INTERFACE & CONTROL ROOM", 
               "NEXUS Frontend — Enterprise Decision Control Room", 
               "A production-grade, dark-themed control room built with React 19, TypeScript, and Tailwind CSS.")

    # High-Res 8-Screen Composite Grid in center
    img_grid = ASSETS_DIR / "slide_frontend_8screens_grid.png"
    if img_grid.exists():
        slide.shapes.add_picture(str(img_grid), Inches(0.8), Inches(1.8), Inches(11.733), Inches(3.9))

    # Bottom Tech Stack & Performance Cards
    add_card(slide, Inches(0.8), Inches(5.85), Inches(5.7), Inches(1.05), title="FRONTEND ARCHITECTURE", fill_color=DARK_ACCENT, border_color=TEAL)
    tb_fe = slide.shapes.add_textbox(Inches(1.0), Inches(6.15), Inches(5.3), Inches(0.7))
    tf_fe = tb_fe.text_frame
    p_fe = tf_fe.paragraphs[0]
    p_fe.text = "React 19  •  TypeScript 5.8  •  Vite 8.3  •  Tailwind CSS  •  Leaflet GIS  •  Recharts  •  Lucide Icons"
    p_fe.font.name = "Segoe UI"
    p_fe.font.size = Pt(9.5)
    p_fe.font.color.rgb = WHITE

    add_card(slide, Inches(6.8), Inches(5.85), Inches(5.733), Inches(1.05), title="BUILD PERFORMANCE & FOOTPRINT", fill_color=DARK_ACCENT, border_color=EMERALD)
    tb_bp = slide.shapes.add_textbox(Inches(7.0), Inches(6.15), Inches(5.333), Inches(0.7))
    tf_bp = tb_bp.text_frame
    p_bp = tf_bp.paragraphs[0]
    p_bp.text = "Code-split bundles (React.lazy)  |  Initial bundle: ~365 kB (117 kB gzip)  |  Build time: 2.19s  |  0 errors"
    p_bp.font.name = "Segoe UI"
    p_bp.font.size = Pt(9.5)
    p_bp.font.color.rgb = WHITE

    add_footer(slide, 17)
    add_speaker_notes(slide, """
To make these analytical tools usable by human decision-makers, we built a production-grade web control room. The frontend is implemented in React 19 with TypeScript, Tailwind CSS, Leaflet for GIS mapping, and Recharts for analytical visualizations. 

It features eight comprehensive screens organized around the decision lifecycle: Executive Overview, Digital Twin GIS Map, Demand Intelligence, Risk Intelligence, Impact Analysis, Scenario Simulation, Optimization Engine, and the Recommendation Center. During our Phase 2 development, we code-split all eight routes using React.lazy, reducing the initial bundle footprint down to 365 kilobytes and achieving an instantaneous sub-2.5 second build.
""")

def build_slide_18(prs):
    """Slide 18: Frontend Screen-by-Screen Flow"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 18, "USER JOURNEY", 
               "One Continuous User Journey Through NEXUS", 
               "An intuitive eight-stage progression from initial crisis visibility to mathematically verified mitigation.")

    # 8 Journey Cards in 2 rows of 4
    journey_steps = [
        ("1. Dashboard", "What is happening?", "Alert flags an operational risk event on Tier-1 vendor SUP_001.", CYAN),
        ("2. Digital Twin", "Where is it located?", "Operator inspects geospatial map and zooms into the Pune industrial cluster.", TEAL),
        ("3. Demand", "What will happen?", "Forecasting models project 153k units of demand with 4-week forecast bands.", RGBColor(129, 140, 248)),
        ("4. Supplier Risk", "Who is failing & why?", "XGBoost surfaces 85% disruption probability driven by lead-time volatility.", AMBER),
        ("5. Impact Analysis", "What will it affect?", "Graph engine exposes WH_01 stockout in 5.07 days and 69.8k units at risk.", CRIMSON),
        ("6. Simulation", "What if it lasts 10 days?", "Operator runs what-if stress simulation; confirms net capacity surplus in system.", AMBER),
        ("7. Optimization", "What should change?", "OR-Tools linear program solves global multi-echelon allocation in 0.0094s.", EMERALD),
        ("8. Recommendation", "What should we do?", "Reviews plain-language directives and simulates dispatch to enterprise ERP.", CYAN)
    ]

    card_w = Inches(2.75)
    card_h = Inches(2.3)
    gap_x = Inches(0.24)
    gap_y = Inches(0.2)
    start_x = Inches(0.8)

    for idx, (title, question, desc, border_c) in enumerate(journey_steps):
        row = idx // 4
        col = idx % 4
        x = start_x + col * (card_w + gap_x)
        y = Inches(1.8) + row * (card_h + gap_y)

        add_card(slide, x, y, card_w, card_h, fill_color=PANEL_BG, border_color=border_c)
        
        tb = slide.shapes.add_textbox(x + Inches(0.12), y + Inches(0.15), card_w - Inches(0.24), card_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = border_c

        p2 = tf.add_paragraph()
        p2.text = f'"{question}"'
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(9.5)
        p2.font.bold = True
        p2.font.color.rgb = WHITE
        p2.space_before = Pt(2)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(8.5)
        p3.font.color.rgb = SLATE
        p3.space_before = Pt(4)

    add_footer(slide, 18)
    add_speaker_notes(slide, """
This slide demonstrates the operator's journey through NEXUS during an operational crisis. It follows an intuitive narrative:

The operator starts on the Dashboard to see what is happening.
They move to the Map to see where the affected facility is located.
They check Demand Intelligence to understand future consumption needs.
They check Risk Intelligence to identify which vendor is failing and why.
They open Impact Analysis to see which warehouses will run out of stock and when.
They use Scenario Simulation to test the disruption's severity and duration.
They trigger the Optimization Engine to compute the lowest-cost alternative allocation.
And finally, they open the Recommendation Center to approve the plain-language directives and simulate dispatching them to the ERP system.

This creates an effortless, unified workflow for any supply chain professional.
""")

def build_slide_19(prs):
    """Slide 19: API & System Integration"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 19, "SYSTEM INTEGRATION", 
               "Frontend ↔ Backend Integration — 20 RESTful APIs", 
               "A high-performance API service layer connecting UI views with asynchronous analytical pipelines.")

    # Left: Swagger Screenshot
    img_swagger = ASSETS_DIR / "09_swagger_api_docs.png"
    if img_swagger.exists():
        slide.shapes.add_picture(str(img_swagger), Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.9))

    # Right: Verified 20 Endpoints Breakdown
    add_card(slide, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.9), title="VERIFIED 20 RESTFUL ENDPOINTS", fill_color=PANEL_BG, border_color=CYAN)
    tb_api = slide.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_api = tb_api.text_frame
    tf_api.word_wrap = True

    endpoints = [
        ("GET /health", "System status, loaded ML model verifications, database health check."),
        ("GET /api/v1/suppliers", "Master data for 20 Tier-1/Tier-2 vendor profiles and metrics."),
        ("GET /api/v1/warehouses", "10 central warehouse facilities with capacities and operating costs."),
        ("GET /api/v1/routes", "160 multimodal transit lanes with distances and transit times."),
        ("GET /api/v1/analytics/summary", "Executive KPIs: inventory valuation, mean on-time rates, routes."),
        ("GET /api/v1/analytics/gis/facilities", "GeoJSON FeatureCollection of 83 coordinates across India."),
        ("POST /api/v1/forecast", "4-week multi-step demand predictions with XGBoost error bounds."),
        ("POST /api/v1/risk/predict", "Disruption probability, risk tier, and feature driver importance."),
        ("POST /api/v1/anomaly/detect", "Isolation Forest transaction scan for volume spikes & late transit."),
        ("POST /api/v1/impact/analyze", "Graph BFS traversal, runway days, and affected demand zones."),
        ("POST /api/v1/scenario/simulate", "In-memory state cloning across 5 disruption shock scenarios."),
        ("POST /api/v1/optimize", "Google OR-Tools multi-echelon LP solve vs baseline heuristic comparison."),
        ("GET /api/v1/recommendations", "Synthesized plain-language executive directives with LP robustness.")
    ]
    add_formatted_bullets(tf_api, endpoints, font_size=8, space_after=2.5)

    add_footer(slide, 19)
    add_speaker_notes(slide, """
The connection between our React frontend and backend is facilitated by 20 fully documented RESTful API endpoints managed by FastAPI. Every request and response payload is strictly validated using Pydantic v2 schemas. 

As shown in the Swagger documentation screenshot, our endpoints handle everything from geospatial facility coordinates and demand forecasts to scenario simulations and Google OR-Tools optimization runs. In our integration audit, all 20 API service functions were verified against the live backend, returning 100% HTTP 200 OK responses with zero type mismatches.
""")

def build_slide_20(prs):
    """Slide 20: Testing & Validation"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 20, "QUALITY ASSURANCE", 
               "Testing, Reliability & Verification Suite", 
               "Comprehensive unit, integration, and build verification ensuring rock-solid system stability.")

    # 4 Verification Cards in 2x2 grid
    test_cards = [
        ("BACKEND TEST SUITE (PYTEST)", "29 / 29 PASSED (100%)", EMERALD, [
            ("Execution Time", "2.66 seconds automated execution."),
            ("Data Pipeline", "Ingestion schemas, entity count thresholds, type checks."),
            ("ML Models", "Forecasting lags, chronological splits, risk classification."),
            ("Graph & Impact", "NetworkX BFS traversal, dependency paths, runway math."),
            ("Optimization", "OR-Tools linear constraints, conservation of flow, baseline diff."),
            ("API Endpoints", "FastAPI schema validation and HTTP 200 response codes.")
        ]),
        ("FRONTEND TEST SUITE (VITEST)", "10 / 10 PASSED (100%)", EMERALD, [
            ("Execution Time", "33.85 seconds test suite run."),
            ("Formatters", "Indian Rupee (Lakh/Crore) formatting, percentage strings."),
            ("UI Components", "KpiCard, RiskBadge, StatusBadge, WorkflowBreadcrumb."),
            ("Feedback States", "Empty states, error alerts, loading skeleton screens.")
        ]),
        ("PRODUCTION BUILD QUALITY", "0 COMPILATION ERRORS", CYAN, [
            ("TypeScript Compiler", "tsc -b passed with zero type errors."),
            ("Vite Bundler", "Vite 8.3 production build succeeded in 9.5 seconds."),
            ("Code Splitting", "React.lazy dynamic chunking across all 8 routes."),
            ("Initial Chunk", "365 kB lightweight bundle (117 kB gzip).")
        ]),
        ("DATA CREDIBILITY GUARANTEE", "ZERO MOCK FALLBACKS", AMBER, [
            ("No Silent Mocks", "Frontend is hardwired directly to FastAPI backend."),
            ("Traceable KPIs", "Every metric displayed traces to authenticated SQL or ML output."),
            ("Reproducibility", "Fixed random seeds (seed=42) ensure exact experimental recreation.")
        ])
    ]

    card_w = Inches(5.6)
    card_h = Inches(2.35)
    positions = [
        (Inches(0.8), Inches(1.8)),
        (Inches(6.8), Inches(1.8)),
        (Inches(0.8), Inches(4.45)),
        (Inches(6.8), Inches(4.45))
    ]

    for idx, (title, badge, border_c, bullets) in enumerate(test_cards):
        x, y = positions[idx]
        add_card(slide, x, y, card_w, card_h, title=title, fill_color=PANEL_BG, border_color=border_c)
        
        # Badge
        tb_badge = slide.shapes.add_textbox(x + Inches(0.18), y + Inches(0.38), card_w - Inches(0.36), Inches(0.28))
        tf_b = tb_badge.text_frame
        p_b = tf_b.paragraphs[0]
        p_b.text = f"Status: {badge}"
        p_b.font.name = "Segoe UI"
        p_b.font.size = Pt(9.5)
        p_b.font.bold = True
        p_b.font.color.rgb = border_c

        tb = slide.shapes.add_textbox(x + Inches(0.18), y + Inches(0.68), card_w - Inches(0.36), card_h - Inches(0.78))
        tf = tb.text_frame
        tf.word_wrap = True
        add_formatted_bullets(tf, bullets, font_size=8.5, space_after=3)

    add_footer(slide, 20)
    add_speaker_notes(slide, """
Engineering credibility requires exhaustive verification. NEXUS has undergone complete automated testing across both backend and frontend. 

On the backend, all 29 pytest test cases pass with 100% success in 2.66 seconds, verifying our data pipeline, ML regressors, classifiers, graph traversal, and optimization formulations. On the frontend, all 10 Vitest unit tests pass, and the production build compiles with zero TypeScript errors and zero bundler warnings. Most importantly, we instituted a strict credibility guarantee: there are zero silent mock fallbacks in the production frontend code. Every number, chart, and recommendation displayed in the control room is generated live by the backend engine.
""")

def build_slide_21(prs):
    """Slide 21: Limitations & Academic Integrity"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 21, "ACADEMIC INTEGRITY", 
               "What NEXUS Does — and Does Not — Claim", 
               "Maintaining scientific honesty by clearly differentiating verified implementations from future enterprise requirements.")

    # Two Columns: Currently Implemented vs Not Claimed as Live
    add_card(slide, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.9), title="CURRENTLY IMPLEMENTED & VERIFIED", fill_color=PANEL_BG, border_color=EMERALD)
    tb_imp = slide.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.3))
    tf_imp = tb_imp.text_frame
    tf_imp.word_wrap = True

    implemented = [
        ("Empirical Public Datasets", "Grounded in Walmart 421k weekly sales records and DataCo 35k shipment logs."),
        ("Calibrated Digital Twin", "83 facilities and 160 corridors modeled on Indian national logistics geography."),
        ("Supervised ML Models", "Out-of-sample evaluated XGBoost Regressor (demand) and XGBoost Classifier (vendor risk)."),
        ("Unsupervised Anomaly Detection", "Isolation Forest continuously flagging order volume surges and transit outliers."),
        ("Graph-Based Impact Propagation", "NetworkX directed graph BFS traversal and stock runway calculus."),
        ("In-Memory Scenario Simulation", "Copy-on-write state cloning supporting 5 distinct parameterized disruption modes."),
        ("Operations Research", "Google OR-Tools multi-echelon linear program (GLOP) minimizing cost and SLA penalties."),
        ("Executive Control Room", "8 production React 19 screens with Leaflet GIS mapping and Recharts telemetry.")
    ]
    add_formatted_bullets(tf_imp, implemented, font_size=8.5, space_after=4.5)

    add_card(slide, Inches(6.8), Inches(1.8), Inches(5.733), Inches(4.9), title="NOT CLAIMED AS LIVE (ACADEMIC BOUNDARIES)", fill_color=PANEL_BG, border_color=AMBER)
    tb_bound = slide.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.333), Inches(4.3))
    tf_bound = tb_bound.text_frame
    tf_bound.word_wrap = True

    boundaries = [
        ("No Live ERP/WMS Integration", "Strategy dispatch simulates enterprise handoff; no live connection to SAP S/4HANA or Oracle."),
        ("No Live GPS / IoT Feeds", "Transit variability is derived from empirical DataCo distributions rather than physical telematics sensors."),
        ("Synthetic Enterprise Topology", "Facility operations represent calibrated digital twin models, not proprietary corporate records."),
        ("Continuous LP Relaxation", "OR-Tools solver uses linear programming (continuous flow) rather than integer pallet constraints (MILP/VRP)."),
        ("Database Architecture", "Default SQLite database is optimized for standalone evaluation and viva demonstration (PostgreSQL DDL ready).")
    ]
    add_formatted_bullets(tf_bound, boundaries, font_size=8.5, space_after=6)

    add_footer(slide, 21)
    add_speaker_notes(slide, """
As a final-year engineering project, maintaining academic integrity is paramount. This slide clearly outlines what NEXUS does—and does not—claim. 

What is implemented and fully verified is an end-to-end decision intelligence prototype combining empirical datasets, machine learning, graph analysis, in-memory scenario simulation, Google OR-Tools linear programming, and an interactive React control room. However, we do not make false claims of enterprise deployment. We do not claim a live connection to SAP or Oracle; strategy dispatch is simulated. We do not claim live GPS satellite feeds; lead-time variance is derived from empirical DataCo distributions. And our digital twin facilities represent calibrated mathematical models rather than proprietary internal records. Transparently acknowledging these boundaries demonstrates rigorous engineering maturity.
""")

def build_slide_22(prs):
    """Slide 22: Future Scope"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 22, "PROJECT ROADMAP", 
               "From Prototype to Enterprise Decision Platform", 
               "A structured engineering roadmap for advancing NEXUS into an industrial-scale deployment.")

    # 6 Phase Roadmap Cards in 2 columns of 3
    phases = [
        ("Phase 1: Academic Prototype [COMPLETE]", "Integrated ML, graph cascade, in-memory simulation, Google OR-Tools LP, and React control room.", EMERALD),
        ("Phase 2: Live ERP/WMS Connectors", "Standardized REST, RFC, and OData connectors for SAP S/4HANA, Oracle NetSuite, and Microsoft Dynamics.", CYAN),
        ("Phase 3: IoT & Telematics Streaming", "Apache Kafka and MQTT pipelines ingesting real-time GPS container tracking and cold-chain temperature telemetry.", TEAL),
        ("Phase 4: Mixed-Integer & Stochastic Optimization", "Transitioning from continuous LP to Mixed-Integer Linear Programming (MILP) with discrete pallet packing and vehicle routing.", RGBColor(129, 140, 248)),
        ("Phase 5: Autonomous Multi-Agent Negotiation", "Autonomous LLM agents negotiating spot freight rates and emergency vendor capacity allocations in real time.", AMBER),
        ("Phase 6: Cloud-Native Enterprise Deployment", "Containerized Kubernetes microservices backed by distributed PostgreSQL and Redis caching.", CYAN)
    ]

    card_w = Inches(5.6)
    card_h = Inches(1.5)
    start_x1 = Inches(0.8)
    start_x2 = Inches(6.8)
    start_y = Inches(1.8)
    gap_y = Inches(0.2)

    for idx, (title, desc, border_c) in enumerate(phases):
        col = idx // 3
        row = idx % 3
        x = start_x1 if col == 0 else start_x2
        y = start_y + row * (card_h + gap_y)

        add_card(slide, x, y, card_w, card_h, title=title, fill_color=PANEL_BG, border_color=border_c)
        tb = slide.shapes.add_textbox(x + Inches(0.18), y + Inches(0.48), card_w - Inches(0.36), card_h - Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = desc
        p.font.name = "Segoe UI"
        p.font.size = Pt(8.5)
        p.font.color.rgb = SLATE

    add_footer(slide, 22)
    add_speaker_notes(slide, """
Looking forward, NEXUS has a clear roadmap toward industrial deployment. Phase 1 is complete with our fully functioning prototype. 

In Phase 2, we plan to implement authentic enterprise connectors using SAP RFC and Oracle OData APIs. Phase 3 will introduce Apache Kafka event streaming to ingest real-time GPS telematics and IoT cold-chain sensor data. In Phase 4, we will enhance our optimization engine from continuous linear programming to Mixed-Integer Linear Programming (MILP) and Vehicle Routing Problem (VRP) formulations to handle discrete pallet packing and truckload limits. Phase 5 explores autonomous multi-agent AI for spot-contract negotiations, and Phase 6 will package the entire architecture into Kubernetes microservices for multi-tenant enterprise deployment.
""")

def build_slide_23(prs):
    """Slide 23: Final Takeaway"""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(slide)
    add_header(slide, 23, "CONCLUSION & DEFENSE", 
               "NEXUS in One Picture — The Complete Journey", 
               "Transforming fragmented supply chain data into mathematically verified, actionable decisions.")

    # High-level journey banner
    add_card(slide, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.8), fill_color=DARK_ACCENT, border_color=CYAN)
    tb_banner = slide.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(11.333), Inches(0.5))
    tf_b = tb_banner.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "DATA   →   UNDERSTAND   →   PREDICT   →   TRACE   →   SIMULATE   →   OPTIMIZE   →   DECIDE"
    p_b.font.name = "Segoe UI"
    p_b.font.size = Pt(13)
    p_b.font.bold = True
    p_b.font.color.rgb = CYAN

    # Core Summary Box
    add_card(slide, Inches(0.8), Inches(2.8), Inches(11.733), Inches(1.4), title="PLATFORM SUMMARY STATEMENT", fill_color=PANEL_BG, border_color=TEAL)
    tb_sum = slide.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(11.333), Inches(0.9))
    tf_sum = tb_sum.text_frame
    tf_sum.word_wrap = True
    p_s = tf_sum.paragraphs[0]
    p_s.text = '"NEXUS is a closed-loop supply-chain decision-intelligence platform that combines empirical data, a simulated digital twin, machine learning, graph-based impact analysis, what-if simulation, mathematical optimization, and actionable recommendations in a single interactive control room."'
    p_s.font.name = "Segoe UI"
    p_s.font.size = Pt(11)
    p_s.font.bold = True
    p_s.font.color.rgb = WHITE

    # 4 Bottom Verification Highlights
    highlights = [
        ("421k Empirical Sales", "Walmart & DataCo empirical grounding"),
        ("29.5% RMSE Reduction", "XGBoost Regressor demand forecasting"),
        ("53.19% Cost Reduction", "INR 21.92M saved via Google OR-Tools"),
        ("100% Test Pass Rate", "29/29 Backend, 10/10 Frontend tests")
    ]
    card_w = Inches(2.75)
    gap = Inches(0.24)
    for idx, (title, sub) in enumerate(highlights):
        x = Inches(0.8) + idx * (card_w + gap)
        add_card(slide, x, Inches(4.4), card_w, Inches(1.2), fill_color=DARK_ACCENT, border_color=EMERALD)
        tb_h = slide.shapes.add_textbox(x + Inches(0.1), Inches(4.55), card_w - Inches(0.2), Inches(0.9))
        tf_h = tb_h.text_frame
        p1 = tf_h.paragraphs[0]
        p1.text = title
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = EMERALD
        p2 = tf_h.add_paragraph()
        p2.text = sub
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = SLATE
        p2.space_before = Pt(2)

    # Closing Presenter & Thank You Card
    add_card(slide, Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.1), fill_color=PANEL_BG, border_color=CYAN)
    tb_close = slide.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.333), Inches(0.8))
    tf_close = tb_close.text_frame
    p_c1 = tf_close.paragraphs[0]
    p_c1.text = "Thank You!   |   Questions & Discussion"
    p_c1.font.name = "Segoe UI"
    p_c1.font.size = Pt(14)
    p_c1.font.bold = True
    p_c1.font.color.rgb = CYAN

    p_c2 = tf_close.add_paragraph()
    p_c2.text = "Presented by: Shreyansh Uttam  |  B.Tech CSE (Artificial Intelligence & Machine Learning)  |  VIT Bhopal University"
    p_c2.font.name = "Segoe UI"
    p_c2.font.size = Pt(10)
    p_c2.font.color.rgb = WHITE
    p_c2.space_before = Pt(2)

    add_footer(slide, 23)
    add_speaker_notes(slide, """
To conclude, NEXUS transforms supply chain management from reactive firefighting into proactive decision intelligence. 

By combining empirical data, digital twin graph modeling, machine learning, scenario simulation, and Google OR-Tools optimization, the platform doesn't just predict problems—it solves them. In our verified demonstration, NEXUS eliminated 24.45 million rupees in stockout penalties, maintained 100% service level, and reduced total operational costs by 53.19% in under 10 milliseconds. 

Thank you very much for your time and guidance. I would be delighted to take any questions and demonstrate the live platform.
""")

# =============================================================
# MAIN ORCHESTRATOR
# =============================================================

def generate_presentation():
    print("=" * 70)
    print(" GENERATING NEXUS COMPLETE FACULTY-REVIEW PRESENTATION ")
    print("=" * 70)

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    builders = [
        build_slide_01, build_slide_02, build_slide_03, build_slide_04,
        build_slide_05, build_slide_06, build_slide_07, build_slide_08,
        build_slide_09, build_slide_10, build_slide_11, build_slide_12,
        build_slide_13, build_slide_14, build_slide_15, build_slide_16,
        build_slide_17, build_slide_18, build_slide_19, build_slide_20,
        build_slide_21, build_slide_22, build_slide_23
    ]

    for idx, builder in enumerate(builders, 1):
        print(f"Building Slide {idx:02d} / 23: {builder.__doc__}...")
        builder(prs)

    prs.save(str(PPTX_OUTPUT))
    print(f"\nSuccessfully generated PowerPoint presentation:")
    print(f"-> {PPTX_OUTPUT} ({os.path.getsize(PPTX_OUTPUT):,} bytes)")

    # Try PowerPoint COM PDF export
    export_to_pdf()

def export_to_pdf():
    print("\nAttempting native PDF export via PowerPoint COM automation...")
    import subprocess
    ps_cmd = f"""
    $ppt = New-Object -ComObject PowerPoint.Application
    $ppt.Visible = [Microsoft.Office.Core.MsoTriState]::msoFalse
    $presentation = $ppt.Presentations.Open('{PPTX_OUTPUT}')
    $presentation.SaveAs('{PDF_OUTPUT}', 32)
    $presentation.Close()
    $ppt.Quit()
    Write-Host "PDF Export Successful: {PDF_OUTPUT}"
    """
    try:
        res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, timeout=60)
        if res.returncode == 0 and PDF_OUTPUT.exists():
            print(f"-> PDF Successfully generated: {PDF_OUTPUT} ({os.path.getsize(PDF_OUTPUT):,} bytes)")
        else:
            print("PowerPoint COM PDF export message:", res.stdout, res.stderr)
    except Exception as e:
        print("PDF export failed or timed out:", e)

if __name__ == "__main__":
    generate_presentation()
