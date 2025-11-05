# 🤖 LangGraph Multi-Agent System + MCP + LLM Gateway

Sistema multi-agente inteligente con **Model Context Protocol (MCP)**, **LLM Gateway centralizado** y soporte para múltiples proveedores de IA (AWS Bedrock, OpenAI, Google Gemini).

## 📋 Descripción

Este proyecto implementa una arquitectura de microservicios para agentes de IA que:
- 🧠 **LLM Gateway Centralizado**: Gestión unificada de múltiples proveedores de LLMs
- 🔧 **MCP Toolbox**: Servidor de herramientas usando Model Context Protocol sobre HTTP
- 🤖 **Múltiples Agentes**: HTTP REST y WebSocket para diferentes tipos de integración
- 📊 **LangGraph**: Orquestación avanzada de flujos de trabajo
- 🐳 **Containerizado**: Todo en Docker para fácil deployment
- ☁️ **Production Ready**: Listo para Kubernetes/AWS EKS

### 🎯 Características Principales

- ✅ **Selección dinámica de modelos**: Cambia entre Bedrock, OpenAI y Gemini desde el prompt
- ✅ **Cache inteligente**: Respuestas cacheadas con TTL configurable
- ✅ **Métricas en tiempo real**: Tracking de costos, tokens y latencia
- ✅ **Manejo de herramientas**: Ejecución de tools a través de MCP
- ✅ **Streaming**: Soporte WebSocket para respuestas en tiempo real
- ✅ **Health checks**: Monitoreo de salud de todos los servicios

## 🏗️ Arquitectura

```
                    ┌─────────────────────┐
                    │   Browser/Client    │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │ WebSocket                   │ HTTP REST
                ▼                             ▼
    ┌───────────────────────┐    ┌───────────────────────┐
    │  Agent WebSocket      │    │  Agent HTTP           │
    │  Port: 8002           │    │  Port: 8001           │
    │  • Streaming real-time│    │  • REST API           │
    │  • Múltiples clientes │    │  • Request/Response   │
    │  • FastAPI + WS       │    │  • FastAPI            │
    │  • LangGraph          │    │  • LangGraph          │
    └───────────┬───────────┘    └───────────┬───────────┘
                │                            │
                │      MCP Protocol          │
                ├────────────┬───────────────┤
                │            │               │
                ▼            ▼               │
    ┌──────────────────┐  ┌─────────────────▼──────┐
    │  LLM Gateway     │  │   MCP Toolbox          │
    │  Port: 8003      │  │   Port: 8000           │
    │                  │  │                        │
    │  3 Providers:    │  │   Tools:               │
    │  • Bedrock Nova  │  │   • add                │
    │  • OpenAI GPT-4o │  │   • multiply           │
    │  • Gemini Flash  │  │   • uppercase          │
    │                  │  │   • count_words        │
    │  Features:       │  └────────────────────────┘
    │  • Cache (TTL)   │
    │  • Metrics       │
    │  • Cost tracking │
    └──────────────────┘
                
        Docker Network (mcp-network)
```

## 🔧 Componentes

### 1. 🧠 LLM Gateway (Puerto 8003)
**Servidor centralizado de gestión de LLMs**

- **Propósito**: Abstrae y unifica el acceso a múltiples proveedores de IA
- **Proveedores soportados**:
  - AWS Bedrock Nova Pro (`bedrock-nova-pro`)
  - OpenAI GPT-4o (`gpt-4o`)
  - Google Gemini 1.5 Flash (`gemini-pro`)
- **Características**:
  - 💰 **Cálculo de costos**: Estima costos por request
  - 🚀 **Cache TTL**: Reduce llamadas a APIs externas
  - 📊 **Métricas**: Requests, tokens, latencia, hit rate
  - 🔌 **Patrón Registry**: Fácil agregar nuevos LLMs
  - 🔐 **Credenciales centralizadas**: Los agentes no necesitan API keys

**Endpoints**:
- `GET /mcp/llm/list` - Lista modelos disponibles
- `POST /mcp/llm/generate` - Genera respuesta con modelo seleccionado
- `GET /metrics` - Obtiene métricas del gateway
- `POST /cache/clear` - Limpia el cache

