"""
Injecte les 35 aquarelles + sections "Langage oral" dans les 5 fichiers HTML CE1.
Remplace les placeholders "Illustration à venir" par l'image + 3 questions d'oral.
Structure pédagogique : Je regarde → Je parle → Je lis
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── CSS supplémentaire ────────────────────────────────────────────────────────
NEW_CSS = """
/* ════ ILLUSTRATION BANDEAU ════ */
.illus-bandeau {
  width: 100%;
  height: 58mm;
  overflow: hidden;
  border-radius: 5px;
  margin-bottom: 3mm;
  border: 0.5px solid #ddd;
  page-break-inside: avoid;
}
.illus-bandeau img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
/* ════ LANGAGE ORAL ════ */
.oral-section {
  background: #FFF8E7;
  border-left: 3.5px solid #F9A825;
  padding: 2.5mm 4mm;
  margin-bottom: 3mm;
  border-radius: 0 4px 4px 0;
  page-break-inside: avoid;
}
.oral-title {
  font-size: 8.5pt;
  font-weight: 700;
  color: #E65100;
  margin-bottom: 1.5mm;
  letter-spacing: 0.3px;
}
.oral-questions {
  margin: 0;
  padding-left: 5mm;
}
.oral-questions li {
  font-size: 8.5pt;
  color: #4E342E;
  margin-bottom: 1mm;
  line-height: 1.45;
}
"""

# ─── Données : image + 3 questions d'oral par semaine ─────────────────────────
# Structure : [img_slug, titre_alt, [q1_observation, q2_description, q3_interprétation]]
PERIODES = {
    "P1": [
        ["p1s1_rentree",       "La rentrée de septembre",
         ["Que vois-tu sur cette image ?",
          "Décris les personnages et le lieu où ils se trouvent.",
          "Que ressent Aminata ce premier matin de CE1 ?"]],
        ["p1s2_cartable",      "Mon cartable",
         ["Que vois-tu dans le cartable et sur le bureau ?",
          "Décris la salle de classe en arrière-plan.",
          "Pourquoi Kofi est-il si fier de son cartable ?"]],
        ["p1s3_recreation",    "La récréation",
         ["Quels jeux pratiquent les enfants dans la cour ?",
          "Décris ce que font les filles et ce que font les garçons.",
          "Comment se sentent ces enfants ? Comment le sais-tu ?"]],
        ["p1s4_marche_matin",  "Au marché de Kindia",
         ["Quels fruits et légumes vois-tu sur les étals ?",
          "Décris la marchande et ses paniers.",
          "Pourquoi Sékou a-t-il les yeux brillants ?"]],
        ["p1s5_famille_table", "Le repas en famille",
         ["Qui vois-tu autour du grand plat ?",
          "Décris l'ambiance et les couleurs de la scène.",
          "Que pourrait raconter grand-père Mamadou ce soir ?"]],
        ["p1s6_bibliotheque",  "La bibliothèque",
         ["Que font les enfants dans cette salle ?",
          "Décris les rayons et l'atmosphère de la bibliothèque.",
          "Quel livre choisirais-tu et pourquoi ?"]],
        ["p1s7_village",       "Village de Faranah",
         ["Que vois-tu dans ce village au bord du fleuve ?",
          "Décris le griot et les enfants autour de lui.",
          "Qu'est-ce qu'un griot ? Que raconte-t-il selon toi ?"]],
    ],
    "P2": [
        ["p2s1_arc_en_ciel",   "L'arc-en-ciel",
         ["Que vois-tu dans le ciel après la pluie ?",
          "Décris la fillette et ce qu'elle ressent.",
          "Pourquoi l'arc-en-ciel rend-il les enfants heureux ?"]],
        ["p2s2_conte_nuit",    "Le soir du conte",
         ["Qui raconte l'histoire ? Où se passent la scène ?",
          "Décris les visages des enfants qui écoutent.",
          "Quel conte le griot pourrait-il raconter selon toi ?"]],
        ["p2s3_foret",         "La forêt guinéenne",
         ["Quels animaux vois-tu dans cette forêt ?",
          "Décris la lumière et les couleurs de la forêt.",
          "Comment se sentent les deux enfants sur le sentier ?"]],
        ["p2s4_fete_annee",    "La fête de fin d'année",
         ["Comment la classe est-elle décorée pour la fête ?",
          "Décris les costumes et les expressions des enfants.",
          "Que ressent-on à la fin de l'année scolaire ?"]],
        ["p2s5_pecheur",       "Le pêcheur de crevettes",
         ["Que fait le vieux pêcheur sur sa pirogue ?",
          "Décris le fleuve au lever du soleil.",
          "Pourquoi le métier de pêcheur demande-t-il du courage ?"]],
        ["p2s6_ceremonie",     "La cérémonie scolaire",
         ["Que se passe-t-il sur l'estrade de cette cérémonie ?",
          "Décris l'élève qui prend la parole et son attitude.",
          "As-tu déjà participé à une cérémonie à l'école ? Raconte."]],
        ["p2s7_vacances_dec",  "Les vacances de décembre",
         ["Que portent ces enfants joyeux sur la route ?",
          "Décris le paysage et le véhicule en arrière-plan.",
          "Où ces enfants vont-ils selon toi ? Qui vont-ils retrouver ?"]],
    ],
    "P3": [
        ["p3s1_rentree_jan",   "La rentrée de janvier",
         ["Quelle saison vois-tu dans ce paysage ?",
          "Décris les uniformes et les accessoires des élèves.",
          "En quoi cette rentrée de janvier ressemble-t-elle à celle de septembre ?"]],
        ["p3s2_harmattan",     "Le vent d'harmattan",
         ["Quel effet le vent a-t-il sur les enfants et les feuilles ?",
          "Décris le ciel et les couleurs de cette scène.",
          "As-tu déjà ressenti le vent d'harmattan ? Décris ta sensation."]],
        ["p3s3_marche",        "Le grand marché",
         ["Que vendent les marchandes sur leurs étals ?",
          "Décris les couleurs des tenues et des marchandises.",
          "Quel étal t'attirerait le plus et pourquoi ?"]],
        ["p3s4_animaux_foret", "Les animaux de la forêt",
         ["Quels animaux surprennent les trois enfants ?",
          "Décris les expressions de surprise sur leurs visages.",
          "Que ferais-tu si tu rencontrais un singe rouge en forêt ?"]],
        ["p3s5_lettre",        "La lettre d'Aminata",
         ["Que tient Aminata dans sa main ? Où est-elle ?",
          "Décris la lumière et le jardin visible par la fenêtre.",
          "À qui Aminata écrit-elle cette lettre selon toi ?"]],
        ["p3s6_cafe",          "La récolte du café",
         ["Que font les membres de la famille dans la plantation ?",
          "Décris les collines du Fouta Djalon en arrière-plan.",
          "Pourquoi est-il important que toute la famille travaille ensemble ?"]],
        ["p3s7_berger",        "Le berger du Fouta",
         ["Que garde ce jeune berger sur les collines ?",
          "Décris le paysage : les couleurs, les formes, la lumière.",
          "Quel est le quotidien d'un berger ? Raconte une de ses journées."]],
    ],
    "P4": [
        ["p4s1_journee_femme", "La Journée de la Femme",
         ["Que portent les femmes dans ce défilé ?",
          "Décris les drapeaux, les fleurs et la place publique.",
          "Pourquoi célèbre-t-on la Journée de la Femme selon toi ?"]],
        ["p4s2_premieres_pluies","Les premières pluies",
         ["Comment les enfants réagissent-ils devant la pluie ?",
          "Décris le ciel et le sol mouillé.",
          "Qu'est-ce que la pluie apporte à la nature et aux gens ?"]],
        ["p4s3_fete_ecole",    "La fête de l'école",
         ["Que se passe-t-il sur le podium ?",
          "Décris les costumes des élèves et les spectateurs.",
          "As-tu déjà participé à une fête d'école ? Qu'as-tu fait ?"]],
        ["p4s4_jardin",        "Le jardin potager",
         ["Quels légumes poussent dans ce jardin scolaire ?",
          "Décris ce que font les élèves avec leurs arrosoirs.",
          "Pourquoi est-il utile d'avoir un jardin potager à l'école ?"]],
        ["p4s5_pecheurs_fleuve","Les pêcheurs du fleuve",
         ["Combien de pirogues vois-tu ? Que font les pêcheurs ?",
          "Décris le fleuve, la brume et les hérons blancs.",
          "Pourquoi le fleuve est-il si important pour les gens de Guinée ?"]],
        ["p4s6_case",          "La case familiale",
         ["Que se passe-t-il à l'intérieur de cette case ?",
          "Décris les objets, les tapis et la lumière.",
          "En quoi la case ressemble-t-elle ou diffère-t-elle de ta maison ?"]],
        ["p4s7_vacances_paques","Les vacances de Pâques",
         ["Que fait cette famille pour se préparer au départ ?",
          "Décris le jardin et la voiture chargée.",
          "Où cette famille va-t-elle selon toi ? Chez qui ?"]],
    ],
    "P5": [
        ["p5s1_fete_travail",  "La Fête du Travail",
         ["Que brandissent les participants de ce défilé ?",
          "Décris les drapeaux guinéens et les banderoles colorées.",
          "Pourquoi célèbre-t-on la Fête du Travail le 1er mai ?"]],
        ["p5s2_mangues",       "La saison des mangues",
         ["Comment les enfants cueillent-ils les mangues ?",
          "Décris les couleurs du manguier et des fruits.",
          "Qu'est-ce que la saison des mangues représente pour les familles guinéennes ?"]],
        ["p5s3_dispensaire",   "Au dispensaire",
         ["Que fait l'infirmière ? Comment est-elle habillée ?",
          "Décris l'expression de l'enfant et celle de sa mère.",
          "Pourquoi est-il important d'aller au dispensaire quand on est malade ?"]],
        ["p5s4_grande_famille","La grande famille",
         ["Combien de générations vois-tu sur cette image ?",
          "Décris les plats, les tenues et l'atmosphère.",
          "Raconte un moment de fête en famille que tu as vécu."]],
        ["p5s5_football",      "Le match de football",
         ["Décris l'action de jeu : qui attaque, qui défend ?",
          "Décris le terrain, les maillots et les supporters.",
          "Quel sport pratiques-tu ? Explique comment on joue."]],
        ["p5s6_remise_prix",   "La remise des prix",
         ["Que reçoit l'élève sur l'estrade ?",
          "Décris les expressions des parents et des camarades.",
          "Comment se sent-on quand on reçoit un prix ? Pourquoi mérite-t-on d'être récompensé ?"]],
        ["p5s7_grandes_vacances","Les grandes vacances !",
         ["Que font les enfants avec leurs cartables et leurs livres ?",
          "Décris le fleuve, le ciel et la joie visible sur les visages.",
          "Qu'as-tu envie de faire pendant les grandes vacances ?"]],
    ],
}

# ─── Pattern du placeholder ────────────────────────────────────────────────────
# Le placeholder est un div contenant "Illustration à venir"
PLACEHOLDER_PATTERN = re.compile(
    r'<div[^>]*style="[^"]*width:100%[^"]*min-height:[^"]*"[^>]*>.*?Illustration à venir.*?</div>',
    re.DOTALL
)

def build_injection(img_slug, alt_text, questions):
    q_items = "\n    ".join(f"<li>{q}</li>" for q in questions)
    return f"""<div class="illus-bandeau">
  <img src="imgs/{img_slug}.jpg" alt="{alt_text}">
