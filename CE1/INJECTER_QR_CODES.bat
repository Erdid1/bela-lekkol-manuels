@echo off
title Bela Lekkol CE1 — Injection QR codes Canopé
echo ================================================
echo  Injection des 33 QR codes Reseau Canope
echo  dans les 5 fichiers HTML du manuel CE1
echo ================================================
echo.
python "%~dp0INJECTER_QR_CODES.py"
if ERRORLEVEL 1 (
    echo.
    echo ERREUR : verifiez que Python est installe.
    pause
)
