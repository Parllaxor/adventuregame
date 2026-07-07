@echo off
set PY=c:\Users\parll\OneDrive\Desktop\Work\Games\AdventureGame\.venv\Scripts\python.exe
"%PY%" -c "import pathlib, sys; p=pathlib.Path(r'c:\Users\parll\OneDrive\Desktop\Work\Games\AdventureGame\backend\app.py'); src=p.read_text(encoding='utf-8'); compile(src, str(p), 'exec')"
