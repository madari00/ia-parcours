# ============================================================================
#  DIAGNOSTIC GIT — Windows
#  À lancer dans PowerShell :   powershell -ExecutionPolicy Bypass -File diagnostic_git.ps1
#  Ou copie-colle simplement les blocs un par un si tu préfères.
# ============================================================================

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  DIAGNOSTIC GIT — où est le problème ?" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[1] La commande git est-elle accessible ?" -ForegroundColor Yellow
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if ($gitCmd) {
    Write-Host "    OK — git est trouve ici :" -ForegroundColor Green
    Write-Host "    $($gitCmd.Source)"
    git --version
    $script:gitOK = $true
} else {
    Write-Host "    ABSENT — la commande 'git' n'est pas reconnue." -ForegroundColor Red
    $script:gitOK = $false
}

# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[2] Git est-il installe quelque part sur le disque ?" -ForegroundColor Yellow
$chemins = @(
    "$env:ProgramFiles\Git\cmd\git.exe",
    "${env:ProgramFiles(x86)}\Git\cmd\git.exe",
    "$env:LOCALAPPDATA\Programs\Git\cmd\git.exe",
    "$env:ProgramFiles\Git\bin\git.exe",
    "$env:LOCALAPPDATA\GitHubDesktop\app-*\resources\app\git\cmd\git.exe"
)
$trouve = $null
foreach ($c in $chemins) {
    $resolus = Get-Item $c -ErrorAction SilentlyContinue
    if ($resolus) {
        foreach ($r in $resolus) {
            Write-Host "    TROUVE : $($r.FullName)" -ForegroundColor Green
            if (-not $trouve) { $trouve = $r.FullName }
        }
    }
}
if (-not $trouve) {
    Write-Host "    Aucune installation de Git detectee aux emplacements habituels." -ForegroundColor Red
    Write-Host "    -> Git n'est probablement PAS installe. Voir l'etape 3 ci-dessous."
}

# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[3] Le dossier de Git est-il dans le PATH ?" -ForegroundColor Yellow
$entreesGit = $env:PATH -split ';' | Where-Object { $_ -match 'git' }
if ($entreesGit) {
    foreach ($e in $entreesGit) { Write-Host "    $e" -ForegroundColor Green }
} else {
    Write-Host "    Aucune entree 'git' dans le PATH." -ForegroundColor Red
}

# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[4] Python actif dans ce terminal" -ForegroundColor Yellow
try { python --version } catch { Write-Host "    python non reconnu" -ForegroundColor Red }
if ($env:VIRTUAL_ENV) {
    Write-Host "    environnement virtuel actif : $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "    pas d'environnement virtuel actif (normal si tu n'as pas encore active .venv)"
}

# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  VERDICT ET SOLUTION" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

if ($script:gitOK) {
    Write-Host ""
    Write-Host "  Git fonctionne dans CE terminal." -ForegroundColor Green
    Write-Host "  Si 'git' ne fonctionne pas dans le terminal de VS Code, c'est que"
    Write-Host "  VS Code n'a pas ete redemarre COMPLETEMENT depuis l'installation."
    Write-Host ""
    Write-Host "  -> Ferme TOUTES les fenetres de VS Code (verifie la barre des taches)"
    Write-Host "  -> Reouvre VS Code"
    Write-Host "  -> Ouvre un nouveau terminal : git --version"
}
elseif ($trouve) {
    Write-Host ""
    Write-Host "  Git est installe mais absent du PATH." -ForegroundColor Yellow
    Write-Host "  Copie-colle ces deux lignes pour l'ajouter (utilisateur courant uniquement) :"
    Write-Host ""
    $dossier = Split-Path (Split-Path $trouve -Parent) -Parent   # ...\Git
    Write-Host "  `$p = [Environment]::GetEnvironmentVariable('Path','User')" -ForegroundColor White
    Write-Host "  [Environment]::SetEnvironmentVariable('Path', `$p + ';$dossier\cmd', 'User')" -ForegroundColor White
    Write-Host ""
    Write-Host "  Puis FERME et REOUVRE VS Code, et reteste : git --version"
}
else {
    Write-Host ""
    Write-Host "  Git n'est pas installe sur cette machine." -ForegroundColor Red
    Write-Host ""
    Write-Host "  Methode 1 (winget) :" -ForegroundColor White
    Write-Host "    winget install --id Git.Git -e --source winget"
    Write-Host ""
    Write-Host "  Methode 2 (installateur manuel) :" -ForegroundColor White
    Write-Host "    https://git-scm.com/download/win"
    Write-Host "    Lance le fichier telecharge, clique 'Next' partout, puis 'Install'."
    Write-Host ""
    Write-Host "  IMPORTANT : apres l'installation, FERME COMPLETEMENT VS Code et rouvre-le."
}

Write-Host ""
Write-Host "Appuie sur Entree pour fermer..."
Read-Host
