"""
Génère l'illustration aquarelle de couverture du Manuel CE1 Bela Lekkol.
Sauvegarde dans CE1/imgs/couverture.jpg

Lancer : double-cliquer sur GENERER_COUVERTURE.bat
"""
import urllib.request, urllib.parse, os, time

BASE   = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(BASE, "imgs")
OUT    = os.path.join(OUTDIR, "couverture.jpg")

if os.path.exists(OUT) and os.path.getsize(OUT) > 10000:
    print(f"✅ L'image de couverture existe déjà ({os.path.getsize(OUT)//1024} Ko).")
    print(f"   Supprimez {OUT} pour la régénérer.")
    input("\nEntrée pour fermer...")
    exit()

os.makedirs(OUTDIR, exist_ok=True)

STYLE = (
    "Illustration de couverture de manuel scolaire pour enfants de 7 ans en Guinee, "
    "style aquarelle numerique lumineuse et douce, grande scene chaleureuse, "
    "groupe d enfants africains tres joyeux en uniforme scolaire bleu et blanc "
    "tenant des livres ouverts avec des grands sourires, "
    "une belle maitresse africaine souriante et bienveillante au centre, "
    "grand manguier majestueux au feuillage genereux donnant de l ombre, "
    "paysage guineeen serein avec collines vertes au loin et ciel bleu tropical, "
    "lumiere doree chaude de matin tropical, couleurs vives saturees, "
    "composition verticale portrait, ambiance joyeuse studieuse et inspirante, "
    "style illustration jeunesse professionnelle haute qualite, "
    "sans texte ni lettres ni chiffres dans l image."
)

prompt  = urllib.parse.quote(STYLE)
url     = (f"https://image.pollinations.ai/prompt/{prompt}"
           f"?width=768&height=1024&nologo=true&seed=999&enhance=true")

print("=" * 60)
print(" Génération de l'illustration de couverture")
print(" Pollinations.ai — environ 60 secondes...")
print("=" * 60)

req = urllib.request.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (compatible; BelaLekkol-Cover/1.0)"
})

for attempt in range(1, 3):
    try:
        print(f"\n  Tentative {attempt}/2...")
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = resp.read()
        elapsed = time.time() - t0

        if len(data) < 10000:
            raise ValueError(f"Réponse trop petite ({len(data)} octets)")
        if data[:2] != b'\xff\xd8':
            raise ValueError(f"Pas un JPEG (entête: {data[:4].hex()})")

        with open(OUT, "wb") as f:
            f.write(data)
        print(f"\n  ✅ Image générée : {len(data)//1024} Ko en {elapsed:.1f}s")
        print(f"  📁 Sauvegardée dans : {OUT}")
        break

    except Exception as e:
        print(f"  ❌ Erreur : {e}")
        if attempt < 2:
            print("  Nouvelle tentative dans 8 secondes...")
            time.sleep(8)
        else:
            print("\n  Impossible de générer l'image. Vérifiez votre connexion internet.")

print("\n" + "=" * 60)
input("Appuyez sur Entrée pour fermer...")
