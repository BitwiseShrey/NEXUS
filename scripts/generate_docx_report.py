"""
NEXUS - Complete Technical Documentation Master Generator
Assembles the complete report across all 35 chapters and appendices,
applying consistent styling, headers, footers, callouts, and figures.
"""

import os
import sys
import time
import shutil

# Ensure workspace root is in python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.doc_builder_helpers import init_document, add_cover_page
import scripts.sections_part1 as part1
import scripts.sections_part2 as part2
import scripts.sections_part3 as part3
import scripts.sections_part4 as part4
import scripts.sections_part5 as part5


def generate_documentation():
    print("=" * 80)
    print("NEXUS COMPLETE TECHNICAL DOCUMENTATION GENERATOR")
    print("=" * 80)
    start_time = time.time()

    print("[1/7] Initializing Document Template, Margins, Header/Footer Styles...")
    doc = init_document()

    print("[2/7] Generating Cover Page & Preliminaries...")
    add_cover_page(doc)
    part1.build_preliminaries(doc)

    print("[3/7] Generating Part 1: Chapters 1 to 6 (Introduction to Data Pipeline)...")
    part1.build_chapter_1(doc)
    part1.build_chapter_2(doc)
    part1.build_chapter_3(doc)
    part1.build_chapter_4(doc)
    part1.build_chapter_5(doc)
    part1.build_chapter_6(doc)

    print("[4/7] Generating Part 2: Chapters 7 to 13 (Database to Simulation)...")
    part2.build_chapter_7(doc)
    part2.build_chapter_8(doc)
    part2.build_chapter_9(doc)
    part2.build_chapter_10(doc)
    part2.build_chapter_11(doc)
    part2.build_chapter_12(doc)
    part2.build_chapter_13(doc)

    print("[5/7] Generating Part 3: Chapters 14 to 19 (Optimization, Flagship Scenario, API, Frontend)...")
    part3.build_chapter_14(doc)
    part3.build_chapter_15(doc)
    part3.build_chapter_16(doc)
    part3.build_chapter_17(doc)
    part3.build_chapter_18(doc)
    part3.build_chapter_19(doc)

    print("[6/7] Generating Part 4: Chapters 20 to 27 (Data Flow, Benchmarks, Testing, Security, Structure)...")
    part4.build_chapter_20(doc)
    part4.build_chapter_21(doc)
    part4.build_chapter_22(doc)
    part4.build_chapter_23(doc)
    part4.build_chapter_24(doc)
    part4.build_chapter_25(doc)
    part4.build_chapter_26(doc)
    part4.build_chapter_27(doc)

    print("[7/7] Generating Part 5: Chapters 28 to 35 (Code Snippets, Math, Guides, 55 Viva Q&As, Appendices)...")
    part5.build_chapter_28(doc)
    part5.build_chapter_29(doc)
    part5.build_chapter_30(doc)
    part5.build_chapter_31(doc)
    part5.build_chapter_32(doc)
    part5.build_chapter_33(doc)
    part5.build_chapter_34(doc)
    part5.build_chapter_35(doc)

    # Save to Root and Docs directory
    output_filename = "NEXUS_Complete_Technical_Documentation.docx"
    root_output_path = os.path.join(ROOT_DIR, output_filename)
    docs_dir = os.path.join(ROOT_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    docs_output_path = os.path.join(docs_dir, output_filename)

    print(f"\nSaving Document to {root_output_path}...")
    doc.save(root_output_path)

    print(f"Creating backup mirror in {docs_output_path}...")
    shutil.copy2(root_output_path, docs_output_path)

    elapsed = time.time() - start_time
    file_size_mb = os.path.getsize(root_output_path) / (1024 * 1024)

    # Calculate structural counts
    num_paragraphs = len(doc.paragraphs)
    num_tables = len(doc.tables)
    
    # Count inline shapes / drawings across document
    drawing_count = 0
    for p in doc.paragraphs:
        if "w:drawing" in p._p.xml:
            drawing_count += 1
    for t in doc.tables:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    if "w:drawing" in p._p.xml:
                        drawing_count += 1

    print("\n" + "=" * 80)
    print("NEXUS DOCUMENTATION GENERATION COMPLETE!")
    print("=" * 80)
    print(f"Output Path 1:        {root_output_path}")
    print(f"Output Path 2:        {docs_output_path}")
    print(f"File Size:            {file_size_mb:.2f} MB")
    print(f"Generation Time:      {elapsed:.2f} seconds")
    print(f"Total Paragraphs:     {num_paragraphs:,}")
    print(f"Total Tables:         {num_tables}")
    print(f"Total Figures/Images: {drawing_count}")
    print("=" * 80)


if __name__ == "__main__":
    generate_documentation()
