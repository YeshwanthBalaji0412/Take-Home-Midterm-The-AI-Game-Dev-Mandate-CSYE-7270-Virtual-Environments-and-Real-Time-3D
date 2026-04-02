"""
PDF Generator for CSYE 7270 Midterm Submission
Converts essay.md and authors_note.md to publication-quality PDFs using ReportLab.
Run: python3 generate_pdfs.py
Outputs: essay.pdf, authors_note.pdf
"""

import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, Preformatted
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ─────────────────────────────────────────────
# Style definitions
# ─────────────────────────────────────────────

def build_styles():
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "DocTitle",
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            spaceAfter=6,
            alignment=TA_LEFT,
            textColor=colors.HexColor("#1a1a2e"),
        ),
        "subtitle": ParagraphStyle(
            "DocSubtitle",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            spaceAfter=4,
            textColor=colors.HexColor("#444444"),
        ),
        "h1": ParagraphStyle(
            "H1",
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            spaceBefore=18,
            spaceAfter=6,
            textColor=colors.HexColor("#1a1a2e"),
            borderPad=0,
        ),
        "h2": ParagraphStyle(
            "H2",
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            spaceBefore=12,
            spaceAfter=4,
            textColor=colors.HexColor("#2d3748"),
        ),
        "h3": ParagraphStyle(
            "H3",
            fontName="Helvetica-BoldOblique",
            fontSize=10,
            leading=14,
            spaceBefore=10,
            spaceAfter=3,
            textColor=colors.HexColor("#4a5568"),
        ),
        "body": ParagraphStyle(
            "Body",
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1a1a1a"),
        ),
        "bold_body": ParagraphStyle(
            "BoldBody",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=15,
            spaceAfter=4,
            textColor=colors.HexColor("#1a1a1a"),
        ),
        "blockquote": ParagraphStyle(
            "Blockquote",
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=14,
            spaceBefore=6,
            spaceAfter=6,
            leftIndent=24,
            rightIndent=12,
            textColor=colors.HexColor("#374151"),
            backColor=colors.HexColor("#f7f7f7"),
            borderPad=6,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="Courier",
            fontSize=8.5,
            leading=12,
            spaceBefore=4,
            spaceAfter=4,
            leftIndent=18,
            textColor=colors.HexColor("#1e3a5f"),
            backColor=colors.HexColor("#f0f4f8"),
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            spaceAfter=3,
            leftIndent=18,
            firstLineIndent=0,
            textColor=colors.HexColor("#1a1a1a"),
        ),
        "figprompt": ParagraphStyle(
            "FigPrompt",
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=13,
            spaceBefore=6,
            spaceAfter=6,
            leftIndent=18,
            rightIndent=12,
            textColor=colors.HexColor("#2d3748"),
            backColor=colors.HexColor("#eef2ff"),
            borderPad=5,
        ),
        "page_label": ParagraphStyle(
            "PageLabel",
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            spaceBefore=20,
            spaceAfter=8,
            textColor=colors.HexColor("#c05621"),
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=colors.white,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#1a1a1a"),
        ),
        "hr_label": ParagraphStyle(
            "HRLabel",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#9ca3af"),
            alignment=TA_CENTER,
        ),
    }
    return styles


# ─────────────────────────────────────────────
# Markdown → ReportLab flowable parser
# ─────────────────────────────────────────────

