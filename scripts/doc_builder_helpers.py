"""
NEXUS Document Builder Helpers - Compact & Justified Academic Layout
Provides styling, XML manipulation, and formatting functions for python-docx.
Configured for A4 paper size, justified body typography, compact headings,
professional table padding, and minimal vertical whitespace.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# Color Palette Constants
COLOR_NAVY = RGBColor(15, 23, 42)      # #0F172A
COLOR_PRIMARY = RGBColor(30, 58, 138)  # #1E3A8A
COLOR_SECONDARY = RGBColor(2, 132, 199)# #0284C7
COLOR_DARK_SLATE = RGBColor(51, 65, 85)# #334155
COLOR_BODY = RGBColor(30, 41, 59)      # #1E293B
COLOR_MUTED = RGBColor(100, 116, 139)  # #64748B
COLOR_WHITE = RGBColor(255, 255, 255)

HEX_NAVY = "0F172A"
HEX_PRIMARY = "1E3A8A"
HEX_SECONDARY = "0284C7"
HEX_SLATE_BG = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_ALERT_NOTE = "0284C7"
HEX_ALERT_WARN = "D97706"
HEX_ALERT_SUCCESS = "059669"
HEX_ALERT_DANGER = "DC2626"


def set_cell_background(cell, fill_hex):
    """Sets background shading of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    existing_shd = tcPr.find(qn('w:shd'))
    if existing_shd is not None:
        tcPr.remove(existing_shd)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=30, bottom=30, left=70, right=70):
    """Sets inner margins (padding) of a table cell in dxa (twips)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_callout_box_borders(cell, border_hex="0284C7", fill_hex="F0F9FF"):
    """Sets callout box with a crisp left accent border and clean light background."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(shd)
    tcPr.append(borders)


def set_code_block_borders(cell, fill_hex="F8FAFC", border_hex="CBD5E1"):
    """Sets code block styling with thin light borders and monospace background."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(shd)
    tcPr.append(borders)


def set_table_borders(table, border_hex="CBD5E1"):
    """Sets crisp, thin horizontal borders across a table for an academic look."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{border_hex}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{border_hex}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def init_document():
    """Initializes and returns an A4 Document with 1-inch margins and default styles."""
    doc = docx.Document()
    for section in doc.sections:
        # A4 Page Dimensions (210 mm x 297 mm)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

        # Header: Right-aligned academic context
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hp.paragraph_format.space_after = Pt(4)
        hrun = hp.add_run("NEXUS — AI-Powered Supply Chain Intelligence & Risk Optimization Platform")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = COLOR_MUTED

        # Footer: Academic attribution and page numbers
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        fp.paragraph_format.space_before = Pt(4)
        frun_left = fp.add_run("B.Tech Capstone Project Report | VIT Bhopal University\t\tPage ")
        frun_left.font.name = "Calibri"
        frun_left.font.size = Pt(8.5)
        frun_left.font.color.rgb = COLOR_MUTED
        
        # Add native Page field
        fldSimple = parse_xml(f'<w:fldSimple {nsdecls("w")} w:instr="PAGE"/>')
        fp._p.append(fldSimple)

    return doc


