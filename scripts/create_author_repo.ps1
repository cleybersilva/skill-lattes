param(
    [Parameter(Mandatory = $true)]
    [string]$Name,
    [ValidateSet("public", "private")]
    [string]$Visibility = "private",
    [string]$Description = "",
    [switch]$Push,
    [switch]$NoInit
)

$TemplateRoot = Join-Path $HOME "Templates/repo-author-card"
$ReadmeTemplate = Join-Path $TemplateRoot "author-card-template.md"
$LogoSource = Join-Path $TemplateRoot "logo-cesar.png"

if (-not (Test-Path -LiteralPath $ReadmeTemplate)) {
    throw "Template global não encontrado em $TemplateRoot"
}

New-Item -ItemType Directory -Force $Name | Out-Null
Set-Location $Name
if (-not $NoInit) {
    git init -b main
}
New-Item -ItemType Directory -Force "assets" | Out-Null
Copy-Item -LiteralPath $LogoSource -Destination "assets/logo-cesar.png" -Force
Copy-Item -LiteralPath $ReadmeTemplate -Destination "README.md" -Force

$visibilityArg = if ($Visibility -eq "public") { "--public" } else { "--private" }
if ($Push) {
    gh repo create $Name $visibilityArg --source=. --remote=origin --push
    git config branch.main.remote origin
    git config branch.main.merge refs/heads/main
}

Write-Output "Repositório preparado em $Name"
