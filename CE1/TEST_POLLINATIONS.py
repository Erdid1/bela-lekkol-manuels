"""
TEST rapide : est-ce que Pollinations répond sans auth depuis Python ?
Lance ce script, il télécharge UNE seule image test.
"""
import urllib.request
import os, sys

url = (
    "https://image.pollinations.ai/prompt/"
    "enfant+africain+aquarelle+test"
    "?width=256&height=192&nologo=true&seed=999"
)

out = os.path.join(os.path.dirname(__file__), "imgs", "_test_python.jpg")
os.makedirs(os.path.dirname(out), exist_ok=True)

print("Appel Pollinations via Python (sans cookies navigateur)...")
print(f"URL : {url}")
print()

try:
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (compatible; Python-test/1.0)"
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
        ct = resp.headers.get("Content-Type", "?")

    print(f"Content-Type : {ct}")
    print(f"Taille reçue : {len(data)} octets")

    if b"error" in data[:200].lower() or len(data) < 5000:
        print()
        print("⚠  Réponse suspecte (trop petite ou contient 'error') :")
        print(data[:300])
        sys.exit(1)

    with open(out, "wb") as f:
        f.write(data)

    print(f"\n✅ IMAGE SAUVEGARDÉE : {out}")
    print("→ Pollinations fonctionne depuis Python. On peut lancer les 25 images !")

except Exception as e:
    print(f"\n❌ ERREUR : {e}")
    print("→ Il faut une alternative (Hugging Face / Raphael).")

input("\nAppuyez sur Entrée pour fermer...")