def add_cover_page(doc):
    """Adds a compact, professional B.Tech Capstone cover page."""
    # Top space
    p_top = doc.add_paragraph()
    p_top.paragraph_format.space_before = Pt(18)
    p_top.paragraph_format.space_after = Pt(12)

    # Category banner
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(18)
    r_meta = p_meta.add_run("FINAL YEAR B.TECH CAPSTONE ENGINEERING PROJECT REPORT")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(11)
    r_meta.font.bold = True
    r_meta.font.color.rgb = COLOR_SECONDARY

    # Main Project Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("NEXUS")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(34)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(4)
    r_sub = p_sub.add_run("AI-Powered Supply Chain Intelligence, Risk Prediction & Optimization Platform")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = COLOR_DARK_SLATE

    # Tagline
    p_tag = doc.add_paragraph()
    p_tag.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tag.paragraph_format.space_after = Pt(20)
    r_tag = p_tag.add_run("A Closed-Loop Multi-Echelon Decision-Support System: Monitor → Predict → Analyze Impact → Simulate → Optimize → Recommend")
    r_tag.font.name = "Calibri"
    r_tag.font.size = Pt(10)
    r_tag.font.italic = True
    r_tag.font.color.rgb = COLOR_MUTED

    # Decorative Rule Table
    div_table = doc.add_table(rows=1, cols=1)
    div_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    div_cell = div_table.cell(0, 0)
    div_cell.width = Inches(4.5)
    set_cell_background(div_cell, HEX_SECONDARY)
    div_p = div_cell.paragraphs[0]
    div_p.paragraph_format.space_before = Pt(1)
    div_p.paragraph_format.space_after = Pt(1)
    div_r = div_p.add_run("")
    div_r.font.size = Pt(2)

    # Space before info table
    p_gap = doc.add_paragraph()
    p_gap.paragraph_format.space_before = Pt(20)
    p_gap.paragraph_format.space_after = Pt(4)

    # Candidate and Degree Info Box Table
    info_table = doc.add_table(rows=6, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(info_table, "CBD5E1")

    info_data = [
        ("Candidate Name:", "Shreyansh Uttam"),
        ("Degree & Specialization:", "B.Tech Computer Science & Engineering (AI & ML)"),
        ("Department / School:", "School of Computing Science & Engineering (SCSE)"),
        ("Institution:", "Vellore Institute of Technology (VIT) Bhopal University"),
        ("Academic Year:", "2025 – 2026"),
        ("Project Classification:", "Major Project / Capstone Evaluation")
    ]

    for row_idx, (label, val) in enumerate(info_data):
        row = info_table.rows[row_idx]
        cell_lbl, cell_val = row.cells[0], row.cells[1]
        cell_lbl.width = Inches(2.2)
        cell_val.width = Inches(4.2)
        set_cell_margins(cell_lbl, 50, 50, 90, 90)
        set_cell_margins(cell_val, 50, 50, 90, 90)
        set_cell_background(cell_lbl, "F1F5F9")
        set_cell_background(cell_val, "FFFFFF")

        p_l = cell_lbl.paragraphs[0]
        p_l.paragraph_format.space_before = Pt(1)
        p_l.paragraph_format.space_after = Pt(1)
        r_l = p_l.add_run(label)
        r_l.font.name = "Calibri"
        r_l.font.size = Pt(9.5)
        r_l.font.bold = True
        r_l.font.color.rgb = COLOR_DARK_SLATE

        p_v = cell_val.paragraphs[0]
        p_v.paragraph_format.space_before = Pt(1)
        p_v.paragraph_format.space_after = Pt(1)
        r_v = p_v.add_run(val)
        r_v.font.name = "Calibri"
        r_v.font.size = Pt(9.5)
        r_v.font.bold = (row_idx == 0 or row_idx == 1)
        r_v.font.color.rgb = COLOR_PRIMARY if row_idx == 0 else COLOR_BODY

    # Page break after cover
    doc.add_page_break()


def add_heading_1(doc, title):
    """Adds a major section heading (Heading 1) with compact academic spacing."""
    p = doc.add_paragraph(style='Heading 1')
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    if not p.runs:
        r = p.add_run(title)
    else:
        r = p.runs[0]
        r.text = title
    r.font.name = "Arial"
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY
    return p


def add_heading_2(doc, title):
    """Adds a subsection heading (Heading 2) with compact academic spacing."""
    p = doc.add_paragraph(style='Heading 2')
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    if not p.runs:
        r = p.add_run(title)
    else:
        r = p.runs[0]
        r.text = title
    r.font.name = "Arial"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    return p


def add_heading_3(doc, title):
    """Adds a sub-subsection heading (Heading 3) with compact academic spacing."""
    p = doc.add_paragraph(style='Heading 3')
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    if not p.runs:
        r = p.add_run(title)
    else:
        r = p.runs[0]
        r.text = title
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_DARK_SLATE
    return p


def add_paragraph(doc, text="", bold_prefix=None, italic=False, space_after=3.5):
    """Adds a strictly JUSTIFIED body paragraph with 1.12 line spacing and compact margins."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.12
    if bold_prefix:
        r_b = p.add_run(bold_prefix + " ")
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(10)
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_DARK_SLATE
    if text:
        r_t = p.add_run(text)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10)
        r_t.font.italic = italic
        r_t.font.color.rgb = COLOR_BODY
    return p


def add_bullet(doc, text="", bold_prefix=None):
    """Adds a justified bullet point item with compact spacing."""
    p = doc.add_paragraph(style='List Bullet')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.10
    if bold_prefix:
        r_b = p.add_run(bold_prefix + " ")
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(10)
        r_b.font.bold = True
        r_b.font.color.rgb = COLOR_DARK_SLATE
    if text:
        r_t = p.add_run(text)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = COLOR_BODY
    return p


def add_callout(doc, text, alert_type="NOTE", title=None):
    """Adds a shaded callout alert box with a thick left border and justified text."""
    border_hex = HEX_ALERT_NOTE
    fill_hex = "F0F9FF"
    tag_name = "NOTE"
    if alert_type.upper() in ["WARNING", "CAUTION"]:
        border_hex = HEX_ALERT_WARN
        fill_hex = "FFFBEB"
        tag_name = "WARNING"
    elif alert_type.upper() in ["IMPORTANT", "CRITICAL"]:
        border_hex = HEX_ALERT_DANGER
        fill_hex = "FEF2F2"
        tag_name = "IMPORTANT"
    elif alert_type.upper() in ["TIP", "SUCCESS"]:
        border_hex = HEX_ALERT_SUCCESS
        fill_hex = "F0FDF4"
        tag_name = "KEY FINDING"

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_callout_box_borders(cell, border_hex, fill_hex)
    set_cell_margins(cell, top=45, bottom=45, left=90, right=90)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.10

    header_text = title if title else f"[{tag_name}]"
    r_hdr = p.add_run(header_text + "\n")
    r_hdr.font.name = "Calibri"
    r_hdr.font.size = Pt(9.0)
    r_hdr.font.bold = True
    r_hdr.font.color.rgb = RGBColor.from_string(border_hex)

    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(9.0)
    r_body.font.italic = False
    r_body.font.color.rgb = COLOR_BODY


def add_code_block(doc, code_str, caption=None):
    """Adds a styled monospace code snippet block with minimal padding."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_code_block_borders(cell, "F8FAFC", "CBD5E1")
    set_cell_margins(cell, top=35, bottom=35, left=80, right=80)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.0

    lines = code_str.strip().split("\n")
    for i, line in enumerate(lines):
        r = p.add_run(line + ("\n" if i < len(lines) - 1 else ""))
        r.font.name = "Consolas"
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(15, 23, 42)

    if caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(4)
        r_cap = p_cap.add_run(f"Listing: {caption}")
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.0)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED


