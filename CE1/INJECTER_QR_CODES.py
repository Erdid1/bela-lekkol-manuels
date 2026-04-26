"""
Génère les QR codes Réseau Canopé (33 leçons animées) et les injecte
dans les pages Grammaire / Conjugaison / Vocabulaire des 5 fichiers HTML CE1.

Les QR codes sont encodés en base64 et intégrés directement dans le HTML
(aucun fichier image externe nécessaire).

Lancer : double-cliquer sur INJECTER_QR_CODES.bat
"""

import os, re, base64, io
import qrcode

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── CSS QR codes (injecté une fois par fichier) ───────────────────────────────
QR_CSS = """
/* ════ QR CODES CANOPÉ ════ */
.canope-qr {
  display: inline-flex;
  align-items: center;
  gap: 2.5mm;
  background: #EBF3FB;
  border: 1px solid #2E75B6;
  border-radius: 5px;
  padding: 1.5mm 3mm;
  margin: 1.5mm 0 2mm 0;
  page-break-inside: avoid;
  float: right;
  margin-left: 4mm;
}
.canope-qr img {
  width: 18mm;
  height: 18mm;
  display: block;
  flex-shrink: 0;
}
.canope-qr-label {
  font-size: 6.5pt;
  color: #1a4a8a;
  line-height: 1.5;
  font-weight: 600;
  max-width: 30mm;
}
.canope-qr-label .qr-url {
  font-size: 5.5pt;
  color: #555;
  font-weight: 400;
  word-break: break-all;
}
"""

# ─── Mapping semaines → URLs Canopé ──────────────────────────────────────────
# Structure : { 'gram': url|None, 'conj': url|None, 'voc': url|None }
# null = pas de leçon animée disponible pour cette notion

BASE_URL = "https://rebrand.ly/MHF_CE1_"

def L(code):
    """Construit l'URL complète depuis le code de leçon"""
    return BASE_URL + code if code else None

