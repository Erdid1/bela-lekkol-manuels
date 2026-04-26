"""
Injecte le contenu pédagogique des 33 leçons Canopé (règle "Je retiens" + exemples)
dans les 5 fichiers HTML CE1, directement sous chaque QR code existant.

Détecte le code de leçon depuis <span class="qr-url">rebrand.ly/MHF_CE1_LXX</span>
et insère le bloc "Je retiens" correspondant.

Lancer : double-cliquer sur INJECTER_LECONS_MHF.bat
"""

import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# ─── CSS "Je retiens" ──────────────────────────────────────────────────────────
LECON_CSS = """
/* ════ BLOCS LEÇON MHF ════ */
.lecon-retiens {
  background: white;
  border: 1.5px solid #2E75B6;
  border-radius: 5px;
  padding: 2.5mm 3.5mm;
  margin: 2mm 0 3mm 0;
  page-break-inside: avoid;
  clear: both;
}
.lecon-retiens-title {
  font-size: 7.5pt;
  font-weight: 700;
  color: #1F4E79;
  margin-bottom: 1.5mm;
  padding-bottom: 1mm;
  border-bottom: 1px solid #BDD7EE;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}
.lecon-retiens-body {
  font-size: 8pt;
  color: #222;
  line-height: 1.55;
}
.lecon-retiens-body .regle {
  margin-bottom: 1.5mm;
}
.lecon-retiens-body .exemple {
  font-style: italic;
  color: #1a4a8a;
  margin-left: 3mm;
  margin-bottom: 1mm;
}
.lecon-retiens-body .tableau {
  width: 100%;
  border-collapse: collapse;
  font-size: 7.5pt;
  margin-top: 1.5mm;
}
.lecon-retiens-body .tableau td {
  border: 0.5px solid #ccc;
  padding: 0.8mm 2mm;
  text-align: center;
}
.lecon-retiens-body .tableau td:first-child {
  text-align: left;
  font-weight: 600;
  background: #EBF3FB;
  width: 22%;
}
"""

# ─── Contenu des 33 leçons MHF ────────────────────────────────────────────────
# Clé : code leçon (L01, L02a…), valeur : HTML du bloc "Je retiens"

def retiens(titre, contenu_html):
    return (f'<div class="lecon-retiens">'
            f'<div class="lecon-retiens-title">📖 Je retiens — {titre}</div>'
            f'<div class="lecon-retiens-body">{contenu_html}</div>'
            f'</div>')

