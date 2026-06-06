@echo off
echo ============================================
echo   Push railway.toml fix to Railway
echo ============================================
echo.

cd /d "%~dp0"

echo Adding railway.toml...
git add railway.toml

echo.
echo Committing changes...
git commit -m "fix: add explicit startCommand in railway.toml"

echo.
echo Pushing to GitHub...
git push

echo.
echo ============================================
echo   Done! Railway should now redeploy.
echo ============================================
pause