### 2. 🛠️ MCP Toolbox (Puerto 8000)
**Servidor de herramientas con Model Context Protocol**

- **Protocolo**: MCP sobre HTTP REST
- **4 Herramientas**:
  - `add(a, b)` - Suma dos números
  - `multiply(a, b)` - Multiplica dos números
  - `uppercase(text)` - Convierte texto a mayúsculas
  - `count_words(text)` - Cuenta palabras en un texto

**Endpoints**:
- `GET /mcp/tools/list` - Lista herramientas disponibles
- `POST /mcp/tools/call` - Ejecuta una herramienta

### 3. 🤖 Agent HTTP (Puerto 8001)
**Agente con API REST**

- **Framework**: FastAPI + LangGraph
- **Tipo**: Request/Response tradicional
- **Uso**: Integraciones síncronas, APIs externas
- **Características**:
  - Selección de modelo por request
  - Detección automática de modelo en prompt
  - Tracking de pasos de ejecución

**Endpoint**:
```bash
POST /process
{
  "input": "usa gemini, cuanto es 5 + 3",
  "model": "gemini-pro"  # Opcional
}
```

### 4. 🔌 Agent WebSocket (Puerto 8002)
**Agente con comunicación en tiempo real**

- **Framework**: FastAPI WebSocket + LangGraph
- **Tipo**: Streaming bidireccional
- **Uso**: Interfaces conversacionales, dashboards
- **Características**:
  - Múltiples clientes concurrentes
  - Streaming de pasos de ejecución
  - Notificaciones en tiempo real

**Conexión**:
```javascript
ws://localhost:8002/ws/{connection_id}
```

## 📁 Estructura del Proyecto

```
MCP-Example/
├── llm-gateway/                     # 🧠 LLM Gateway (NUEVO)
│   ├── src/
│   │   ├── models/                 # Implementaciones LLM
│   │   │   ├── base.py            # Clase abstracta
│   │   │   ├── bedrock.py         # AWS Bedrock
│   │   │   ├── openai.py          # OpenAI GPT-4
│   │   │   └── gemini.py          # Google Gemini
│   │   ├── cache.py               # Sistema de cache TTL
│   │   ├── metrics.py             # Métricas y tracking
│   │   ├── registry.py            # Registry de LLMs
│   │   ├── config.py              # Configuración
│   │   └── server.py              # FastAPI server MCP
│   ├── Dockerfile
│   └── requirements.txt
│
├── agents/                          # Agentes del sistema
│   ├── agent-http/                  # Agent REST API
│   │   ├── src/
│   │   │   ├── graph/              # LangGraph workflow
│   │   │   │   ├── nodes.py        # Nodos del grafo
│   │   │   │   ├── state.py        # Estado del agente
│   │   │   │   └── workflow.py     # Definición del workflow
│   │   │   ├── llm_client/         # Cliente LLM Gateway (NUEVO)
│   │   │   ├── mcp_client/         # Cliente MCP Toolbox
│   │   │   ├── api/                # FastAPI routes
│   │   │   ├── config.py           # Configuración
│   │   │   └── main.py             # Entry point
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── agent-websocket/             # Agent WebSocket
│       ├── src/
│       │   ├── graph/              # LangGraph workflow
│       │   ├── llm_client/         # Cliente LLM Gateway (NUEVO)
│       │   ├── mcp_client/         # Cliente MCP Toolbox
│       │   ├── websocket/          # WebSocket handlers
│       │   ├── config.py           # Configuración
│       │   └── main.py             # Entry point
│       ├── Dockerfile
│       └── requirements.txt
│
├── mcp-server/                      # MCP Toolbox Server
│   ├── src/
│   │   ├── tools/                  # 4 herramientas
│   │   │   ├── calculator.py
│   │   │   └── text_tools.py
│   │   ├── server.py               # MCP server HTTP
│   │   └── config.py
│   ├── Dockerfile
│   └── requirements.txt
│   │   ├── server.py               # MCP server HTTP
│   │   └── config.py               # Configuración
│   ├── Dockerfile
│   └── requirements.txt
│
├── k8s/                             # Manifiestos Kubernetes
│   ├── namespace.yaml
│   ├── mcp-toolbox-*.yaml
│
├── frontend/                        # Interfaz web (opcional)
├── k8s/                             # Manifiestos Kubernetes
│   ├── namespace.yaml
│   ├── llm-gateway-*.yaml          # Deployment LLM Gateway
│   ├── mcp-toolbox-*.yaml
│   ├── agent-*.yaml
│   ├── websocket-agent-*.yaml
│   └── ingress.yaml
│
├── docs/                            # Documentación
│   ├── DEPLOYMENT_EKS.md           # Guía AWS EKS
│   └── WEBSOCKET_AGENT.md          # Docs WebSocket
│
├── docker-compose.yml               # Orquestación Docker
├── test-websocket.html              # Cliente HTML WebSocket
├── .env                             # Variables de entorno (NO SUBIR)
└── README.md
```

