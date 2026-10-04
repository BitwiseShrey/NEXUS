"""
Generates custom pastel assets for the 13-slide NEXUS presentation.
Theme: Pastel Supply Chain Control Tower
Background: Warm Ivory (#FAF8F3) / Soft Cream (#FFFDF9)
Accents: Mint (#D9F3EE), Pastel Blue (#DCEBFA), Lavender (#E9E1F7), Peach (#FCE3D6), Yellow (#FFF0C7)
Text: Charcoal (#20252B), Slate (#626A73), Muted (#9299A1)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = "NEXUS_Pastel_Presentation_Assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

IVORY = "#FAF8F3"
CREAM = "#FFFDF9"
CHARCOAL = "#20252B"
SECONDARY = "#626A73"
MUTED = "#9299A1"
BORDER_COLOR = "#E2DDD2"

MINT = "#D9F3EE"
MINT_BORDER = "#10B981"
BLUE = "#DCEBFA"
BLUE_BORDER = "#3B82F6"
LAVENDER = "#E9E1F7"
LAVENDER_BORDER = "#8B5CF6"
PEACH = "#FCE3D6"
PEACH_BORDER = "#F97316"
YELLOW = "#FFF0C7"
YELLOW_BORDER = "#EAB308"
CORAL = "#FEE2E2"
CORAL_BORDER = "#EF4444"

# Set matplotlib parameters for clean pastel style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = BORDER_COLOR
plt.rcParams['axes.linewidth'] = 1.0

# -------------------------------------------------------------
# 1. ABSTRACT COVER SUPPLY CHAIN NETWORK
# -------------------------------------------------------------
def generate_cover_network():
    fig, ax = plt.subplots(figsize=(8, 7), dpi=300)
    fig.patch.set_facecolor(IVORY)
    ax.set_facecolor(IVORY)
    ax.axis('off')

    # Subtle background grid dots
    for x in np.linspace(0.05, 0.95, 12):
        for y in np.linspace(0.05, 0.95, 12):
            ax.plot(x, y, 'o', color='#EAE5DB', markersize=2, alpha=0.6)

    # Define tier positions
    tiers = {
        'Suppliers': [(0.15, 0.78), (0.15, 0.50), (0.15, 0.22)],
        'Production': [(0.35, 0.65), (0.35, 0.35)],
        'Warehouses': [(0.55, 0.75), (0.55, 0.45), (0.55, 0.18)],
        'Hubs': [(0.72, 0.60), (0.72, 0.32)],
        'Demand': [(0.90, 0.80), (0.90, 0.52), (0.90, 0.25)]
    }

    # Draw connection lines (curved-like arcs or thin clean segments)
    all_nodes = [
        (0.15, 0.78), (0.15, 0.50), (0.15, 0.22),
        (0.35, 0.65), (0.35, 0.35),
        (0.55, 0.75), (0.55, 0.45), (0.55, 0.18),
        (0.72, 0.60), (0.72, 0.32),
        (0.90, 0.80), (0.90, 0.52), (0.90, 0.25)
    ]

    # Connections
    edges = [
        ((0.15, 0.78), (0.35, 0.65)),
        ((0.15, 0.50), (0.35, 0.65)),
        ((0.15, 0.50), (0.35, 0.35)),
        ((0.15, 0.22), (0.35, 0.35)),
        ((0.35, 0.65), (0.55, 0.75)),
        ((0.35, 0.65), (0.55, 0.45)),
        ((0.35, 0.35), (0.55, 0.45)),
        ((0.35, 0.35), (0.55, 0.18)),
        ((0.55, 0.75), (0.72, 0.60)),
        ((0.55, 0.45), (0.72, 0.60)),
        ((0.55, 0.45), (0.72, 0.32)),
        ((0.55, 0.18), (0.72, 0.32)),
        ((0.72, 0.60), (0.90, 0.80)),
        ((0.72, 0.60), (0.90, 0.52)),
        ((0.72, 0.32), (0.90, 0.52)),
        ((0.72, 0.32), (0.90, 0.25))
    ]

    for (x1, y1), (x2, y2) in edges:
        ax.plot([x1, x2], [y1, y2], '-', color='#D5D1C8', linewidth=1.5, alpha=0.8, zorder=1)

    # Highlight active flow corridor
    active_path = [(0.15, 0.50), (0.35, 0.65), (0.55, 0.45), (0.72, 0.60), (0.90, 0.52)]
    px = [p[0] for p in active_path]
    py = [p[1] for p in active_path]
    ax.plot(px, py, '-', color=BLUE_BORDER, linewidth=2.5, alpha=0.9, zorder=2)

    # Draw Nodes with pastel styling
    tier_styles = [
        ('Suppliers', tiers['Suppliers'], MINT, MINT_BORDER, "Supplier"),
        ('Production', tiers['Production'], BLUE, BLUE_BORDER, "Factory"),
        ('Warehouses', tiers['Warehouses'], LAVENDER, LAVENDER_BORDER, "Warehouse"),
        ('Hubs', tiers['Hubs'], YELLOW, YELLOW_BORDER, "Hub"),
        ('Demand', tiers['Demand'], PEACH, PEACH_BORDER, "Demand")
    ]

    for name, coords, bg, border, label in tier_styles:
        for x, y in coords:
            # Outer subtle halo
            circle_halo = patches.Circle((x, y), 0.045, facecolor=bg, edgecolor=border, linewidth=1.8, alpha=0.4, zorder=3)
            ax.add_patch(circle_halo)
            # Inner solid circle
            circle = patches.Circle((x, y), 0.028, facecolor=bg, edgecolor=border, linewidth=2.0, zorder=4)
            ax.add_patch(circle)

    # Header labels for echelons
    tier_headers = [
        (0.15, "SUPPLIERS"), (0.35, "PRODUCTION"), (0.55, "WAREHOUSES"),
        (0.72, "HUBS"), (0.90, "DEMAND")
    ]
    for x, title in tier_headers:
        ax.text(x, 0.90, title, ha='center', va='center', fontsize=7.5, fontweight='bold', color=SECONDARY)

    # Disruption indicator tag
    ax.text(0.15, 0.58, "SUP_001", ha='center', va='center', fontsize=7.5, fontweight='bold', color=CHARCOAL,
            bbox=dict(boxstyle='round,pad=0.2', facecolor=CREAM, edgecolor='#CBD5E1', alpha=0.95))

    ax.set_xlim(0.05, 0.98)
    ax.set_ylim(0.05, 0.98)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "pastel_cover_network.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 2. PASTEL DECISION LOOP
# -------------------------------------------------------------
def generate_decision_loop():
    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=300)
    fig.patch.set_facecolor(IVORY)
    ax.set_facecolor(IVORY)
    ax.axis('off')

    stages = [
        ("MONITOR", "What is happening?", "Live state of 83 nodes across 5 tiers", MINT, MINT_BORDER),
        ("PREDICT", "What is likely to happen?", "XGBoost demand & supplier risk", BLUE, BLUE_BORDER),
        ("IMPACT", "What will it affect?", "Graph BFS & warehouse runway days", LAVENDER, LAVENDER_BORDER),
        ("SIMULATE", "What if we intervene?", "Non-destructive what-if stress tests", YELLOW, YELLOW_BORDER),
        ("OPTIMIZE", "What is the best allocation?", "Google OR-Tools multi-echelon LP", "#DDEEDB", "#16A34A"),
        ("RECOMMEND", "What should we do?", "Plain directives & simulated dispatch", PEACH, PEACH_BORDER)
    ]

    n = len(stages)
    w = 0.14
    h = 0.65
    gap = (0.92 - (n * w)) / (n - 1)

    for i, (title, question, desc, bg, border) in enumerate(stages):
        x = 0.04 + i * (w + gap)
        y = 0.18

        # Rounded card
        card = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                      linewidth=1.5, edgecolor=border, facecolor=bg)
        ax.add_patch(card)

        # Content
        ax.text(x + w/2, y + h - 0.12, f"0{i+1}", ha='center', va='center', fontsize=12, fontweight='bold', color=border)
        ax.text(x + w/2, y + h - 0.24, title, ha='center', va='center', fontsize=9.5, fontweight='bold', color=CHARCOAL)
        ax.text(x + w/2, y + h - 0.38, question, ha='center', va='center', fontsize=7.5, fontstyle='italic', fontweight='bold', color=SECONDARY)
        ax.text(x + w/2, y + 0.12, desc, ha='center', va='center', fontsize=7.0, color=SECONDARY, multialignment='center')

        # Arrow to next
        if i < n - 1:
            next_x = x + w
            arrow_end = next_x + gap
            ax.annotate('', xy=(arrow_end - 0.005, y + h/2), xytext=(next_x + 0.005, y + h/2),
                        arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.5", color='#94A3B8', lw=1.6))

    # Bottom loop return arrow
    ax.annotate('', xy=(0.04 + w/2, 0.08), xytext=(0.04 + (n-1)*(w+gap) + w/2, 0.08),
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4", color='#CBD5E1', lw=1.4, linestyle='--'))
    ax.text(0.5, 0.08, "Closed Feedback Loop — Prediction directly drives operational decisions",
            ha='center', va='center', fontsize=8, color=MUTED, bbox=dict(boxstyle='round,pad=0.2', facecolor=CREAM, edgecolor='#E2DDD2'))

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 0.95)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "pastel_decision_loop.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 3. PASTEL DIGITAL TWIN SIMPLIFIED TOPOLOGY & CASCADE
# -------------------------------------------------------------
def generate_digital_twin_map():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    fig.patch.set_facecolor(IVORY)
    ax.set_facecolor(IVORY)
    ax.axis('off')

    # Five echelon columns
    col_x = [0.10, 0.30, 0.50, 0.70, 0.90]
    titles = [
        ("20 Suppliers", MINT, MINT_BORDER),
        ("8 Factories", BLUE, BLUE_BORDER),
        ("10 Warehouses", LAVENDER, LAVENDER_BORDER),
        ("15 Hubs", YELLOW, YELLOW_BORDER),
        ("30 Zones", PEACH, PEACH_BORDER)
    ]

    for idx, (t, bg, border) in enumerate(titles):
        cx = col_x[idx]
        card = patches.FancyBboxPatch((cx - 0.08, 0.15), 0.16, 0.70, boxstyle="round,pad=0.02",
                                      linewidth=1.2, edgecolor=border, facecolor=CREAM)
        ax.add_patch(card)
        # Header pill
        pill = patches.FancyBboxPatch((cx - 0.075, 0.72), 0.15, 0.10, boxstyle="round,pad=0.01",
                                      linewidth=0, facecolor=bg)
        ax.add_patch(pill)
        ax.text(cx, 0.77, t, ha='center', va='center', fontsize=8.5, fontweight='bold', color=CHARCOAL)

    # Disruption flow in coral
    # Supplier (SUP_001) -> Factory (PROD_01) -> WH_01 -> Hubs -> Demand
    disrupted_nodes = [
        (col_x[0], 0.55, "SUP_001\n(-80%)"),
        (col_x[1], 0.55, "Assembly\nStarved"),
        (col_x[2], 0.55, "WH_01\n(5.07d)"),
        (col_x[3], 0.55, "Hubs\nLow Stock"),
        (col_x[4], 0.55, "5 Metro\nZones")
    ]

    for i in range(len(disrupted_nodes) - 1):
        x1, y1, _ = disrupted_nodes[i]
        x2, y2, _ = disrupted_nodes[i+1]
        ax.annotate('', xy=(x2 - 0.05, y2), xytext=(x1 + 0.05, y1),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.5", color=CORAL_BORDER, lw=2.2, linestyle='--'))

    for x, y, lbl in disrupted_nodes:
        node_box = patches.FancyBboxPatch((x - 0.065, y - 0.08), 0.13, 0.16, boxstyle="round,pad=0.02",
                                          linewidth=1.6, edgecolor=CORAL_BORDER, facecolor=CORAL)
        ax.add_patch(node_box)
        ax.text(x, y, lbl, ha='center', va='center', fontsize=7.5, fontweight='bold', color="#991B1B", multialignment='center')

    # Mitigation flow from alternative vendor
    alt_nodes = [
        (col_x[0], 0.28, "SUP_005\n(Backup)"),
        (col_x[2], 0.28, "WH_01\n(Rebalanced)")
    ]
    ax.annotate('', xy=(alt_nodes[1][0] - 0.05, 0.28), xytext=(alt_nodes[0][0] + 0.05, 0.28),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.5", color="#16A34A", lw=2.0))
    ax.text(0.30, 0.32, "NEXUS Reallocation (+₹5.04M Logistics)", ha='center', va='center', fontsize=7.5, fontweight='bold', color="#16A34A")

    for x, y, lbl in alt_nodes:
        node_box = patches.FancyBboxPatch((x - 0.065, y - 0.08), 0.13, 0.16, boxstyle="round,pad=0.02",
                                          linewidth=1.4, edgecolor="#16A34A", facecolor="#DCFCE7")
        ax.add_patch(node_box)
        ax.text(x, y, lbl, ha='center', va='center', fontsize=7.5, fontweight='bold', color="#166534", multialignment='center')

    ax.text(0.5, 0.90, "INDIAN MULTI-ECHELON TOPOLOGY (83 NODES, 160 CORRIDORS)",
            ha='center', va='center', fontsize=11, fontweight='bold', color=CHARCOAL)
    ax.text(0.5, 0.06, "Highlighting failure cascade from SUP_001 in Pune to WH_01, alongside optimal secondary vendor rerouting",
            ha='center', va='center', fontsize=8, color=SECONDARY)

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 0.98)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "pastel_supply_chain_twin.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 4. PASTEL MODEL COMPARISON
# -------------------------------------------------------------
def generate_pastel_model_charts():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.8), dpi=300, gridspec_kw={'width_ratios': [1.1, 1.1]})
    fig.patch.set_facecolor(IVORY)

    # Chart 1: Demand RMSE
    ax1.set_facecolor(CREAM)
    models = ['8-Week Moving Avg', '4-Week Moving Avg', 'Naive Persistence', 'XGBoost (NEXUS)']
    rmse_vals = [210775.27, 153446.84, 136255.10, 96042.50]
    colors = ['#E2E8F0', '#E2E8F0', '#CBD5E1', MINT]
    edgecolors = ['#CBD5E1', '#CBD5E1', '#94A3B8', MINT_BORDER]

    y_pos = np.arange(len(models))
    bars1 = ax1.barh(y_pos, rmse_vals, height=0.45, color=colors, edgecolor=edgecolors, linewidth=1.5)

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(models, fontsize=9, fontweight='bold', color=CHARCOAL)
    ax1.set_xlabel('Root Mean Squared Error (RMSE)', fontsize=8.5, color=SECONDARY, labelpad=8)
    ax1.set_title('Demand Forecasting Error (Walmart Series)', fontsize=10.5, fontweight='bold', color=CHARCOAL, pad=12)
    ax1.grid(axis='x', color='#EAE5DB', linestyle='--', alpha=0.8)
    ax1.tick_params(colors=SECONDARY, labelsize=8)
    ax1.set_xlim(0, 250000)

    for b in bars1:
        w = b.get_width()
        ax1.text(w + 3500, b.get_y() + b.get_height()/2, f"{w:,.0f}", va='center', ha='left', color=CHARCOAL, fontsize=8, fontweight='bold')

    # Callout badge for XGBoost
    ax1.text(96042.50 / 2, 3, "-29.51% RMSE", va='center', ha='center', color="#065F46", fontsize=8, fontweight='bold')

    # Chart 2: Supplier Risk Metrics
    ax2.set_facecolor(CREAM)
    metrics = ['Precision', 'Recall', 'F1-Score']
    lr = [0.7531, 0.7349, 0.7439]
    xgb = [0.7442, 0.7711, 0.7574]

    x = np.arange(len(metrics))
    w = 0.32

    b1 = ax2.bar(x - w/2, lr, w, label='Logistic Regression Baseline', color='#F1F5F9', edgecolor='#94A3B8', linewidth=1.2)
    b2 = ax2.bar(x + w/2, xgb, w, label='XGBoost Classifier (NEXUS)', color=BLUE, edgecolor=BLUE_BORDER, linewidth=1.4)

    ax2.set_ylabel('Score (0.0 - 1.0)', fontsize=8.5, color=SECONDARY)
    ax2.set_title('Supplier Risk on 10 Unseen Vendors', fontsize=10.5, fontweight='bold', color=CHARCOAL, pad=12)
    ax2.set_xticks(x)
    ax2.set_xticklabels(metrics, fontsize=9, fontweight='bold', color=CHARCOAL)
    ax2.set_ylim(0.65, 0.85)
    ax2.grid(axis='y', color='#EAE5DB', linestyle='--', alpha=0.8)
    ax2.tick_params(colors=SECONDARY, labelsize=8)
    ax2.legend(loc='lower right', facecolor=CREAM, edgecolor='#CBD5E1', fontsize=7.5)

    for b in b1:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 0.005, f"{h:.3f}", ha='center', va='bottom', color=SECONDARY, fontsize=7.5)
    for b in b2:
        h = b.get_height()
        ax2.text(b.get_x() + b.get_width()/2, h + 0.005, f"{h:.3f}", ha='center', va='bottom', color="#1E40AF", fontsize=7.5, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "pastel_model_charts.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 5. PASTEL OPTIMIZATION COMPARISON CARDS
# -------------------------------------------------------------
def generate_pastel_optimization_diff():
    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=300)
    fig.patch.set_facecolor(IVORY)
    ax.set_facecolor(IVORY)
    ax.axis('off')

    # Baseline Card (Left)
    card1 = patches.FancyBboxPatch((0.05, 0.15), 0.38, 0.70, boxstyle="round,pad=0.03",
                                   linewidth=1.5, edgecolor=PEACH_BORDER, facecolor=PEACH)
    ax.add_patch(card1)
    ax.text(0.24, 0.76, "BASELINE HEURISTIC", ha='center', va='center', fontsize=11, fontweight='bold', color="#9A3412")
    ax.text(0.24, 0.65, "₹41.22M", ha='center', va='center', fontsize=24, fontweight='bold', color=CHARCOAL)
    ax.text(0.24, 0.58, "Total Operational Cost", ha='center', va='center', fontsize=9, color=SECONDARY)
    ax.text(0.24, 0.44, "69,843 Units", ha='center', va='center', fontsize=14, fontweight='bold', color="#B91C1C")
    ax.text(0.24, 0.38, "Unmet Demand Shortage", ha='center', va='center', fontsize=8.5, color=SECONDARY)
    ax.text(0.24, 0.26, "54.57% Service Level", ha='center', va='center', fontsize=12, fontweight='bold', color="#9A3412")

    # Center Differential Pill
    diff_box = patches.FancyBboxPatch((0.44, 0.22), 0.12, 0.56, boxstyle="round,pad=0.02",
                                      linewidth=1.4, edgecolor=MINT_BORDER, facecolor=CREAM)
    ax.add_patch(diff_box)
    ax.text(0.50, 0.66, "-53.19%", ha='center', va='center', fontsize=13, fontweight='bold', color=MINT_BORDER)
    ax.text(0.50, 0.59, "Cost Cut", ha='center', va='center', fontsize=7.5, color=SECONDARY)
    ax.text(0.50, 0.48, "₹21.92M", ha='center', va='center', fontsize=11, fontweight='bold', color=CHARCOAL)
    ax.text(0.50, 0.42, "Saved", ha='center', va='center', fontsize=7.5, color=SECONDARY)
    ax.text(0.50, 0.32, "+45.43 pp", ha='center', va='center', fontsize=10, fontweight='bold', color=MINT_BORDER)
    ax.text(0.50, 0.26, "SLA Gain", ha='center', va='center', fontsize=7.5, color=SECONDARY)

    # NEXUS Optimized Card (Right)
    card2 = patches.FancyBboxPatch((0.57, 0.15), 0.38, 0.70, boxstyle="round,pad=0.03",
                                   linewidth=1.8, edgecolor=MINT_BORDER, facecolor=MINT)
    ax.add_patch(card2)
    ax.text(0.76, 0.76, "NEXUS OPTIMIZED (OR-TOOLS)", ha='center', va='center', fontsize=11, fontweight='bold', color="#065F46")
    ax.text(0.76, 0.65, "₹19.29M", ha='center', va='center', fontsize=24, fontweight='bold', color=CHARCOAL)
    ax.text(0.76, 0.58, "Total Operational Cost", ha='center', va='center', fontsize=9, color=SECONDARY)
    ax.text(0.76, 0.44, "0 Units", ha='center', va='center', fontsize=14, fontweight='bold', color="#065F46")
    ax.text(0.76, 0.38, "Zero Unmet Shortage", ha='center', va='center', fontsize=8.5, color=SECONDARY)
    ax.text(0.76, 0.26, "100.00% Service Level", ha='center', va='center', fontsize=12, fontweight='bold', color="#065F46")

    ax.text(0.50, 0.90, "FLAGSHIP DISRUPTION: 80% CAPACITY LOSS ON SUP_001 (10 DAYS)",
            ha='center', va='center', fontsize=10.5, fontweight='bold', color=CHARCOAL)
    ax.text(0.50, 0.06, "Simulated stress scenario outcome using Google OR-Tools multi-echelon linear program (Solver runtime: 0.0094s)",
            ha='center', va='center', fontsize=8, color=SECONDARY)

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 0.98)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, "pastel_optimization_diff.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 6. PASTEL PRODUCT COLLAGE (CROPPED FRONTEND SCREENS)
# -------------------------------------------------------------
def generate_product_collage():
    doc_assets = "NEXUS_Documentation_Assets"
    
    # We will pick 4 key screens and crop them into clean rounded cards
    screens = [
        ("01_executive_overview.png", "MONITOR", MINT, MINT_BORDER),
        ("02_digital_twin_network.png", "TRACE", BLUE, BLUE_BORDER),
        ("03_demand_intelligence.png", "PREDICT", LAVENDER, LAVENDER_BORDER),
        ("07_optimization_engine.png", "OPTIMIZE", YELLOW, YELLOW_BORDER),
        ("08_recommendation_center.png", "DECIDE", PEACH, PEACH_BORDER)
    ]

    canvas_w, canvas_h = 1600, 750
    collage = Image.new('RGB', (canvas_w, canvas_h), color=IVORY)
    draw = ImageDraw.Draw(collage)

    thumb_w, thumb_h = 300, 600
    gap = (canvas_w - 60 - (5 * thumb_w)) // 4

    for idx, (fname, label, bg, border) in enumerate(screens):
        p = os.path.join(doc_assets, fname)
        x = 30 + idx * (thumb_w + gap)
        y = 50

        if os.path.exists(p):
            im = Image.open(p).convert('RGB')
            # Intelligent crop: take the most interesting upper-middle portion of the dashboard
            w_orig, h_orig = im.size
            crop_box = (int(w_orig * 0.15), int(h_orig * 0.10), int(w_orig * 0.95), int(h_orig * 0.90))
            im_cropped = im.crop(crop_box)
            im_thumb = im_cropped.resize((thumb_w, thumb_h - 70), Image.Resampling.LANCZOS)

            # Paste thumbnail
            collage.paste(im_thumb, (x, y + 60))

            # Draw card frame
            draw.rectangle([x-2, y+58, x+thumb_w+1, y+thumb_h-8], outline=border, width=2)

            # Draw top label bar
            draw.rounded_rectangle([x, y, x+thumb_w, y+50], radius=8, fill=bg, outline=border, width=1)
            draw.text((x + thumb_w//2 - 35, y + 16), label, fill=CHARCOAL)

    path = os.path.join(OUTPUT_DIR, "pastel_product_collage.png")
    collage.save(path, quality=95)
    print("Saved:", path)

generate_cover_network()
generate_decision_loop()
generate_digital_twin_map()
generate_pastel_model_charts()
generate_pastel_optimization_diff()
generate_product_collage()
print("All pastel presentation assets successfully generated!")
