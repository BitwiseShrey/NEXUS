"""
NEXUS Capstone Phase-I Master Assembler
Runs the complete report generation pipeline, building all chapters,
embedding high-resolution assets, applying styles, and saving the document.
"""

import os
import sys
import time
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.build_full_capstone_report import init_report_doc
from scripts.capstone_sections import build_preliminaries
from scripts.capstone_chapters import build_chapter_1, build_chapter_2, build_chapter_3
from scripts.capstone_chapters_part2 import (
    build_chapter_4, build_chapter_5, build_chapter_6, build_chapter_7,
    build_appendix_a, build_appendix_b, build_references
)


def generate_capstone_report():
    print("=" * 80)
    print("GENERATING NEXUS DSN4091 CAPSTONE PHASE-I REPORT")
    print("=" * 80)
    start_time = time.time()

    print("[1/5] Initializing Document Structure & Styling...")
    doc = init_report_doc()

    print("[2/5] Building Preliminaries (Cover, Certificate, Acknowledgement, Figures, Abstract, TOC)...")
    build_preliminaries(doc)

    print("[3/5] Building Core Chapters (Chapters 1 to 7)...")
    build_chapter_1(doc)
    build_chapter_2(doc)
    build_chapter_3(doc)
    build_chapter_4(doc)
    build_chapter_5(doc)
    build_chapter_6(doc)
    build_chapter_7(doc)

    print("[4/5] Building Appendix A (Screenshots), Appendix B (Coding), and References...")
    build_appendix_a(doc)
    build_appendix_b(doc)
    build_references(doc)

    # Save to Root and Docs directory
    output_filename = "NEXUS_Capstone_Phase_I_Report.docx"
    root_output_path = os.path.join(ROOT_DIR, output_filename)
    docs_output_path = os.path.join(ROOT_DIR, "docs", output_filename)

    print(f"\n[5/5] Saving Document to {root_output_path}...")
    doc.save(root_output_path)
    shutil.copy2(root_output_path, docs_output_path)

    elapsed = time.time() - start_time
    file_size_mb = os.path.getsize(root_output_path) / (1024 * 1024)

    # Count elements
    num_paras = len(doc.paragraphs)
    num_tables = len(doc.tables)
    num_drawings = sum("w:drawing" in p._p.xml for p in doc.paragraphs)

    print("=" * 80)
    print("REPORT GENERATION COMPLETE!")
    print("=" * 80)
    print(f"Saved Path:           {root_output_path}")
    print(f"Mirror Path:          {docs_output_path}")
    print(f"File Size:            {file_size_mb:.2f} MB")
    print(f"Elapsed Time:         {elapsed:.2f} seconds")
    print(f"Total Paragraphs:     {num_paras}")
    print(f"Total Tables:         {num_tables}")
    print(f"Total Figures/Images: {num_drawings}")
    print("=" * 80)


if __name__ == "__main__":
    generate_capstone_report()