LECONS = {

"L01": retiens("La phrase",
  '<div class="regle">Une phrase commence par une <strong>majuscule</strong>, '
  'se termine par un <strong>point</strong> et a un <strong>sens complet</strong>.</div>'
  '<div class="exemple">✏ Les enfants arrivent à l\'école.</div>'
  '<div class="regle">Signes de ponctuation : point . &nbsp;|&nbsp; '
  'point d\'interrogation ? &nbsp;|&nbsp; point d\'exclamation !</div>'),

"L02a": retiens("Les types de phrases",
  '<div class="regle"><strong>Déclarative</strong> : donne une information → point.<br>'
  '<strong>Interrogative</strong> : pose une question → ?<br>'
  '<strong>Impérative</strong> : donne un ordre ou un conseil → point ou !</div>'
  '<div class="exemple">Aminata mange à la cantine.&nbsp; / &nbsp;'
  'Viens-tu à l\'école ?&nbsp; / &nbsp; Range ton cartable !</div>'),

"L02b": retiens("La phrase interrogative",
  '<div class="regle">La phrase interrogative <strong>pose une question</strong>. '
  'Elle se termine par <strong>?</strong></div>'
  '<div class="exemple">Est-ce que tu viens à l\'école ? &nbsp;/ &nbsp;Viens-tu ?</div>'
  '<div class="regle">Mots interrogatifs : Qui ? Quand ? Où ? Pourquoi ? Comment ?</div>'),

"L02c": retiens("La phrase impérative",
  '<div class="regle">La phrase impérative exprime <strong>un ordre, un conseil ou une interdiction</strong>. '
  'Elle se termine par un point ou un point d\'exclamation.</div>'
  '<div class="exemple">Range tes affaires ! &nbsp;/ &nbsp;Ne cours pas dans les couloirs.</div>'),

"L03": retiens("La phrase interrogative",
  '<div class="regle">Elle pose une question et se termine par <strong>?</strong><br>'
  'Pour transformer : <strong>Est-ce que… ?</strong> ou <strong>inverser sujet-verbe</strong></div>'
  '<div class="exemple">Tu viens. → Est-ce que tu viens ? → Viens-tu ?</div>'
  '<div class="regle">Mots interrogatifs : Qui ? Où ? Quand ? Pourquoi ? Comment ?</div>'),

"L04": retiens("La phrase négative",
  '<div class="regle">Forme positive → forme négative : <strong>ne … pas</strong> '
  '(n\'…pas devant voyelle).</div>'
  '<div class="exemple">Kofi mange. → Kofi <em>ne</em> mange <em>pas</em>.</div>'
  '<div class="regle">Au passé composé : ne + auxiliaire + pas + participe.<br>'
  '<em>Il n\'a pas mangé.</em></div>'),

"L05": retiens("La phrase exclamative",
  '<div class="regle">La phrase exclamative exprime <strong>une émotion forte</strong> '
  '(joie, surprise, ordre). Elle se termine par <strong>!</strong></div>'
  '<div class="exemple">Comme il fait beau ! &nbsp;/ &nbsp;Quelle belle journée !</div>'),

"L06a": retiens("Le déterminant",
  '<div class="regle">Le déterminant <strong>accompagne le nom</strong>. '
  'Il indique le genre (masculin/féminin) et le nombre (singulier/pluriel).</div>'
  '<div class="exemple">un manguier · une case · le fleuve · les enfants · mon cartable</div>'
  '<div class="regle">Articles définis : le, la, les, l\' &nbsp;|&nbsp; '
  'indéfinis : un, une, des</div>'),

"L06b": retiens("Le genre des noms",
  '<div class="regle">Un nom est <strong>masculin</strong> (le, un) ou <strong>féminin</strong> (la, une).</div>'
  '<div class="exemple">le garçon / la fille &nbsp;· &nbsp; un lion / une lionne</div>'
  '<div class="regle">Pour former le féminin : on ajoute souvent un <strong>e</strong> '
  'ou on change la terminaison.</div>'),

"L07a": retiens("Le nom",
  '<div class="regle">Le <strong>nom commun</strong> désigne une personne, un animal, '
  'une chose ou un lieu. Il est accompagné d\'un déterminant.</div>'
  '<div class="exemple">un élève · un singe · un manguier · le marché</div>'
  '<div class="regle">Le <strong>nom propre</strong> commence par une majuscule.</div>'
  '<div class="exemple">Aminata · Conakry · la Guinée</div>'),

"L07b": retiens("Le nom — genre et nombre",
  '<div class="regle">Le nom varie en <strong>genre</strong> (masc./fém.) '
  'et en <strong>nombre</strong> (sing./plur.).</div>'
  '<div class="exemple">un enfant → des enfants · le cahier → les cahiers</div>'),

"L08a": retiens("L'adjectif qualificatif",
  '<div class="regle">L\'adjectif <strong>donne des précisions sur le nom</strong>. '
  'Il s\'accorde en genre et en nombre avec le nom.</div>'
  '<div class="exemple">un beau manguier · de jolies fleurs · le vieux griot</div>'
  '<div class="regle">Il peut être placé avant ou après le nom.</div>'),

"L08b": retiens("L'accord de l'adjectif",
  '<div class="regle">L\'adjectif s\'accorde avec le nom : même genre et même nombre.</div>'
  '<table class="tableau"><tr><td></td><td>Masculin</td><td>Féminin</td></tr>'
  '<tr><td>Singulier</td><td>grand</td><td>grande</td></tr>'
  '<tr><td>Pluriel</td><td>grands</td><td>grandes</td></tr></table>'),

"L09": retiens("Les pronoms personnels sujets",
  '<div class="regle">Le pronom personnel <strong>remplace un groupe nominal sujet</strong> '
  'pour éviter les répétitions.</div>'
  '<table class="tableau">'
  '<tr><td>je / j\'</td><td>tu</td><td>il / elle / on</td></tr>'
  '<tr><td>nous</td><td>vous</td><td>ils / elles</td></tr>'
  '</table>'
  '<div class="exemple">Aminata lit. → <em>Elle</em> lit.</div>'),

"L10a": retiens("Le verbe",
  '<div class="regle">Le verbe <strong>indique une action ou un état</strong>. '
  'Il change de forme selon la personne et le temps.</div>'
  '<div class="exemple">Les enfants <em>jouent</em> dans la cour. '
  '(action) &nbsp;/ &nbsp;Kofi <em>est</em> content. (état)</div>'),

"L10b": retiens("L'infinitif",
  '<div class="regle">L\'infinitif est la <strong>forme de base du verbe</strong> '
  '(non conjuguée). Il se termine en <strong>-er, -ir, -re, -oir</strong>.</div>'
  '<div class="exemple">lire · écrire · chanter · finir · voir</div>'
  '<div class="regle">Après un verbe conjugué, le deuxième verbe est à l\'infinitif.</div>'
  '<div class="exemple">Je veux <em>lire</em>. / Elle aime <em>chanter</em>.</div>'),

"L11": retiens("Le sujet du verbe",
  '<div class="regle">Le sujet <strong>fait l\'action</strong> exprimée par le verbe. '
  'Pour le trouver : poser la question <strong>« Qui est-ce qui… ? »</strong></div>'
  '<div class="exemple">La maîtresse écrit au tableau. '
  '→ <em>Qui est-ce qui</em> écrit ? → La maîtresse.</div>'
  '<div class="regle">Le sujet peut être un nom, un groupe nominal ou un pronom.</div>'),

"L12": retiens("Les compléments",
  '<div class="regle">Les compléments <strong>apportent des précisions</strong> '
  'sur le temps, le lieu ou l\'action.</div>'
  '<div class="regle">• CC de temps : <em>quand ?</em> → Hier, Aminata lisait.<br>'
  '• CC de lieu : <em>où ?</em> → Elle lit dans la cour.<br>'
  '• COD : <em>quoi ?</em> → Elle lit <em>un livre</em>.</div>'
  '<div class="regle">Les CC peuvent souvent être déplacés dans la phrase.</div>'),

"L13": retiens("Passé, présent, futur",
  '<div class="regle">• <strong>Passé</strong> : action déjà faite → hier, avant<br>'
  '• <strong>Présent</strong> : action en cours → maintenant, aujourd\'hui<br>'
  '• <strong>Futur</strong> : action à venir → demain, bientôt</div>'
  '<div class="exemple">Hier, Kofi <em>est allé</em> au marché. (passé)<br>'
  'Aujourd\'hui, il <em>joue</em> avec ses amis. (présent)<br>'
  'Demain, il <em>ira</em> à l\'école. (futur)</div>'),

"L14": retiens("Le présent des verbes en -er",
  '<div class="regle">Les verbes en <strong>-er</strong> se conjuguent au présent '
  'avec les terminaisons : <strong>-e, -es, -e, -ons, -ez, -ent</strong></div>'
  '<table class="tableau">'
  '<tr><td>je</td><td>chant<strong>e</strong></td><td>nous</td><td>chant<strong>ons</strong></td></tr>'
  '<tr><td>tu</td><td>chant<strong>es</strong></td><td>vous</td><td>chant<strong>ez</strong></td></tr>'
  '<tr><td>il/elle</td><td>chant<strong>e</strong></td><td>ils/elles</td><td>chant<strong>ent</strong></td></tr>'
  '</table>'),

"L15": retiens("Présent de être et avoir",
  '<table class="tableau">'
  '<tr><td>je suis</td><td>j\'ai</td></tr>'
  '<tr><td>tu es</td><td>tu as</td></tr>'
  '<tr><td>il/elle est</td><td>il/elle a</td></tr>'
  '<tr><td>nous sommes</td><td>nous avons</td></tr>'
  '<tr><td>vous êtes</td><td>vous avez</td></tr>'
  '<tr><td>ils/elles sont</td><td>ils/elles ont</td></tr>'
  '</table>'),

"L16": retiens("Présent des verbes irréguliers",
  '<div class="regle">Certains verbes très utilisés ont un présent irrégulier '
  'à apprendre par cœur.</div>'
  '<table class="tableau">'
  '<tr><td>aller</td><td>je vais · tu vas · il va · nous allons · ils vont</td></tr>'
  '<tr><td>venir</td><td>je viens · tu viens · il vient · nous venons</td></tr>'
  '<tr><td>faire</td><td>je fais · tu fais · il fait · nous faisons · ils font</td></tr>'
  '<tr><td>pouvoir</td><td>je peux · tu peux · il peut · nous pouvons</td></tr>'
  '</table>'),

"L17": retiens("Futur simple de être et avoir",
  '<table class="tableau">'
  '<tr><td>je serai</td><td>je/j\'aurai</td></tr>'
  '<tr><td>tu seras</td><td>tu auras</td></tr>'
  '<tr><td>il/elle sera</td><td>il/elle aura</td></tr>'
  '<tr><td>nous serons</td><td>nous aurons</td></tr>'
  '<tr><td>vous serez</td><td>vous aurez</td></tr>'
  '<tr><td>ils/elles seront</td><td>ils/elles auront</td></tr>'
  '</table>'),

"L18": retiens("Imparfait des verbes en -er",
  '<div class="regle">L\'imparfait décrit une <strong>action passée répétée ou durable</strong>. '
  'Terminaisons : <strong>-ais, -ais, -ait, -ions, -iez, -aient</strong></div>'
  '<table class="tableau">'
  '<tr><td>je</td><td>chant<strong>ais</strong></td><td>nous</td><td>chant<strong>ions</strong></td></tr>'
  '<tr><td>tu</td><td>chant<strong>ais</strong></td><td>vous</td><td>chant<strong>iez</strong></td></tr>'
  '<tr><td>il/elle</td><td>chant<strong>ait</strong></td><td>ils/elles</td><td>chant<strong>aient</strong></td></tr>'
  '</table>'),

"L19": retiens("Imparfait de être et avoir",
  '<table class="tableau">'
  '<tr><td>j\'étais</td><td>j\'avais</td></tr>'
  '<tr><td>tu étais</td><td>tu avais</td></tr>'
  '<tr><td>il/elle était</td><td>il/elle avait</td></tr>'
  '<tr><td>nous étions</td><td>nous avions</td></tr>'
  '<tr><td>vous étiez</td><td>vous aviez</td></tr>'
  '<tr><td>ils/elles étaient</td><td>ils/elles avaient</td></tr>'
  '</table>'),

"L20": retiens("Imparfait des verbes en -er",
  '<div class="regle">Même conjugaison que les verbes en -er avec '
  'terminaisons <strong>-ais, -ais, -ait, -ions, -iez, -aient</strong></div>'
  '<div class="exemple">Chaque soir, Aminata <em>lisait</em> un livre. '
  '/ Les enfants <em>jouaient</em> dans la cour.</div>'),

"L21": retiens("Le passé composé",
  '<div class="regle">Le passé composé = <strong>auxiliaire (avoir ou être) conjugué au présent '
  '+ participe passé</strong>.</div>'
  '<div class="exemple">Kofi <em>a mangé</em> une mangue. '
  '/ Aminata <em>est allée</em> au marché.</div>'
  '<div class="regle">Avec <strong>être</strong> : le participe s\'accorde avec le sujet.<br>'
  'Verbes mouvement : aller, venir, partir, arriver, entrer, sortir, monter, descendre…</div>'),

"L23": retiens("Les familles de mots",
  '<div class="regle">Les mots d\'une même famille partagent un <strong>radical commun</strong> '
  'et ont une idée en commun.</div>'
  '<div class="exemple">dent → édenté · dentiste · dentition · dentifrice</div>'
  '<div class="regle">On peut ajouter un préfixe (avant) ou un suffixe (après) au radical.</div>'
  '<div class="exemple">re-lire · dé-faire · in-utile &nbsp;·&nbsp; lect-ure · chant-eur</div>'),

"L24": retiens("Les synonymes",
  '<div class="regle">Les synonymes sont des mots qui ont <strong>le même sens ou un sens proche</strong>. '
  'Ils sont de la même classe grammaticale.</div>'
  '<div class="exemple">bateau = navire &nbsp;·&nbsp; gentil = adorable &nbsp;·&nbsp; '
  'manger = grignoter &nbsp;·&nbsp; beau = joli</div>'),

"L25": retiens("Les antonymes",
  '<div class="regle">Les antonymes sont des mots qui ont <strong>un sens contraire</strong>. '
  'Ils sont de la même classe grammaticale.</div>'
  '<div class="exemple">jour ≠ nuit &nbsp;·&nbsp; petit ≠ grand &nbsp;·&nbsp; '
  'adorer ≠ détester &nbsp;·&nbsp; chaud ≠ froid</div>'),

"L26": retiens("Les mots étiquettes (hyperonymes)",
  '<div class="regle">Un <strong>mot étiquette</strong> (ou hyperonyme) désigne une catégorie '
  'qui regroupe plusieurs éléments ayant une idée commune.</div>'
  '<div class="exemple">mangue, banane, papaye → <strong>fruits</strong><br>'
  'lion, singe, éléphant → <strong>animaux</strong><br>'
  'lire, écrire, compter → <strong>activités scolaires</strong></div>'),

"L27": retiens("La lettre g",
  '<div class="regle">• Devant <strong>a, o, u</strong> ou une consonne : son [g] dur → <em>gare, gorge, guide</em><br>'
  '• Devant <strong>e, i, y</strong> : son [j] doux → <em>girafe, géant</em><br>'
  '• Pour garder le son [g] devant e/i : on écrit <strong>gu</strong> → <em>guêpe, guitare</em></div>'),

"L28a": retiens("La lettre c",
  '<div class="regle">• Devant <strong>a, o, u</strong> ou une consonne : son [k] dur → <em>canard, corps</em><br>'
  '• Devant <strong>e, i, y</strong> : son [s] → <em>cerise, cible</em><br>'
  '• Pour le son [s] devant a/o/u : on écrit <strong>ç</strong> → <em>garçon, leçon</em></div>'),

"L29": retiens("La lettre s",
  '<div class="regle">• En début de mot ou après consonne : son [s] → <em>soleil, maison</em><br>'
  '• Entre deux voyelles : son [z] → <em>rose, maison</em><br>'
  '• Pour le son [s] entre voyelles : on écrit <strong>ss</strong> → <em>poisson, dessert</em></div>'),

"L30a": retiens("Le pluriel des noms",
  '<div class="regle">En général, on forme le pluriel en ajoutant un <strong>s</strong> au nom singulier.</div>'
  '<div class="exemple">un cahier → des cahier<strong>s</strong> &nbsp;·&nbsp; '
  'une école → des école<strong>s</strong></div>'
  '<div class="regle">Cas particuliers : -eau → -eaux &nbsp;|&nbsp; '
  '-al → -aux &nbsp;|&nbsp; -s,-x,-z → invariable</div>'
  '<div class="exemple">gâteau → gâteaux &nbsp;·&nbsp; cheval → chevaux &nbsp;·&nbsp; voix → voix</div>'),

"L30b": retiens("Le pluriel des noms — cas particuliers",
  '<div class="regle">• Noms en <strong>-eau</strong> → <strong>-eaux</strong> : gâteau → gâteaux<br>'
  '• Noms en <strong>-al</strong> → <strong>-aux</strong> : cheval → chevaux<br>'
  '• Noms en <strong>-s, -x, -z</strong> : ne changent pas → une voix → des voix</div>'),

"L31": retiens("Le pluriel des adjectifs",
  '<div class="regle">En général, on ajoute un <strong>s</strong> à l\'adjectif au pluriel.</div>'
  '<div class="exemple">un beau manguier → de beaux manguiers<br>'
  'une grande case → de grandes cases</div>'),

"L32a": retiens("Le féminin des noms",
  '<div class="regle">En général, on forme le féminin en ajoutant un <strong>e</strong> au nom masculin.</div>'
  '<div class="exemple">un ami → une ami<strong>e</strong> &nbsp;·&nbsp; '
  'un élève → une élève</div>'
  '<div class="regle">Cas spéciaux : -er → -ère &nbsp;|&nbsp; -eur → -euse &nbsp;|&nbsp; '
  '-teur → -trice</div>'),

"L33": retiens("Le féminin des adjectifs",
  '<div class="regle">En général, on ajoute <strong>e</strong> à l\'adjectif masculin.</div>'
  '<div class="exemple">petit → petite &nbsp;·&nbsp; joli → jolie &nbsp;·&nbsp; '
  'grand → grande</div>'
  '<div class="regle">Cas spéciaux : -eux → -euse &nbsp;|&nbsp; '
  '-eur → -euse &nbsp;|&nbsp; -er → -ère</div>'),

}