</div>
<div class="oral-section">
  <div class="oral-title">🗣 Langage oral — J'observe et je parle</div>
  <ol class="oral-questions">
    {q_items}
  </ol>
</div>"""

def process_file(filepath, semaines):
    print(f"\n  Traitement de : {os.path.basename(filepath)}")
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Ajouter le CSS
    if "illus-bandeau" not in html:
        html = html.replace("</style>", NEW_CSS + "\n</style>", 1)
        print("    ✅ CSS ajouté")
    else:
        print("    ⏭  CSS déjà présent")

    # 2. Trouver tous les placeholders
    placeholders = list(PLACEHOLDER_PATTERN.finditer(html))
    print(f"    Placeholders trouvés : {len(placeholders)}/7")

    if len(placeholders) != len(semaines):
        print(f"    ⚠  ATTENTION : {len(placeholders)} placeholders pour {len(semaines)} semaines !")

    # 3. Remplacer en ordre inverse (pour ne pas décaler les positions)
    for i, match in enumerate(reversed(placeholders)):
        sem_index = len(semaines) - 1 - i
        img_slug, alt_text, questions = semaines[sem_index]
        injection = build_injection(img_slug, alt_text, questions)
        html = html[:match.start()] + injection + html[match.end():]
        print(f"    ✅ S{sem_index+1} → {img_slug}.jpg injectée")

    # 4. Sauvegarder
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"    💾 Fichier sauvegardé")

# ─── Main ──────────────────────────────────────────────────────────────────────
print("=" * 65)
print(" Injection images + langage oral — Manuel CE1 Bela Lekkol")
print("=" * 65)

for periode, semaines in PERIODES.items():
    filename = f"MANUEL_CE1_{periode}_Bela_Lekkol_v3.html"
    filepath = os.path.join(BASE, filename)
    if os.path.exists(filepath):
        process_file(filepath, semaines)
    else:
        print(f"\n  ❌ Fichier introuvable : {filename}")

print("\n" + "=" * 65)
print(" ✅ Injection terminée ! Ouvrez les HTML pour vérifier.")
print("=" * 65)
input("\nAppuyez sur Entrée pour fermer...")