## 🚀 Instalación y Uso

### Prerrequisitos

- Docker y Docker Compose instalados
- **Credenciales de al menos uno de:**
  - AWS (para Bedrock Nova Pro)
  - OpenAI (para GPT-4o)
  - Google Cloud (para Gemini)

### Configuración

1. **Clona el repositorio**

```bash
git clone https://github.com/LeonAchata/MCP-Server-Prueba.git
cd MCP-Example
```

2. **Configura las variables de entorno**

Crea el archivo `.env` en la raíz del proyecto:

```bash
# LLM Gateway Configuration
HOST=0.0.0.0
PORT=8003
LOG_LEVEL=INFO

# Cache Configuration
CACHE_ENABLED=true
CACHE_TTL=3600
CACHE_MAX_SIZE=1000

# AWS Bedrock Credentials (Opcional)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
BEDROCK_MODEL_ID=us.amazon.nova-pro-v1:0

# OpenAI Credentials (Opcional)
OPENAI_API_KEY=sk-proj-...
OPENAI_DEFAULT_MODEL=gpt-4o

# Google Gemini Credentials (Opcional)
GOOGLE_API_KEY=AIzaSy...
GEMINI_DEFAULT_MODEL=gemini-1.5-flash

# MCP Configuration
MCP_SERVER_URL=http://toolbox:8000
LLM_GATEWAY_URL=http://llm-gateway:8003
```

**⚠️ Notas importantes:**
- Configura al menos un proveedor de LLM (Bedrock, OpenAI o Gemini)
- Si usas AWS, asegúrate de tener acceso a Bedrock Nova Pro en tu región
- Para OpenAI, necesitas créditos en tu cuenta
- Para Gemini, habilita la API en Google Cloud Console

### Ejecución

**Construir e iniciar todos los contenedores:**

```bash
docker-compose up --build -d
```

El sistema iniciará 4 servicios:
- 🧠 **LLM Gateway** en `http://localhost:8003`
- 🔧 **MCP Toolbox** en `http://localhost:8000` (interno)
- 📡 **Agent HTTP** en `http://localhost:8001`
- 🔌 **Agent WebSocket** en `http://localhost:8002`

**Ver logs en tiempo real:**
```bash
# Todos los servicios
docker-compose logs -f

# Servicio específico
docker-compose logs -f llm-gateway
docker-compose logs -f agent-http
```

**Verificar estado de los servicios:**
```bash
docker-compose ps
```

**Detener el sistema:**
```bash
docker-compose down
```

**Reconstruir un servicio específico:**
```bash
docker-compose build llm-gateway
docker-compose up -d llm-gateway
```

## 📡 API Reference

### 🧠 LLM Gateway (Port 8003)

#### GET /health
Verifica el estado del gateway:
```bash
curl http://localhost:8003/health
```

#### GET /mcp/llm/list
Lista todos los modelos disponibles:
```bash
curl -X GET http://localhost:8003/mcp/llm/list
```

Respuesta:
```json
{
  "llms": [
    {
      "name": "bedrock-nova-pro",
      "provider": "aws",
      "description": "AWS Bedrock Nova Pro - Advanced reasoning model"
    },
    {
      "name": "gpt-4o",
      "provider": "openai",
      "description": "OpenAI GPT-4o - Most capable model"
    },
    {
      "name": "gemini-pro",
      "provider": "google",
      "description": "Google Gemini - Advanced multimodal AI model (using gemini-1.5-flash)"
    }
  ]
}
```

