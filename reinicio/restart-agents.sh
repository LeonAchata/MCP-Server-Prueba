#!/bin/bash

# Script para reiniciar los agentes MCP después de cambios en el código
# Uso: chmod +x restart-agents.sh && ./restart-agents.sh

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     🔄 REINICIO DE AGENTES MCP - SCRIPT COMPLETO     ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Paso 1: Detener servicios
echo -e "${YELLOW}📍 Paso 1/7: Deteniendo servicios...${NC}"
docker-compose down
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Servicios detenidos correctamente${NC}"
else
    echo -e "${YELLOW}   ⚠️  Advertencia al detener servicios${NC}"
fi
echo ""

# Paso 2: Limpiar contenedores antiguos
echo -e "${YELLOW}📍 Paso 2/7: Limpiando contenedores antiguos...${NC}"
docker stop agent-http agent-websocket mcp-server 2>/dev/null
docker rm agent-http agent-websocket mcp-server 2>/dev/null
echo -e "${GREEN}   ✅ Contenedores limpiados${NC}"
echo ""

# Paso 3: Reconstruir imágenes
echo -e "${YELLOW}📍 Paso 3/7: Reconstruyendo imágenes (esto puede tardar)...${NC}"
docker-compose build --no-cache
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Imágenes reconstruidas correctamente${NC}"
else
    echo -e "${RED}   ❌ Error al reconstruir imágenes${NC}"
    exit 1
fi
echo ""

# Paso 4: Iniciar servicios
echo -e "${YELLOW}📍 Paso 4/7: Iniciando servicios...${NC}"
docker-compose up -d
if [ $? -eq 0 ]; then
    echo -e "${GREEN}   ✅ Servicios iniciados en modo detached${NC}"
else
    echo -e "${RED}   ❌ Error al iniciar servicios${NC}"
    exit 1
fi
echo ""

# Paso 5: Esperar a que los servicios estén listos
echo -e "${YELLOW}📍 Paso 5/7: Esperando a que los servicios inicien...${NC}"
for i in {10..1}; do
    echo -ne "${CYAN}   ⏳ $i segundos restantes...\r${NC}"
    sleep 1
done
echo -e "${GREEN}   ✅ Tiempo de espera completado                    ${NC}"
echo ""

# Paso 6: Verificar estado
echo -e "${YELLOW}📍 Paso 6/7: Verificando estado de los servicios...${NC}"
docker-compose ps
echo ""

# Paso 7: Mostrar logs recientes
echo -e "${YELLOW}📍 Paso 7/7: Logs recientes de los servicios...${NC}"
docker-compose logs --tail=10
echo ""

# Paso 8: Prueba de conectividad
echo -e "${CYAN}🧪 Prueba de conectividad...${NC}"
echo -e "${WHITE}   Probando endpoint /health...${NC}"
if curl -s -f http://localhost:8001/health > /dev/null 2>&1; then
    echo -e "${GREEN}   ✅ Agent HTTP responde correctamente${NC}"
else
    echo -e "${YELLOW}   ⚠️  Agent HTTP no responde aún (puede necesitar más tiempo)${NC}"
fi
echo ""

# Resumen final
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            ✅ REINICIO COMPLETADO                     ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}📋 Comandos útiles:${NC}"
echo -e "   • Ver logs en tiempo real:  ${WHITE}docker-compose logs -f${NC}"
echo -e "   • Ver logs de un servicio:  ${WHITE}docker-compose logs agent -f${NC}"
echo -e "   • Estado de servicios:      ${WHITE}docker-compose ps${NC}"
echo -e "   • Detener servicios:        ${WHITE}docker-compose down${NC}"
echo -e "   • Entrar a un contenedor:   ${WHITE}docker exec -it agent-http /bin/bash${NC}"
echo ""
echo -e "${CYAN}🌐 URLs disponibles:${NC}"
echo -e "   • MCP Server (interno):     ${WHITE}http://localhost:8000${NC}"
echo -e "   • Agent HTTP:               ${WHITE}http://localhost:8001${NC}"
echo -e "   • Agent WebSocket:          ${WHITE}http://localhost:8002${NC}"
echo -e "   • Frontend:                 ${WHITE}Abre frontend/index.html en tu navegador${NC}"
echo ""
