from __future__ import annotations

import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.platypus import (
        Flowable,
        HRFlowable,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )
except ModuleNotFoundError as exc:
    if exc.name == "reportlab":
        raise SystemExit(
            "Missing dependency: reportlab. Use the Codex bundled Python runtime for document/PDF work, "
            "or install reportlab in the Python environment that runs this script."
        ) from exc
    raise


INK = colors.HexColor("#101936")
PRIMARY = colors.HexColor("#1677FF")
PRIMARY_DARK = colors.HexColor("#174EA6")
PURPLE = colors.HexColor("#635BFF")
CYAN = colors.HexColor("#14B8A6")
STEEL = colors.HexColor("#64748B")
MUTED = colors.HexColor("#8EA2C0")
PAGE_BG = colors.HexColor("#F6FAFF")
CARD_BG = colors.HexColor("#FFFFFF")
SOFT_BLUE = colors.HexColor("#F1F7FF")
SOFT_PURPLE = colors.HexColor("#F4F2FF")
SOFT_CYAN = colors.HexColor("#ECFEFF")
LINE = colors.HexColor("#DDE8F7")
WARNING = colors.HexColor("#F59E0B")
WARNING_SOFT = colors.HexColor("#FFF7E6")
SUCCESS = colors.HexColor("#10B981")
SUCCESS_SOFT = colors.HexColor("#ECFDF5")
WHITE = colors.white

PAGE_WIDTH, PAGE_HEIGHT = A4
INTERNAL_MARKDOWN = {
    "plan.md",
    "case.md",
    "skill_outputs.md",
    "case_dashboard.md",
    "consultation_note.md",
    "case_package.md",
    "pleading_framework.md",
    "hearing_playbook.md",
    "review_delta.md",
    "timeline.md",
    "evidence.md",
    "sources.md",
    "analysis.md",
    "advice.md",
    "drafts.md",
    "hearing.md",
    "negotiation.md",
    "contract.md",
    "clause_review.md",
    "term_sheet.md",
    "contract_draft.md",
}
REPORT_PATTERNS = (
    "*专业报告.md",
    "*法律研究报告.md",
    "*合同审查专业报告.md",
    "*合同草案.md",
    "*Professional Report.md",
    "*Report.md",
)


def register_fonts() -> str:
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    return "STSong-Light"


FONT = register_fonts()


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CNBody",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=9.8,
            leading=15.2,
            textColor=INK,
            wordWrap="CJK",
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverKicker",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=8.6,
            leading=12,
            textColor=PRIMARY,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName=FONT,
            fontSize=27,
            leading=34,
            alignment=TA_LEFT,
            textColor=INK,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=11.5,
            leading=18,
            textColor=PRIMARY,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMetaLabel",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=7.2,
            leading=10,
            textColor=STEEL,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverMetaValue",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=8.8,
            leading=13,
            textColor=INK,
            wordWrap="CJK",
        )
    )
    styles.add(
        ParagraphStyle(
            name="SideMark",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=20,
            leading=30,
            alignment=TA_CENTER,
            textColor=WHITE,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SideText",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=8.3,
            leading=14,
            alignment=TA_CENTER,
            textColor=PRIMARY_DARK,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNTitle",
            parent=styles["Title"],
            fontName=FONT,
            fontSize=20,
            leading=26,
            alignment=TA_LEFT,
            textColor=INK,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNH2",
            parent=styles["Heading2"],
            fontName=FONT,
            fontSize=12.2,
            leading=20,
            textColor=INK,
            spaceBefore=12,
            spaceAfter=7,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNH3",
            parent=styles["Heading3"],
            fontName=FONT,
            fontSize=10.6,
            leading=16,
            textColor=PRIMARY_DARK,
            spaceBefore=9,
            spaceAfter=5,
            keepWithNext=True,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNQuote",
            parent=styles["CNBody"],
            fontName=FONT,
            fontSize=9.5,
            leading=14.6,
            leftIndent=8,
            rightIndent=8,
            borderColor=WARNING,
            borderWidth=0.8,
            borderPadding=7,
            backColor=colors.HexColor("#FFFFFF"),
            textColor=INK,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNTable",
            parent=styles["CNBody"],
            fontName=FONT,
            fontSize=7.1,
            leading=9.7,
            wordWrap="CJK",
            alignment=TA_LEFT,
            textColor=INK,
        )
    )
    styles.add(ParagraphStyle(name="CNTableSmall", parent=styles["CNTable"], fontSize=6.65, leading=8.8))
    styles.add(
        ParagraphStyle(
            name="CNTableHeader",
            parent=styles["CNTable"],
            fontName=FONT,
            fontSize=7.1,
            leading=9.2,
            alignment=TA_CENTER,
            textColor=PRIMARY_DARK,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CNBullet",
            parent=styles["CNBody"],
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BadgeText",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=7.6,
            leading=10,
            alignment=TA_CENTER,
            textColor=WHITE,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardTitle",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=10.5,
            leading=14,
            textColor=INK,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CardNote",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=7.8,
            leading=11,
            textColor=STEEL,
        )
    )
    styles.add(
        ParagraphStyle(
            name="MetricValue",
            parent=styles["Normal"],
            fontName=FONT,
            fontSize=13.5,
            leading=17,
            textColor=PRIMARY,
            alignment=TA_CENTER,
        )
    )
    return styles


