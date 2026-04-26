@echo off
title Bela Lekkol CE1 — Injection lecons MHF
echo ================================================
echo  Injection du contenu "Je retiens" des 33 lecons
echo  Canope dans les 5 fichiers HTML du manuel CE1
echo ================================================
echo.
python "%~dp0INJECTER_LECONS_MHF.py"
if ERRORLEVEL 1 (
    echo.
    echo ERREUR : verifiez que Python est installe.
    pause
)
