"""
Corrige le CSS des images : object-fit:cover coupait les aquarelles.
Nouveau comportement : image pleine largeur, ratio 4:3 préservé,
avec object-position: center 20% pour montrer la partie haute (personnages).
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

# CSS à remplacer
OLD = """.illus-bandeau {
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
}"""

NEW = """.illus-bandeau {
  width: 100%;
  overflow: hidden;
  border-radius: 5px;
  margin-bottom: 3mm;
  border: 0.5px solid #ccc;
  page-break-inside: avoid;
  background: #faf9f5;
}
.illus-bandeau img {
  width: 100%;
  height: auto;          /* ratio 4:3 naturel, aucune déformation */
  max-height: 72mm;      /* plafond pour les petites pages */
  display: block;
  object-fit: cover;
  object-position: center 18%;  /* montre la partie haute : personnages */
}"""

fixed = 0
for p in ["P1","P2","P3","P4","P5"]:
    fn = f"MANUEL_CE1_{p}_Bela_Lekkol_v3.html"
    fp = os.path.join(BASE, fn)
    if not os.path.exists(fp): continue
    with open(fp,"r",encoding="utf-8") as f: html = f.read()
    if OLD in html:
        html = html.replace(OLD, NEW)
        with open(fp,"w",encoding="utf-8") as f: f.write(html)
        print(f"  ✅ {fn} — CSS corrigé")
        fixed += 1
    else:
        print(f"  ⚠  {fn} — pattern non trouvé (déjà corrigé ?)")

print(f"\n{fixed}/5 fichiers corrigés.")
input("Entrée pour fermer...")
