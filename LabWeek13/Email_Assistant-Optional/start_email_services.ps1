$root = Split-Path -Parent $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"

if (-not (Test-Path $python)) {
    Write-Error "Python virtual environment not found at $python"
    exit 1
}

$env:M3_EMAIL_SERVER_API_URL = "http://127.0.0.1:5000"
$env:UI_EMAIL_SERVER = "http://127.0.0.1:5000"
$env:UI_LLM_SERVER = "http://127.0.0.1:5001"

Write-Host "Starting email API on http://127.0.0.1:5000"
Start-Process -FilePath $python -ArgumentList @(
    "-m",
    "uvicorn",
    "email_server.email_service:app",
    "--host",
    "127.0.0.1",
    "--port",
    "5000"
) -WorkingDirectory $PSScriptRoot

Write-Host "Starting LLM API on http://127.0.0.1:5001"
Start-Process -FilePath $python -ArgumentList @(
    "-m",
    "uvicorn",
    "email_server.llm_service:app",
    "--host",
    "127.0.0.1",
    "--port",
    "5001"
) -WorkingDirectory $PSScriptRoot

Write-Host "Services launched."
Write-Host "Email API: http://127.0.0.1:5000/health"
Write-Host "LLM API:   http://127.0.0.1:5001/prompt"