STYLES = build_styles()


def clean_inline(text: str) -> str:
    text = escape(text.strip())
    text = re.sub(r"`([^`]+)`", r"<font name='STSong-Light'>\1</font>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    return text


def para(text: str, style_name: str) -> Paragraph:
    return Paragraph(clean_inline(text), STYLES[style_name])


def card_table(content, col_widths, style_commands=None):
    table = Table(content, colWidths=col_widths)
    base_style = [
        ("BOX", (0, 0), (-1, -1), 0.65, LINE),
        ("BACKGROUND", (0, 0), (-1, -1), CARD_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]
    if style_commands:
        base_style.extend(style_commands)
    table.setStyle(TableStyle(base_style))
    return table


def badge(text: str, color=PRIMARY):
    table = Table([[para(text, "BadgeText")]], colWidths=[20 * mm], rowHeights=[8 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), color),
                ("BOX", (0, 0), (-1, -1), 0.1, color),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return table


class CoverVisual(Flowable):
    def __init__(self, width: float, height: float):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, avail_width, avail_height):
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        width = self.width
        height = self.height
        canvas.saveState()
        canvas.setFillColor(PRIMARY)
        canvas.roundRect(0, 0, width, height, 7, stroke=0, fill=1)

        canvas.setFillColor(PURPLE)
        canvas.roundRect(width * 0.08, height * 0.11, width * 0.84, height * 0.26, 5, stroke=0, fill=1)
        canvas.setFillColor(colors.HexColor("#2D8CFF"))
        canvas.roundRect(width * 0.16, height * 0.41, width * 0.68, height * 0.12, 4, stroke=0, fill=1)
        canvas.setFillColor(CYAN)
        canvas.rect(0, height * 0.55, width, 1.7, stroke=0, fill=1)

        canvas.setStrokeColor(colors.HexColor("#9CC8FF"))
        canvas.setLineWidth(0.45)
        for offset in (0.18, 0.30, 0.42):
            canvas.line(width * offset, height * 0.08, width * (offset + 0.24), height * 0.94)

        canvas.setFillColor(WHITE)
        canvas.setFont(FONT, 18)
        canvas.drawCentredString(width / 2, height * 0.78, "LEGAL")
        canvas.drawCentredString(width / 2, height * 0.67, "REPORT")
        canvas.setFont(FONT, 7.8)
        canvas.drawCentredString(width / 2, height * 0.47, "DATA  /  ISSUES  /  EVIDENCE")
        canvas.drawCentredString(width / 2, height * 0.30, "ACTIONS  /  REVIEW")

        canvas.setFillColor(colors.HexColor("#EAF4FF"))
        for index, label in enumerate(("01", "02", "03")):
            x = width * (0.22 + index * 0.28)
            y = height * 0.16
            canvas.roundRect(x - 8, y - 4, 16, 8, 3, stroke=0, fill=1)
            canvas.setFillColor(PRIMARY_DARK)
            canvas.setFont(FONT, 5.6)
            canvas.drawCentredString(x, y - 1.8, label)
            canvas.setFillColor(colors.HexColor("#EAF4FF"))
        canvas.restoreState()


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def extract_report_parts(markdown: str) -> tuple[str, dict[str, str], str]:
    lines = markdown.splitlines()
    title = "法律事务专业报告"
    meta: dict[str, str] = {}
    idx = 0

    if lines and lines[0].startswith("# "):
        title = lines[0][2:].strip()
        idx = 1

    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    while idx < len(lines) and lines[idx].startswith(">"):
        item = lines[idx].lstrip("> ").strip()
        if "：" in item:
            key, value = item.split("：", 1)
            meta[key.strip()] = value.strip()
        idx += 1

    while idx < len(lines) and not lines[idx].strip():
        idx += 1

    return title, meta, "\n".join(lines[idx:])


def strip_markdown_toc(markdown: str) -> str:
    lines = markdown.splitlines()
    if not lines:
        return markdown
    output: list[str] = []
    idx = 0
    while idx < len(lines):
        if lines[idx].strip() == "## 目录":
            idx += 1
            while idx < len(lines) and not lines[idx].startswith("## "):
                idx += 1
            continue
        output.append(lines[idx])
        idx += 1
    return "\n".join(output)


def extract_headings(markdown: str) -> list[str]:
    headings: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("## ") and line.strip() != "## 目录":
            headings.append(line[3:].strip())
    return headings


def find_report_markdown(directory: Path, explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit)
        if not path.is_absolute():
            path = directory / path
        if not path.exists():
            raise FileNotFoundError(f"Report markdown not found: {path}")
        return path

    for pattern in REPORT_PATTERNS:
        matches = sorted(path for path in directory.glob(pattern) if path.name not in INTERNAL_MARKDOWN)
        if matches:
            return matches[0]

    fallback = sorted(
        path
        for path in directory.glob("*.md")
        if path.name not in INTERNAL_MARKDOWN and any(token in path.stem.lower() for token in ("报告", "report", "草案"))
    )
    if fallback:
        return fallback[0]

    raise FileNotFoundError(
        f"No professional report markdown found in {directory}. "
        "Pass --report <filename.md> if the report uses a custom name."
    )


def build_cover(title: str, meta: dict[str, str], directory: Path, usable_width: float, usable_height: float) -> list:
    report_id = meta.get("报告编号", "LA-2026-REPORT")
    meta_items = [
        ("案件编号", report_id),
        ("事项类型", meta.get("事项类型", "法律事务分析")),
        ("报告日期", meta.get("生成日期", "未标注")),
        ("报告状态", meta.get("报告状态", "draft")),
        ("PDF 状态", meta.get("PDF 状态", "ready")),
        ("版本", meta.get("版本", "V1.0")),
    ]
    meta_rows = [[para(label, "CoverMetaLabel"), para(value, "CoverMetaValue")] for label, value in meta_items]
    meta_table = Table(meta_rows, colWidths=[24 * mm, 72 * mm])
    meta_table.setStyle(
        TableStyle(
            [
                ("LINEBELOW", (0, 0), (-1, -1), 0.35, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    note = meta.get("重要提示", "本报告为法律信息整理和分析辅助，不替代律师意见。")
    note_box = card_table(
        [[para("交付说明 / DELIVERY NOTE", "CoverMetaLabel")], [para(note, "CoverMetaValue")]],
        [usable_width * 0.56],
        [("BACKGROUND", (0, 0), (-1, -1), SOFT_BLUE), ("BOX", (0, 0), (-1, -1), 0.65, colors.HexColor("#BFD7FF"))],
    )

    brand = Table(
        [[badge("LA", PRIMARY), [para("Legal Assistant Agent", "CoverKicker"), para("法律助手", "CoverMetaLabel")]]],
        colWidths=[24 * mm, 55 * mm],
    )
    brand.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    left = [
        brand,
        Spacer(1, 22),
        para(title, "CoverTitle"),
        para("LEGAL ANALYSIS REPORT", "CoverSubtitle"),
        para("专业分析 / 深度论证 / 风险评估 / 行动建议", "CoverMetaLabel"),
        Spacer(1, 18),
        meta_table,
        Spacer(1, 14),
        note_box,
        Spacer(1, 16),
        para("以事实为依据，以法律为准绳", "CoverMetaLabel"),
    ]

    right_inner_width = usable_width * 0.34
    visual_panel = CoverVisual(right_inner_width, 112 * mm)

    feature_cards = Table(
        [
            [
                card_table([[para("专业可信", "CardTitle")], [para("严谨专业的法律表达", "CardNote")]], [right_inner_width * 0.47]),
                card_table([[para("清晰高效", "CardTitle")], [para("信息层级清晰易读", "CardNote")]], [right_inner_width * 0.47]),
            ],
            [
                card_table([[para("数据驱动", "CardTitle")], [para("可视化呈现关键洞察", "CardNote")]], [right_inner_width * 0.47]),
                card_table([[para("一致规范", "CardTitle")], [para("统一风格与组件体系", "CardNote")]], [right_inner_width * 0.47]),
            ],
        ],
        colWidths=[right_inner_width * 0.50, right_inner_width * 0.50],
    )
    feature_cards.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )

    right = [visual_panel, Spacer(1, 12), feature_cards]
    cover = Table([[left, right]], colWidths=[usable_width * 0.58, usable_width * 0.42], rowHeights=[usable_height - 18])
    cover.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (0, 0), 14 * mm),
                ("RIGHTPADDING", (0, 0), (0, 0), 8 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 16 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12 * mm),
                ("LEFTPADDING", (1, 0), (1, 0), 6 * mm),
                ("RIGHTPADDING", (1, 0), (1, 0), 10 * mm),
            ]
        )
    )
    return [cover, PageBreak()]