def add_image_with_caption(doc, image_path, caption, width=Inches(5.2)):
    """Inserts a centered image with compact spacing and formal figure caption."""
    if not os.path.exists(image_path):
        p_err = doc.add_paragraph(f"[Image Missing: {image_path}]")
        p_err.font.color.rgb = COLOR_MUTED
        return

    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(1)
    run_img = p_img.add_run()
    run_img.add_picture(image_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(5)
    p_cap.paragraph_format.keep_with_next = False

    r_cap = p_cap.add_run(caption)
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(8.5)
    r_cap.font.italic = True
    r_cap.font.color.rgb = COLOR_MUTED


def add_custom_table(doc, headers, data, col_widths=None, alignment=None, title=None):
    """Creates a compact, professional table with shaded headers, alternating rows, and optional title."""
    if title:
        p_t = doc.add_paragraph()
        p_t.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_t.paragraph_format.space_before = Pt(5)
        p_t.paragraph_format.space_after = Pt(2)
        p_t.paragraph_format.keep_with_next = True
        r_t = p_t.add_run(title)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(9.5)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_DARK_SLATE

    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, "CBD5E1")

    # If col_widths sum exceeds 6.35 inches on A4, scale proportionally
    scaled_widths = None
    if col_widths:
        total_w = sum(w.inches for w in col_widths)
        max_allowed = 6.35
        if total_w > max_allowed:
            scale_factor = max_allowed / total_w
            scaled_widths = [Inches(w.inches * scale_factor) for w in col_widths]
        else:
            scaled_widths = col_widths

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = ""
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if (alignment and alignment[i] == 'C') else WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(h_text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.0)
        r.font.bold = True
        r.font.color.rgb = COLOR_WHITE
        set_cell_background(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=35, bottom=35, left=70, right=70)
        if scaled_widths and i < len(scaled_widths):
            hdr_cells[i].width = scaled_widths[i]

    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg_hex = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = ""
            p = row_cells[col_idx].paragraphs[0]
            if alignment and col_idx < len(alignment):
                if alignment[col_idx] == 'C':
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif alignment[col_idx] == 'R':
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

            p.paragraph_format.space_before = Pt(0.5)
            p.paragraph_format.space_after = Pt(0.5)
            p.paragraph_format.line_spacing = 1.0

            r = p.add_run(str(cell_value))
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = COLOR_BODY
            set_cell_background(row_cells[col_idx], bg_hex)
            set_cell_margins(row_cells[col_idx], top=22, bottom=22, left=70, right=70)
            if scaled_widths and col_idx < len(scaled_widths):
                row_cells[col_idx].width = scaled_widths[col_idx]

    return table


def add_equation_block(doc, eq_str, eq_num=None, explanation=None):
    """Adds a styled mathematical equation block with optional numbering and compact explanation."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.3)
    set_code_block_borders(cell, "F1F5F9", "94A3B8")
    set_cell_margins(cell, top=35, bottom=35, left=90, right=90)

    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)

    r_eq = p.add_run(eq_str)
    r_eq.font.name = "Cambria Math"
    r_eq.font.size = Pt(10.5)
    r_eq.font.bold = True
    r_eq.font.color.rgb = COLOR_PRIMARY

    if eq_num:
        r_num = p.add_run(f"\t\t\t({eq_num})")
        r_num.font.name = "Calibri"
        r_num.font.size = Pt(9.0)
        r_num.font.color.rgb = COLOR_MUTED

    if explanation:
        p_exp = doc.add_paragraph()
        p_exp.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_exp.paragraph_format.space_before = Pt(1)
        p_exp.paragraph_format.space_after = Pt(3)
        r_exp = p_exp.add_run(f"Where: {explanation}")
        r_exp.font.name = "Calibri"
        r_exp.font.size = Pt(8.5)
        r_exp.font.italic = True
        r_exp.font.color.rgb = COLOR_MUTED
