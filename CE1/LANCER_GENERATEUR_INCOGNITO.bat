@echo off
echo ============================================
echo  Generateur d'illustrations CE1 Bela Lekkol
echo  Mode INCOGNITO (sans compte Pollinations)
echo ============================================
echo.
echo Ouverture de Chrome en mode incognito...
echo Les 35 images vont se telecharger dans Telechargements\
echo.

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --incognito "C:\Users\ERIC01\Documents\bela-lekkol-manuels\CE1\GENERER_IMAGES.html"

IF ERRORLEVEL 1 (
  start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --incognito "C:\Users\ERIC01\Documents\bela-lekkol-manuels\CE1\GENERER_IMAGES.html"
)

echo Chrome incognito lance. Cliquez le bouton vert dans la page.
echo Autorisez les telechargements multiples si Chrome le demande.
pause
