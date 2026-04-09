# Run Guide

## Start the email services

From the project root:

```powershell
cd c:\Users\hejin\OneDrive\Desktop\COMP3132\LabWeek13
.\Email_Assistant-Optional\start_email_services.ps1
```

Manual alternative:

```powershell
cd c:\Users\hejin\OneDrive\Desktop\COMP3132\LabWeek13\Email_Assistant-Optional
$env:M3_EMAIL_SERVER_API_URL="http://127.0.0.1:5000"
$env:UI_EMAIL_SERVER="http://127.0.0.1:5000"
$env:UI_LLM_SERVER="http://127.0.0.1:5001"
..\.venv\Scripts\python.exe -m uvicorn email_server.email_service:app --host 127.0.0.1 --port 5000
```

Open a second terminal for the LLM service:

```powershell
cd c:\Users\hejin\OneDrive\Desktop\COMP3132\LabWeek13\Email_Assistant-Optional
$env:M3_EMAIL_SERVER_API_URL="http://127.0.0.1:5000"
..\.venv\Scripts\python.exe -m uvicorn email_server.llm_service:app --host 127.0.0.1 --port 5001
```

Quick checks:

```powershell
Invoke-RestMethod http://127.0.0.1:5000/health
Invoke-WebRequest http://127.0.0.1:5001/docs | Select-Object -ExpandProperty StatusCode
```

## Run the notebooks

From the project root:

```powershell
cd c:\Users\hejin\OneDrive\Desktop\COMP3132\LabWeek13
.\.venv\Scripts\python.exe -m notebook
```

Then open:

- `Functions_Tools-Walkthrough/tool_calling.ipynb`
- `Research_Agent_ToolCalling-Exercise/research_agent_toolcalling.ipynb`
- `Email_Assistant-Optional/email_assistant.ipynb`

## Notebook notes

- `research_agent_toolcalling.ipynb` imports `research_tools.py` from its own folder, so run it from that notebook without moving files.
- The research notebook has local fallback logic. If OpenAI quota or external API access fails, its graded functions should still return fallback output instead of crashing.
- `email_assistant.ipynb` expects the email API at `http://127.0.0.1:5000`, which matches the startup script above.
- The LLM email service may return a controlled error if the OpenAI API key has no quota.
