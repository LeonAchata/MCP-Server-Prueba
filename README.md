# 🤖 LangGraph Agent + MCP Server with Bedrock

Sistema de aprendizaje sobre **Model Context Protocol (MCP)** usando LangGraph + Amazon Bedrock Claude 3.5.

## 📋 Descripción

Este proyecto implementa un agente inteligente que:
- Usa **LangGraph** para orquestar el flujo de trabajo
- Se conecta a **Amazon Bedrock Claude 3.5** como LLM
- Comunica con un **MCP Server** que expone 4 herramientas simples
- Todo containerizado con **Docker** para fácil deployment

## 🏗️ Arquitectura

```
┌──────────────────────────────────────────────────────┐
│              Docker Network (mcp-network)             │
│                                                       │
│  ┌────────────────┐         ┌──────────────────┐    │
│  │  MCP Server    │◄────────┤     Agent        │    │
│  │                │  stdio  │                  │    │
│  │  4 Tools:      │         │  • FastAPI       │    │
│  │  • add         │         │  • LangGraph     │    │
│  │  • multiply    │         │  • Bedrock       │    │
│  │  • uppercase   │         │  • MCP Client    │    │
│  │  • count_words │         │                  │    │
│  └────────────────┘         └──────────────────┘    │
│                                      │               │
└──────────────────────────────────────┼───────────────┘
                                       │
                              Usuario (POST /process)
```

## 📁 Estructura del Proyecto

```
JLR/
├── agent/                      # Agente principal
│   ├── src/
│   │   ├── graph/             # LangGraph workflow
│   │   ├── mcp/               # Cliente MCP
│   │   ├── api/               # FastAPI routes
│   │   ├── config.py          # Configuración
│   │   └── main.py            # Entry point
│   ├── Dockerfile
│   └── requirements.txt
│
├── mcp-server/                # Servidor MCP
│   ├── src/
│   │   ├── tools/             # 4 herramientas
│   │   ├── server.py          # MCP server
│   │   └── config.py          # Configuración
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml         # Orquestación
├── .env                       # Variables de entorno (NO SUBIR)
├── .env.example              # Template
└── README.md
```

## 🚀 Instalación y Uso

### Prerrequisitos

- Docker y Docker Compose instalados
- Credenciales de AWS con acceso a Bedrock
- Claude 3.5 habilitado en tu cuenta AWS

### Configuración

1. **Clona el repositorio**

```bash
git clone <tu-repo>
cd JLR
```

2. **Configura las variables de entorno**

Copia el archivo de ejemplo y edita con tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con tus credenciales de AWS:

```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
LOG_LEVEL=DEBUG
```

### Ejecución

**Construir e iniciar los contenedores:**

```bash
docker-compose up --build
```

El sistema iniciará:
- MCP Server (interno)
- Agent API en `http://localhost:8001`

## 📡 Endpoints

### GET /health

Verifica el estado del sistema:

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

### POST /process

Procesa una query en lenguaje natural:

```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "¿Cuánto es 5 + 3?"}'
```

Respuesta:
```json
{
  "result": "El resultado de 5 + 3 es 8",
  "steps": [
    {"node": "process_input", "timestamp": "..."},
    {"node": "llm", "timestamp": "..."},
    {"node": "tool_execution", "tools": [{"name": "add", "args": {...}}]},
    {"node": "llm", "timestamp": "..."},
    {"node": "final_answer", "timestamp": "..."}
  ]
}
```

## 🛠️ Herramientas Disponibles

El MCP Server expone 4 herramientas que Claude puede usar:

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `add` | Suma dos números | `a: float, b: float` |
| `multiply` | Multiplica dos números | `a: float, b: float` |
| `uppercase` | Convierte texto a mayúsculas | `text: string` |
| `count_words` | Cuenta palabras en un texto | `text: string` |

## 💡 Ejemplos de Uso

### Matemáticas básicas
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Calcula 10 multiplicado por 5"}'
```

### Procesamiento de texto
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Convierte hello world a mayúsculas"}'
```

### Combinación de herramientas
```bash
curl -X POST http://localhost:8001/process \
  -H "Content-Type: application/json" \
  -d '{"input": "Suma 4 y 6, luego multiplica el resultado por 2"}'
```

## 🔍 Logs

Para ver los logs en tiempo real:

```bash
docker-compose logs -f
```

Los logs muestran:
- Conexión MCP client ↔ server
- Discovery de herramientas
- Llamadas a Bedrock
- Ejecución de herramientas
- Resultados de cada paso

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

- **Python 3.11**
- **FastAPI** - API REST
- **LangGraph** - Orquestación de workflows
- **LangChain** - Framework LLM
- **Amazon Bedrock** - Claude 3.5 Sonnet
- **MCP (Model Context Protocol)** - Comunicación con herramientas
- **Docker** - Containerización

## ⚠️ Notas Importantes

- **NO subir el archivo `.env`** a GitHub (ya está en `.gitignore`)
- Las credenciales de AWS son sensibles - manéjalas con cuidado
- El sistema es para aprendizaje, no está optimizado para producción
- Los contenedores se reinician automáticamente si fallan

## 📝 Licencia

Este es un proyecto de aprendizaje personal.

---

**Happy coding! 🚀**