#### POST /mcp/llm/generate
Genera una respuesta con el modelo especificado:
```bash
curl -X POST http://localhost:8003/mcp/llm/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-pro",
    "messages": [
      {"role": "user", "content": "Explain quantum computing"}
    ],
    "temperature": 0.7,
    "max_tokens": 2000
  }'
```

#### GET /metrics
Obtiene métricas del gateway:
```bash
curl http://localhost:8003/metrics
```

Respuesta:
```json
{
  "total_requests": 42,
  "total_tokens": 15234,
  "total_cost_usd": 0.0523,
  "average_latency_ms": 1234.5,
  "cache_hit_rate": 0.35,
  "requests_by_model": {
    "bedrock-nova-pro": 20,
    "gpt-4o": 12,
    "gemini-pro": 10
  }
}
```

#### POST /cache/clear
Limpia el cache:
```bash
curl -X POST http://localhost:8003/cache/clear
```

### 🔧 MCP Toolbox (Port 8000)

#### GET /health
```bash
curl http://localhost:8000/health
```

Respuesta:
```json
{
  "status": "healthy",
  "service": "mcp-toolbox",
  "tools_count": 4,
  "protocol": "MCP over HTTP REST"
}
```

#### POST /mcp/tools/list
Lista todas las herramientas disponibles:
```bash
curl -X POST http://localhost:8000/mcp/tools/list
```

#### POST /mcp/tools/call
Ejecuta una herramienta:
```bash
curl -X POST http://localhost:8000/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "add", "arguments": {"a": 5, "b": 3}}'
```

### 🤖 Agent HTTP - REST API (Port 8001)

#### GET /health
Verifica el estado del agente:

```bash
curl http://localhost:8001/health
```

Respuesta:
```json
{
  "status": "healthy",
  "mcp_connected": true,
  "bedrock_available": true
}
```

#### POST /process
Procesa una query usando el agente con LangGraph.

**Sintaxis básica:**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{
    "input": "¿Cuánto es 5 + 3?",
    "model": "bedrock-nova-pro"
  }'
```

**Ejemplo 1: Suma con Bedrock (default)**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "¿Cuánto es 5 + 3?"}'
```

**Ejemplo 2: Con Gemini (especificado)**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Multiplica 7 por 8", "model": "gemini-pro"}'
```

**Ejemplo 3: Detección automática de modelo**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "usa gemini, convierte HELLO a mayúsculas"}'
```

