Set-Location "$PSScriptRoot\backend"
if (-not (Test-Path ".venv")) { py -m venv .venv }
& ".\.venv\Scripts\Activate.ps1"
if (-not (Test-Path ".env")) { Copy-Item ".env.example" ".env" }
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
