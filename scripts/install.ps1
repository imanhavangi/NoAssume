# Thin wrapper around install.py — all installer logic lives there.
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$python = Get-Command py -ErrorAction SilentlyContinue
if ($python) {
    & py -3 "$ScriptDir\install.py" @args
    exit $LASTEXITCODE
}
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    & python "$ScriptDir\install.py" @args
    exit $LASTEXITCODE
}
Write-Error "noassume: python 3 is required (tried py -3 and python)"
exit 1
