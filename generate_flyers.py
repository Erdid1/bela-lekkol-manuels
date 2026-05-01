#!/usr/bin/env python3
"""
Générateur de flyers A5 impression professionnelle
Bela Lekkol Montessori — Format A5 148×210mm + bleed 3mm — 300 DPI
"""

import os
import base64
from weasyprint import HTML, CSS

OUTPUT_DIR = "/mnt/user-data/outputs"
LOGO_PATH = f"{OUTPUT_DIR}/logo.png"

# Logo en base64 pour intégration HTML inline
with open(LOGO_PATH, "rb") as f:
    LOGO_B64 = base64.b64encode(f.read()).decode()

# ─── DIMENSIONS ──────────────────────────────────────────────────────────────
# A5 = 148 × 210 mm
# Bleed 3mm → page totale = 154 × 216 mm
# Zone de sécurité (safe zone) = 6mm depuis le bord (bleed+3mm)
# ─────────────────────────────────────────────────────────────────────────────

CSS_BASE = """
@page {
    size: 154mm 216mm;
    margin: 0;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    width: 154mm;
    height: 216mm;
    overflow: hidden;
    font-family: 'Arial', 'Helvetica Neue', sans-serif;
}
/* Repères de coupe visuels (bleed area = 3mm de chaque côté) */
.bleed-wrapper {
    width: 154mm;
    height: 216mm;
    position: relative;
}
/* Zone imprimable = A5 avec 3mm de bleed */
.page-content {
    position: absolute;
    top: 0; left: 0;
    width: 154mm;
    height: 216mm;
    padding: 9mm 9mm 7mm 9mm;  /* safe zone = bleed(3)+margin(6) */
}
"""

# ─── RECTO ───────────────────────────────────────────────────────────────────
HTML_RECTO = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
{CSS_BASE}

body {{
    background: #1a5276;
}}

.bleed-wrapper {{
    background: linear-gradient(160deg, #1a5276 0%, #154360 50%, #0e2f44 100%);
}}

/* ── EN-TÊTE ── */
.header {{
    display: flex;
    align-items: center;
    gap: 4mm;
    padding-bottom: 4mm;
    border-bottom: 0.8mm solid #f0b429;
    margin-bottom: 4mm;
}}
.logo-wrap img {{
    width: 22mm;
    height: 22mm;
    object-fit: contain;
    border-radius: 50%;
    background: white;
    padding: 1mm;
}}
.header-text h1 {{
    font-size: 9pt;
    font-weight: 900;
    color: #f0b429;
    letter-spacing: 0.5pt;
    text-transform: uppercase;
    line-height: 1.2;
}}
.header-text p {{
    font-size: 7pt;
    color: #aed6f1;
    margin-top: 1mm;
    font-style: italic;
}}

/* ── BANDEAU ACCROCHE ── */
.tagline {{
    background: #f0b429;
    color: #1a5276;
    text-align: center;
    padding: 2.5mm 3mm;
    border-radius: 1.5mm;
    font-size: 9.5pt;
    font-weight: 900;
    letter-spacing: 0.3pt;
    text-transform: uppercase;
    margin-bottom: 4mm;
}}

/* ── LABELS ── */
.badges {{
    display: flex;
    gap: 2mm;
    margin-bottom: 4mm;
}}
.badge {{
    flex: 1;
    background: rgba(240, 180, 41, 0.15);
    border: 0.4mm solid #f0b429;
    border-radius: 1.5mm;
    padding: 2mm 1.5mm;
    text-align: center;
}}
.badge .badge-icon {{
    font-size: 11pt;
    display: block;
    margin-bottom: 1mm;
}}
.badge .badge-title {{
    font-size: 6pt;
    font-weight: 900;
    color: #f0b429;
    text-transform: uppercase;
    letter-spacing: 0.3pt;
    display: block;
}}
.badge .badge-sub {{
    font-size: 5.5pt;
    color: #aed6f1;
    display: block;
    margin-top: 0.5mm;
}}

/* ── DIRECTION ── */
.direction {{
    background: rgba(255,255,255,0.07);
    border-left: 1mm solid #f0b429;
    border-radius: 0 1.5mm 1.5mm 0;
    padding: 2.5mm 3mm;
    margin-bottom: 4mm;
}}
.direction h3 {{
    font-size: 6.5pt;
    font-weight: 900;
    color: #f0b429;
    text-transform: uppercase;
    margin-bottom: 1.5mm;
}}
.direction ul {{
    list-style: none;
    padding: 0;
}}
.direction ul li {{
    font-size: 6pt;
    color: #d6eaf8;
    padding: 0.7mm 0;
    padding-left: 3mm;
    position: relative;
    line-height: 1.3;
}}
.direction ul li::before {{
    content: "▸";
    color: #f0b429;
    position: absolute;
    left: 0;
    font-size: 5pt;
    top: 1mm;
}}

/* ── PROGRAMMES ── */
.programmes {{
    background: rgba(255,255,255,0.07);
    border-radius: 1.5mm;
    padding: 2.5mm 3mm;
    margin-bottom: 4mm;
}}
.programmes h3 {{
    font-size: 6.5pt;
    font-weight: 900;
    color: #f0b429;
    text-transform: uppercase;
    margin-bottom: 1.5mm;
}}
.prog-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5mm;
}}
.prog-item {{
    font-size: 5.5pt;
    color: #d6eaf8;
    padding-left: 2.5mm;
    position: relative;
    line-height: 1.3;
}}
.prog-item::before {{
    content: "✓";
    color: #27ae60;
    position: absolute;
    left: 0;
    font-size: 5pt;
}}

