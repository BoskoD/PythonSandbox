# Change CODING_DIRECTORY to your projects folder 'C:\path\to\your\code'
$CODING_DIRECTORY = ""
$PROJECT_NAME = [String]$args[0]
$PROJECT_DIRECTORY = "$CODING_DIRECTORY\$PROJECT_NAME"
$VENV_NAME = "venv-$PROJECT_NAME"
$VENV_DIRECTORY = "$PROJECT_DIRECTORY\$VENV_NAME"
# Check if code directory exists, exit if it does not
if (-Not $(Test-Path $CODING_DIRECTORY)) {
Write-Error `
-Message "ERROR: Path $CODING_DIRECTORY does not exist. Please check CODING_DIRECTORY" `
-Category InvalidData
}
# Create the project folder if it doesn't already exist
if (-Not $(Test-Path $PROJECT_DIRECTORY)) {
Write-Host "Creating directory $PROJECT_DIRECTORY"
[Void](New-Item -ItemType Directory -Path $PROJECT_DIRECTORY)
if (-Not $(Test-Path $PROJECT_DIRECTORY)) {
Write-Error `
-Message "Path $PROJECT_DIRECTORY couldn't be created" `
-Category InvalidData
}
}
# Create the virtual environment if it doesn't already exist
if (-Not $(Test-Path $VENV_DIRECTORY)) {
Write-Host "Creating environment $VENV_NAME"
python.exe -m venv $VENV_DIRECTORY
}
# Move to venv folder and run the activation script
Set-Location "$VENV_DIRECTORY\Scripts"
.\Activate.ps1
# Move to the project folder and launch VS Code
Set-Location $PROJECT_DIRECTORY
Write-Host "Launching VS Code"
code $PROJECT_DIRECTORY 
```