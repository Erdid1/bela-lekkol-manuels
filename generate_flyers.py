#!/usr/bin/env python3
"""
Générateur de flyers A5 impression professionnelle — Bela Lekkol Montessori
Design fidèle au handoff : recto sombre #141414, verso crème #FFFBF4
Format A5 148×210mm + bleed 3mm → page totale 154×216mm
"""

import os, base64
from weasyprint import HTML, CSS

OUT = "/mnt/user-data/outputs"
os.makedirs(OUT, exist_ok=True)

# ── Assets ────────────────────────────────────────────────────────────────────
def b64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

LOGO_B64     = b64(f"{OUT}/logo.png")
PHOTO_B64    = b64(f"{OUT}/school_building.jpg") or b64(f"{OUT}/school_photo.jpg")
ERIC_B64     = b64(f"{OUT}/eric_photo.jpg")
LOGO_SRC     = f"data:image/png;base64,{LOGO_B64}"   if LOGO_B64  else ""
PHOTO_SRC    = f"data:image/jpeg;base64,{PHOTO_B64}" if PHOTO_B64 else ""
ERIC_SRC     = f"data:image/jpeg;base64,{ERIC_B64}"  if ERIC_B64  else ""

# ── Polices Google Fonts ─────────────────────────────────────────────────────
FONTS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Lato:wght@400;700;900&family=Dancing+Script:wght@600&display=swap');
"""

# ── CSS base partagé ──────────────────────────────────────────────────────────
CSS_PAGE = """
@page { size: 154mm 216mm; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body { width: 154mm; height: 216mm; overflow: hidden; }
"""

# ══════════════════════════════════════════════════════════════════════════════
# RECTO
# ══════════════════════════════════════════════════════════════════════════════
HTML_RECTO = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<style>
{FONTS}
{CSS_PAGE}

body {{
  font-family: 'Lato', Arial, sans-serif;
  background: #141414;
  background-image:
    repeating-linear-gradient(45deg, transparent, transparent 28px, rgba(201,168,76,0.07) 28px, rgba(201,168,76,0.07) 29px),
    repeating-linear-gradient(-45deg, transparent, transparent 28px, rgba(201,168,76,0.05) 28px, rgba(201,168,76,0.05) 29px);
  color: #FFFFFF;
  display: flex;
  flex-direction: column;
}}

/* ── Bande tricolore ── */
.tricolor {{
  display: flex;
  height: 6px;
  width: 100%;
  flex-shrink: 0;
}}
.tricolor span {{ flex: 1; }}
.t1 {{ background: #C0392B; }}
.t2 {{ background: #C8873A; }}
.t3 {{ background: #3A7D44; }}
.t4 {{ background: #1A1A1A; }}

/* ── Header ── */
.header {{
  padding: 4.5mm 8mm 3.5mm;
  text-align: center;
  flex-shrink: 0;
  background: #141414;
}}
.school-name {{
  font-family: 'Playfair Display', serif;
  font-size: 6pt;
  font-weight: 900;
  color: #C9A84C;
  letter-spacing: 2pt;
  text-transform: uppercase;
  display: block;
  margin-bottom: 1mm;
}}
.school-tagline {{
  font-family: 'Playfair Display', serif;
  font-size: 7pt;
  font-weight: 900;
  color: #FFFFFF;
  display: block;
}}

/* ── Photo hero ── */
.hero {{
  position: relative;
  height: 64mm;
  flex-shrink: 0;
  overflow: hidden;
}}
.hero img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.5;
  display: block;
}}
.hero-overlay {{
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom, rgba(20,20,20,0.25), rgba(20,20,20,0.96));
}}
.hero-placeholder {{
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a2a1a 0%, #0d1f0d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}}
.hero-placeholder span {{
  font-size: 20pt;
  opacity: 0.4;
}}

/* ── Bande rentrée ── */
.rentree {{
  background: #C9A84C;
  padding: 2.5mm 8mm;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}}
.rentree-left {{
  font-family: 'Lato', sans-serif;
  font-size: 5.5pt;
  font-weight: 900;
  color: #0D2B1F;
  letter-spacing: 1pt;
  text-transform: uppercase;
}}
.rentree-right {{
  font-family: 'Playfair Display', serif;
  font-size: 6pt;
  font-weight: 900;
  color: #0D2B1F;
}}

/* ── Corps ── */
.body {{
  padding: 4mm 8mm;
  display: flex;
  flex-direction: column;
  gap: 3.5mm;
  flex: 1;
}}

/* Niveaux pills */
.niveaux {{
  display: flex;
  flex-wrap: wrap;
  gap: 1.5mm;
}}
.pill {{
  padding: 1mm 3mm;
  border-radius: 10mm;
  font-size: 5pt;
  font-weight: 700;
  border: 0.3mm solid;
  white-space: nowrap;
}}
.pill-mat  {{ background: rgba(192,57,43,0.15);  color: #E74C3C; border-color: rgba(192,57,43,0.4); }}
.pill-prim {{ background: rgba(58,125,68,0.15);  color: #5CBA6A; border-color: rgba(58,125,68,0.4); }}
.pill-col  {{ background: rgba(201,168,76,0.12); color: #C9A84C; border-color: rgba(201,168,76,0.4); }}
.pill-fr   {{ background: rgba(255,255,255,0.1); color: #FFFFFF; border-color: rgba(255,255,255,0.3); }}

/* Feature cards 2x2 */
.features {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2mm;
}}
.card {{
  background: rgba(255,255,255,0.95);
  border: 0.3mm solid rgba(201,168,76,0.25);
  border-radius: 2mm;
  padding: 2.5mm;
  display: flex;
  flex-direction: column;
  gap: 1mm;
}}
.card-icon {{ font-size: 8pt; }}
.card-title {{
  font-family: 'Lato', sans-serif;
  font-size: 5.5pt;
  font-weight: 700;
  color: #141414;
}}
.card-text {{
  font-size: 5pt;
  color: #555;
  line-height: 1.3;
}}

/* Citation */
.quote {{
  border-left: 0.8mm solid #C9A84C;
  padding-left: 3.5mm;
}}
.quote-text {{
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 5.5pt;
  color: rgba(255,255,255,0.8);
  line-height: 1.4;
}}
.quote-sub {{
  font-size: 5pt;
  color: #C9A84C;
  margin-top: 1mm;
  font-weight: 700;
}}

/* Contact */
.contact-band {{
  background: rgba(201,168,76,0.08);
  border: 0.3mm solid rgba(201,168,76,0.2);
  border-radius: 2mm;
  padding: 2.5mm 3mm;
  display: flex;
  justify-content: space-between;
  align-items: center;
}}
.contact-phone {{
  font-family: 'Playfair Display', serif;
  font-size: 6.5pt;
  color: #C9A84C;
  font-weight: 900;
}}
.contact-details {{
  font-size: 5pt;
  color: rgba(255,255,255,0.6);
  text-align: right;
  line-height: 1.6;
}}
</style>
</head>
<body>

<!-- Bande tricolore haut -->
<div class="tricolor">
  <span class="t1"></span><span class="t2"></span><span class="t3"></span>
  <span class="t4"></span><span class="t2"></span><span class="t1"></span>
</div>

<!-- Header -->
<div class="header">
  <span class="school-name">Bela Lekkol Montessori</span>
  <span class="school-tagline">L'école française de Guinée</span>
</div>

<!-- Photo hero -->
<div class="hero">
  {'<img src="' + PHOTO_SRC + '" alt=""><div class="hero-overlay"></div>' if PHOTO_SRC else '<div class="hero-placeholder"><span>🏫</span></div>'}
</div>

<!-- Bande rentrée -->
<div class="rentree">
  <span class="rentree-left">Inscriptions ouvertes</span>
  <span class="rentree-right">Rentrée 2026–2027</span>
</div>

<!-- Corps -->
<div class="body">

  <div class="niveaux">
    <span class="pill pill-mat">Maternelle</span>
    <span class="pill pill-prim">Primaire</span>
    <span class="pill pill-col">Collège</span>
    <span class="pill pill-col">Lycée</span>
    <span class="pill pill-fr">Franco-guinéen</span>
  </div>

  <div class="features">
    <div class="card">
      <span class="card-icon">🎓</span>
      <div class="card-title">Pédagogie Montessori</div>
      <div class="card-text">Méthodes MHF &amp; MHM agréées</div>
    </div>
    <div class="card">
      <span class="card-icon">🧠</span>
      <div class="card-title">N°1 IA en Guinée</div>
      <div class="card-text">Leader en intégration de l'IA</div>
    </div>
    <div class="card">
      <span class="card-icon">🏫</span>
      <div class="card-title">Centre de formation</div>
      <div class="card-text">Profs formés par Éric Didier</div>
    </div>
    <div class="card">
      <span class="card-icon">🏅</span>
      <div class="card-title">Diplômes reconnus</div>
      <div class="card-text">DELF · Institut Français · ISSEG</div>
    </div>
  </div>

  <div class="quote">
    <div class="quote-text">« Plus belle, plus compétente et moins chère »</div>
    <div class="quote-sub">Système français · Méthodes Montessori · IA intégrée</div>
  </div>

  <div class="contact-band">
    <div class="contact-phone">626 31 31 80</div>
    <div class="contact-details">
      KIPE, Conakry, Guinée<br>
      belalekkol.montessori@gmail.com<br>
      Bela Lekkol Montessori
    </div>
  </div>

</div>

<!-- Bande tricolore bas -->
<div class="tricolor">
  <span class="t1"></span><span class="t2"></span><span class="t3"></span>
  <span class="t4"></span><span class="t2"></span><span class="t1"></span>
</div>

</body></html>"""

# ══════════════════════════════════════════════════════════════════════════════
# VERSO
# ══════════════════════════════════════════════════════════════════════════════
HTML_VERSO = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8">
<style>
{FONTS}
{CSS_PAGE}

body {{
  font-family: 'Lato', Arial, sans-serif;
  background: #FFFBF4;
  color: #141414;
  display: flex;
  flex-direction: column;
}}

.tricolor {{ display: flex; height: 5px; width: 100%; flex-shrink: 0; }}
.tricolor span {{ flex: 1; }}
.t1 {{ background: #C0392B; }}
.t2 {{ background: #C8873A; }}
.t3 {{ background: #3A7D44; }}
.t4 {{ background: #1A1A1A; }}

.header {{
  background: #0D2B1F;
  padding: 4mm 7mm;
  display: flex;
  align-items: center;
  gap: 3.5mm;
  flex-shrink: 0;
}}
.logo-circle {{
  width: 13mm;
  height: 13mm;
  background: white;
  border-radius: 2mm;
  padding: 1mm;
  flex-shrink: 0;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}}
.logo-circle img {{
  width: 100%;
  height: 100%;
  object-fit: contain;
}}
.header-text {{ flex: 1; }}
.header-title {{
  font-family: 'Playfair Display', serif;
  font-size: 6.5pt;
  font-weight: 700;
  color: #C9A84C;
  display: block;
}}
.header-sub {{
  font-size: 5pt;
  color: rgba(255,255,255,0.7);
  display: block;
  margin: 0.5mm 0;
  line-height: 1.3;
}}
.header-phone {{
  font-size: 5.5pt;
  color: #C9A84C;
  font-weight: 700;
  display: block;
}}

.body {{
  padding: 5mm 7mm;
  display: flex;
  flex-direction: column;
  gap: 4mm;
  flex: 1;
}}

.prog-cards {{
  display: flex;
  gap: 2mm;
}}
.prog-card {{
  flex: 1;
  border-radius: 2.5mm;
  padding: 3mm 2.5mm;
  color: white;
}}
.prog-card.mat  {{ background: #C0392B; }}
.prog-card.prim {{ background: #3A7D44; }}
.prog-card.col  {{ background: #1A1A1A; }}
.prog-label {{
  font-size: 5pt;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.5pt;
  display: block;
  margin-bottom: 1mm;
}}
.prog-level {{
  font-family: 'Playfair Display', serif;
  font-size: 5.5pt;
  font-weight: 700;
  display: block;
  margin-bottom: 1.5mm;
  opacity: 0.9;
}}
.prog-detail {{
  font-size: 4.5pt;
  opacity: 0.85;
  line-height: 1.4;
}}

.info-row {{
  display: flex;
  gap: 3mm;
}}
.info-box {{
  flex: 1;
  background: white;
  border: 0.3mm solid rgba(201,168,76,0.3);
  border-radius: 2mm;
  padding: 2.5mm 3mm;
}}
.info-box h4 {{
  font-size: 5.5pt;
  font-weight: 900;
  color: #0D2B1F;
  text-transform: uppercase;
  letter-spacing: 0.5pt;
  margin-bottom: 1.5mm;
  padding-bottom: 1mm;
  border-bottom: 0.3mm solid #C9A84C;
}}
.info-box p {{
  font-size: 5pt;
  color: #444;
  line-height: 1.6;
}}

.partners {{
  display: flex;
  flex-wrap: wrap;
  gap: 1.5mm;
  align-items: center;
}}
.partner-label {{
  font-size: 5pt;
  font-weight: 900;
  color: #0D2B1F;
  text-transform: uppercase;
  letter-spacing: 0.3pt;
  margin-right: 1mm;
  white-space: nowrap;
}}
.badge {{
  background: white;
  border: 0.3mm solid rgba(201,168,76,0.4);
  border-radius: 1mm;
  padding: 0.8mm 2mm;
  font-size: 4.5pt;
  color: #0D2B1F;
  font-weight: 700;
  white-space: nowrap;
}}

.direction {{
  display: flex;
  gap: 3mm;
  align-items: flex-start;
}}
.director-wrap {{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1mm;
  flex-shrink: 0;
}}
.director-photo {{
  width: 15mm;
  height: 15mm;
  border-radius: 50%;
  border: 0.5mm solid #C9A84C;
  background: linear-gradient(135deg, #0D2B1F, #1a4a2a);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 12pt;
  opacity: 0.8;
}}
.director-name {{
  font-size: 5.5pt;
  font-weight: 700;
  color: #C9A84C;
}}
.director-title {{
  font-size: 4pt;
  color: #555;
  text-align: center;
  line-height: 1.3;
}}
.contacts-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5mm;
  flex: 1;
}}
.contact-item {{
  font-size: 5pt;
  color: #333;
  line-height: 1.4;
}}
.contact-item strong {{
  font-size: 5pt;
  color: #0D2B1F;
  display: block;
}}

.cta {{
  background: linear-gradient(135deg, #C0392B, #F0A500);
  border-radius: 2.5mm;
  padding: 4mm 6mm;
  text-align: center;
}}
.cta-main {{
  font-family: 'Playfair Display', serif;
  font-size: 7.5pt;
  font-weight: 900;
  color: white;
  display: block;
}}
.cta-sub {{
  font-size: 5pt;
  color: rgba(255,255,255,0.9);
  display: block;
  margin-top: 1mm;
}}
</style>
</head>
<body>

<div class="header">
  <div class="logo-circle">
    {'<img src="' + LOGO_SRC + '" alt="Logo">' if LOGO_SRC else '<span style="font-size:12pt">🏫</span>'}
  </div>
  <div class="header-text">
    <span class="header-title">Bela Lekkol Montessori</span>
    <span class="header-sub">Programme &amp; Informations pratiques<br>Rentrée 2026–2027</span>
    <span class="header-phone">📞 626 31 31 80</span>
  </div>
</div>

<div class="tricolor">
  <span class="t1"></span><span class="t2"></span><span class="t3"></span>
  <span class="t4"></span><span class="t2"></span><span class="t1"></span>
</div>

<div class="body">

  <div class="prog-cards">
    <div class="prog-card mat">
      <span class="prog-label">Maternelle</span>
      <span class="prog-level">PS · MS · GS</span>
      <span class="prog-detail">Méthode Montessori<br>Éveil &amp; motricité</span>
    </div>
    <div class="prog-card prim">
      <span class="prog-label">Primaire</span>
      <span class="prog-level">CP → CM2</span>
      <span class="prog-detail">Système français<br>MHF / MHM</span>
    </div>
    <div class="prog-card col">
      <span class="prog-label">Collège / Lycée</span>
      <span class="prog-level">6ème → Terminale</span>
      <span class="prog-detail">Franco-guinéen<br>Examens DELF</span>
    </div>
  </div>

  <div class="info-row">
    <div class="info-box">
      <h4>🕐 Horaires</h4>
      <p>Lun–Ven : 7h30–17h00<br>Samedi : 7h30–12h00<br>Garderie disponible<br>Cantine sur place</p>
    </div>
    <div class="info-box">
      <h4>💰 Tarifs</h4>
      <p>Tarifs compétitifs<br>Moins cher du secteur<br>Facilités de paiement<br>Inscription gratuite*</p>
    </div>
  </div>

  <div class="partners">
    <span class="partner-label">Partenaires :</span>
    <span class="badge">Institut Français</span>
    <span class="badge">ISSEG</span>
    <span class="badge">Examens DELF</span>
    <span class="badge">Diplômes FR</span>
    <span class="badge">Diplômes GN</span>
    <span class="badge">IA Éducation</span>
  </div>

  <div class="direction">
    <div class="director-wrap">
      <div class="director-photo">{'<img src="' + ERIC_SRC + '" style="width:100%;height:100%;object-fit:cover;border-radius:50%">' if ERIC_SRC else '👤'}</div>
      <span class="director-name">Éric Didier</span>
      <span class="director-title">Directeur &amp;<br>Conseiller Péd.</span>
    </div>
    <div class="contacts-grid">
      <div class="contact-item">
        <strong>📞 Téléphone</strong>626 31 31 80
      </div>
      <div class="contact-item">
        <strong>📍 Adresse</strong>KIPE, Conakry, Guinée
      </div>
      <div class="contact-item">
        <strong>✉ Email</strong>belalekkol.montessori@gmail.com
      </div>
      <div class="contact-item">
        <strong>📘 Facebook</strong>Bela Lekkol Montessori
      </div>
    </div>
  </div>

  <div class="cta">
    <span class="cta-main">Inscrivez votre enfant !</span>
    <span class="cta-sub">Découvrez notre équipe &amp; notre programme</span>
  </div>

</div>

<div class="tricolor">
  <span class="t1"></span><span class="t2"></span><span class="t3"></span>
  <span class="t4"></span><span class="t2"></span><span class="t1"></span>
</div>

</body></html>"""

# ── Génération PDFs ───────────────────────────────────────────────────────────
CSS_PRINT = CSS(string="@page { size: 154mm 216mm; margin: 0; }")

def gen(html, path, label):
    print(f"  Génération {label}...")
    HTML(string=html, base_url=OUT).write_pdf(
        path, stylesheets=[CSS_PRINT], presentational_hints=True
    )
    kb = os.path.getsize(path) // 1024
    print(f"  ✓ {label} → {path} ({kb} Ko)")

HTML_COMPLET = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<style>{FONTS}{CSS_PAGE}</style></head><body>
{HTML_RECTO.split('<body>',1)[1].rsplit('</body>',1)[0]}
<div style="page-break-before:always">
{HTML_VERSO.split('<body>',1)[1].rsplit('</body>',1)[0]}
</div></body></html>"""

if __name__ == "__main__":
    print("=" * 56)
    print("  Bela Lekkol Montessori — Flyer A5 impression pro")
    print("  154x216mm (A5+bleed 3mm) · Design handoff fidele")
    print("=" * 56)
    gen(HTML_RECTO,   f"{OUT}/flyer_recto_A5.pdf",           "RECTO")
    gen(HTML_VERSO,   f"{OUT}/flyer_verso_A5.pdf",           "VERSO")
    gen(HTML_COMPLET, f"{OUT}/flyer_complet_avec_bleed.pdf", "COMPLET recto+verso")
    print()
    print("=" * 56)
    for f in ["flyer_recto_A5.pdf", "flyer_verso_A5.pdf", "flyer_complet_avec_bleed.pdf"]:
        p = f"{OUT}/{f}"
        if os.path.exists(p):
            print(f"  OK {f} — {os.path.getsize(p)//1024} Ko")
    print("=" * 56)
