"""
Générateur automatique des 35 illustrations — Manuel CE1 Bela Lekkol Montessori
=================================================================================
- Appelle Pollinations.ai via Python (SANS cookies navigateur → pas de blocage auth)
- Sauvegarde directement dans CE1\imgs\
- Saute les images déjà présentes
- Réutilisable pour CP, CE2, CM1, CM2 (changer IMAGES et OUTPUT_DIR)

Lancer : double-cliquer sur GENERER_IMAGES_PYTHON.bat
"""

import urllib.request
import urllib.parse
import os, sys, time

# ─── Configuration ─────────────────────────────────────────────────────────────
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imgs")
WIDTH, HEIGHT = 1024, 768
DELAY = 5          # secondes entre chaque image (poli envers le serveur)
MAX_RETRIES = 2

STYLE = (
    "Illustration de livre de lecture pour enfants de 7 ans, "
    "style aquarelle numerique douce, traits arrondis et expressifs, "
    "couleurs chaudes et lumineuses, personnages enfants africains souriants, "
    "uniforme scolaire bleu et blanc ou tenues locales guineennes, "
    "decor Afrique de l Ouest Guinee, lumiere doree de soleil tropical, "
    "format paysage 4 sur 3, sans texte ni lettres dans l image, "
    "fond legerement texture."
)

