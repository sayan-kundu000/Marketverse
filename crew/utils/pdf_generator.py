"""Programmatic PDF Report Generator for Marketverse.

Compiles publication-grade A4 PDF market reports using ReportLab.
Features:
- Professional header banner with document metadata
- Styled sections containing the writer's report copy
- Tabular grids rendering Pandas summary statistics and corporate metrics
- Two-pass NumberedCanvas for dynamic 'Page X of Y' numbering and running footers
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)

from crew.tools.financial_tool import (
    load_and_preprocess_dataframe,
    get_financial_summary_stats,
    DEFAULT_CSV_PATH
)

# Color Palette
COLOR_PRIMARY = colors.HexColor("#0F172A")    # Deep Navy Slate
COLOR_SECONDARY = colors.HexColor("#1E3A8A")  # Royal Navy
COLOR_ACCENT = colors.HexColor("#2563EB")     # Bright Blue
COLOR_CYAN = colors.HexColor("#0284C7")       # Cyan / Teal Accent
COLOR_TEXT = colors.HexColor("#1E293B")       # Dark Charcoal Text
COLOR_MUTED = colors.HexColor("#64748B")      # Muted Gray
COLOR_BG_LIGHT = colors.HexColor("#F8FAFC")   # Light background
COLOR_BORDER = colors.HexColor("#E2E8F0")     # Light border


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw total page count ('Page X of Y') and footers."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)

        page_w, page_h = A4
        margin_x = 40
        footer_y = 28
        header_y = page_h - 30

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(margin_x, header_y, "MARKETVERSE RESEARCH | MULTI-AGENT MARKET INTELLIGENCE REPORT")
            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.5)
            self.line(margin_x, header_y - 6, page_w - margin_x, header_y - 6)

        # Running Footer (all pages)
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.5)
        self.line(margin_x, footer_y + 12, page_w - margin_x, footer_y + 12)

        # Footer Left: Attribution & Confidentiality
        footer_left = "Confidential - Marketverse Multi-Agent Report | Powered by CrewAI & Pandas"
        self.drawString(margin_x, footer_y, footer_left)

        # Footer Right: Page X of Y
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(page_w - margin_x, footer_y, page_str)

        self.restoreState()


class MarketversePDFGenerator:
    """Compiles styled executive A4 PDF reports with ReportLab."""

    def __init__(self, output_path: str = "output/market_report.pdf"):
        self.output_path = Path(output_path).resolve()
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.styles = self._init_styles()

    def _init_styles(self) -> Dict[str, ParagraphStyle]:
        """Initialize comprehensive typographic hierarchy."""
        base = getSampleStyleSheet()

        styles = {
            "BannerTitle": ParagraphStyle(
                "BannerTitle",
                parent=base["Normal"],
                fontName="Helvetica-Bold",
                fontSize=22,
                leading=26,
                textColor=colors.white,
                spaceAfter=6,
            ),
            "BannerSubtitle": ParagraphStyle(
                "BannerSubtitle",
                parent=base["Normal"],
                fontName="Helvetica",
                fontSize=12,
                leading=16,
                textColor=colors.HexColor("#93C5FD"),
                spaceAfter=12,
            ),
            "BannerMeta": ParagraphStyle(
                "BannerMeta",
                parent=base["Normal"],
                fontName="Helvetica",
                fontSize=9,
                leading=13,
                textColor=colors.HexColor("#E2E8F0"),
            ),
            "Heading1": ParagraphStyle(
                "CustomH1",
                parent=base["Normal"],
                fontName="Helvetica-Bold",
                fontSize=14,
                leading=18,
                textColor=COLOR_PRIMARY,
                spaceBefore=14,
                spaceAfter=8,
                keepWithNext=True,
            ),
            "Heading2": ParagraphStyle(
                "CustomH2",
                parent=base["Normal"],
                fontName="Helvetica-Bold",
                fontSize=11,
                leading=15,
                textColor=COLOR_SECONDARY,
                spaceBefore=10,
                spaceAfter=4,
                keepWithNext=True,
            ),
            "Heading3": ParagraphStyle(
                "CustomH3",
                parent=base["Normal"],
                fontName="Helvetica-Bold",
                fontSize=10,
                leading=13,
                textColor=COLOR_CYAN,
                spaceBefore=6,
                spaceAfter=3,
                keepWithNext=True,
            ),
            "Body": ParagraphStyle(
                "CustomBody",
                parent=base["Normal"],
                fontName="Helvetica",
                fontSize=9.5,
                leading=13.5,
                textColor=COLOR_TEXT,
                spaceAfter=6,
            ),
            "Bullet": ParagraphStyle(
                "CustomBullet",
                parent=base["Normal"],
                fontName="Helvetica",
                fontSize=9,
                leading=13,
                textColor=COLOR_TEXT,
                leftIndent=15,
                firstLineIndent=-10,
                spaceAfter=4,
            ),
            "TableHead": ParagraphStyle(
                "TableHead",
                parent=base["Normal"],
                fontName="Helvetica-Bold",
                fontSize=8,
                leading=10,
                textColor=colors.white,
                alignment=1,  # Center
            ),
            "TableCell": ParagraphStyle(
                "TableCell",
                parent=base["Normal"],
                fontName="Helvetica",
                fontSize=8,
                leading=10,
                textColor=COLOR_TEXT,
                alignment=0,  # Left
            ),
            "TableCellNumeric": ParagraphStyle(
                "TableCellNumeric",
                parent=base["Normal"],
                fontName="Helvetica",
                fontSize=8,
                leading=10,
                textColor=COLOR_TEXT,
                alignment=2,  # Right
            ),
            "Callout": ParagraphStyle(
                "Callout",
                parent=base["Normal"],
                fontName="Helvetica-Oblique",
                fontSize=9,
                leading=13,
                textColor=COLOR_SECONDARY,
                backColor=COLOR_BG_LIGHT,
                borderColor=COLOR_ACCENT,
                borderWidth=1,
                borderPadding=6,
                spaceBefore=6,
                spaceAfter=8,
            )
        }
        return styles

    def build_header_banner(self, query: str, date_str: str) -> Table:
        """Construct the full-width corporate header banner."""
        content = [
            Paragraph("MARKET RESEARCH & FINANCIAL BENCHMARK REPORT", self.styles["BannerTitle"]),
            Paragraph(f"Executive Strategic Dossier: {query}", self.styles["BannerSubtitle"]),
            Paragraph(
                f"<b>System</b>: Marketverse Multi-Agent Platform &nbsp;|&nbsp; "
                f"<b>Process</b>: CrewAI Hierarchical &nbsp;|&nbsp; "
                f"<b>Generated</b>: {date_str} &nbsp;|&nbsp; "
                f"<b>Status</b>: Verified",
                self.styles["BannerMeta"]
            )
        ]

        banner_table = Table([[content]], colWidths=[515])
        banner_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOR_PRIMARY),
            ("PADDING", (0, 0), (-1, -1), 16),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
            ("LINEBELOW", (0, 0), (-1, -1), 3, COLOR_ACCENT),
        ]))
        return banner_table

    def build_pandas_summary_table(self, csv_path: Optional[str] = None) -> Table:
        """Render Pandas summary statistics (mean, std, min, max, percentiles) as a styled Table."""
        df = load_and_preprocess_dataframe(csv_path)
        summary_df = get_financial_summary_stats(df).reset_index()
        summary_df.rename(columns={"index": "Metric"}, inplace=True)

        # Simplify column headers for compact layout
        col_names = {
            "Metric": "Stat",
            "Revenue_Billions": "Rev ($B)",
            "YoY_Growth_Pct": "Growth %",
            "Operating_Margin_Pct": "Op Margin %",
            "Net_Income_Billions": "Net Inc ($B)",
            "Free_Cash_Flow_Billions": "FCF ($B)",
            "PE_Ratio": "P/E",
            "Market_Cap_Billions": "Mkt Cap ($B)"
        }
        summary_df.rename(columns=col_names, inplace=True)

        headers = list(summary_df.columns)
        table_data = [[Paragraph(f"<b>{h}</b>", self.styles["TableHead"]) for h in headers]]

        for _, row in summary_df.iterrows():
            row_cells = []
            for i, val in enumerate(row):
                if i == 0:
                    row_cells.append(Paragraph(f"<b>{str(val).capitalize()}</b>", self.styles["TableCell"]))
                else:
                    formatted_val = f"{val:,.2f}" if isinstance(val, (int, float)) else str(val)
                    row_cells.append(Paragraph(formatted_val, self.styles["TableCellNumeric"]))
            table_data.append(row_cells)

        col_widths = [65, 60, 65, 75, 70, 65, 45, 70]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_SECONDARY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_BG_LIGHT, colors.white]),
        ]))
        return table

    def build_corporate_peers_table(self, csv_path: Optional[str] = None) -> Table:
        """Render individual corporate peer metrics as a clean data grid."""
        df = load_and_preprocess_dataframe(csv_path)
        
        display_cols = [
            ("Company", "Company", 115),
            ("Ticker", "Ticker", 45),
            ("Revenue_Billions", "Rev ($B)", 55),
            ("YoY_Growth_Pct", "YoY %", 55),
            ("Operating_Margin_Pct", "Margin %", 55),
            ("Net_Income_Billions", "Net Inc ($B)", 60),
            ("PE_Ratio", "P/E", 45),
            ("Market_Cap_Billions", "Mkt Cap ($B)", 75),
        ]

        headers = [Paragraph(f"<b>{title}</b>", self.styles["TableHead"]) for _, title, _ in display_cols]
        widths = [width for _, _, width in display_cols]
        table_data = [headers]

        for _, row in df.iterrows():
            row_cells = []
            for col_id, _, _ in display_cols:
                val = row.get(col_id, "")
                if col_id in ("Company", "Ticker"):
                    row_cells.append(Paragraph(str(val), self.styles["TableCell"]))
                else:
                    formatted_val = f"{val:,.2f}" if isinstance(val, (int, float)) else str(val)
                    row_cells.append(Paragraph(formatted_val, self.styles["TableCellNumeric"]))
            table_data.append(row_cells)

        table = Table(table_data, colWidths=widths, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_PRIMARY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, COLOR_BG_LIGHT]),
        ]))
        return table

    def generate_pdf(
        self,
        markdown_content: str,
        query: str = "Tech Sector Q3 Analysis",
        csv_path: Optional[str] = None
    ) -> Path:
        """Compile complete publication-grade A4 PDF document."""
        doc = SimpleDocTemplate(
            str(self.output_path),
            pagesize=A4,
            leftMargin=40,
            rightMargin=40,
            topMargin=46,
            bottomMargin=46
        )

        date_str = datetime.now().strftime("%B %d, %Y")
        story = []

        # 1. Header Banner
        banner = self.build_header_banner(query, date_str)
        story.append(banner)
        story.append(Spacer(1, 14))

        # 2. Parse Markdown Sections and interleave flowables
        lines = markdown_content.splitlines()
        in_table_section = False

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Skip top markdown title (already in banner)
            if line_str.startswith("# ") and "Market Research" in line_str:
                continue
            if line_str.startswith("**Publication Date**") or line_str.startswith("**Security Classification**"):
                continue

            # Heading 1
            if line_str.startswith("# "):
                text = line_str[2:].strip()
                story.append(Spacer(1, 8))
                story.append(Paragraph(f"<b>{text}</b>", self.styles["Heading1"]))
                story.append(HRFlowable(width="100%", thickness=1, color=COLOR_ACCENT, spaceAfter=8))
                continue

            # Heading 2
            if line_str.startswith("## "):
                text = line_str[3:].strip()
                story.append(Spacer(1, 6))
                story.append(Paragraph(f"<b>{text}</b>", self.styles["Heading2"]))
                continue

            # Heading 3
            if line_str.startswith("### "):
                text = line_str[4:].strip()
                story.append(Paragraph(f"<b>{text}</b>", self.styles["Heading3"]))
                continue

            # Bullet items
            if line_str.startswith("- ") or line_str.startswith("* "):
                bullet_text = line_str[2:].strip()
                # Clean bold tags
                formatted_bullet = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", bullet_text)
                story.append(Paragraph(f"&bull; {formatted_bullet}", self.styles["Bullet"]))
                continue

            # Markdown Table Row detection (skip raw pipe tables, we inject the styled tables below)
            if line_str.startswith("|"):
                in_table_section = True
                continue

            # Horizontal dividers
            if line_str in ("---", "***", "___"):
                story.append(HRFlowable(width="100%", thickness=0.5, color=COLOR_BORDER, spaceBefore=4, spaceAfter=6))
                continue

            # Standard body text
            formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", line_str)
            formatted_text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", formatted_text)
            story.append(Paragraph(formatted_text, self.styles["Body"]))

        # 3. Interleave Tabular Grids
        story.append(Spacer(1, 10))
        story.append(Paragraph("<b>Table 1: Pandas Statistical Matrix (Summary Distributions)</b>", self.styles["Heading2"]))
        story.append(self.build_pandas_summary_table(csv_path))
        story.append(Spacer(1, 14))

        story.append(Paragraph("<b>Table 2: Corporate Peer Group Baseline Metrics</b>", self.styles["Heading2"]))
        story.append(self.build_corporate_peers_table(csv_path))
        story.append(Spacer(1, 14))

        # Build document with custom NumberedCanvas
        doc.build(story, canvasmaker=NumberedCanvas)
        return self.output_path


def compile_pdf_report(
    markdown_content: str,
    output_path: str = "output/market_report.pdf",
    query: str = "Tech Sector Q3 Analysis",
    csv_path: Optional[str] = None
) -> str:
    """Convenience helper to compile PDF report."""
    generator = MarketversePDFGenerator(output_path=output_path)
    result_path = generator.generate_pdf(markdown_content, query=query, csv_path=csv_path)
    return str(result_path)