/* ── NIVEAUX ── */
.niveaux {{
    display: flex;
    gap: 1.5mm;
    margin-bottom: 4mm;
}}
.niveau-box {{
    flex: 1;
    border: 0.4mm solid rgba(240,180,41,0.4);
    border-radius: 1.5mm;
    padding: 1.5mm 1mm;
    text-align: center;
}}
.niveau-box .niv-label {{
    font-size: 5pt;
    font-weight: 900;
    color: #f0b429;
    text-transform: uppercase;
    display: block;
}}
.niveau-box .niv-name {{
    font-size: 5pt;
    color: #aed6f1;
    display: block;
    margin-top: 0.5mm;
}}

/* ── PIED DE PAGE ── */
.footer {{
    position: absolute;
    bottom: 6mm;
    left: 9mm;
    right: 9mm;
    border-top: 0.5mm solid rgba(240,180,41,0.5);
    padding-top: 2mm;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}}
.contact-block {{
    font-size: 5.5pt;
    color: #aed6f1;
    line-height: 1.6;
}}
.contact-block strong {{
    color: #f0b429;
    font-size: 6pt;
}}
.address-block {{
    font-size: 5pt;
    color: #7fb3d3;
    text-align: right;
    line-height: 1.5;
}}
</style>
</head>
<body>
<div class="bleed-wrapper">
  <div class="page-content">

    <!-- EN-TÊTE -->
    <div class="header">
      <div class="logo-wrap">
        <img src="data:image/png;base64,{LOGO_B64}" alt="Logo Bela Lekkol Montessori">
      </div>
      <div class="header-text">
        <h1>Groupe Scolaire<br>Bela Lekkol Montessori</h1>
        <p>L'école française au service de la Guinée</p>
      </div>
    </div>

    <!-- ACCROCHE -->
    <div class="tagline">La meilleure maternelle au meilleur prix du secteur privé</div>

    <!-- BADGES -->
    <div class="badges">
      <div class="badge">
        <span class="badge-icon">🎓</span>
        <span class="badge-title">Formation Continue</span>
        <span class="badge-sub">Enseignants certifiés</span>
      </div>
      <div class="badge">
        <span class="badge-icon">🏅</span>
        <span class="badge-title">Éducation Reconnue</span>
        <span class="badge-sub">Label officiel</span>
      </div>
      <div class="badge">
        <span class="badge-icon">🇫🇷</span>
        <span class="badge-title">Programmes Français</span>
        <span class="badge-sub">Conformes EN</span>
      </div>
      <div class="badge">
        <span class="badge-icon">🌍</span>
        <span class="badge-title">Contexte Guinéen</span>
        <span class="badge-sub">Ancrage local</span>
      </div>
    </div>

    <!-- DIRECTION -->
    <div class="direction">
      <h3>Direction &amp; Partenariats</h3>
      <ul>
        <li>Directeur français issu du Ministère de l'Éducation Nationale</li>
        <li>Ex-Directeur de l'Alliance Française de Guinée</li>
        <li>Directeur du Centre de Formation Pédagogique Maria Montessori</li>
        <li>Partenaire du MEPU-A et de l'Institut Français (1er degré privé)</li>
        <li>Coopération avec des établissements européens et africains</li>
      </ul>
    </div>

    <!-- PROGRAMMES -->
    <div class="programmes">
      <h3>Nos Engagements Pédagogiques</h3>
      <div class="prog-grid">
        <div class="prog-item">Volumes horaires en conformité</div>
        <div class="prog-item">Pédagogie différenciée Montessori</div>
        <div class="prog-item">Livret de réussite élève (Mat. &amp; Prim.)</div>
        <div class="prog-item">Évaluations &amp; relevés de notes trimestriels</div>
        <div class="prog-item">Anglais, Espagnol — DELF/DALF</div>
        <div class="prog-item">Événements culturels &amp; sportifs</div>
        <div class="prog-item">Logiciel ADMISCO (gestion scolaire)</div>
        <div class="prog-item">Aide aux devoirs GRATUITE</div>
      </div>
    </div>

    <!-- NIVEAUX -->
    <div class="niveaux">
      <div class="niveau-box">
        <span class="niv-label">Maternelle</span>
        <span class="niv-name">Montessori</span>
      </div>
      <div class="niveau-box">
        <span class="niv-label">Primaire</span>
        <span class="niv-name">Prog. français</span>
      </div>
      <div class="niveau-box">
        <span class="niv-label">Collège</span>
        <span class="niv-name">Prog. guinéen</span>
      </div>
      <div class="niveau-box">
        <span class="niv-label">Lycée</span>
        <span class="niv-name">Enrichi / Bac</span>
      </div>
    </div>

    <!-- PIED DE PAGE -->
    <div class="footer">
      <div class="contact-block">
        <strong>✉ belalekkol.montessori@gmail.com</strong><br>
        📞 626 31 31 80 &nbsp;|&nbsp; 623-23-18-07
      </div>
      <div class="address-block">
        KIPE / Centre Émetteur<br>Carrefour Alpha Condé<br>Conakry, Guinée
      </div>
    </div>

  </div>