# ─── Pattern : trouver le code de leçon dans chaque QR block ──────────────────
# Structure : <span class="qr-url">rebrand.ly/MHF_CE1_L01</span>
QR_BLOCK_PATTERN = re.compile(
    r'(<div class="canope-qr">.*?</div>)',
    re.DOTALL
)
LECON_CODE_PATTERN = re.compile(r'MHF_CE1_(L\d+[a-z]?)')

# ─── Injection ────────────────────────────────────────────────────────────────
def inject_lecons(html):
    """Remplace chaque div.canope-qr par lui-même + le bloc Je retiens."""
    injected = 0
    skipped  = 0

    def replacer(match):
        nonlocal injected, skipped
        block = match.group(1)
        codes = LECON_CODE_PATTERN.findall(block)
        if not codes:
            skipped += 1
            return block
        code = codes[0]  # prendre le premier code (ex: L02a, L09…)
        if code not in LECONS:
            skipped += 1
            return block
        injected += 1
        return block + "\n" + LECONS[code]

    new_html = QR_BLOCK_PATTERN.sub(replacer, html)
    return new_html, injected, skipped

# ─── Main ──────────────────────────────────────────────────────────────────────
print("=" * 65)
print(" Injection leçons MHF — Manuel CE1 Bela Lekkol")
print(" Contenu 'Je retiens' sous chaque QR code Canopé")
print("=" * 65)

total_ok = 0
for periode in ["P1", "P2", "P3", "P4", "P5"]:
    fn = f"MANUEL_CE1_{periode}_Bela_Lekkol_v3.html"
    fp = os.path.join(BASE, fn)
    print(f"\n── {fn}")

    if not os.path.exists(fp):
        print("   ❌ Fichier introuvable")
        continue

    with open(fp, "r", encoding="utf-8") as f:
        html = f.read()

    # Vérifier si déjà injecté
    if "lecon-retiens" in html:
        print("   ⏭  Leçons déjà présentes")
        continue

    # Ajouter CSS
    html = html.replace("</style>", LECON_CSS + "\n</style>", 1)

    # Injecter
    html, nb_inj, nb_skip = inject_lecons(html)

    with open(fp, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"   ✅ {nb_inj} leçons injectées · {nb_skip} non mappées · sauvegardé")
    total_ok += 1

print(f"\n{'='*65}")
print(f" ✅ {total_ok}/5 fichiers mis à jour avec les leçons MHF")
print(f"{'='*65}")
input("\nAppuyez sur Entrée pour fermer...")
