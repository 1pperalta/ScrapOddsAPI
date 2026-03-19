# 🏆 ScrapOddsAPI

**Plataforma completa de análisis de cuotas de apuestas deportivas con IA**

Una aplicación full-stack que recopila, almacena y analiza cuotas de apuestas en tiempo real de las principales ligas europeas usando inteligencia artificial (Google Gemini).

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg)

## ✨ Características

- 📊 **Scraping Automatizado**: Recolección de cuotas de 6 ligas europeas principales
- 🤖 **Análisis con IA**: Análisis inteligente de partidos usando Google Gemini
- 💰 **Comparación de Cuotas**: Visualización de odds de múltiples casas de apuestas
- 🔍 **Búsqueda Inteligente**: Lenguaje natural y búsqueda directa
- 📈 **Value Betting**: Identificación de oportunidades de valor
- 🎨 **UI Moderna**: Interfaz React responsive con TailwindCSS

## 🏗️ Arquitectura

```
┌─────────────────┐
│  The Odds API   │  ← Fuente de datos en tiempo real
└────────┬────────┘
         ↓
┌─────────────────┐
│ Python Scrapper │  ← Recolección y procesamiento
└────────┬────────┘
         ↓
┌─────────────────┐
│   PostgreSQL    │  ← Almacenamiento persistente
└────────┬────────┘
         ↓
┌─────────────────┐
│ Flask + Gemini  │  ← Backend API + Agente IA
└────────┬────────┘
         ↓
┌─────────────────┐
│  React Frontend │  ← Interfaz de usuario
└─────────────────┘
```

### Módulos del Proyecto

- **scrapping/**: Scripts Python para obtener datos desde The Odds API y almacenarlos en PostgreSQL
- **odds-agent/backend/server_py/**: API REST en Flask con agente de IA (Google Gemini)
- **odds-agent/frontend/**: Aplicación React con Vite para visualización interactiva

## ⚽ Ligas Soportadas

- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League (Inglaterra)
- 🇪🇸 La Liga (España)
- 🇮🇹 Serie A (Italia)
- 🇩🇪 Bundesliga (Alemania)
- 🇫🇷 Ligue 1 (Francia)
- 🏆 Champions League (Europa)

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.11+ 
- Node.js 18+
- Docker Desktop
- API Keys: [The Odds API](https://the-odds-api.com/) + [Google Gemini](https://aistudio.google.com/app/apikey)

### Instalación Express (5 minutos)

```bash
# 1. Clonar repositorio
git clone <your-repo-url>
cd ScrapOddsAPI

# 2. Configurar variables de entorno
cd scrapping
echo "ODDS_API_KEY=tu_key_aqui" > .env
echo "GOOGLE_API_KEY=tu_key_aqui" >> .env
echo "DB_HOST=localhost" >> .env
echo "DB_PASSWORD=oddsupb" >> .env

# 3. Instalar dependencias Python
pip install -r requirements.txt

# 4. Iniciar base de datos
cd ..
docker-compose up -d

# 5. Ejecutar scrapper
cd scrapping
python scrapping.py

# 6. Instalar dependencias frontend
cd ../odds-agent/frontend
npm install
```

### Ejecutar la Aplicación

**Terminal 1 - Backend (Flask):**
```bash
cd odds-agent/backend/server_py
python3 app.py
```

**Terminal 2 - Frontend (React):**
```bash
cd odds-agent/frontend
npm run dev
```

**Acceder a:** http://localhost:3000

---

## 📁 Estructura del Proyecto

```
ScrapOddsAPI/
├── scrapping/              # Módulo de recolección de datos
│   ├── scrapping.py        # Script principal de scraping
│   ├── requirements.txt    # Dependencias Python
│   └── .env               # Variables de entorno
│
├── odds-agent/
│   ├── backend/
│   │   └── server_py/     # Backend Flask + Gemini AI
│   │       ├── app.py     # API REST
│   │       ├── agent.py   # Lógica del agente IA
│   │       └── services/  # Servicios de datos
│   │
│   └── frontend/          # Frontend React
│       ├── src/
│       │   ├── components/  # Componentes UI
│       │   ├── services/    # Llamadas a API
│       │   └── hooks/       # React hooks
│       └── package.json
│
├── docker-compose.yml     # Configuración PostgreSQL
├── README.md             # Este archivo
└── SETUP_GUIDE.md        # Guía detallada de instalación
```

## 🛠️ Stack Tecnológico

### Backend
- **Flask** - Framework web Python
- **Google Gemini 2.5 Flash** - Modelo de IA para análisis
- **PostgreSQL** - Base de datos relacional
- **psycopg2** - Conector PostgreSQL

### Frontend
- **React 18** - Librería UI
- **Vite** - Build tool y dev server
- **TailwindCSS** - Framework CSS
- **httpx** - Cliente HTTP

### Scraping & Data
- **The Odds API** - Fuente de datos de cuotas
- **httpx** - Cliente HTTP asíncrono
- **pandas** - Procesamiento de datos
- **Docker** - Contenedorización

## 🎯 Funcionalidades

### 1. Búsqueda Directa
Busca partidos específicos por equipos:
```
Arsenal vs Chelsea
Real Madrid vs Barcelona
```

### 2. Lenguaje Natural
Pregunta en lenguaje natural:
```
"Analiza el Manchester United"
"¿Cuáles son las mejores apuestas de hoy?"
"Dame value bets de la Premier League"
```

### 3. Comparación de Cuotas
- Visualiza odds de múltiples bookmakers
- Identifica las mejores cuotas disponibles
- Información de regiones (UK, US, AU, EU)

### 4. Análisis con IA
- Análisis de equipos y forma reciente
- Predicciones de partidos
- Recomendaciones de value betting
- Estrategias de apuesta

## 📊 API Endpoints

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/health` | GET | Health check del servidor |
| `/api/agent/analyze-team` | POST | Analizar equipo específico |
| `/api/agent/analyze-match` | POST | Analizar partido específico |
| `/api/agent/value-bets` | POST | Obtener value bets |
| `/api/agent/process` | POST | Query en lenguaje natural |
| `/api/agent/direct-search` | POST | Búsqueda directa de partido |

## 🧪 Testing

```bash
# Test de conexión API
curl http://localhost:3001/api/health

# Test de búsqueda directa
curl -X POST http://localhost:3001/api/agent/direct-search \
  -H "Content-Type: application/json" \
  -d '{"home_team": "Arsenal", "away_team": "Chelsea"}'
```

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama de feature: `git checkout -b feature/nueva-feature`
3. Commit tus cambios: `git commit -m 'Añadir nueva feature'`
4. Push a la rama: `git push origin feature/nueva-feature`
5. Abre un Pull Request

## 📝 Notas Importantes

- **Límites de API**: The Odds API tiene 500 requests/mes en el tier gratuito
- **Uso Responsable**: Este proyecto es para fines educativos
- **Costos**: Gemini API tiene tier gratuito con límites generosos
- **Datos**: Los datos persisten en volumes de Docker

## 📄 Licencia

Este proyecto es para fines educativos. Respeta siempre:
- Términos de uso de The Odds API
- Términos de uso de Google Gemini
- Prácticas de juego responsable

---

**⚡ Desarrollado con Python, React y Gemini AI**