**Ejemplo 4: Operaciones complejas**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Multiplica 25 por 8, luego convierte el resultado a texto en mayúsculas"}'
```

**Con PowerShell:**
```powershell
$body = @{
    input = "usa gemini, cuanto es 10 + 5"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8001/process" `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

Respuesta:
```json
{
  "result": "La suma de 5 y 3 es 8",
  "steps": [
    {
      "node": "process_input",
      "timestamp": "2024-11-03T19:00:00",
      "input": "¿Cuánto es 5 + 3?",
      "model_selected": "bedrock-nova-pro"
    },
    {
      "node": "llm",
      "timestamp": "2024-11-03T19:00:01",
      "model": "bedrock-nova-pro",
      "has_tool_calls": true
    },
    {
      "node": "tool_execution",
      "timestamp": "2024-11-03T19:00:01",
      "tools": [
        {"name": "add", "args": {"a": 5, "b": 3}, "result": "8"}
      ]
    },
    {
      "node": "llm",
      "timestamp": "2024-11-03T19:00:02",
      "model": "bedrock-nova-pro",
      "has_tool_calls": false
    },
    {"node": "final_answer", "timestamp": "2024-11-03T19:00:02"}
  ]
}
```

**Modelos disponibles:**
- `bedrock-nova-pro` - AWS Bedrock Nova Pro (default)
- `gpt-4o` - OpenAI GPT-4o
- `gemini-pro` - Google Gemini 1.5 Flash

**Detección automática:**
El agente puede detectar el modelo desde el prompt con palabras clave:
- "usa openai", "use gpt", "con gpt-4" → OpenAI
- "usa gemini", "use google", "con gemini" → Gemini
- "usa bedrock", "use nova", "con aws" → Bedrock

---

### 🔌 Agent WebSocket - Real-time Streaming (Port 8002)

#### GET /health
Verifica el estado del agente WebSocket:

```bash
curl http://localhost:8002/health
```

Respuesta:
```json
{
  "status": "healthy",
  "service": "websocket-agent",
  "mcp_connected": true,
  "mcp_tools": 4,
  "active_connections": 0
}
```

#### WebSocket /ws/{connection_id}
Conexión WebSocket para comunicación en tiempo real con streaming de respuestas.

**Usando el cliente HTML:**
1. Abre `test-websocket.html` en tu navegador
2. La conexión se establece automáticamente
3. Escribe mensajes como:
   - "Suma 10 y 5"
   - "usa gemini, multiplica 25 por 8"
   - "Convierte HOLA a mayúsculas"

**Mensaje con modelo específico:**
```javascript
{
  "type": "message",
  "content": "Suma 100 y 50",
  "model": "gemini-pro"  // Opcional
}
```

**Usando JavaScript:**
```javascript
const connectionId = 'user-' + Date.now();
const ws = new WebSocket(`ws://localhost:8002/ws/${connectionId}`);

ws.onopen = () => {
    console.log('Conectado');
    
    // Enviar mensaje con modelo específico
    ws.send(JSON.stringify({
        type: 'message',
        content: 'usa gemini, suma 100 y 50',
        model: 'gemini-pro'  // Opcional, también detecta del texto
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Recibido:', data);
    
    switch(data.type) {
        case 'connected':
            console.log('✅ Conectado:', data.message);
            break;
        case 'start':
            console.log('🚀', data.message);
            break;
        case 'step':
            console.log(`⚙️ ${data.node}:`, data.message);
            if (data.model) {
                console.log('  🧠 Modelo:', data.model);
            }
            break;
        case 'tool_call':
            console.log('🔧 Llamando:', data.tool, data.args);
            break;
        case 'tool_result':
            console.log('✅ Resultado:', data.tool, '→', data.result);
            break;
        case 'response':
            console.log('🤖 Respuesta:', data.content);
            break;
        case 'complete':
            console.log('✓ Completado en', data.steps, 'pasos');
            break;
        case 'error':
            console.error('❌ Error:', data.message);
            break;
    }
};

ws.onerror = (error) => console.error('Error:', error);
ws.onclose = () => console.log('Desconectado');
```

**Usando wscat (Node.js):**
```bash
npm install -g wscat
wscat -c ws://localhost:8002/ws/test-client

# Enviar mensaje
> {"type":"message","content":"usa gemini, suma 10 y 5"}

# Recibirás streaming en tiempo real:
< {"type":"start","message":"Procesando..."}
< {"type":"step","node":"process_input","model":"gemini-pro"}
< {"type":"step","node":"llm","model":"gemini-pro","message":"Consultando LLM..."}
< {"type":"tool_call","tool":"add","args":{"a":10,"b":5}}
< {"type":"tool_result","tool":"add","result":"15"}
< {"type":"response","content":"La suma de 10 y 5 es 15"}
< {"type":"complete","steps":5}
```
```

**Usando Python:**
```python
import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8002/ws"
    async with websockets.connect(uri) as websocket:
        # Enviar mensaje
        await websocket.send(json.dumps({
            "type": "message",
            "content": "Suma 10 y 5"
        }))
        
        # Recibir respuestas en streaming
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(f"{data['type']}: {data}")
            
            if data['type'] == 'complete':
                break

asyncio.run(test_websocket())
```

## 🛠️ Herramientas Disponibles

El MCP Server expone 4 herramientas que Claude puede usar:

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `add` | Suma dos números | `a: float, b: float` |
| `multiply` | Multiplica dos números | `a: float, b: float` |
| `uppercase` | Convierte texto a mayúsculas | `text: string` |
| `count_words` | Cuenta palabras en un texto | `text: string` |

## 💡 Ejemplos de Uso Completos

### 🧠 Selección de Modelos LLM

**Modelo por defecto (Bedrock):**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Suma 10 y 5"}'
```

**Especificando modelo explícitamente:**
```bash
# Con Gemini
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Multiplica 7 por 8", "model": "gemini-pro"}'

# Con OpenAI (si tienes créditos)
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Cuenta las palabras en: hola mundo", "model": "gpt-4o"}'
```

**Detección automática desde el prompt:**
```bash
# Detecta Gemini
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "usa gemini, cuanto es 15 + 25"}'

# Detecta OpenAI
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "con gpt-4, convierte HELLO a mayúsculas"}'

# Detecta Bedrock
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "usa bedrock, multiplica 3 por 9"}'
```

### 📡 HTTP REST Agent

**Matemáticas básicas:**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Calcula 10 multiplicado por 5"}'
```

**Procesamiento de texto:**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Convierte hello world a mayúsculas"}'
```

**Combinación de herramientas:**
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Suma 4 y 6, luego multiplica el resultado por 2"}'
```

**Con PowerShell:**
```powershell
# Suma con Bedrock
$body = '{"input":"Suma 100 y 50"}'
Invoke-WebRequest -Uri "http://localhost:8001/process" -Method POST -Body $body -ContentType "application/json"

# Multiplicación con Gemini
$body = '{"input":"usa gemini, multiplica 25 por 8"}'
Invoke-WebRequest -Uri "http://localhost:8001/process" -Method POST -Body $body -ContentType "application/json"

# Texto
$body = '{"input":"Convierte HOLA MUNDO a mayúsculas y cuenta las palabras"}'
Invoke-WebRequest -Uri "http://localhost:8001/process" -Method POST -Body $body -ContentType "application/json"
```

### 🔌 WebSocket Agent

**Usando el cliente HTML (Recomendado):**
1. Abre el archivo `test-websocket.html` en tu navegador
2. Verás una interfaz bonita con el estado de conexión
3. Escribe en el input y presiona Enter o clic en "Enviar"
4. Observa el streaming en tiempo real de cada paso
5. Los steps mostrarán el modelo usado (en el campo `model`)

**Ejemplos de mensajes:**
- "Suma 10 y 5"
- "usa gemini, multiplica 7 por 8"
- "con gpt-4, convierte HELLO a mayúsculas"
- "usa bedrock, cuenta palabras en: el cielo es azul"

**Pruebas desde línea de comandos:**
```bash
# Instalar wscat
npm install -g wscat

# Conectar
wscat -c ws://localhost:8002/ws/test-123

# Probar diferentes comandos:
> {"type":"message","content":"Suma 10 y 5"}
> {"type":"message","content":"usa gemini, multiplica 100 por 2"}
> {"type":"message","content":"Convierte python a mayúsculas","model":"gemini-pro"}
> {"type":"message","content":"Cuenta las palabras en: El MCP es genial"}
```

### 🧪 Verificar Métricas del LLM Gateway

```bash
# Ver métricas actuales
curl http://localhost:8003/metrics

# Limpiar cache
curl -X POST http://localhost:8003/cache/clear

# Listar modelos disponibles
curl http://localhost:8003/mcp/llm/list
```

## 🔍 Logs y Debugging

**Ver todos los logs en tiempo real:**
```bash
docker-compose logs -f
```

**Ver logs de un servicio específico:**
```bash
docker-compose logs -f llm-gateway
docker-compose logs -f agent-http
docker-compose logs -f agent-websocket
docker-compose logs -f toolbox
```

**Ver últimas 50 líneas:**
```bash
docker-compose logs --tail 50 agent-http
```

**Buscar errores en PowerShell:**
```powershell
docker-compose logs agent-http | Select-String -Pattern "error|Error|ERROR"
```

**Los logs muestran:**
- ✅ Inicialización del LLM Gateway con 3 proveedores
- ✅ Conexión MCP client ↔ servers
- ✅ Discovery de herramientas (4 tools)
- ✅ Selección de modelo (Bedrock/OpenAI/Gemini)
- ✅ Llamadas a LLMs con cache hit/miss
- ✅ Ejecución de herramientas via MCP
- ✅ Métricas de costos y tokens
- ✅ Conexiones WebSocket activas
- ✅ Streaming de mensajes en tiempo real

## 🛑 Detener el Sistema

```bash
docker-compose down
```

## 🔧 Desarrollo

### Reconstruir después de cambios

```bash
docker-compose up --build
```

### Ver logs de un servicio específico

```bash
docker-compose logs -f agent
docker-compose logs -f mcp-server
```

## 📚 Tecnologías

- **Python 3.11** - Runtime
- **FastAPI** - Framework web para REST y WebSocket
- **LangGraph** - Orquestación de workflows con grafos
- **LangChain** - Framework para LLM
- **Amazon Bedrock** - Nova Pro (modelo LLM)
- **MCP (Model Context Protocol)** - Protocolo de herramientas sobre HTTP REST
- **WebSocket** - Comunicación bidireccional en tiempo real
- **Docker & Docker Compose** - Containerización y orquestación
- **httpx** - Cliente HTTP asíncrono
- **boto3** - SDK de AWS para Bedrock

## ⚠️ Notas Importantes

- **NO subir el archivo `.env`** a GitHub (ya está en `.gitignore`)
- Las credenciales de AWS son sensibles - manéjalas con cuidado
## 📝 Notas Importantes

- **Arquitectura de microservicios**: 4 contenedores independientes (LLM Gateway, Toolbox, Agent HTTP, Agent WebSocket)
- **LLM Gateway centralizado**: Un solo punto para gestionar múltiples proveedores de IA
- **Credenciales seguras**: Solo el LLM Gateway tiene las API keys, los agentes no las necesitan
- **Cache inteligente**: Reduce costos y mejora latencia con TTL configurable
- **MCP sobre HTTP REST**: Protocolo MCP real con transporte HTTP para compatibilidad K8s
- **Selección dinámica de modelos**: Cambia entre Bedrock/OpenAI/Gemini por request o desde el prompt
- **Métricas en tiempo real**: Tracking de costos, tokens, latencia y cache hit rate
- **Listo para Kubernetes**: Funciona perfecto en EKS con service discovery
- **WebSocket vs HTTP**: WebSocket para UIs interactivas, HTTP para integraciones
- **Arquitectura centralizada**: Ambos agentes comparten el mismo Toolbox y LLM Gateway
- Los contenedores se reinician automáticamente si fallan
- Si tu `AWS_SECRET_ACCESS_KEY` tiene `/`, regenera las credenciales (causa errores de firma)

## 🎯 Casos de Uso

### Cuándo usar Agent HTTP (REST):
- ✅ Integraciones con otros servicios/APIs
- ✅ APIs públicas REST
- ✅ Webhooks
- ✅ Automatizaciones batch
- ✅ Sistemas que necesitan caching
- ✅ Request/response simple

### Cuándo usar Agent WebSocket:
- ✅ Chatbots interactivos
- ✅ Aplicaciones de chat en tiempo real
- ✅ Dashboards que necesitan updates live
- ✅ Streaming de respuestas largas
- ✅ Notificaciones push
- ✅ Ver el "pensamiento" del agente paso a paso

### Cuándo usar cada LLM:
- **Bedrock Nova Pro** (`bedrock-nova-pro`):
  - ✅ Razonamiento complejo
  - ✅ Largo contexto (300K tokens)
  - ✅ Costo medio
  - ✅ Mejor para análisis profundo

- **OpenAI GPT-4o** (`gpt-4o`):
  - ✅ Más capaz y versátil
  - ✅ Mejor en seguir instrucciones
  - ✅ Costo más alto
  - ✅ Requiere créditos activos

- **Gemini 1.5 Flash** (`gemini-pro`):
  - ✅ Más rápido
  - ✅ Costo más bajo
  - ✅ Bueno para tareas simples
  - ✅ Excelente para producción

## 🏢 Deployment a AWS/EKS

Este proyecto está **listo para producción** en AWS EKS. Ver guía completa en [`docs/DEPLOYMENT_EKS.md`](./docs/DEPLOYMENT_EKS.md)

**Resumen de deployment:**

1. **Crear repositorios ECR** para las 4 imágenes (llm-gateway, toolbox, agent-http, agent-websocket)
2. **Push imágenes Docker** a ECR
3. **Crear cluster EKS** (o usar existente)
4. **Configurar Secrets Manager** con credenciales (AWS, OpenAI, Gemini)
5. **Aplicar manifiestos K8s**:
   ```bash
   kubectl apply -f k8s/namespace.yaml
   kubectl apply -f k8s/llm-gateway-deployment.yaml
   kubectl apply -f k8s/llm-gateway-service.yaml
   kubectl apply -f k8s/mcp-toolbox-deployment.yaml
   kubectl apply -f k8s/mcp-toolbox-service.yaml
   kubectl apply -f k8s/agent-deployment.yaml
   kubectl apply -f k8s/agent-service.yaml
   kubectl apply -f k8s/websocket-agent-deployment.yaml
   kubectl apply -f k8s/websocket-agent-service.yaml
   kubectl apply -f k8s/ingress.yaml
   ```

**Service Discovery en Kubernetes:**
```yaml
# Los agents se conectan via DNS interno:
LLM_GATEWAY_URL: "http://llm-gateway.mcp-system.svc.cluster.local:8003"
MCP_SERVER_URL: "http://mcp-toolbox.mcp-system.svc.cluster.local:8000"
```

**Arquitectura en EKS:**
```
Internet → ALB Ingress → {
    /api/http → Agent HTTP Service → Agent HTTP Pods
    /api/ws   → WebSocket Agent Service → WebSocket Agent Pods
}

Agent HTTP Pods ────┬──→ LLM Gateway Service → LLM Gateway Pods → {Bedrock, OpenAI, Gemini}
                    │
WebSocket Agent ────┤
                    │
                    └──→ MCP Toolbox Service → MCP Toolbox Pods
```

## 📖 Documentación Adicional

- [`docs/DEPLOYMENT_EKS.md`](./docs/DEPLOYMENT_EKS.md) - Guía completa de despliegue en AWS EKS
- [`docs/WEBSOCKET_AGENT.md`](./docs/WEBSOCKET_AGENT.md) - Documentación del Agent WebSocket
- [`test-websocket.html`](./test-websocket.html) - Cliente de prueba interactivo
- [`k8s/`](./k8s/) - Manifiestos de Kubernetes listos para usar

## 🚀 Quick Start

```bash
# 1. Clonar repo
git clone https://github.com/LeonAchata/MCP-Server-Prueba.git
cd MCP-Example

# 2. Configurar credenciales (al menos un proveedor)
nano .env
# Agregar credenciales de AWS Bedrock, OpenAI o Google Gemini

# 3. Levantar servicios
docker-compose up -d

# 4. Verificar que todo esté funcionando
docker-compose ps
docker-compose logs -f

# 5. Probar HTTP Agent
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input":"Suma 10 y 5"}'

# 6. Probar con diferentes modelos
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input":"usa gemini, multiplica 7 por 8"}'

# 7. Probar WebSocket Agent
# Abre test-websocket.html en tu navegador

# 8. Ver métricas del gateway
curl http://localhost:8003/metrics
```

## 🔧 Troubleshooting

### Error: "LLM Gateway error (404): LLM 'xxx' not found"
- Verifica que el nombre del modelo sea correcto: `bedrock-nova-pro`, `gpt-4o`, o `gemini-pro`
- Revisa los logs: `docker-compose logs llm-gateway --tail=50`

### Error: OpenAI "insufficient_quota"
- No tienes créditos en tu cuenta de OpenAI
- Solución: Usa Bedrock o Gemini, o agrega créditos en OpenAI

### Error: Gemini "model not found"
- Verifica que `GEMINI_DEFAULT_MODEL=gemini-1.5-flash` en tu `.env`
- Asegúrate de tener habilitada la API de Gemini en Google Cloud

### Error: "RuntimeError: Event loop is closed"
- Ya fue corregido en la versión actual
- Si persiste, verifica que estés usando `async/await` correctamente

### Los contenedores no inician
```bash
# Ver logs detallados
docker-compose logs

# Reconstruir todo desde cero
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Si encuentras un bug o tienes una mejora:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 📝 Licencia

Este es un proyecto de aprendizaje personal. Libre de usar para propósitos educativos.

## 👨‍💻 Autor

**Leon Achata**
- GitHub: [@LeonAchata](https://github.com/LeonAchata)
- Proyecto: [MCP-Server-Prueba](https://github.com/LeonAchata/MCP-Server-Prueba)

---

**Happy coding! 🚀**

*Sistema Multi-Agent con MCP Protocol + LLM Gateway - Production Ready*