IMAGES = [
    # ── PÉRIODE 1 ───────────────────────────────────────────────────────────────
    {"f": "p1s1_rentree",       "seed": 101, "p": "Fillette africaine en uniforme scolaire bleu et blanc marche joyeusement vers son ecole avec son cartable rouge sur le dos accompagnee d un garcon souriant grands manguiers en arriere-plan matin ensoleille de Guinee Conakry cour d ecole visible au fond"},
    {"f": "p1s2_cartable",      "seed": 102, "p": "Garcon africain souriant ouvre fierement son cartable bleu sur un bureau d ecole sort une trousse rouge stylos et cahiers neufs salle de classe lumineuse decoree de cartes colorees tableau noir au fond fenetres ensoleillees"},
    {"f": "p1s3_recreation",    "seed": 103, "p": "Cour d ecole guineenne animee pendant la recreation filles africaines jouent a la corde a sauter garcons jouent au football pres d un grand manguier enfants qui rient soleil tropical maitresse qui surveille"},
    {"f": "p1s4_marche_matin",  "seed": 104, "p": "Femme africaine en tenue traditionnelle coloree et son jeune fils parcourent un grand marche anime de Guinee etals debordants de mangues dorees tomates rouges et legumes verts marchandes souriantes atmosphere matinale lumineuse paniers en rotin"},
    {"f": "p1s5_famille_table", "seed": 105, "p": "Famille guineenne reunie le soir dans une grande cour assis en cercle autour d un grand plat de riz fumant et sauce arachide grand-pere age bienveillant enfants souriants lumiere chaude coucher de soleil ambiance chaleureuse"},
    {"f": "p1s6_bibliotheque",  "seed": 106, "p": "Interieur d une bibliotheque scolaire africaine lumineuse rayons remplis de livres colores garcon africain assis sur un coussin lisant un album illustre avec fascination autres enfants qui choisissent des livres ambiance calme"},
    {"f": "p1s7_village",       "seed": 107, "p": "Vue panoramique de Faranah en Guinee au bord du fleuve Niger cases en banco aux toits de tole baobabs majestueux vieux griot en boubou assis sous un arbre entoure d enfants en cercle qui ecoutent feu de camp ciel etoile"},
    # ── PÉRIODE 2 ───────────────────────────────────────────────────────────────
    {"f": "p2s1_arc_en_ciel",   "seed": 201, "p": "Fillette africaine en robe coloree debout devant sa case bras leves vers un magnifique arc-en-ciel aux couleurs vives au-dessus d un village guineen apres la pluie feuilles de manguiers mouillees sol rouge humide joie"},
    {"f": "p2s2_conte_nuit",    "seed": 202, "p": "Enfants africains assis en cercle serre autour d un vieux griot en boubou blanc nuit etoilee de Guinee feu de bois au centre projetant une lumiere chaude orange expressions d emerveillement sur les visages des enfants"},
    {"f": "p2s3_foret",         "seed": 203, "p": "Deux enfants africains marchent sur un sentier d une foret guineenne dense et luxuriante singes rouges dans les branches papillons colores calao au grand bec en vol lumiere doree filtree a travers le feuillage tropical"},
    {"f": "p2s4_fete_annee",    "seed": 204, "p": "Salle de classe africaine decoree pour une fete de fin d annee enfants en tenues colorees et uniformes sapin decore avec ornements locaux fruits fleurs tropicales parents souriants et applaudissant maitresse au tableau ambiance festive"},
    {"f": "p2s5_pecheur",       "seed": 205, "p": "Vieux pecheur africain debout dans une pirogue en bois sur le fleuve guineen a l aube filets argentes dans l eau translucide crevettes brillantes herons blancs sur les rives reflets dores du soleil levant brume matinale"},
    {"f": "p2s6_ceremonie",     "seed": 206, "p": "Ceremonie scolaire africaine en plein air sous un grand fromager eleve africaine en uniforme recite fierement devant un micro parents et enseignants applaudissent directrice tenant des bulletins estrade decoree de fleurs et drapeaux guineen"},
    {"f": "p2s7_vacances_dec",  "seed": 207, "p": "Groupe d enfants africains joyeux sur une route de savane guineenne petites valises colorees et sacs a dos un vieux car bleu et jaune en arriere-plan paysage de savane verdoyante joie et liberte des vacances"},
    # ── PÉRIODE 3 ───────────────────────────────────────────────────────────────
    {"f": "p3s1_rentree_jan",   "seed": 301, "p": "File d eleves africains en uniforme qui marchent en rang vers leur ecole en janvier arbres aux feuilles seches de la saison seche legere poussiere ocre de l harmattan dans l air nouveaux cahiers sous les bras sourires"},
    {"f": "p3s2_harmattan",     "seed": 302, "p": "Enfants africains dans une rue de village guineen luttant contre un fort vent d harmattan poussiere orange soulevee feuilles seches qui tournoient garcon retenant son chapeau fillette tenant sa jupe ciel voile de sable"},
    {"f": "p3s3_marche",        "seed": 303, "p": "Vue d ensemble plongeante sur un grand marche guineen tres anime rangees de femmes en tenues wax colorees derriere leurs etals pyramides de mangues tomates ignames et epices foule dense et coloree toit de marche lumiere tropicale"},
    {"f": "p3s4_animaux_foret", "seed": 304, "p": "Trois enfants africains s arretent sur un sentier forestier guineen bouche ouverte d emerveillement un singe rouge dans les branches une antilope gracieuse entre les arbres un chimpanze au loin foret dense verte lumiere tamisee"},
    {"f": "p3s5_lettre",        "seed": 305, "p": "Fillette africaine concentree ecrit une lettre a son bureau en bois dans une case guineenne enveloppe blanche et timbre poses a cote fenetre ouverte donnant sur un jardin tropical verdoyant lumiere douce de l apres-midi stylo en main"},
    {"f": "p3s6_cafe",          "seed": 306, "p": "Famille guineenne dans une plantation de cafe en montagne hommes et femmes et enfants cueillant des baies de cafe rouges sur des arbustes verts grands paniers en rotin collines verdoyantes du Fouta Djalon atmosphere de travail joyeux"},
    {"f": "p3s7_berger",        "seed": 307, "p": "Jeune berger africain de 12 ans surveille son troupeau de moutons blancs sur les collines rouges du Fouta Djalon baton de berger paysage majestueux de savane et falaises ocre lumiere doree de fin de journee ciel orange et bleu"},
    # ── PÉRIODE 4 ───────────────────────────────────────────────────────────────
    {"f": "p4s1_journee_femme", "seed": 401, "p": "Ceremonie de la Journee de la Femme en Guinee femmes africaines magnifiques en tenues traditionnelles colorees defilent eleves en uniforme leur offrent des fleurs drapeau guineen rouge-jaune-vert place publique decoree foule festive"},
    {"f": "p4s2_premieres_pluies","seed":402, "p": "Enfants africains dans la cour de leur ecole surprise et joie devant les premieres grosses gouttes de pluie tropicale ciel dramatique gris-violet sol rouge qui commence a fumer un enfant leve les mains vers la pluie un autre court s abriter"},
    {"f": "p4s3_fete_ecole",    "seed": 403, "p": "Grande fete scolaire en plein air dans une ecole guineenne podium colore avec des eleves en costumes traditionnels africains parents spectateurs assis sous le grand fromager banderoles colorees ambiance joyeuse et festive soleil eclatant"},
    {"f": "p4s4_jardin",        "seed": 404, "p": "Groupe d enfants africains en uniforme scolaire arrosent et entretiennent un grand jardin potager scolaire rangees bien ordonnees de tomates rouges aubergines violettes et salades vertes arrosoirs colores soleil matin fierte visible"},
    {"f": "p4s5_pecheurs_fleuve","seed":405, "p": "Trois pecheurs africains adultes dans des pirogues en bois sur un grand fleuve guineen au matin filets tendus dans l eau verte herons blancs perches sur des pieux mangroves sur les rives reflets dores et brume legere ambiance paisible"},
    {"f": "p4s6_case",          "seed": 406, "p": "Scene d interieur chaleureuse d une grande case familiale guineenne en banco femmes qui cuisinent autour d un foyer enfants qui jouent sur des nattes colorees tapis africains aux motifs geometriques poutres en bois lumiere tamisee et doree"},
    {"f": "p4s7_vacances_paques","seed":407, "p": "Enfants africains font joyeusement leurs valises pour les vacances de Paques dans une maison coloree de Guinee mere qui prepare des provisions cocotiers et bougainvillees dans le jardin voiture chargee devant la maison excitation palpable"},
    # ── PÉRIODE 5 ───────────────────────────────────────────────────────────────
    {"f": "p5s1_fete_travail",  "seed": 501, "p": "Defile festif du 1er mai dans une rue principale de Conakry travailleurs guineen avec banderoles colorees rouge et jaune eleves en uniforme brandissant des petits drapeaux guineen immeubles colores ambiance joyeuse et civique"},
    {"f": "p5s2_mangues",       "seed": 502, "p": "Groupe d enfants africains souriants cueillent des mangues dorees et orangees dans un grand manguier charge de fruits sous un ciel bleu certains dans l arbre d autres en bas avec des paniers en rotin jus de mangue qui coule joie de la recolte"},
    {"f": "p5s3_dispensaire",   "seed": 503, "p": "Salle de consultation propre d un dispensaire de village guineen infirmiere africaine en blouse blanche rassurante examine doucement un enfant assis mere souriante et attentive a cote affiches de sante colorees aux murs lumiere naturelle claire"},
    {"f": "p5s4_grande_famille","seed": 504, "p": "Grande reunion de famille africaine dans une vaste cour ombragee trois generations reunies grand-parents parents enfants et bebes tables chargees de plats guineen colores rires et embrassades tenues traditionnelles atmosphere de bonheur"},
    {"f": "p5s5_football",      "seed": 505, "p": "Match de football passionne sur un terrain de terre rouge en Guinee enfants africains en maillots colores rouge contre bleu gardien qui plonge pour arreter un tir supporters enthousiastes sur les bords poussiere de terre rouge soleil"},
    {"f": "p5s6_remise_prix",   "seed": 506, "p": "Ceremonie solennelle de remise des prix scolaires jeune eleve africaine en uniforme monte les marches d une estrade fleurie pour recevoir son diplome des mains de la directrice parents et camarades qui applaudissent chaleureusement drapeaux et fleurs"},
    {"f": "p5s7_grandes_vacances","seed":507,"p": "Explosion de joie des grandes vacances groupe d enfants africains en shorts et robes colorees courent vers un grand fleuve guineen scintillant cartables et livres abandonnes sur l herbe verte bras leves vers le ciel bleu sourires radieux"},
]

