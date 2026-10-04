import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image

output_dir = "NEXUS_Presentation_Assets"
os.makedirs(output_dir, exist_ok=True)

# Set high-quality styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#334155'
plt.rcParams['axes.linewidth'] = 1.0

# -------------------------------------------------------------
# 1. FORECASTING BENCHMARK CHART
# -------------------------------------------------------------
def generate_forecast_chart():
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#111D4A')

    models = ['Moving Average\n(8-Week)', 'Moving Average\n(4-Week)', 'Naive\nPersistence', 'XGBoost\nRegressor (NEXUS)']
    rmse = [210775.27, 153446.84, 136255.10, 96042.50]
    mae = [194063.88, 135495.41, 110961.63, 68553.14]
    smape = [11.80, 8.42, 7.20, 4.35]

    y = np.arange(len(models))
    height = 0.35

    bar1 = ax.barh(y + height/2, rmse, height, label='RMSE (Root Mean Squared Error)', color='#38BDF8', alpha=0.9, edgecolor='#0284C7', linewidth=1.5)
    bar2 = ax.barh(y - height/2, mae, height, label='MAE (Mean Absolute Error)', color='#818CF8', alpha=0.9, edgecolor='#4F46E5', linewidth=1.5)

    ax.set_yticks(y)
    ax.set_yticklabels(models, fontsize=11, fontweight='bold', color='#F1F5F9')
    ax.set_xlabel('Demand Units (Weekly Sales)', fontsize=11, color='#94A3B8', labelpad=10)
    ax.set_title('Demand Forecasting Benchmark — Empirical Walmart Dataset (421k Records)', fontsize=13, fontweight='bold', color='#FFFFFF', pad=15)
    ax.grid(axis='x', color='#1E293B', linestyle='--', alpha=0.7)
    ax.tick_params(colors='#94A3B8', labelsize=10)

    # Value labels on bars
    for b in bar1:
        w = b.get_width()
        ax.text(w + 3000, b.get_y() + b.get_height()/2, f"{w:,.0f}", va='center', ha='left', color='#38BDF8', fontsize=9, fontweight='bold')
    for b in bar2:
        w = b.get_width()
        ax.text(w + 3000, b.get_y() + b.get_height()/2, f"{w:,.0f}", va='center', ha='left', color='#C7D2FE', fontsize=9)

    # Highlight box for winner
    rect = patches.FancyBboxPatch((2000, 2.5), 180000, 1.2, boxstyle="round,pad=0.08", linewidth=1.5, edgecolor='#10B981', facecolor='#064E3B', alpha=0.35)
    ax.add_patch(rect)
    ax.text(120000, 3.25, "WINNER: -29.5% RMSE vs Naive | sMAPE: 4.35%", fontsize=9.5, fontweight='bold', color='#34D399', bbox=dict(boxstyle='round,pad=0.3', facecolor='#064E3B', edgecolor='#10B981', alpha=0.9))

    ax.set_xlim(0, 260000)
    ax.legend(loc='lower right', facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=9.5)
    plt.tight_layout()
    path = os.path.join(output_dir, "slide_forecast_benchmark.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 2. SUPPLIER RISK BENCHMARK & FEATURE IMPORTANCE
# -------------------------------------------------------------
def generate_risk_chart():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300, gridspec_kw={'width_ratios': [1.1, 1.3]})
    fig.patch.set_facecolor('#0B132B')

    # Subplot 1: Model Comparison
    ax1.set_facecolor('#111D4A')
    metrics = ['Precision', 'Recall', 'F1-Score', 'ROC-AUC']
    lr_vals = [0.7531, 0.7349, 0.7439, 0.7401]
    xgb_vals = [0.7442, 0.7711, 0.7574, 0.6988]

    x = np.arange(len(metrics))
    w = 0.35

    b1 = ax1.bar(x - w/2, lr_vals, w, label='Logistic Regression Baseline', color='#64748B', edgecolor='#94A3B8', linewidth=1.2)
    b2 = ax1.bar(x + w/2, xgb_vals, w, label='XGBoost Risk Classifier', color='#06B6D4', edgecolor='#22D3EE', linewidth=1.2)

    ax1.set_ylabel('Score (0.0 to 1.0)', fontsize=10, color='#94A3B8')
    ax1.set_title('Out-of-Sample Vendor Evaluation\n(GroupShuffleSplit, 10 Unseen Vendors)', fontsize=11, fontweight='bold', color='#FFFFFF', pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(metrics, fontsize=10, fontweight='bold', color='#F1F5F9')
    ax1.set_ylim(0.5, 0.90)
    ax1.grid(axis='y', color='#1E293B', linestyle='--', alpha=0.7)
    ax1.tick_params(colors='#94A3B8', labelsize=9)
    ax1.legend(loc='upper right', facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=8.5)

    for b in b1:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, h + 0.008, f"{h:.3f}", ha='center', va='bottom', color='#CBD5E1', fontsize=8)
    for b in b2:
        h = b.get_height()
        ax1.text(b.get_x() + b.get_width()/2, h + 0.008, f"{h:.3f}", ha='center', va='bottom', color='#67E8F9', fontsize=8, fontweight='bold')

    # Subplot 2: Feature Importance
    ax2.set_facecolor('#111D4A')
    features = [
        'Delay Frequency (3.6%)',
        'Capacity Utilization (6.1%)',
        'Quality Score (11.3%)',
        'On-Time Delivery Rate (12.0%)',
        'Average Delay Days (12.1%)',
        'Historical Delays (12.7%)',
        'Nominal Lead Time (19.8%)',
        'Lead Time Variability (22.4%)'
    ]
    imp_vals = [0.0362, 0.0611, 0.1125, 0.1202, 0.1213, 0.1271, 0.1979, 0.2238]

    colors = ['#1E3A8A', '#1E40AF', '#1D4ED8', '#2563EB', '#3B82F6', '#0284C7', '#0EA5E9', '#06B6D4']
    bars = ax2.barh(features, imp_vals, color=colors, edgecolor='#38BDF8', linewidth=1)

    ax2.set_title('Predictive Risk Drivers\n(XGBoost Feature Importance)', fontsize=11, fontweight='bold', color='#FFFFFF', pad=12)
    ax2.set_xlabel('Relative Importance Weight', fontsize=10, color='#94A3B8', labelpad=8)
    ax2.grid(axis='x', color='#1E293B', linestyle='--', alpha=0.7)
    ax2.tick_params(colors='#94A3B8', labelsize=8.5)
    ax2.set_xlim(0, 0.28)

    for b in bars:
        w_val = b.get_width()
        ax2.text(w_val + 0.006, b.get_y() + b.get_height()/2, f"{w_val*100:.1f}%", va='center', ha='left', color='#E0F2FE', fontsize=8.5, fontweight='bold')

    plt.tight_layout()
    path = os.path.join(output_dir, "slide_risk_benchmark.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 3. OPTIMIZATION COST COMPARISON WATERFALL / BARS
# -------------------------------------------------------------
def generate_optimization_chart():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300, gridspec_kw={'width_ratios': [1.3, 0.9]})
    fig.patch.set_facecolor('#0B132B')

    # Subplot 1: Cost breakdown comparison
    ax1.set_facecolor('#111D4A')
    categories = ['Procurement', 'Freight Transit', 'Inventory Holding', 'Shortage Penalties', 'TOTAL COST']
    baseline = [12.41, 1.85, 2.51, 24.45, 41.22]
    nexus = [15.82, 3.47, 0.00, 0.00, 19.29]

    x = np.arange(len(categories))
    w = 0.35

    rects1 = ax1.bar(x - w/2, baseline, w, label='Baseline Heuristic (Unoptimized)', color='#DC2626', alpha=0.85, edgecolor='#EF4444', linewidth=1.2)
    rects2 = ax1.bar(x + w/2, nexus, w, label='NEXUS Optimized (Google OR-Tools)', color='#10B981', alpha=0.85, edgecolor='#34D399', linewidth=1.2)

    ax1.set_ylabel('Cost in Millions (INR ₹)', fontsize=10.5, color='#94A3B8')
    ax1.set_title('Operational Cost Breakdown Under 80% Supplier Failure\n(SUP_001 Disruption Scenario)', fontsize=11, fontweight='bold', color='#FFFFFF', pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=9, fontweight='bold', color='#F1F5F9', rotation=15, ha='right')
    ax1.set_ylim(0, 48)
    ax1.grid(axis='y', color='#1E293B', linestyle='--', alpha=0.7)
    ax1.tick_params(colors='#94A3B8', labelsize=9)
    ax1.legend(loc='upper right', facecolor='#0F172A', edgecolor='#334155', labelcolor='#F8FAFC', fontsize=8.5)

    for r in rects1:
        h = r.get_height()
        if h > 0:
            ax1.text(r.get_x() + r.get_width()/2, h + 0.6, f"₹{h:.2f}M", ha='center', va='bottom', color='#FCA5A5', fontsize=8)
    for r in rects2:
        h = r.get_height()
        if h > 0:
            ax1.text(r.get_x() + r.get_width()/2, h + 0.6, f"₹{h:.2f}M", ha='center', va='bottom', color='#6EE7B7', fontsize=8, fontweight='bold')

    # Subplot 2: Operational KPI comparison (Service Level & Shortages)
    ax2.set_facecolor('#111D4A')
    ax2.axis('off')

    # Card 1: Cost Saved
    c1 = patches.FancyBboxPatch((0.05, 0.70), 0.90, 0.26, boxstyle="round,pad=0.03", linewidth=1.5, edgecolor='#10B981', facecolor='#064E3B')
    ax2.add_patch(c1)
    ax2.text(0.5, 0.88, "TOTAL COST REDUCTION", ha='center', va='center', color='#A7F3D0', fontsize=9.5, fontweight='bold')
    ax2.text(0.5, 0.78, "-53.19% (₹21.92M Saved)", ha='center', va='center', color='#FFFFFF', fontsize=15, fontweight='bold')
    ax2.text(0.5, 0.72, "Avoided ₹24.45M in stockout penalties", ha='center', va='center', color='#6EE7B7', fontsize=8)

    # Card 2: Service Level
    c2 = patches.FancyBboxPatch((0.05, 0.38), 0.90, 0.26, boxstyle="round,pad=0.03", linewidth=1.5, edgecolor='#0284C7', facecolor='#082F49')
    ax2.add_patch(c2)
    ax2.text(0.5, 0.56, "NETWORK SERVICE LEVEL", ha='center', va='center', color='#BAE6FD', fontsize=9.5, fontweight='bold')
    ax2.text(0.5, 0.46, "54.57% → 100.00%", ha='center', va='center', color='#FFFFFF', fontsize=15, fontweight='bold')
    ax2.text(0.5, 0.40, "+45.43 Percentage Points Fulfilled", ha='center', va='center', color='#38BDF8', fontsize=8)

    # Card 3: Solver Speed
    c3 = patches.FancyBboxPatch((0.05, 0.06), 0.90, 0.26, boxstyle="round,pad=0.03", linewidth=1.5, edgecolor='#6366F1', facecolor='#1E1B4B')
    ax2.add_patch(c3)
    ax2.text(0.5, 0.24, "OR-TOOLS GLOP SOLVER RUNTIME", ha='center', va='center', color='#DDD6FE', fontsize=9.5, fontweight='bold')
    ax2.text(0.5, 0.14, "0.0094 Seconds", ha='center', va='center', color='#FFFFFF', fontsize=15, fontweight='bold')
    ax2.text(0.5, 0.08, "Sub-10ms global multi-echelon solve", ha='center', va='center', color='#A5B4FC', fontsize=8)

    plt.tight_layout()
    path = os.path.join(output_dir, "slide_optimization_comparison.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 4. DECISION INTELLIGENCE CLOSED-LOOP DIAGRAM
# -------------------------------------------------------------
def generate_decision_loop_diagram():
    fig, ax = plt.subplots(figsize=(12, 4.5), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#0B132B')
    ax.axis('off')

    stages = [
        ("MONITOR", "Real-Time State\n& Digital Twin", "#0284C7"),
        ("PREDICT", "Demand Forecast\n& Supplier Risk", "#2563EB"),
        ("ANALYZE IMPACT", "Graph Cascade\n& Stock Runway", "#7C3AED"),
        ("SIMULATE", "What-If Stress\nState Cloning", "#D97706"),
        ("OPTIMIZE", "Google OR-Tools\nLinear Program", "#059669"),
        ("RECOMMEND", "Plain Directives\n& Action Plan", "#0D9488")
    ]

    n = len(stages)
    step_width = 1.0 / n

    for i, (title, desc, color) in enumerate(stages):
        x = i * step_width + 0.015
        y = 0.25
        w = step_width - 0.03
        h = 0.55

        # Node box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03", linewidth=1.8, edgecolor=color, facecolor='#111D4A')
        ax.add_patch(rect)

        # Header bar
        header_bar = patches.FancyBboxPatch((x, y + h - 0.18), w, 0.18, boxstyle="round,pad=0.01", linewidth=0, facecolor=color)
        ax.add_patch(header_bar)

        ax.text(x + w/2, y + h - 0.09, f"0{i+1}. {title}", ha='center', va='center', color='#FFFFFF', fontsize=9.5, fontweight='bold')
        ax.text(x + w/2, y + 0.18, desc, ha='center', va='center', color='#E2E8F0', fontsize=8.5, multialignment='center')

        # Arrow to next stage
        if i < n - 1:
            ax.annotate('', xy=(x + w + 0.025, y + h/2), xytext=(x + w + 0.005, y + h/2),
                        arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color='#38BDF8', lw=2))

    ax.text(0.5, 0.92, "NEXUS CLOSED-LOOP DECISION INTELLIGENCE ARCHITECTURE", ha='center', va='center', color='#38BDF8', fontsize=12, fontweight='bold')
    ax.text(0.5, 0.08, "Closed feedback loop converting empirical sensing into mathematically verified operational allocations", ha='center', va='center', color='#94A3B8', fontsize=8.5)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    plt.tight_layout()
    path = os.path.join(output_dir, "slide_closed_loop_flow.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 5. IMPACT PROPAGATION CASCADE DIAGRAM
# -------------------------------------------------------------
def generate_impact_cascade_diagram():
    fig, ax = plt.subplots(figsize=(11, 5), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#0B132B')
    ax.axis('off')

    # Draw 5 echelons
    echelons = [
        ("Disrupted Supplier\nSUP_001 (Pune)\n[-80% Capacity]", 0.1, 0.5, '#EF4444', '#7F1D1D'),
        ("Production Unit\nPROD_01 (Sanand)\n[Component Starvation]", 0.32, 0.5, '#F59E0B', '#78350F'),
        ("Central Warehouses\nWH_01 (West) & WH_02 (North)\n[Runway: 5.07 Days]", 0.55, 0.5, '#3B82F6', '#1E3A8A'),
        ("Distribution Hubs\nHUB_01 to HUB_04\n[Stock Depletion]", 0.77, 0.5, '#6366F1', '#312E81'),
        ("Demand Zones\n5 Metro Zones\n[69.8k Shortage Risk]", 0.94, 0.5, '#EC4899', '#831843')
    ]

    for title, x, y, border, fill in echelons:
        box = patches.FancyBboxPatch((x - 0.08, y - 0.22), 0.16, 0.44, boxstyle="round,pad=0.03", linewidth=1.8, edgecolor=border, facecolor=fill)
        ax.add_patch(box)
        ax.text(x, y, title, ha='center', va='center', color='#FFFFFF', fontsize=8.5, fontweight='bold', multialignment='center')

    # Connect with cascading disruption arrows
    for i in range(len(echelons) - 1):
        x1 = echelons[i][1] + 0.085
        x2 = echelons[i+1][1] - 0.085
        ax.annotate('', xy=(x2, 0.5), xytext=(x1, 0.5),
                    arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.6", color='#F87171', lw=2.5, linestyle='--'))

    # Alternative supplier mitigation arrow
    alt_box = patches.FancyBboxPatch((0.1 - 0.08, 0.08), 0.16, 0.22, boxstyle="round,pad=0.03", linewidth=1.5, edgecolor='#10B981', facecolor='#064E3B')
    ax.add_patch(alt_box)
    ax.text(0.1, 0.19, "Alternative Suppliers\nSUP_005 (Jamshedpur)\nSUP_009 (Pantnagar)", ha='center', va='center', color='#A7F3D0', fontsize=8, fontweight='bold', multialignment='center')

    # Arrow from alternative to warehouse
    ax.annotate('', xy=(0.55 - 0.06, 0.35), xytext=(0.18, 0.19),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.6", color='#34D399', lw=2, linestyle='-'))
    ax.text(0.35, 0.22, "NEXUS Optimization Rerouting (+₹5.04M Freight/Proc)", ha='center', va='center', color='#34D399', fontsize=8, fontweight='bold')

    ax.text(0.5, 0.90, "DOWNSTREAM IMPACT PROPAGATION & MITIGATION REROUTING", ha='center', va='center', color='#FFFFFF', fontsize=12, fontweight='bold')
    ax.text(0.5, 0.82, "Graph Traversal (BFS) reveals failure path from Tier-1 vendor to 5 metropolitan demand zones", ha='center', va='center', color='#94A3B8', fontsize=8.5)

    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.0)
    plt.tight_layout()
    path = os.path.join(output_dir, "slide_impact_propagation.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

# -------------------------------------------------------------
# 6. DIGITAL TWIN TOPOLOGY SUMMARY
# -------------------------------------------------------------
def generate_digital_twin_topology():
    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
    fig.patch.set_facecolor('#0B132B')
    ax.set_facecolor('#0B132B')
    ax.axis('off')

    nodes = [
        ("20 Suppliers", "Tier-1 & Tier-2 component vendors\n(Auto, Metals, Chemicals, Electronics)", "#38BDF8", 0.10),
        ("8 Production Units", "OEM manufacturing & assembly plants\n(Sanand, Pune, Gurgaon, Sriperumbudur)", "#818CF8", 0.30),
        ("10 Central Warehouses", "Regional distribution centers\n(500 SKUs, ₹45.9M inventory valuation)", "#34D399", 0.50),
        ("15 Distribution Hubs", "Transit sorting & transshipment hubs\n(Connecting national freight corridors)", "#FBBF24", 0.70),
        ("30 Demand Zones", "Tier-1/Tier-2 urban consumption zones\n(153k gross units demand horizon)", "#F472B6", 0.90)
    ]

    for title, desc, color, x in nodes:
        box = patches.FancyBboxPatch((x - 0.085, 0.20), 0.17, 0.55, boxstyle="round,pad=0.03", linewidth=1.5, edgecolor=color, facecolor='#111D4A')
        ax.add_patch(box)
        # badge
        badge = patches.FancyBboxPatch((x - 0.08, 0.60), 0.16, 0.12, boxstyle="round,pad=0.01", linewidth=0, facecolor=color)
        ax.add_patch(badge)
        ax.text(x, 0.66, title, ha='center', va='center', color='#0B132B', fontsize=9, fontweight='bold')
        ax.text(x, 0.40, desc, ha='center', va='center', color='#E2E8F0', fontsize=8, multialignment='center')

    ax.text(0.5, 0.90, "CALIBRATED INDIAN LOGISTICS DIGITAL TWIN TOPOLOGY (83 NODES, 160 CORRIDORS)", ha='center', va='center', color='#FFFFFF', fontsize=12, fontweight='bold')
    ax.text(0.5, 0.82, "Simulated multi-echelon network grounded in authentic Indian freight corridors & highway geodesy", ha='center', va='center', color='#94A3B8', fontsize=8.5)

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    plt.tight_layout()
    path = os.path.join(output_dir, "slide_network_topology.png")
    plt.savefig(path, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print("Saved:", path)

generate_forecast_chart()
generate_risk_chart()
generate_optimization_chart()
generate_decision_loop_diagram()
generate_impact_cascade_diagram()
generate_digital_twin_topology()
print("All custom presentation chart assets generated successfully!")
