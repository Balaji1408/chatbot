@echo off
echo Starting Enterprise GenAI Knowledge Assistant...
echo Ensure you have Ollama running with 'ollama serve' and have pulled the model (e.g., 'ollama pull llama3')
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
