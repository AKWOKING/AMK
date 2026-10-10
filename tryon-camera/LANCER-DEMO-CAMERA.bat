@echo off
title UO essayage camera : serveur local (fermer cette fenetre pour arreter)
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python n'est pas installe sur cet ordinateur.
  echo Ouverture directe du fichier...
  start "" "V2 Try-On Camera.html"
  pause
  exit /b
)
start "uo-cam-server" /min cmd /c "python -m http.server 8017 & pause"
timeout /t 3 /nobreak >nul
start "" "http://localhost:8017/V2%20Try-On%20Camera.html"
echo.
echo Page ouverte dans le navigateur : http://localhost:8017/
echo Pour arreter le serveur, fermer la petite fenetre "uo-cam-server".
pause