</div>
</body>
</html>"""

# ─── VERSO ───────────────────────────────────────────────────────────────────
HTML_VERSO = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
{CSS_BASE}

body {{
    background: #ffffff;
}}

.bleed-wrapper {{
    background: #ffffff;
}}

/* ── EN-TÊTE VERSO ── */
.header-verso {{
    background: linear-gradient(135deg, #1a5276, #154360);
    margin: -9mm -9mm 5mm -9mm;
    padding: 5mm 9mm 4mm 9mm;
    display: flex;
    align-items: center;
    gap: 3mm;
}}
.header-verso img {{
    width: 15mm;
    height: 15mm;
    object-fit: contain;
    border-radius: 50%;
    background: white;
    padding: 0.8mm;
}}
.header-verso-text h2 {{
    font-size: 8pt;
    font-weight: 900;
    color: #f0b429;
    text-transform: uppercase;
    letter-spacing: 0.3pt;
}}
.header-verso-text p {{
    font-size: 6pt;
    color: #aed6f1;
    font-style: italic;
}}

/* ── TITRE TARIFS ── */
.tarifs-title {{
    background: #1a5276;
    color: white;
    text-align: center;
    padding: 2mm 3mm;
    border-radius: 1.5mm;
    font-size: 9pt;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.5pt;
    margin-bottom: 3mm;
}}
.tarifs-subtitle {{
    text-align: center;
    font-size: 6.5pt;
    color: #7f8c8d;
    margin-bottom: 4mm;
    font-style: italic;
}}

/* ── TABLEAU TARIFS ── */
.tarifs-table {{
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 3.5mm;
    font-size: 6.5pt;
}}
.tarifs-table thead tr {{
    background: #1a5276;
    color: white;
}}
.tarifs-table thead th {{
    padding: 1.5mm 2mm;
    text-align: left;
    font-size: 6pt;
    text-transform: uppercase;
    letter-spacing: 0.2pt;
}}
.tarifs-table thead th:last-child {{
    text-align: right;
}}
.tarifs-table tbody tr:nth-child(even) {{
    background: #eaf4fc;
}}
.tarifs-table tbody tr:nth-child(odd) {{
    background: #fdfefe;
}}
.tarifs-table tbody td {{
    padding: 1.5mm 2mm;
    vertical-align: middle;
    border-bottom: 0.2mm solid #d5d8dc;
}}
.tarifs-table tbody td:last-child {{
    text-align: right;
    font-weight: 900;
    color: #1a5276;
    white-space: nowrap;
}}
.level-name {{
    font-weight: 700;
    color: #1a5276;
}}
.level-sub {{
    font-size: 5.5pt;
    color: #7f8c8d;
    display: block;
}}
.gratuit {{
    color: #27ae60;
    font-weight: 900;
}}
.prix-gnf {{
    font-size: 7pt;
}}

/* ── VERSEMENTS ── */
.versements {{
    background: #fef9e7;
    border: 0.4mm solid #f0b429;
    border-radius: 1.5mm;
    padding: 2.5mm 3mm;
    margin-bottom: 3mm;
}}
.versements h4 {{
    font-size: 6.5pt;
    font-weight: 900;
    color: #1a5276;
    text-transform: uppercase;
    margin-bottom: 2mm;
    padding-bottom: 1mm;
    border-bottom: 0.3mm solid #f0b429;
}}
.versements-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5mm;
}}
.vers-item {{
    text-align: center;
    background: white;
    border-radius: 1mm;
    padding: 1.5mm 1mm;
    border: 0.3mm solid #fadbd8;
}}
.vers-num {{
    font-size: 5pt;
    font-weight: 900;
    color: #e74c3c;
    text-transform: uppercase;
    display: block;
}}
.vers-amount {{
    font-size: 6.5pt;
    font-weight: 900;
    color: #1a5276;
    display: block;
    margin: 0.5mm 0;
}}
.vers-date {{
    font-size: 5pt;
    color: #7f8c8d;
    display: block;
}}

/* ── REMISES ── */
.remises {{
    background: #eafaf1;
    border-left: 1mm solid #27ae60;
    border-radius: 0 1.5mm 1.5mm 0;
    padding: 2mm 3mm;
    margin-bottom: 3mm;
    font-size: 6pt;
    color: #1e8449;
}}
.remises strong {{
    font-size: 6.5pt;
    text-transform: uppercase;
}}

/* ── SERVICES ── */
.services {{
    display: flex;
    gap: 2mm;
    margin-bottom: 3mm;
}}
.service-item {{
    flex: 1;
    background: #f8f9fa;
    border-radius: 1.5mm;
    padding: 2mm 1.5mm;
    text-align: center;
    border: 0.3mm solid #dee2e6;
}}
.service-item .svc-name {{
    font-size: 5.5pt;
    font-weight: 700;
    color: #1a5276;
    text-transform: uppercase;
    display: block;
    margin-bottom: 0.5mm;
}}
.service-item .svc-price {{
    font-size: 6pt;
    font-weight: 900;
    color: #e74c3c;
    display: block;
}}

/* ── NOTE ── */
.note {{
    background: #eaf4fc;
    border-radius: 1.5mm;
    padding: 2mm 3mm;
    font-size: 5.5pt;
    color: #2c3e50;
    line-height: 1.4;
    font-style: italic;
    margin-bottom: 3mm;
}}

/* ── FOOTER ── */
.footer-verso {{
    position: absolute;
    bottom: 5mm;
    left: 9mm;
    right: 9mm;
    background: linear-gradient(135deg, #1a5276, #154360);
    border-radius: 1.5mm;
    padding: 2.5mm 4mm;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
.footer-verso .contact {{
    font-size: 5.5pt;
    color: #aed6f1;
    line-height: 1.6;
}}
.footer-verso .contact strong {{
    color: #f0b429;
    font-size: 6pt;
    display: block;
}}
.footer-verso .tests {{
    font-size: 5.5pt;
    color: #f0b429;
    font-weight: 900;
    text-align: right;
    line-height: 1.4;
}}
</style>
</head>
<body>
<div class="bleed-wrapper">
  <div class="page-content">

    <!-- EN-TÊTE -->
    <div class="header-verso">
      <img src="data:image/png;base64,{LOGO_B64}" alt="Logo">
      <div class="header-verso-text">
        <h2>Bela Lekkol Montessori</h2>
        <p>L'école française au service de la Guinée</p>
      </div>
    </div>

    <!-- TITRE -->
    <div class="tarifs-title">Frais de Scolarité Annuels en GNF</div>
    <div class="tarifs-subtitle">Année scolaire 2025-2026</div>

    <!-- TABLEAU -->
    <table class="tarifs-table">
      <thead>
        <tr>
          <th>Niveau</th>
          <th>Inscription</th>
          <th>Dossier</th>
          <th>Tests</th>
          <th style="text-align:right">Scolarité totale</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>
            <span class="level-name">Maternelle Montessori</span>
          </td>
          <td class="gratuit">GRATUIT*</td>
          <td class="gratuit">GRATUIT</td>
          <td class="gratuit">GRATUIT</td>
          <td class="prix-gnf">12 000 000 GNF</td>
        </tr>
        <tr>
          <td>
            <span class="level-name">Primaire</span>
            <span class="level-sub">Programme français</span>
          </td>
          <td class="gratuit">GRATUIT*</td>
          <td class="gratuit">GRATUIT</td>
          <td class="gratuit">GRATUIT</td>
          <td class="prix-gnf">12 000 000 GNF</td>
        </tr>
        <tr>
          <td>
            <span class="level-name">Collège</span>
            <span class="level-sub">Programme guinéen</span>
          </td>
          <td>—</td>
          <td>—</td>
          <td>—</td>
          <td class="prix-gnf">3 350 000 GNF</td>
        </tr>
        <tr>
          <td>
            <span class="level-name">Collège</span>
            <span class="level-sub">10ème année — Brevet</span>
          </td>
          <td>—</td>
          <td>—</td>
          <td>—</td>
          <td class="prix-gnf">3 650 000 GNF</td>
        </tr>
        <tr>
          <td>
            <span class="level-name">Lycée</span>
            <span class="level-sub">Programme guinéen enrichi</span>
          </td>
          <td>incluse</td>
          <td>—</td>
          <td>—</td>
          <td class="prix-gnf">3 650 000 GNF</td>
        </tr>
        <tr>
          <td>
            <span class="level-name">Terminale</span>
            <span class="level-sub">Préparation Bac</span>
          </td>
          <td>incluse</td>
          <td>—</td>
          <td>—</td>
          <td class="prix-gnf">3 750 000 GNF</td>
        </tr>
        <tr style="background:#fef5e4">
          <td>
            <span class="level-name">Activités périscolaires</span>
          </td>
          <td colspan="3" style="color:#7f8c8d;font-style:italic">Garderie incluse</td>
          <td class="prix-gnf" style="color:#e74c3c">200 000 GNF/mois</td>
        </tr>
        <tr style="background:#fef5e4">
          <td>
            <span class="level-name">Aide aux devoirs</span>
            <span class="level-sub">Activités pédagogiques complémentaires</span>
          </td>
          <td colspan="3"></td>
          <td class="gratuit">GRATUIT</td>
        </tr>
      </tbody>
    </table>

    <!-- VERSEMENTS MAT/PRIMAIRE -->
    <div class="versements">
      <h4>Échéancier Maternelle &amp; Primaire (12 000 000 GNF)</h4>
      <div class="versements-grid">
        <div class="vers-item">
          <span class="vers-num">Versement 1</span>
          <span class="vers-amount">3 800 000</span>
          <span class="vers-date">À l'inscription</span>
        </div>
        <div class="vers-item">
          <span class="vers-num">Versement 2</span>
          <span class="vers-amount">3 000 000</span>
          <span class="vers-date">05/12/2024</span>
        </div>
        <div class="vers-item">
          <span class="vers-num">Versement 3</span>
          <span class="vers-amount">2 700 000</span>
          <span class="vers-date">05/02/2025</span>
        </div>
        <div class="vers-item">
          <span class="vers-num">Versement 4</span>
          <span class="vers-amount">2 500 000</span>
          <span class="vers-date">05/04/2025</span>
        </div>
      </div>
    </div>

    <!-- REMISES + SERVICES côte à côte -->
    <div style="display:flex; gap:2mm; margin-bottom:3mm;">
      <div class="remises" style="flex:1.5; margin-bottom:0;">
        <strong>🎁 Remises Famille</strong><br>
        À partir du 3ème enfant inscrit :<br>
        Collège : <strong>700 000 GNF</strong> de remise<br>
        Lycée : <strong>400 000 GNF</strong> de remise<br>
        <em style="font-size:5pt;color:#1e8449">* Inscription gratuite si parrainage</em>
      </div>
      <div class="services" style="flex:1; flex-direction:column; margin-bottom:0;">
        <div class="service-item" style="margin-bottom:1mm;">
          <span class="svc-name">🚌 Garderie</span>
          <span class="svc-price">200 000 GNF/mois</span>
        </div>
        <div class="service-item">
          <span class="svc-name">📚 Aide aux devoirs</span>
          <span class="svc-price" style="color:#27ae60">GRATUIT</span>
        </div>
      </div>
    </div>

    <!-- NOTE RÉNOVATION -->
    <div class="note">
      ℹ️ Le groupe scolaire a changé de direction. Une rénovation importante est en cours afin d'offrir aux enseignants et aux élèves les meilleures conditions d'enseignement et d'apprentissage.
    </div>

    <!-- FOOTER -->
    <div class="footer-verso">
      <div class="contact">
        <strong>📧 belalekkol.montessori@gmail.com</strong>
        📞 626 31 31 80 &nbsp;|&nbsp; 623-23-18-07<br>
        KIPE / Centre Émetteur / Carrefour Alpha Condé
      </div>
      <div class="tests">
        TESTS D'ADMISSION<br>
        <span style="color:white;font-weight:normal;font-size:5pt">Sur rendez-vous</span>
      </div>
    </div>

  </div>
</div>
</body>
</html>"""