def escape_xml(text):
    """Escape characters that break ReportLab XML parser."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def inline_markup(text, styles):
    """Convert inline markdown (**bold**, *italic*, `code`) to ReportLab markup."""
    # Escape XML first
    text = escape_xml(text)
    # Bold-italic ***text***
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    # Bold **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic *text* or _text_
    text = re.sub(r'\*([^*\n]+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_([^_\n]+?)_', r'<i>\1</i>', text)
    # Inline code `text`
    text = re.sub(r'`([^`]+?)`', r'<font name="Courier" color="#1e3a5f">\1</font>', text)
    return text


def parse_table(lines, styles):
    """Parse a markdown table into a ReportLab Table."""
    rows = []
    for line in lines:
        if re.match(r'^\s*\|[-: |]+\|\s*$', line):
            continue  # separator row
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        rows.append(cells)

    if not rows:
        return []

    col_count = max(len(r) for r in rows)
    # Normalise row lengths
    rows = [r + [''] * (col_count - len(r)) for r in rows]

    table_data = []
    for i, row in enumerate(rows):
        if i == 0:
            table_data.append([
                Paragraph(inline_markup(cell, styles), styles["table_header"])
                for cell in row
            ])
        else:
            table_data.append([
                Paragraph(inline_markup(cell, styles), styles["table_cell"])
                for cell in row
            ])

    col_width = (6.5 * inch) / col_count
    tbl = Table(table_data, colWidths=[col_width] * col_count, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2d3748")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f7fafc")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#e2e8f0")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [Spacer(1, 6), tbl, Spacer(1, 8)]


def md_to_flowables(md_text, styles, is_authors_note=False):
    """
    Convert markdown text to a list of ReportLab flowables.
    Handles: headings (#/##/###), paragraphs, bold/italic/code inline,
    blockquotes (>), code blocks (```), bullet lists (- / *), tables, <hr> (---),
    figure prompt blocks, and page breaks for Author's Note pages.
    """
    flowables = []
    lines = md_text.split('\n')
    i = 0
    page_count = 0

    while i < len(lines):
        line = lines[i]

        # ── Page break detection for Author's Note (## Page N) ──────────────
        if is_authors_note and re.match(r'^## Page \d+', line):
            if page_count > 0:
                flowables.append(PageBreak())
            page_count += 1
            label = line.lstrip('#').strip()
            flowables.append(Paragraph(label, styles["page_label"]))
            flowables.append(HRFlowable(width="100%", thickness=1.2,
                                        color=colors.HexColor("#c05621"),
                                        spaceAfter=10))
            i += 1
            continue

        # ── Horizontal rule ─────────────────────────────────────────────────
        if re.match(r'^---+\s*$', line) or re.match(r'^\*\*\*+\s*$', line):
            flowables.append(Spacer(1, 4))
            flowables.append(HRFlowable(width="100%", thickness=0.5,
                                        color=colors.HexColor("#cbd5e0"),
                                        spaceBefore=4, spaceAfter=4))
            i += 1
            continue

        # ── H1 # ────────────────────────────────────────────────────────────
        if line.startswith('# ') and not line.startswith('## '):
            text = inline_markup(line[2:].strip(), styles)
            flowables.append(Paragraph(text, styles["title"]))
            flowables.append(HRFlowable(width="100%", thickness=1.5,
                                        color=colors.HexColor("#1a1a2e"),
                                        spaceAfter=8))
            i += 1
            continue

        # ── H2 ## ───────────────────────────────────────────────────────────
        if line.startswith('## '):
            text = inline_markup(line[3:].strip(), styles)
            flowables.append(Paragraph(text, styles["h1"]))
            i += 1
            continue

        # ── H3 ### ──────────────────────────────────────────────────────────
        if line.startswith('### '):
            text = inline_markup(line[4:].strip(), styles)
            flowables.append(Paragraph(text, styles["h2"]))
            i += 1
            continue

        # ── H4 #### ─────────────────────────────────────────────────────────
        if line.startswith('#### '):
            text = inline_markup(line[5:].strip(), styles)
            flowables.append(Paragraph(text, styles["h3"]))
            i += 1
            continue

        # ── Figure Architect prompt block (> **[FIGURE) ─────────────────────
        if line.startswith('> **[FIGURE'):
            block_lines = []
            while i < len(lines) and lines[i].startswith('>'):
                block_lines.append(lines[i][1:].strip())
                i += 1
            text = ' '.join(block_lines)
            text = inline_markup(text, styles)
            flowables.append(Paragraph(text, styles["figprompt"]))
            continue

        # ── Blockquote > ────────────────────────────────────────────────────
        if line.startswith('>'):
            block_lines = []
            while i < len(lines) and lines[i].startswith('>'):
                block_lines.append(lines[i][1:].strip())
                i += 1
            text = ' '.join(block_lines)
            text = inline_markup(text, styles)
            flowables.append(Paragraph(text, styles["blockquote"]))
            continue

        # ── Code block ``` ───────────────────────────────────────────────────
        if line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing ```
            code_text = '\n'.join(code_lines)
            # Truncate very long code blocks for PDF readability
            if len(code_lines) > 30:
                code_text = '\n'.join(code_lines[:30]) + '\n... [see notebook for full code]'
            flowables.append(Preformatted(code_text, styles["code"]))
            flowables.append(Spacer(1, 4))
            continue

        # ── Table ────────────────────────────────────────────────────────────
        if line.startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].startswith('|'):
                table_lines.append(lines[i])
                i += 1
            flowables.extend(parse_table(table_lines, styles))
            continue

        # ── Bullet list - or * ───────────────────────────────────────────────
        if re.match(r'^(\s*[-*+])\s+', line):
            while i < len(lines) and re.match(r'^(\s*[-*+])\s+', lines[i]):
                content = re.sub(r'^(\s*[-*+])\s+', '', lines[i])
                content = inline_markup(content, styles)
                flowables.append(Paragraph(f"\u2022\u00a0\u00a0{content}", styles["bullet"]))
                i += 1
            flowables.append(Spacer(1, 4))
            continue

        # ── Numbered list ────────────────────────────────────────────────────
        if re.match(r'^\d+\.\s+', line):
            while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                num_match = re.match(r'^(\d+)\.\s+(.+)', lines[i])
                if num_match:
                    num, content = num_match.group(1), num_match.group(2)
                    content = inline_markup(content, styles)
                    flowables.append(
                        Paragraph(f"<b>{num}.</b>\u00a0\u00a0{content}", styles["bullet"])
                    )
                i += 1
            flowables.append(Spacer(1, 4))
            continue

        # ── Blank line ───────────────────────────────────────────────────────
        if line.strip() == '':
            flowables.append(Spacer(1, 4))
            i += 1
            continue

        # ── Plain paragraph ──────────────────────────────────────────────────
        # Accumulate continuation lines
        para_lines = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if (next_line.strip() == '' or
                    next_line.startswith('#') or
                    next_line.startswith('>') or
                    next_line.startswith('|') or
                    next_line.strip().startswith('```') or
                    re.match(r'^(\s*[-*+])\s+', next_line) or
                    re.match(r'^\d+\.\s+', next_line) or
                    re.match(r'^---+\s*$', next_line)):
                break
            para_lines.append(next_line)
            i += 1

        text = ' '.join(para_lines)
        text = inline_markup(text, styles)

        # Detect metadata lines (bold-only short lines at the top)
        if re.match(r'^<b>.{3,60}</b>$', text.strip()):
            flowables.append(Paragraph(text, styles["subtitle"]))
        else:
            flowables.append(Paragraph(text, styles["body"]))

    return flowables


# ─────────────────────────────────────────────
# Page number footer
# ─────────────────────────────────────────────

def make_footer(title):
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#9ca3af"))
        canvas.drawString(inch, 0.65 * inch, title)
        canvas.drawRightString(
            letter[0] - inch, 0.65 * inch,
            f"Page {doc.page}"
        )
        canvas.setStrokeColor(colors.HexColor("#e2e8f0"))
        canvas.setLineWidth(0.5)
        canvas.line(inch, 0.75 * inch, letter[0] - inch, 0.75 * inch)
        canvas.restoreState()
    return footer


# ─────────────────────────────────────────────
# Build PDFs
# ─────────────────────────────────────────────

def build_pdf(md_path, pdf_path, doc_title, is_authors_note=False):
    styles = build_styles()

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        title=doc_title,
        author="Yeshwanth Balaji",
        subject="CSYE 7270 Midterm",
    )

    flowables = md_to_flowables(md_text, styles, is_authors_note=is_authors_note)
    doc.build(flowables, onFirstPage=make_footer(doc_title),
              onLaterPages=make_footer(doc_title))
    print(f"  Generated: {pdf_path}")


if __name__ == "__main__":
    print("Generating PDFs for CSYE 7270 Midterm...\n")

    build_pdf(
        md_path=os.path.join(BASE_DIR, "essay.md"),
        pdf_path=os.path.join(BASE_DIR, "essay.pdf"),
        doc_title="The Wrong Layer — CSYE 7270 Midterm Essay",
        is_authors_note=False,
    )

    build_pdf(
        md_path=os.path.join(BASE_DIR, "authors_note.md"),
        pdf_path=os.path.join(BASE_DIR, "authors_note.pdf"),
        doc_title="Author's Note — CSYE 7270 Midterm",
        is_authors_note=True,
    )

    print("\nDone. Both PDFs are in csye7270-midterm/")