SEMAINES = {
    "P1": [
        # S1 — La phrase / L'infinitif / L'hyperonyme
        {"gram": L("L01"),  "conj": L("L10b"), "voc": L("L26")},
        # S2 — Types de phrases / Passé-Présent-Futur / Hyperonyme
        {"gram": L("L02a"), "conj": None,       "voc": L("L26")},
        # S3 — Les déterminants / PPF approfond. / Familles de mots
        {"gram": L("L06a"), "conj": None,       "voc": L("L23")},
        # S4 — Sujet et verbe / L'infinitif révision / Pluriel des noms
        {"gram": L("L11"),  "conj": L("L10a"),  "voc": L("L30a")},
        # S5 — Pronoms personnels sujets / PPF révision / Familles de mots
        {"gram": L("L09"),  "conj": None,       "voc": L("L23")},
        # S6 — Accord sujet-verbe / Révision C1+C2 / Préfixes
        {"gram": L("L11"),  "conj": L("L10b"),  "voc": L("L23")},
        # S7 — Bilan P1
        {"gram": L("L01"),  "conj": L("L10b"),  "voc": L("L26")},
    ],
    "P2": [
        # S1 — GN étendu+adjectif / Imparfait être / Synonymes
        {"gram": L("L08a"), "conj": L("L19"),   "voc": L("L24")},
        # S2 — Types de phrases / Imparfait avoir / Antonymes
        {"gram": L("L02a"), "conj": L("L19"),   "voc": L("L25")},
        # S3 — Phrase complexe (et/mais/ou) / Imparfait -ER / Champ lexical
        {"gram": L("L12"),  "conj": L("L20"),   "voc": L("L26")},
        # S4 — Pronoms personnels / Imparfait -ER suite / Suffixes
        {"gram": L("L09"),  "conj": L("L20"),   "voc": L("L23")},
        # S5 — Déterminants art. / Imparfait description / Champ lexical mer
        {"gram": L("L07a"), "conj": L("L20"),   "voc": L("L26")},
        # S6 — Révision GN+types+pronoms / Révision imparfait / Révision vocab
        {"gram": L("L08b"), "conj": L("L19"),   "voc": L("L24")},
        # S7 — Bilan P2
        {"gram": L("L02a"), "conj": L("L20"),   "voc": L("L25")},
    ],
    "P3": [
        # S1 — CC de temps / Présent -ER révision / Préfixes (re- dé- in-)
        {"gram": L("L12"),  "conj": L("L18"),   "voc": L("L23")},
        # S2 — CC de lieu / Présent aller/venir/faire/dire / Homonymes
        {"gram": L("L12"),  "conj": L("L16"),   "voc": None},
        # S3 — COD / Présent être+avoir révision / Champ lexical commerce
        {"gram": L("L12"),  "conj": L("L15"),   "voc": L("L26")},
        # S4 — COI / Présent pouvoir/vouloir/savoir / Niveaux de langue
        {"gram": L("L12"),  "conj": L("L16"),   "voc": L("L26")},
        # S5 — Phrase complexe parce que/quand/si / Futur proche / Épistolaire
        {"gram": L("L12"),  "conj": L("L14"),   "voc": L("L26")},
        # S6 — Révision CC+COD+COI / Révision présent / Agriculture
        {"gram": L("L11"),  "conj": L("L15"),   "voc": L("L23")},
        # S7 — Bilan P3
        {"gram": L("L11"),  "conj": L("L18"),   "voc": L("L24")},
    ],
    "P4": [
        # S1 — PC avec avoir / PC verbes -ER / Familles de mots
        {"gram": L("L21"),  "conj": L("L21"),   "voc": L("L23")},
        # S2 — PC avec être / PC être mouvement / Sens propre et figuré
        {"gram": L("L21"),  "conj": L("L21"),   "voc": L("L24")},
        # S3 — La négation / PC irréguliers / Expressions idiomatiques
        {"gram": L("L04"),  "conj": L("L21"),   "voc": L("L26")},
        # S4 — Phrase interrogative / Révision PC / Mots nature/jardin
        {"gram": L("L03"),  "conj": L("L21"),   "voc": L("L23")},
        # S5 — Révision phrase complexe / Futur simple -ER / Synonymes-antonymes
        {"gram": L("L11"),  "conj": L("L18"),   "voc": L("L24")},
        # S6 — Révision générale P4 / PC+FS révision / Mots invariables
        {"gram": L("L01"),  "conj": L("L21"),   "voc": L("L26")},
        # S7 — Bilan P4
        {"gram": L("L12"),  "conj": L("L21"),   "voc": L("L25")},
    ],
    "P5": [
        # S1 — Révision phrase simple+complexe / FS être/avoir/irréguliers / Champs lexicaux
        {"gram": L("L02a"), "conj": L("L18"),   "voc": L("L26")},
        # S2 — Bilan complet grammaire CE1 / Les 3 temps / Mots composés
        {"gram": L("L01"),  "conj": L("L15"),   "voc": L("L23")},
        # S3 — Révision analyse complète phrase / Révision présent / Vocabulaire médical
        {"gram": L("L11"),  "conj": L("L15"),   "voc": L("L26")},
        # S4 — Révision générale grammaire / Révision tous temps / Révision vocabulaire
        {"gram": L("L01"),  "conj": L("L18"),   "voc": L("L24")},
        # S5 — Écriture texte narratif / Concordance des temps / Champ lexical sport
        {"gram": L("L12"),  "conj": L("L21"),   "voc": L("L26")},
        # S6 — Révision finale CE1 / Révision finale tous temps / Révision finale vocabulaire
        {"gram": L("L01"),  "conj": L("L18"),   "voc": L("L25")},
        # S7 — Bilan général CE1
        {"gram": L("L01"),  "conj": L("L21"),   "voc": L("L26")},
    ],
}

# Noms courts des leçons pour les étiquettes QR
LECON_TITRES = {
    "L01":  "La phrase",
    "L02a": "Types de phrases – décl.",
    "L02b": "Types de phrases – inter.",
    "L02c": "Types de phrases – imp.",
    "L03":  "La phrase interrogative",
    "L04":  "La phrase négative",
    "L05":  "La phrase exclamative",
    "L06a": "Le genre (masculin/féminin)",
    "L06b": "Le genre – suite",
    "L07a": "Le nom",
    "L07b": "Le nom – suite",
    "L08a": "L'adjectif",
    "L08b": "L'adjectif – suite",
    "L09":  "Les pronoms personnels",
    "L10a": "Le verbe",
    "L10b": "L'infinitif",
    "L11":  "Le sujet du verbe",
    "L12":  "Les compléments",
    "L14":  "Le futur proche",
    "L15":  "Présent être et avoir",
    "L16":  "Présent verbes irréguliers",
    "L18":  "Présent verbes en –er",
    "L19":  "Imparfait être et avoir",
    "L20":  "Imparfait verbes en –er",
    "L21":  "Le passé composé",
    "L23":  "Familles de mots",
    "L24":  "Les synonymes",
    "L25":  "Les antonymes",
    "L26":  "Les mots étiquettes",
    "L27":  "La lettre g",
    "L28a": "La lettre c",
    "L30a": "Pluriel des noms",
    "L30b": "Pluriel des noms – suite",
    "L31":  "Pluriel des adjectifs",
    "L32a": "Féminin des noms",
    "L33":  "Féminin des adjectifs",
}

