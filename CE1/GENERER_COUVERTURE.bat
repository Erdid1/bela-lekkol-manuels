@echo off
title Bela Lekkol CE1 — Generation illustration couverture
echo ================================================
echo  Generation de l'illustration de couverture
echo  Manuel CE1 "Mes Lectures" — Bela Lekkol
echo ================================================
echo.
python "%~dp0GENERER_COUVERTURE.py"
if ERRORLEVEL 1 (
    echo.
    echo ERREUR : verifiez que Python est installe.
    pause
)
