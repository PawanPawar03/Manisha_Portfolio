import base64
import subprocess
import os
import fitz

BASE_DIR = r"C:\Users\Lenovo\Desktop\Manisha portfolio"
img_path = os.path.join(BASE_DIR, "profile.jpg")

with open(img_path, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Manisha Avinash Patke - Executive Resume</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap');

    @page {{
      size: A4 portrait;
      margin: 0;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact !important;
      print-color-adjust: exact !important;
    }}

    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      color: #1e293b;
      background: #f8fafc;
      font-size: 11.5px;
      line-height: 1.5;
    }}

    .page {{
      width: 210mm;
      height: 297mm;
      padding: 14mm 16mm;
      background: #ffffff;
      position: relative;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow: hidden;
    }}

    .page:last-child {{
      page-break-after: avoid;
    }}

    /* --- Top Header Strip --- */
    .header-card {{
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 16px 20px;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #1e3a8a 100%);
      color: #ffffff;
      border-radius: 12px;
      margin-bottom: 14px;
      border: 1px solid #334155;
    }}

    .header-photo-wrap {{
      width: 82px;
      height: 98px;
      border-radius: 8px;
      overflow: hidden;
      border: 2.5px solid #38bdf8;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      flex-shrink: 0;
      background: #0f172a;
    }}

    .header-photo-wrap img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
    }}

    .header-info {{
      flex: 1;
    }}

    .header-name {{
      font-family: 'Outfit', sans-serif;
      font-size: 22px;
      font-weight: 800;
      letter-spacing: 0.5px;
      color: #ffffff;
      margin-bottom: 2px;
    }}

    .header-tagline {{
      font-size: 11.5px;
      font-weight: 600;
      color: #38bdf8;
      margin-bottom: 8px;
    }}

    .contact-chips {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px 12px;
      font-size: 10px;
      color: #cbd5e1;
    }}

    .contact-chip {{
      display: flex;
      align-items: center;
      gap: 4px;
      background: rgba(255, 255, 255, 0.08);
      padding: 2px 8px;
      border-radius: 4px;
      border: 1px solid rgba(255, 255, 255, 0.12);
    }}

    .contact-chip strong {{
      color: #ffffff;
    }}

    .portfolio-badge {{
      display: inline-block;
      margin-top: 6px;
      font-size: 9.5px;
      font-weight: 600;
      color: #38bdf8;
      text-decoration: none;
    }}

    /* --- Section Styling --- */
    .section {{
      margin-bottom: 12px;
    }}

    .section-title {{
      font-family: 'Outfit', sans-serif;
      font-size: 13px;
      font-weight: 700;
      color: #0f172a;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
      border-bottom: 1.5px solid #e2e8f0;
      padding-bottom: 3px;
    }}

    .section-title::before {{
      content: '';
      display: inline-block;
      width: 4px;
      height: 13px;
      background: #2563eb;
      border-radius: 2px;
    }}

    /* --- Objective Card --- */
    .objective-box {{
      background: #f1f5f9;
      border-left: 3.5px solid #2563eb;
      padding: 8px 12px;
      border-radius: 0 6px 6px 0;
      font-size: 11px;
      color: #334155;
      line-height: 1.55;
    }}

    /* --- Modern Tables --- */
    .resume-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 10.5px;
      margin-bottom: 4px;
    }}

    .resume-table th {{
      background: #0f172a;
      color: #ffffff;
      padding: 5px 8px;
      text-align: left;
      font-weight: 600;
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }}

    .resume-table td {{
      padding: 5.5px 8px;
      border-bottom: 1px solid #e2e8f0;
      color: #334155;
      vertical-align: middle;
    }}

    .resume-table tr:nth-child(even) td {{
      background: #f8fafc;
    }}

    .score-badge {{
      display: inline-block;
      font-weight: 700;
      color: #0369a1;
      background: #e0f2fe;
      padding: 1.5px 6px;
      border-radius: 4px;
      font-size: 10px;
    }}

    .score-badge.high {{
      color: #065f46;
      background: #d1fae5;
    }}

    /* --- Competency Cards --- */
    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }}

    .skill-card {{
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 6px;
      padding: 8px;
    }}

    .skill-card h4 {{
      font-size: 10.5px;
      font-weight: 700;
      color: #1e293b;
      margin-bottom: 4px;
      display: flex;
      align-items: center;
      gap: 4px;
    }}

    .skill-card p {{
      font-size: 9.5px;
      color: #64748b;
      line-height: 1.4;
    }}

    /* --- Personal Info Grid --- */
    .info-list {{
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 6px 12px;
      background: #f8fafc;
      padding: 10px 14px;
      border-radius: 8px;
      border: 1px solid #e2e8f0;
      font-size: 10.5px;
    }}

    .info-item {{
      display: flex;
      justify-content: space-between;
      border-bottom: 1px dashed #e2e8f0;
      padding-bottom: 3px;
    }}

    .info-label {{
      color: #64748b;
      font-weight: 500;
    }}

    .info-value {{
      color: #0f172a;
      font-weight: 600;
    }}

    /* --- Declaration Box --- */
    .declaration-card {{
      background: #f8fafc;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 10.5px;
    }}

    .dec-text {{
      color: #475569;
      font-style: italic;
      margin-bottom: 10px;
    }}

    .dec-bottom {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      font-size: 10.5px;
    }}

    .signature-area {{
      text-align: right;
    }}

    .sign-name {{
      font-weight: 700;
      color: #0f172a;
    }}

    /* --- Page Footer --- */
    .page-footer {{
      border-top: 1px solid #e2e8f0;
      padding-top: 6px;
      display: flex;
      justify-content: space-between;
      font-size: 9px;
      color: #94a3b8;
    }}

    .page-footer a {{
      color: #2563eb;
      text-decoration: none;
      font-weight: 600;
    }}
  </style>
