@echo off
echo ================================================
echo   Agent Auth Proxy - Manual Tasks Helper
echo ================================================
echo.

cd /d E:\Agents\project\agent-auth-proxy

echo [1/5] Current Git Status:
git status
echo.

echo [2/5] Files ready to commit:
git diff --name-only --cached
git diff --name-only
echo.

echo [3/5] Key files to review:
echo - app\auth.py
echo - app\routes\credentials.py
echo - app\main.py
echo - app\routes\health.py
echo - app\routes\admin.py
echo - scripts\railway_smoke_test.py
echo.

echo [4/5] Suggested commit message:
echo "feat: add auto-migration, admin endpoint, improved logging and tests"
echo.

echo [5/5] Next manual steps:
echo 1. Review changes above
echo 2. git add .
echo 3. git commit -m "your message"
echo 4. git push
echo 5. Deploy on Railway
echo.

pause
