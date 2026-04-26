@echo off
echo ============================================
echo  Deplacement images CE1 → CE1\imgs\
echo ============================================
echo.
echo Copie des images p*.jpg de Telechargements vers CE1\imgs\...
echo.

set SRC=%USERPROFILE%\Downloads
set DST=%USERPROFILE%\Documents\bela-lekkol-manuels\CE1\imgs

for %%f in ("%SRC%\p1s*.jpg" "%SRC%\p2s*.jpg" "%SRC%\p3s*.jpg" "%SRC%\p4s*.jpg" "%SRC%\p5s*.jpg") do (
  IF EXIST "%%f" (
    echo Copie: %%~nxf
    copy /Y "%%f" "%DST%\"
  )
)

echo.
echo Verifications dans CE1\imgs\ :
dir "%DST%\p*.jpg" /B 2>nul | find /c ".jpg" > nul
dir "%DST%\p*.jpg" /B 2>nul

echo.
echo Termine ! Appuyez sur une touche pour fermer.
pause