# ─── Fonctions ─────────────────────────────────────────────────────────────────
def build_url(img):
    prompt = STYLE + " " + img["p"]
    encoded = urllib.parse.quote(prompt)
    return (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={WIDTH}&height={HEIGHT}&nologo=true&seed={img['seed']}"
    )

def download_image(img, out_path):
    url = build_url(img)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; BelaLekkol-ImageGen/1.0)"
    })
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = resp.read()
            if len(data) < 10000:
                raise ValueError(f"Réponse trop petite ({len(data)} octets) — probable erreur API")
            # Vérifier signature JPEG
            if data[:2] != b'\xff\xd8':
                raise ValueError(f"Pas un JPEG (entête: {data[:4].hex()})")
            with open(out_path, "wb") as f:
                f.write(data)
            return len(data)
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"     ↻ Tentative {attempt} échouée : {e} — nouvelle tentative dans 8s...")
                time.sleep(8)
            else:
                raise

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total = len(IMAGES)
    done = 0
    skipped = 0
    errors = []

    print("=" * 65)
    print(" Bela Lekkol CE1 — Génération des illustrations aquarelle")
    print(f" {total} images · 1024×768 · Pollinations.ai (Python, sans auth)")
    print("=" * 65)
    print()

    for i, img in enumerate(IMAGES, 1):
        filename = img["f"] + ".jpg"
        out_path = os.path.join(OUTPUT_DIR, filename)

        if os.path.exists(out_path):
            size = os.path.getsize(out_path)
            if size > 10000:
                print(f"  [{i:02d}/{total}] ⏭  {filename} déjà présent ({size//1024} Ko) — ignoré")
                skipped += 1
                continue

        print(f"  [{i:02d}/{total}] ⏳ {filename}...")
        t0 = time.time()
        try:
            size = download_image(img, out_path)
            elapsed = time.time() - t0
            print(f"           ✅ {size//1024} Ko en {elapsed:.1f}s → {out_path}")
            done += 1
        except Exception as e:
            print(f"           ❌ ERREUR : {e}")
            errors.append(filename)

        if i < total:
            time.sleep(DELAY)

    print()
    print("=" * 65)
    print(f" ✅ Terminé : {done} générées · {skipped} ignorées · {len(errors)} erreur(s)")
    if errors:
        print(f" ❌ Fichiers en erreur : {', '.join(errors)}")
    print(f" 📁 Dossier : {OUTPUT_DIR}")
    print("=" * 65)
    input("\nAppuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()