def build_contents_page(headings: list[str], title: str, usable_width: float) -> list:
    if not headings:
        return []
    rows = []
    palette = [PRIMARY, PURPLE, CYAN, PRIMARY_DARK]
    for index, heading in enumerate(headings[:12], start=1):
        number = f"{index:02d}"
        rows.append(
            [
                badge(number, palette[(index - 1) % len(palette)]),
                [para(heading, "CardTitle"), para("章节内容与关键判断", "CardNote")],
                para(f"{index * 2 + 1:02d}", "CardNote"),
            ]
        )
    contents = Table(rows, colWidths=[23 * mm, usable_width - 42 * mm, 16 * mm])
    contents.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.65, LINE),
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("LINEBELOW", (0, 0), (-1, -2), 0.35, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    brand_mark = Table([[para("§", "MetricValue")]], colWidths=[36 * mm], rowHeights=[36 * mm])
    brand_mark.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT_PURPLE),
                ("BOX", (0, 0), (-1, -1), 0.65, colors.HexColor("#D8D5FF")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    layout = Table(
        [
            [para("目录", "CoverTitle"), para("CONTENTS", "CoverKicker")],
            [contents, brand_mark],
        ],
        colWidths=[usable_width - 45 * mm, 42 * mm],
    )
    layout.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.65, LINE),
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("LINEBELOW", (0, 0), (-1, 0), 0.65, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return [layout, PageBreak()]


def build_section_heading(text: str, usable_width: float, section_index: int) -> Table:
    color = [PRIMARY, PURPLE, CYAN, PRIMARY_DARK][(section_index - 1) % 4]
    heading = Table(
        [[badge(f"{section_index:02d}", color), Paragraph(clean_inline(text), STYLES["CNH2"])]],
        colWidths=[23 * mm, usable_width - 23 * mm],
    )
    heading.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.65, LINE),
                ("BACKGROUND", (0, 0), (-1, -1), WHITE),
                ("LINEBELOW", (0, 0), (-1, -1), 1.0, colors.HexColor("#E8F1FF")),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return heading


