# Script para reiniciar los agentes MCP después de cambios en el código
# Uso: .\restart-agents.ps1

Write-Host "`n" -NoNewline
Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     🔄 REINICIO DE AGENTES MCP - SCRIPT COMPLETO     ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n"

# Paso 1: Detener servicios
Write-Host "📍 Paso 1/7: Deteniendo servicios..." -ForegroundColor Yellow
docker-compose down
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Servicios detenidos correctamente" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Advertencia al detener servicios" -ForegroundColor Yellow
}
Write-Host ""

# Paso 2: Limpiar contenedores antiguos
Write-Host "📍 Paso 2/7: Limpiando contenedores antiguos..." -ForegroundColor Yellow
docker stop agent-http agent-websocket toolbox 2>$null
docker rm agent-http agent-websocket toolbox 2>$null
Write-Host "   ✅ Contenedores limpiados" -ForegroundColor Green
Write-Host ""

# Paso 3: Reconstruir imágenes
Write-Host "📍 Paso 3/7: Reconstruyendo imágenes (esto puede tardar)..." -ForegroundColor Yellow
docker-compose build --no-cache
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Imágenes reconstruidas correctamente" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error al reconstruir imágenes" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Paso 4: Iniciar servicios
Write-Host "📍 Paso 4/7: Iniciando servicios..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Servicios iniciados en modo detached" -ForegroundColor Green
} else {
    Write-Host "   ❌ Error al iniciar servicios" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Paso 5: Esperar a que los servicios estén listos
Write-Host "📍 Paso 5/7: Esperando a que los servicios inicien..." -ForegroundColor Yellow
for ($i = 10; $i -gt 0; $i--) {
    Write-Host "   ⏳ $i segundos restantes..." -ForegroundColor Cyan -NoNewline
    Start-Sleep -Seconds 1
    Write-Host "`r" -NoNewline
}
Write-Host "   ✅ Tiempo de espera completado                    " -ForegroundColor Green
Write-Host ""

# Paso 6: Verificar estado
Write-Host "📍 Paso 6/7: Verificando estado de los servicios..." -ForegroundColor Yellow
$services = docker-compose ps
Write-Host $services
Write-Host ""

# Paso 7: Mostrar logs recientes
Write-Host "📍 Paso 7/7: Logs recientes de los servicios..." -ForegroundColor Yellow
docker-compose logs --tail=10
Write-Host ""

# Paso 8: Prueba de conectividad
Write-Host "🧪 Prueba de conectividad..." -ForegroundColor Cyan
Write-Host "   Probando endpoint /health..." -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -UseBasicParsing -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "   ✅ Agent HTTP responde correctamente" -ForegroundColor Green
    }
} catch {
    Write-Host "   ⚠️  Agent HTTP no responde aún (puede necesitar más tiempo)" -ForegroundColor Yellow
}
Write-Host ""

# Resumen final
Write-Host "╔═══════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║            ✅ REINICIO COMPLETADO                     ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Comandos útiles:" -ForegroundColor Cyan
Write-Host "   • Ver logs en tiempo real:  " -NoNewline; Write-Host "docker-compose logs -f" -ForegroundColor White
Write-Host "   • Ver logs de un servicio:  " -NoNewline; Write-Host "docker-compose logs agent -f" -ForegroundColor White
Write-Host "   • Estado de servicios:      " -NoNewline; Write-Host "docker-compose ps" -ForegroundColor White
Write-Host "   • Detener servicios:        " -NoNewline; Write-Host "docker-compose down" -ForegroundColor White
Write-Host "   • Entrar a un contenedor:   " -NoNewline; Write-Host "docker exec -it agent-http /bin/bash" -ForegroundColor White
Write-Host ""
Write-Host "🌐 URLs disponibles:" -ForegroundColor Cyan
Write-Host "   • MCP Server (interno):     " -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor White
Write-Host "   • Agent HTTP:               " -NoNewline; Write-Host "http://localhost:8001" -ForegroundColor White
Write-Host "   • Agent WebSocket:          " -NoNewline; Write-Host "http://localhost:8002" -ForegroundColor White
Write-Host "   • Frontend:                 " -NoNewline; Write-Host "Abre frontend/index.html en tu navegador" -ForegroundColor White
Write-Host ""
