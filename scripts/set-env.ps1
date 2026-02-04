param(
  [string]$PortalTitle = "Portal de Conferência Tributária",
  [string]$SimplesUrl = "https://simplesdash.manus.space",
  [string]$IrpjUrl = "https://calc-fiscal-2etwmuhb.manus.space/",
  [string]$PisCofinsUrl = "https://dashpiscofins.manus.space",
  [string]$PortalDescription = "Portal stateless para acesso rápido aos módulos tributários."
)

@"
PORTAL_TITLE="$PortalTitle"
SIMPLES_URL="$SimplesUrl"
IRPJ_URL="$IrpjUrl"
PIS_COFINS_URL="$PisCofinsUrl"
PORTAL_DESCRIPTION="$PortalDescription"
"@ | Set-Content -Path "config.env"