</head>
<body>

  <!-- ==================== PAGE 1 ==================== -->
  <div class="page">
    <div>
      <!-- Header Banner -->
      <div class="header-card">
        <div class="header-photo-wrap">
          <img src="data:image/jpeg;base64,{img_b64}" alt="Manisha Avinash Patke">
        </div>
        <div class="header-info">
          <h1 class="header-name">MANISHA AVINASH PATKE</h1>
          <p class="header-tagline">Tally Prime Specialist | Advanced Excel Analyst | Financial Accounting & Office Operations</p>
          <div class="contact-chips">
            <span class="contact-chip"><strong>Phone:</strong> +91 7499059351</span>
            <span class="contact-chip"><strong>Email:</strong> mp5239161@gmail.com</span>
            <span class="contact-chip"><strong>Location:</strong> Biloli, Dist. Nanded – 431711, MH</span>
          </div>
          <a href="https://pawanpawar03.github.io/Manisha_Portfolio/" class="portfolio-badge">
            🌐 Live Portfolio: https://pawanpawar03.github.io/Manisha_Portfolio/
          </a>
        </div>
      </div>

      <!-- Career Objective -->
      <div class="section">
        <h2 class="section-title">Career Objective</h2>
        <div class="objective-box">
          To have a growth-oriented and challenging career, where I can contribute my knowledge and skills to the organization through continuous learning and teamwork. Dedicated to delivering 100% precision in financial accounting, computerized ledger reconciliation, advanced spreadsheets, high-volume data operations, and bilingual office management.
        </div>
      </div>

      <!-- Technical & Professional Certifications -->
      <div class="section">
        <h2 class="section-title">Government & Institute Certifications</h2>
        <table class="resume-table">
          <thead>
            <tr>
              <th>Course / Certification</th>
              <th>Board / Institute</th>
              <th>Year</th>
              <th>Score / %</th>
              <th>Class / Distinction</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>KLIC Tally Prime 2024</strong></td>
              <td>KLIC Institute</td>
              <td>2024</td>
              <td><span class="score-badge high">78.00%</span></td>
              <td>Certified Accounting Specialist</td>
            </tr>
            <tr>
              <td><strong>Certificate in Advanced Excel</strong></td>
              <td>KLIC Institute</td>
              <td>2024</td>
              <td><span class="score-badge high">81.00%</span></td>
              <td>High Distinction</td>
            </tr>
            <tr>
              <td><strong>Certificate in Data Entry & Data Management</strong></td>
              <td>KLIC Institute</td>
              <td>2024</td>
              <td><span class="score-badge high">84.00%</span></td>
              <td>High Distinction</td>
            </tr>
            <tr>
              <td><strong>MSCIT (Information Technology)</strong></td>
              <td>MKCL, Maharashtra</td>
              <td>2019</td>
              <td><span class="score-badge high">88.00%</span></td>
              <td>First Class with Distinction</td>
            </tr>
            <tr>
              <td><strong>English Typing 40 WPM</strong></td>
              <td>MSCE, Pune (Govt. of MH)</td>
              <td>2017</td>
              <td><span class="score-badge">67.00%</span></td>
              <td>First Class</td>
            </tr>
            <tr>
              <td><strong>English Typing 30 WPM</strong></td>
              <td>MSCE, Pune (Govt. of MH)</td>
              <td>2018</td>
              <td><span class="score-badge high">70.00%</span></td>
              <td>First Class</td>
            </tr>
            <tr>
              <td><strong>Marathi Typing 30 WPM</strong></td>
              <td>MSCE, Pune (Govt. of MH)</td>
              <td>2018</td>
              <td><span class="score-badge">62.00%</span></td>
              <td>First Class (Govt. Certified)</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Academic Qualifications -->
      <div class="section">
        <h2 class="section-title">Academic Qualifications</h2>
        <table class="resume-table">
          <thead>
            <tr>
              <th>Degree / Examination</th>
              <th>University / Board</th>
              <th>Year</th>
              <th>Percentage</th>
              <th>Result / Class</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Master of Arts (M.A.)</strong></td>
              <td>SRTMU, Nanded</td>
              <td>2022</td>
              <td><span class="score-badge high">73.33%</span></td>
              <td>First Class</td>
            </tr>
            <tr>
              <td><strong>Bachelor of Arts (B.A.)</strong></td>
              <td>SRTMU, Nanded</td>
              <td>2020</td>
              <td><span class="score-badge high">78.09%</span></td>
              <td>First Class</td>
            </tr>
            <tr>
              <td><strong>Higher Secondary Certificate (H.S.C)</strong></td>
              <td>Latur Divisional Board</td>
              <td>2017</td>
              <td><span class="score-badge high">80.92%</span></td>
              <td>First Class</td>
            </tr>
            <tr>
              <td><strong>Secondary School Certificate (S.S.C)</strong></td>
              <td>Latur Divisional Board</td>
              <td>2015</td>
              <td><span class="score-badge high">82.80%</span></td>
              <td>First Class</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Core Competency Highlights -->
      <div class="section">
        <h2 class="section-title">Core Competencies</h2>
        <div class="cards-grid">
          <div class="skill-card">
            <h4>📊 Tally Prime 2024</h4>
            <p>Voucher entry, GST classification (CGST/SGST/IGST), daybook, ledger reconciliation & BRS.</p>
          </div>
          <div class="skill-card">
            <h4>📈 Advanced Excel (81%)</h4>
            <p>VLOOKUP, Pivot Tables, SUMIFS, logical nested IF formulas, conditional formatting & automated reports.</p>
          </div>
          <div class="skill-card">
            <h4>🗄️ Data Management (84%)</h4>
            <p>High-volume rapid data collation, archival, documentation hygiene, audit check & zero-error entry.</p>
          </div>
          <div class="skill-card">
            <h4>⌨️ MSCE Typing</h4>
            <p>Bilingual touch-typing: English 40 WPM (First Class) & official Marathi correspondence drafting.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Page 1 Footer -->
    <div class="page-footer">
      <span>Manisha Avinash Patke • Curriculum Vitae</span>
      <span>Page 1 of 2</span>
      <span>Portfolio: <a href="https://pawanpawar03.github.io/Manisha_Portfolio/">pawanpawar03.github.io/Manisha_Portfolio</a></span>
    </div>
  </div>

  <!-- ==================== PAGE 2 ==================== -->
  <div class="page">
    <div>
      <!-- Page 2 Header Strip -->
      <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:2px solid #0f172a; padding-bottom:8px; margin-bottom:14px;">
        <div>
          <h2 style="font-family:'Outfit',sans-serif; font-size:16px; color:#0f172a; font-weight:800; margin:0;">MANISHA AVINASH PATKE</h2>
          <p style="font-size:10px; color:#64748b; margin:0;">Accounting Specialist | Advanced Excel | Office Administrator</p>
        </div>
        <div style="text-align:right; font-size:10px; color:#475569;">
          <span>📞 +91 7499059351</span> | <span>✉️ mp5239161@gmail.com</span>
        </div>
      </div>

      <!-- Key Practical Strengths & Capabilities -->
      <div class="section">
        <h2 class="section-title">Practical Capabilities & Professional Expertise</h2>
        
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px;">
            <h4 style="font-size:11px; font-weight:700; color:#1e3a8a; margin-bottom:3px;">
              💼 Computerized Financial Accounting (Tally Prime 2024 & GST)
            </h4>
            <p style="font-size:10px; color:#475569; line-height:1.5;">
              Expert in business voucher recording (Sales, Purchase, Payment, Receipt, Contra, Journal), GST tax invoice generation with HSN codes, multi-ledger organization, debit/credit matching, and trial balance verification.
            </p>
          </div>

          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px;">
            <h4 style="font-size:11px; font-weight:700; color:#065f46; margin-bottom:3px;">
              📊 Advanced Excel & Analytical Modeling (Score: 81% High Distinction)
            </h4>
            <p style="font-size:10px; color:#475569; line-height:1.5;">
              Proficient in complex spreadsheet design, lookup functions (VLOOKUP, HLOOKUP, XLOOKUP), multi-criteria summarization (SUMIFS, COUNTIFS), dynamic Pivot Tables, data validation dropdowns, and automated variance analysis.
            </p>
          </div>

          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px;">
            <h4 style="font-size:11px; font-weight:700; color:#6b21a8; margin-bottom:3px;">
              📁 High-Speed Data Entry & Archival Operations (Score: 84% High Distinction)
            </h4>
            <p style="font-size:10px; color:#475569; line-height:1.5;">
              Extensive training in rapid alphanumeric transcription, document indexing, electronic filing, data cleansing, duplicate detection, and large database auditing with zero discrepancies.
            </p>
          </div>

          <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:10px;">
            <h4 style="font-size:11px; font-weight:700; color:#b45309; margin-bottom:3px;">
              ⌨️ Bilingual Typing & Office Administration (MSCIT 88% & MSCE 40 WPM)
            </h4>
            <p style="font-size:10px; color:#475569; line-height:1.5;">
              Certified bilingual speed transcription in English (40 WPM) and Marathi (30 WPM) with 99%+ accuracy, official business correspondence drafting, record archiving, and administrative discipline.
            </p>
          </div>
        </div>
      </div>

      <!-- Personal Profile -->
      <div class="section">
        <h2 class="section-title">Personal Profile</h2>
        <div class="info-list">
          <div class="info-item">
            <span class="info-label">Full Name:</span>
            <span class="info-value">MANISHA AVINASH PATKE</span>
          </div>
          <div class="info-item">
            <span class="info-label">Date of Birth:</span>
            <span class="info-value">01-09-1999</span>
          </div>
          <div class="info-item">
            <span class="info-label">Gender:</span>
            <span class="info-value">Female</span>
          </div>
          <div class="info-item">
            <span class="info-label">Marital Status:</span>
            <span class="info-value">Married</span>
          </div>
          <div class="info-item">
            <span class="info-label">Category:</span>
            <span class="info-value">OPEN (Maratha)</span>
          </div>
          <div class="info-item">
            <span class="info-label">Nationality:</span>
            <span class="info-value">Indian</span>
          </div>
          <div class="info-item">
            <span class="info-label">Domicile State:</span>
            <span class="info-value">Maharashtra</span>
          </div>
          <div class="info-item">
            <span class="info-label">Languages Known:</span>
            <span class="info-value">English, Hindi, Marathi</span>
          </div>
          <div class="info-item" style="grid-column: span 2;">
            <span class="info-label">Permanent Address:</span>
            <span class="info-value">At post Machnur, Tq. Biloli, Dist. Nanded – 431711, Maharashtra</span>
          </div>
        </div>
      </div>

      <!-- Declaration -->
      <div class="section">
        <h2 class="section-title">Declaration</h2>
        <div class="declaration-card">
          <p class="dec-text">
            "I hereby declare that all the statements made above are true, complete and correct to the best of my knowledge and belief."
          </p>
          <div class="dec-bottom">
            <div>
              <p><strong>Date:</strong> ___________________</p>
              <p style="margin-top:4px;"><strong>Place:</strong> MACHNUR (Nanded)</p>
            </div>
            <div class="signature-area">
              <p style="color:#64748b; font-size:9.5px; margin-bottom:25px;">Yours Faithfully,</p>
              <p class="sign-name">MANISHA AVINASH PATKE</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Online Portfolio Verification Banner -->
      <div style="background: linear-gradient(135deg, #1e3a8a 0%, #0284c7 100%); color:#ffffff; padding:10px 14px; border-radius:8px; display:flex; justify-content:space-between; align-items:center;">
        <div>
          <strong style="font-size:11px;">Interactive Portfolio & Live Simulators:</strong>
          <p style="font-size:9.5px; color:#e0f2fe; margin-top:1px;">Test live Tally GST invoicing, Excel trial balance, and typing speed benchmarks online.</p>
        </div>
        <div style="text-align:right;">
          <a href="https://pawanpawar03.github.io/Manisha_Portfolio/" style="background:#ffffff; color:#0f172a; padding:4px 10px; border-radius:4px; font-weight:700; font-size:10px; text-decoration:none; display:inline-block;">
            Visit Portfolio ↗
          </a>
        </div>
      </div>
    </div>

    <!-- Page 2 Footer -->
    <div class="page-footer">
      <span>Manisha Avinash Patke • Curriculum Vitae</span>
      <span>Page 2 of 2</span>
      <span>Portfolio: <a href="https://pawanpawar03.github.io/Manisha_Portfolio/">pawanpawar03.github.io/Manisha_Portfolio</a></span>
    </div>
  </div>

</body>
</html>
"""

html_file = os.path.join(BASE_DIR, "resume_template.html")
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Generated resume_template.html successfully")