def build_table(rows: list[str], usable_width: float) -> list:
    parsed = [split_table_row(row) for row in rows if not is_table_separator(row)]
    if not parsed:
        return []
    col_count = max(len(row) for row in parsed)
    normalized = [row + [""] * (col_count - len(row)) for row in parsed]
    cell_style = "CNTableSmall" if col_count >= 7 else "CNTable"
    data = []
    for row_index, row in enumerate(normalized):
        style_name = "CNTableHeader" if row_index == 0 else cell_style
        data.append([Paragraph(clean_inline(cell), STYLES[style_name]) for cell in row])

    table = Table(data, colWidths=[usable_width / col_count] * col_count, repeatRows=1, splitByRow=True)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), FONT),
                ("BACKGROUND", (0, 0), (-1, 0), SOFT_BLUE),
                ("LINEABOVE", (0, 0), (-1, 0), 1.3, PRIMARY),
                ("LINEBELOW", (0, 0), (-1, 0), 0.65, colors.HexColor("#BFD7FF")),
                ("BACKGROUND", (0, 1), (-1, -1), WHITE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, colors.HexColor("#F8FBFF")]),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4.2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4.2),
                ("TOPPADDING", (0, 0), (-1, -1), 4.6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4.6),
            ]
        )
    )
    return [table, Spacer(1, 8)]


def flush_paragraph(buffer: list[str], story: list) -> None:
    if not buffer:
        return
    text = " ".join(part.strip() for part in buffer if part.strip())
    if text:
        story.append(Paragraph(clean_inline(text), STYLES["CNBody"]))
    buffer.clear()


