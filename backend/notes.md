* Before running the FastAPI server make sure to activate python virtual environment first

# Activate python virtual environment:
.\venv\Scripts\Activate.ps1

# Run the FastAPI server: 
uvicorn app.main:app --reload --port 3000

# Fix the "Execution Policy" Error (If it happens):
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Save dependencies to txt file:
pip freeze > requirements.txt

# To run a test file inside test folder
