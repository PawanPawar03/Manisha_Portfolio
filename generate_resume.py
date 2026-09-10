import os
import sys
from PIL import Image, ImageDraw, ImageOps
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

BASE_DIR = r"C:\Users\Lenovo\Desktop\Manisha portfolio"
PHOTO_SRC = os.path.join(BASE_DIR, 'profile.jpg')
CROPPED_PHOTO = os.path.join(BASE_DIR, 'profile_cropped.png')
PDF_OUTPUT = os.path.join(BASE_DIR, 'Manisha_Avinash_Patke_Resume.pdf')

def prepare_photo():
    """Crop and prepare high-res photo with elegant circular frame and double ring border."""
    im = Image.open(PHOTO_SRC).convert('RGB')
    w, h = im.size
    
    # Original is 1792 x 2400.
    target_w = int(w * 0.82)
    target_h = target_w
    left = int((w - target_w) / 2)
    top = int(h * 0.04)
    right = left + target_w
    bottom = top + target_h
    
    cropped = im.crop((left, top, right, bottom))
    out_size = (700, 700)
    cropped = cropped.resize(out_size, Image.Resampling.LANCZOS)
    
    # Antialiased circular mask
    mask = Image.new('L', out_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((4, 4, out_size[0]-4, out_size[1]-4), fill=255)
    
    result = Image.new('RGBA', out_size, (255, 255, 255, 0))
    result.paste(cropped, (0, 0), mask=mask)
    
    # Outer sapphire blue ring and inner white ring
    ring_draw = ImageDraw.Draw(result)
    ring_draw.ellipse((4, 4, out_size[0]-4, out_size[1]-4), outline=(29, 78, 216, 255), width=10)
    ring_draw.ellipse((14, 14, out_size[0]-14, out_size[1]-14), outline=(255, 255, 255, 255), width=5)
    
    result.save(CROPPED_PHOTO, 'PNG')
    print(f"Saved cropped photo to {CROPPED_PHOTO}")

class NumberedCanvas(canvas.Canvas):
    """Adds running headers, footers, page count, and executive edge accents."""
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

    def draw_page_decorations(self, page_count):
        self.saveState()
        # Top banner accent stripes
        self.setFillColor(colors.HexColor('#1E3A8A'))
        self.rect(0, 841.89 - 5, 595.27, 5, fill=1, stroke=0)
        self.setFillColor(colors.HexColor('#2563EB'))
        self.rect(0, 841.89 - 7.5, 595.27, 2.5, fill=1, stroke=0)

        # Footer
        self.setFont("Helvetica", 7.8)
        self.setFillColor(colors.HexColor('#64748B'))
        footer_text = "Manisha Avinash Patke — Professional Resume | Verified Digital Portfolio: https://pawanpawar03.github.io/Manisha_Portfolio/"
        self.drawString(32, 16, footer_text)
        
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(595.27 - 32, 16, page_str)
        
        # Bottom thin separator line
        self.setStrokeColor(colors.HexColor('#E2E8F0'))
        self.setLineWidth(0.75)
        self.line(32, 26, 595.27 - 32, 26)
        
        self.restoreState()

def build_pdf():
    prepare_photo()
    
    doc = SimpleDocTemplate(
        PDF_OUTPUT,
        pagesize=A4,
        leftMargin=32,
        rightMargin=32,
        topMargin=26,
        bottomMargin=34
    )

    styles = getSampleStyleSheet()
    
    navy_dark = colors.HexColor('#0F172A')
    accent_blue = colors.HexColor('#1D4ED8')
    text_dark = colors.HexColor('#1E293B')
    text_muted = colors.HexColor('#475569')

    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=23,
        textColor=navy_dark
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=11.5,
        textColor=accent_blue
    )

    contact_style = ParagraphStyle(
        'ContactText',
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=text_muted
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=navy_dark,
        spaceBefore=0,
        spaceAfter=0
    )

    body_style = ParagraphStyle(
        'BodyDark',
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=text_dark
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=11.2,
        textColor=navy_dark
    )

    cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=text_dark
    )

    cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.8,
        textColor=navy_dark
    )

    cell_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # ==================== HEADER (PHOTO + DETAILS) ====================
    photo_img = RLImage(CROPPED_PHOTO, width=29*mm, height=29*mm)
    
    header_text = [
        Paragraph("MANISHA AVINASH PATKE", title_style),
        Spacer(1, 2),
        Paragraph("ACCOUNTING & TAXATION SPECIALIST | ADVANCED EXCEL & OFFICE OPERATIONS", subtitle_style),
        Spacer(1, 3),
        Paragraph(
            "<b>Mobile:</b> +91 7499059351 &nbsp;&nbsp;|&nbsp;&nbsp; "
            "<b>Email:</b> mp5239161@gmail.com &nbsp;&nbsp;|&nbsp;&nbsp; "
            "<b>Address:</b> At Post Machnur, Tq. Biloli, Dist. Nanded 431711, MH",
            contact_style
        ),
        Spacer(1, 1),
        Paragraph(
            "<b>Digital Portfolio:</b> <font color='#1D4ED8'><u>https://pawanpawar03.github.io/Manisha_Portfolio/</u></font> &nbsp;&nbsp;|&nbsp;&nbsp; <b>Status:</b> Immediate Joiner",
            contact_style
        ),
    ]

    header_table = Table([[photo_img, header_text]], colWidths=[33*mm, 154*mm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 5))

    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1D4ED8'), spaceBefore=0, spaceAfter=5))

    def make_section_header(title_text):
        p = Paragraph(f"<font color='#1D4ED8'>■</font> &nbsp;<b>{title_text}</b>", section_heading)
        t = Table([[p]], colWidths=[531])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('LINELEFT', (0, 0), (0, -1), 3, colors.HexColor('#1D4ED8')),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        return t

    # ==================== CAREER OBJECTIVE ====================
    story.append(make_section_header("CAREER OBJECTIVE"))
    story.append(Spacer(1, 3))
    obj_text = (
        "Dedicated, detail-oriented Accounting and Office Administration Specialist equipped with proven practical "
        "expertise in <b>Tally Prime</b>, <b>Advanced Excel</b>, <b>GST Invoicing</b>, and <b>Office Automation</b>. "
        "Demonstrated proficiency in commercial transaction posting, ledger accounting, trial balance reconciliation, "
        "spreadsheet reporting, and bilingual high-speed typing (English 40 WPM & Marathi 30 WPM). Seeking a growth-oriented "
        "role where I can apply financial rigor, continuous learning, and collaborative teamwork to optimize business "
        "accounting, tax compliance, and office administration."
    )
    obj_table = Table([[Paragraph(obj_text, body_style)]], colWidths=[531])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FAFAFA')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(obj_table)
    story.append(Spacer(1, 5))

    # ==================== CORE TECHNICAL PROFICIENCIES & SKILLS ====================
    story.append(make_section_header("CORE TECHNICAL PROFICIENCIES & SKILLS"))
    story.append(Spacer(1, 3))

    card1 = [
        Paragraph("<b>FINANCIAL ACCOUNTING & TALLY</b>", ParagraphStyle('C1H', parent=body_bold, fontSize=8, textColor=colors.HexColor('#1E3A8A'))),
        Spacer(1, 1),
        Paragraph("• <b>Tally Prime</b> (KLIC Certified - 78% First Class)<br/>"
                  "• GST Compliance (CGST, SGST, IGST Rules & Rates)<br/>"
                  "• Voucher Entry: Sales, Purchase, Receipt, Payment, Journal<br/>"
                  "• Ledgers, Trial Balance, Profit & Loss, Balance Sheet<br/>"
                  "• Bank Reconciliation (BRS) & Inventory Stock Tracking", cell_style)
    ]
    card2 = [
        Paragraph("<b>ADVANCED EXCEL & DATA ANALYSIS</b>", ParagraphStyle('C2H', parent=body_bold, fontSize=8, textColor=colors.HexColor('#1E3A8A'))),
        Spacer(1, 1),
        Paragraph("• <b>Advanced Excel</b> (KLIC Certified - 81% First Class)<br/>"
                  "• Formulas: VLOOKUP, HLOOKUP, XLOOKUP, Nested IF, SUMIFS<br/>"
                  "• Pivot Tables, Slicers & Dynamic Interactive Dashboards<br/>"
                  "• Data Validation, Conditional Formatting & Deduplication<br/>"
                  "• Financial Modeling, Payroll Calculation & MIS Reporting", cell_style)
    ]
    card3 = [
        Paragraph("<b>OFFICE IT & DATA MANAGEMENT</b>", ParagraphStyle('C3H', parent=body_bold, fontSize=8, textColor=colors.HexColor('#1E3A8A'))),
        Spacer(1, 1),
        Paragraph("• <b>MS-CIT Certified</b> by MKCL (88.00% First Class Distinction)<br/>"
                  "• Data Entry & Data Management (KLIC - 84% First Class)<br/>"
                  "• MS Word: Business Documentation, Mail Merge, Official Tables<br/>"
                  "• MS PowerPoint: Executive Slide Presentations<br/>"
                  "• Digital Records, Cloud Archiving, Data Privacy & Email", cell_style)
    ]
    card4 = [
        Paragraph("<b>GOVT. COMMERCIAL TYPING</b>", ParagraphStyle('C4H', parent=body_bold, fontSize=8, textColor=colors.HexColor('#1E3A8A'))),
        Spacer(1, 1),
        Paragraph("• <b>English 40 WPM</b> (MSCE Govt. Council - First Class)<br/>"
                  "• <b>English 30 WPM</b> (MSCE Govt. Council - First Class)<br/>"
                  "• <b>Marathi 30 WPM</b> (MSCE Govt. Council - First Class)<br/>"
                  "• High-speed transcription with verified 99%+ accuracy<br/>"
                  "• Bilingual clerical letters, circulars & official drafting", cell_style)
    ]

    skills_grid = Table([
        [card1, card2],
        [card3, card4]
    ], colWidths=[260, 260])
    skills_grid.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(skills_grid)
    story.append(Spacer(1, 5))

    # ==================== EDUCATIONAL QUALIFICATIONS ====================
    story.append(make_section_header("ACADEMIC QUALIFICATIONS"))
    story.append(Spacer(1, 3))

    edu_data = [
        [
            Paragraph("Qualification / Degree", cell_header),
            Paragraph("Board / University", cell_header),
            Paragraph("Year", cell_header),
            Paragraph("Percentage", cell_header),
            Paragraph("Class / Division", cell_header),
        ],
        [
            Paragraph("<b>M.A.</b> (Master of Arts)", cell_bold),
            Paragraph("SRTMU, Nanded (Swami Ramanand Teerth Marathwada Univ.)", cell_style),
            Paragraph("2022", cell_style),
            Paragraph("<font color='#1D4ED8'><b>73.33%</b></font>", cell_style),
            Paragraph("First Class", cell_style),
        ],
        [
            Paragraph("<b>B.A.</b> (Bachelor of Arts)", cell_bold),
            Paragraph("SRTMU, Nanded (Swami Ramanand Teerth Marathwada Univ.)", cell_style),
            Paragraph("2020", cell_style),
            Paragraph("<font color='#1D4ED8'><b>78.09%</b></font>", cell_style),
            Paragraph("First Class", cell_style),
        ],
        [
            Paragraph("<b>H.S.C.</b> (Higher Secondary)", cell_bold),
            Paragraph("Maharashtra State Board (Latur Divisional Board)", cell_style),
            Paragraph("2017", cell_style),
            Paragraph("<font color='#1D4ED8'><b>80.92%</b></font>", cell_style),
            Paragraph("First Class", cell_style),
        ],
        [
            Paragraph("<b>S.S.C.</b> (Secondary School)", cell_bold),
            Paragraph("Maharashtra State Board (Latur Divisional Board)", cell_style),
            Paragraph("2015", cell_style),
            Paragraph("<font color='#1D4ED8'><b>82.80%</b></font>", cell_style),
            Paragraph("First Class", cell_style),
        ],
    ]

    edu_table = Table(edu_data, colWidths=[120, 160, 42, 68, 141])
    edu_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(edu_table)
    story.append(Spacer(1, 5))

    # ==================== PRACTICAL CAPABILITIES & SIMULATORS ====================
    story.append(make_section_header("PRACTICAL WORKFLOWS & LIVE SIMULATOR HIGHLIGHTS"))
    story.append(Spacer(1, 3))

    prac_data = [
        [
            Paragraph("<b>• Live GST Voucher Calculator:</b> Implemented dynamic computation of Subtotal, CGST (9%), SGST (9%), and Net Invoice Amount with automatic round-off adjustments for commercial billing.", cell_style)
        ],
        [
            Paragraph("<b>• Spreadsheet Double-Entry Ledger:</b> Real-time double-entry bookkeeping trial balance matching Debits & Credits with instant discrepancy detection.", cell_style)
        ],
        [
            Paragraph("<b>• Certified High-Speed Bilingual Typing:</b> Demonstrated rapid transcription in English & Marathi with verified 99%+ accuracy under timed examination conditions.", cell_style)
        ]
    ]
    prac_table = Table(prac_data, colWidths=[531])
    prac_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(prac_table)

    # Force page break for Page 2
    story.append(PageBreak())

    # ==================== PAGE 2 ====================
    p2_hdr_left = Paragraph("<b>MANISHA AVINASH PATKE</b> &nbsp;|&nbsp; Professional Curriculum Vitae", subtitle_style)
    p2_hdr_right = Paragraph("<font color='#64748B'>Contact: +91 7499059351 | mp5239161@gmail.com</font>", contact_style)
    p2_hdr_table = Table([[p2_hdr_left, p2_hdr_right]], colWidths=[330, 201])
    p2_hdr_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(p2_hdr_table)
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=2, spaceAfter=6))

    # ==================== TECHNICAL & VOCATIONAL CERTIFICATIONS ====================
    story.append(make_section_header("TECHNICAL & VOCATIONAL CERTIFICATIONS"))
    story.append(Spacer(1, 3))

    cert_data = [
        [
            Paragraph("Certification / Course", cell_header),
            Paragraph("Issuing Authority / Institute", cell_header),
            Paragraph("Year", cell_header),
            Paragraph("Score / Grade", cell_header),
            Paragraph("Credential Status", cell_header),
        ],
        [
            Paragraph("<b>Tally Prime</b>", cell_bold),
            Paragraph("KLIC (MKCL Knowledge Network)", cell_style),
            Paragraph("2024", cell_style),
            Paragraph("<font color='#1D4ED8'><b>78%</b></font>", cell_style),
            Paragraph("Verified & Completed", cell_style),
        ],
        [
            Paragraph("<b>Advanced Excel</b>", cell_bold),
            Paragraph("KLIC (MKCL Knowledge Network)", cell_style),
            Paragraph("2024", cell_style),
            Paragraph("<font color='#1D4ED8'><b>81%</b></font>", cell_style),
            Paragraph("Verified & Completed", cell_style),
        ],
        [
            Paragraph("<b>Data Entry and Data Management</b>", cell_bold),
            Paragraph("KLIC (MKCL Knowledge Network)", cell_style),
            Paragraph("2024", cell_style),
            Paragraph("<font color='#1D4ED8'><b>84%</b></font>", cell_style),
            Paragraph("Verified & Completed", cell_style),
        ],
        [
            Paragraph("<b>MS-CIT</b> (Information Technology)", cell_bold),
            Paragraph("MKCL (Maharashtra Knowledge Corp.)", cell_style),
            Paragraph("2019", cell_style),
            Paragraph("<font color='#1D4ED8'><b>88.00%</b></font>", cell_style),
            Paragraph("First Class with Distinction", cell_style),
        ],
    ]

    cert_table = Table(cert_data, colWidths=[140, 155, 42, 72, 122])
    cert_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(cert_table)
    story.append(Spacer(1, 6))

    # ==================== GOVERNMENT COMMERCIAL TYPING CERTIFICATES ====================
    story.append(make_section_header("GOVERNMENT COMMERCIAL TYPING EXAMINATIONS (MSCE)"))
    story.append(Spacer(1, 3))

    typing_data = [
        [
            Paragraph("Examination Subject & Speed", cell_header),
            Paragraph("Examining Council", cell_header),
            Paragraph("Year", cell_header),
            Paragraph("Percentage", cell_header),
            Paragraph("Grade / Division", cell_header),
        ],
        [
            Paragraph("<b>English 40 WPM Typing</b>", cell_bold),
            Paragraph("MSCE (Maharashtra State Council of Examination)", cell_style),
            Paragraph("2017", cell_style),
            Paragraph("<font color='#1D4ED8'><b>67.00%</b></font>", cell_style),
            Paragraph("First Class", cell_style),
        ],
        [
            Paragraph("<b>English 30 WPM Typing</b>", cell_bold),
            Paragraph("MSCE (Maharashtra State Council of Examination)", cell_style),
            Paragraph("2018", cell_style),
            Paragraph("<font color='#1D4ED8'><b>70.00%</b></font>", cell_style),
            Paragraph("First Class", cell_style),
        ],
        [
            Paragraph("<b>Marathi 30 WPM Typing</b>", cell_bold),
            Paragraph("MSCE (Maharashtra State Council of Examination)", cell_style),
            Paragraph("2018", cell_style),
            Paragraph("<font color='#1D4ED8'><b>62.00%</b></font>", cell_style),
            Paragraph("First Class", cell_style),
        ],
    ]

    typing_table = Table(typing_data, colWidths=[140, 175, 42, 72, 102])
    typing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('ALIGN', (2, 0), (3, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3.8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8FAFC')]),
    ]))
    story.append(typing_table)
    story.append(Spacer(1, 6))

    # ==================== KEY PROFESSIONAL ATTRIBUTES & COMPETENCIES ====================
    story.append(make_section_header("CORE PROFESSIONAL ATTRIBUTES & WORK ETHIC"))
    story.append(Spacer(1, 3))

    attr_cards = [
        [
            Paragraph("<b>Financial Precision & Accuracy</b><br/>Zero-defect approach in recording vouchers, managing multi-tier ledger accounts, and executing bank reconciliations.", cell_style),
            Paragraph("<b>Taxation & GST Compliance</b><br/>Thorough practical understanding of HSN codes, SGST/CGST/IGST tax rates, and compliant commercial invoicing procedures.", cell_style),
        ],
        [
            Paragraph("<b>Rapid Bilingual Documentation</b><br/>Certified high-speed transcription in both English and Marathi; capable of drafting official letters, circulars, and notices.", cell_style),
            Paragraph("<b>Data Security & Administration</b><br/>Strict confidentiality of corporate payroll, customer records, audit ledgers, and systematic digital folder archiving.", cell_style),
        ]
    ]
    attr_table = Table(attr_cards, colWidths=[260, 260])
    attr_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    story.append(attr_table)
    story.append(Spacer(1, 6))

    # ==================== PERSONAL PROFILE & DEMOGRAPHICS ====================
    story.append(make_section_header("PERSONAL PROFILE & DEMOGRAPHICS"))
    story.append(Spacer(1, 3))

    profile_data = [
        [
            Paragraph("<b>Candidate Name:</b>", cell_bold),
            Paragraph("MANISHA AVINASH PATKE", cell_style),
            Paragraph("<b>Date of Birth:</b>", cell_bold),
            Paragraph("01-09-1999 (01 September 1999)", cell_style),
        ],
        [
            Paragraph("<b>Gender:</b>", cell_bold),
            Paragraph("Female", cell_style),
            Paragraph("<b>Marital Status:</b>", cell_bold),
            Paragraph("Married", cell_style),
        ],
        [
            Paragraph("<b>Social Category:</b>", cell_bold),
            Paragraph("OPEN (Maratha)", cell_style),
            Paragraph("<b>Nationality:</b>", cell_bold),
            Paragraph("Indian", cell_style),
        ],
        [
            Paragraph("<b>Domicile State:</b>", cell_bold),
            Paragraph("Maharashtra", cell_style),
            Paragraph("<b>Languages Known:</b>", cell_bold),
            Paragraph("English, Hindi, Marathi", cell_style),
        ],
        [
            Paragraph("<b>Permanent Address:</b>", cell_bold),
            Paragraph("At post Machnur, Tq. Biloli, Dist. Nanded, Maharashtra - 431711", cell_style),
            Paragraph("<b>Cell / Contact:</b>", cell_bold),
            Paragraph("+91 7499059351 | mp5239161@gmail.com", cell_style),
        ],
    ]

    profile_table = Table(profile_data, colWidths=[95, 170, 90, 176])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 6))

    # ==================== DECLARATION & SIGNATURE ====================
    story.append(make_section_header("FORMAL DECLARATION"))
    story.append(Spacer(1, 3))

    dec_text = (
        "I hereby solemnly declare that all the statements and details provided in this curriculum vitae are true, "
        "complete, and correct to the best of my knowledge, belief, and official educational certificates."
    )
    story.append(Paragraph(dec_text, body_style))
    story.append(Spacer(1, 8))

    sig_data = [
        [
            Paragraph("<b>Date:</b> ______________<br/><br/><b>Place:</b> MACHNUR (NANDED)", body_style),
            Paragraph(
                "Yours Faithfully,<br/><br/>"
                "<b>MANISHA AVINASH PATKE</b><br/>"
                "<font size='7' color='#64748B'>Signature of Candidate</font>",
                ParagraphStyle('SigRight', parent=body_style, alignment=TA_RIGHT)
            )
        ]
    ]
    sig_table = Table(sig_data, colWidths=[240, 291])
    sig_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 6))

    # Interactive Portfolio Verification Box
    qr_info = [
        [
            Paragraph(
                "<b>Interactive Portfolio & Practical Simulator Verification:</b><br/>"
                "To explore live interactive accounting simulations including the <i>GST & Invoice Voucher Calculator</i>, "
                "<i>Live Excel Double-Entry Spreadsheet</i>, and <i>Live Typing Tester</i>, please visit: "
                "<font color='#1D4ED8'><b><u>https://pawanpawar03.github.io/Manisha_Portfolio/</u></b></font>",
                ParagraphStyle('Verif', parent=cell_style, fontSize=7.2, leading=9.5, textColor=text_muted)
            )
        ]
    ]
    verif_table = Table(qr_info, colWidths=[531])
    verif_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#BFDBFE')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(verif_table)

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {PDF_OUTPUT}")

def render_preview_images():
    """Convert PDF pages to PNG using PyMuPDF to inspect."""
    doc = fitz.open(PDF_OUTPUT)
    print(f"Total pages generated: {len(doc)}")
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        out_png = os.path.join(r"C:\Users\Lenovo\.gemini\antigravity\brain\e648bf5a-5287-412c-b90c-95a7033fdc8e", f"resume_preview_p{i+1}.png")
        pix.save(out_png)
        print(f"Rendered page {i+1} to {out_png}")

if __name__ == '__main__':
    build_pdf()
    render_preview_images()