def parse_markdown(markdown: str, usable_width: float) -> list:
    story: list = []
    lines = markdown.splitlines()
    paragraph: list[str] = []
    table_rows: list[str] = []
    in_code_block = False
    code_buffer: list[str] = []
    section_index = 0

    def flush_table() -> None:
        nonlocal table_rows
        if table_rows:
            story.extend(build_table(table_rows, usable_width))
            table_rows = []

    for raw in lines:
        line = raw.rstrip()

        if line.startswith("```"):
            flush_paragraph(paragraph, story)
            flush_table()
            if in_code_block:
                if code_buffer:
                    story.append(Paragraph(clean_inline(" / ".join(code_buffer)), STYLES["CNQuote"]))
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        if line.startswith("|") and line.endswith("|"):
            flush_paragraph(paragraph, story)
            table_rows.append(line)
            continue

        flush_table()
        if not line.strip():
            flush_paragraph(paragraph, story)
            story.append(Spacer(1, 3))
            continue
        if line.startswith("# "):
            flush_paragraph(paragraph, story)
            story.append(Paragraph(clean_inline(line[2:]), STYLES["CNTitle"]))
            continue
        if line.startswith("## "):
            flush_paragraph(paragraph, story)
            section_index += 1
            story.append(build_section_heading(line[3:], usable_width, section_index))
            continue
        if line.startswith("### "):
            flush_paragraph(paragraph, story)
            story.append(Paragraph(clean_inline(line[4:]), STYLES["CNH3"]))
            continue
        if line.strip() in {"---", "***", "___"}:
            flush_paragraph(paragraph, story)
            story.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=8, spaceAfter=8))
            continue
        if line.startswith(">"):
            flush_paragraph(paragraph, story)
            quote = line.lstrip("> ").strip()
            if quote:
                story.append(Paragraph(clean_inline(quote), STYLES["CNQuote"]))
            continue
        if re.match(r"^\s*[-*]\s+", line):
            flush_paragraph(paragraph, story)
            item = re.sub(r"^\s*[-*]\s+", "• ", line)
            story.append(Paragraph(clean_inline(item), STYLES["CNBullet"]))
            continue
        if re.match(r"^\s*\d+\.\s+", line):
            flush_paragraph(paragraph, story)
            story.append(Paragraph(clean_inline(line), STYLES["CNBullet"]))
            continue
        paragraph.append(line)

    flush_paragraph(paragraph, story)
    flush_table()
    return story


def add_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.45)
        canvas.line(16 * mm, PAGE_HEIGHT - 13 * mm, PAGE_WIDTH - 16 * mm, PAGE_HEIGHT - 13 * mm)
        canvas.setFont(FONT, 8)
        canvas.setFillColor(PRIMARY_DARK)
        canvas.drawString(16 * mm, PAGE_HEIGHT - 10 * mm, "法律分析报告  LEGAL ANALYSIS REPORT")
        canvas.setFillColor(STEEL)
        canvas.drawRightString(PAGE_WIDTH - 16 * mm, PAGE_HEIGHT - 10 * mm, f"LA-REPORT-{doc.page:02d}")
        canvas.line(16 * mm, 13 * mm, PAGE_WIDTH - 16 * mm, 13 * mm)
        canvas.setFillColor(STEEL)
        canvas.drawString(16 * mm, 9 * mm, "Legal Assistant Agent / Professional Deliverable")
        canvas.drawRightString(PAGE_WIDTH - 16 * mm, 9 * mm, str(doc.page))
    canvas.restoreState()


def render_pdf(target: Path, report_name: str | None = None, output: str | None = None) -> Path:
    target = target.resolve()
    if target.is_file():
        if report_name:
            raise ValueError("--report is only valid when the target is a directory.")
        directory = target.parent
        md_path = target
    elif target.is_dir():
        directory = target
        md_path = find_report_markdown(directory, report_name)
    else:
        raise FileNotFoundError(f"Input path not found: {target}")

    pdf_path = Path(output) if output else md_path.with_suffix(".pdf")
    if not pdf_path.is_absolute():
        pdf_path = directory / pdf_path

    markdown = md_path.read_text(encoding="utf-8")
    title, meta, body = extract_report_parts(markdown)
    body = strip_markdown_toc(body)
    headings = extract_headings(body)
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title=title,
        author="Legal-Assistant_agent",
    )
    story = []
    story.extend(build_cover(title, meta, directory, doc.width, doc.height))
    story.extend(build_contents_page(headings, title, doc.width))
    story.extend(parse_markdown(body, doc.width))
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    return pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Render a professional report Markdown to a styled PDF. "
            "Pass either a matter directory or a report .md file. "
            "By default, the input directory is also the output directory."
        )
    )
    parser.add_argument("target", nargs="?", default=".", help="Matter folder or report Markdown file.")
    parser.add_argument("--report", help="Report Markdown filename or path. Auto-detected when omitted.")
    parser.add_argument("--output", help="Output PDF filename or path. Defaults to report basename with .pdf.")
    args = parser.parse_args()

    pdf_path = render_pdf(Path(args.target), report_name=args.report, output=args.output)
    print(pdf_path)


if __name__ == "__main__":
    main()