# ─── CSS POUR IMPRESSION 300 DPI ─────────────────────────────────────────────
CSS_PRINT = CSS(string="""
@page {
    size: 154mm 216mm;
    margin: 0;
}
""")

def generate_pdf(html_content, output_path, label):
    print(f"  Génération {label}...")
    html = HTML(string=html_content, base_url=OUTPUT_DIR)
    html.write_pdf(output_path, stylesheets=[CSS_PRINT],
                   presentational_hints=True,
                   uncompressed_pdf=False)
    size_kb = os.path.getsize(output_path) // 1024
    print(f"  ✓ {label} → {output_path} ({size_kb} Ko)")


# ─── FLYER COMPLET (recto + verso sur 2 pages) ───────────────────────────────
HTML_COMPLET = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<style>
@page {{
    size: 154mm 216mm;
    margin: 0;
}}
</style>
</head>
<body>
<!-- PAGE 1 : RECTO -->
{HTML_RECTO.split('<body>')[1].split('</body>')[0]}
<!-- PAGE 2 : VERSO -->
<div style="page-break-before: always;">
{HTML_VERSO.split('<body>')[1].split('</body>')[0]}
</div>
</body>
</html>"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("═" * 55)
    print("  Bela Lekkol Montessori — Génération PDF impression")
    print("  Format A5 (154×216mm avec bleed 3mm) — 300 DPI")
    print("═" * 55)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    generate_pdf(HTML_RECTO,  f"{OUTPUT_DIR}/flyer_recto_A5.pdf",   "RECTO")
    generate_pdf(HTML_VERSO,  f"{OUTPUT_DIR}/flyer_verso_A5.pdf",   "VERSO")
    generate_pdf(HTML_COMPLET, f"{OUTPUT_DIR}/flyer_complet_avec_bleed.pdf", "COMPLET (recto+verso)")

    print()
    print("═" * 55)
    print("  Fichiers générés dans", OUTPUT_DIR)
    print("═" * 55)
    for f in ["flyer_recto_A5.pdf", "flyer_verso_A5.pdf", "flyer_complet_avec_bleed.pdf"]:
        path = f"{OUTPUT_DIR}/{f}"
        if os.path.exists(path):
            print(f"  ✓ {f} — {os.path.getsize(path)//1024} Ko")