# ─── Génération QR ────────────────────────────────────────────────────────────
_qr_cache = {}

def make_qr_base64(url):
    if url in _qr_cache:
        return _qr_cache[url]
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=5,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1a4a8a", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    _qr_cache[url] = b64
    return b64

def get_titre(url):
    """Extrait le titre lisible depuis l'URL rebrand.ly"""
    code = url.split("MHF_CE1_")[-1] if "MHF_CE1_" in url else url
    return LECON_TITRES.get(code, "Leçon Canopé")

def qr_html_block(url, section_label):
    """Génère le bloc HTML complet pour un QR code"""
    b64   = make_qr_base64(url)
    titre = get_titre(url)
    short = url.replace("https://", "")
    return (
        f'<div class="canope-qr">'
        f'<img src="data:image/png;base64,{b64}" alt="QR Code {titre}">'
        f'<div class="canope-qr-label">'
        f'🎬 Leçon animée Canopé<br>'
        f'<strong>{titre}</strong><br>'
        f'<span class="qr-url">{short}</span>'
        f'</div></div>'
    )

# ─── Injection dans le HTML ───────────────────────────────────────────────────
# Pattern pour trouver un en-tête de section :
#   <div class="sh">📝 Grammaire…</div>
#   <div class="sh">🔄 Conjugaison…</div>
#   <div class="sh">📚 Vocabulaire…</div>

PATTERNS = {
    "gram": re.compile(r'(<div class="sh">📝 Grammaire[^<]*</div>)'),
    "conj": re.compile(r'(<div class="sh">🔄 Conjugaison[^<]*</div>)'),
    "voc":  re.compile(r'(<div class="sh">📚 Vocabulaire[^<]*</div>)'),
}

def inject_into_html(html, semaines_periode):
    """
    Pour chaque semaine de la période, injecte les QR codes
    après les en-têtes de section Grammaire / Conjugaison / Vocabulaire.
    """
    # Trouver toutes les occurrences de chaque section
    gram_matches = list(PATTERNS["gram"].finditer(html))
    conj_matches = list(PATTERNS["conj"].finditer(html))
    voc_matches  = list(PATTERNS["voc"].finditer(html))

    n_sem = len(semaines_periode)
    print(f"    Sections trouvées : {len(gram_matches)} gram, {len(conj_matches)} conj, {len(voc_matches)} voc")

    # Construire la liste des insertions (position, texte)
    # On insère en ordre inverse pour ne pas décaler les positions
    insertions = []

    for i, sem in enumerate(semaines_periode):
        for key, matches in [("gram", gram_matches), ("conj", conj_matches), ("voc", voc_matches)]:
            url = sem.get(key)
            if not url or i >= len(matches):
                continue
            match = matches[i]
            block = qr_html_block(url, key)
            insertions.append((match.end(), "\n" + block + "\n"))

    # Trier par position décroissante
    insertions.sort(key=lambda x: x[0], reverse=True)

    for pos, block in insertions:
        html = html[:pos] + block + html[pos:]

    return html

def process_file(filepath, semaines_periode):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Vérifier si déjà injecté
    if "canope-qr" in html:
        print(f"    ⏭  QR codes déjà présents — ignoré")
        return False

    # 1. Ajouter le CSS
    html = html.replace("</style>", QR_CSS + "\n</style>", 1)
    print(f"    ✅ CSS QR ajouté")

    # 2. Injecter les QR codes
    html = inject_into_html(html, semaines_periode)

    # 3. Sauvegarder
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    return True

# ─── Main ──────────────────────────────────────────────────────────────────────
print("=" * 65)
print(" Injection QR codes Réseau Canopé — Manuel CE1 Bela Lekkol")
print(f" {sum(len(v)*3 for v in SEMAINES.values())} QR codes à générer (max)")
print("=" * 65)

total_ok = 0
for periode, semaines in SEMAINES.items():
    filename = f"MANUEL_CE1_{periode}_Bela_Lekkol_v3.html"
    filepath = os.path.join(BASE, filename)
    print(f"\n  ── {filename}")
    if not os.path.exists(filepath):
        print(f"    ❌ Fichier introuvable !")
        continue
    if process_file(filepath, semaines):
        total_ok += 1
        print(f"    💾 Sauvegardé")
    else:
        print(f"    ⏭  Ignoré (déjà fait)")

print(f"\n{'='*65}")
print(f" ✅ {total_ok}/5 fichiers mis à jour avec les QR codes Canopé")
print(f"{'='*65}")
input("\nAppuyez sur Entrée pour fermer...")
