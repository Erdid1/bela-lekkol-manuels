@echo off
title Bela Lekkol CE1 — Generation illustrations
echo ================================================
echo  Bela Lekkol CE1 - Generation des 35 illustrations
echo  Pollinations.ai via Python (sans authentification)
echo ================================================
echo.
echo Demarrage de la generation...
echo Les images seront sauvegardees dans : CE1\imgs\
echo.
python "%~dp0GENERER_IMAGES_PYTHON.py"
if ERRORLEVEL 1 (
    echo.
    echo ERREUR : Python n'est pas installe ou une erreur s'est produite.
    echo Installez Python depuis python.org et relancez.
    pause
)
