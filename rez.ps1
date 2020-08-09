$env:PATH="$env:USERPROFILE\rez\core\Scripts\rez;$env:PATH"
$env:REZ_CONFIG_FILE="$PSScriptRoot\rezconfig.py"
python .\rez_.py %*
