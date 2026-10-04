import os
from PIL import Image, ImageDraw, ImageFont

output_dir = "NEXUS_Presentation_Assets"
screen_files = [
    ("01_executive_overview.png", "1. Executive Overview"),
    ("02_digital_twin_network.png", "2. Digital Twin Network"),
    ("03_demand_intelligence.png", "3. Demand Intelligence"),
    ("04_risk_intelligence.png", "4. Supplier Risk"),
    ("05_impact_analysis.png", "5. Impact Analysis"),
    ("06_scenario_simulation.png", "6. Scenario Simulation"),
    ("07_optimization_engine.png", "7. Optimization Engine"),
    ("08_recommendation_center.png", "8. Recommendation Center")
]

# We will create a 4x2 grid of screens
# Each thumb 700x400
thumb_w, thumb_h = 700, 396
cols, rows = 4, 2
canvas_w = cols * thumb_w + (cols + 1) * 20
canvas_h = rows * thumb_h + (rows + 1) * 35 + 20

grid_img = Image.new('RGB', (canvas_w, canvas_h), color='#0B132B')
draw = ImageDraw.Draw(grid_img)

for idx, (fname, label) in enumerate(screen_files):
    p = os.path.join(output_dir, fname)
    if os.path.exists(p):
        img = Image.open(p).convert('RGB')
        img = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        
        c = idx % cols
        r = idx // cols
        
        x = 20 + c * (thumb_w + 20)
        y = 20 + r * (thumb_h + 45)
        
        # Draw border
        draw.rectangle([x-2, y-2, x+thumb_w+1, y+thumb_h+1], outline='#38BDF8', width=2)
        grid_img.paste(img, (x, y))
        
        # Label bar
        draw.rectangle([x, y+thumb_h-30, x+thumb_w, y+thumb_h], fill='#0F172A')
        draw.text((x + 12, y + thumb_h - 24), label, fill='#38BDF8')

grid_path = os.path.join(output_dir, "slide_frontend_8screens_grid.png")
grid_img.save(grid_path, quality=95)
print("Saved 8-screen grid composite to:", grid_path)
