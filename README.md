# ScrapOddsAPI

Aplicación monolítica organizada para obtener, analizar y mostrar cuotas de apuestas deportivas de la Premier League usando scraping, backend y frontend modernos.

## Arquitectura del Proyecto

La app está organizada en tres grandes módulos:

- **scrapping/**: Scripts de Python para obtener y procesar datos desde The Odds API. Exporta los datos a CSV para análisis o consumo por el backend.
- **odds-agent/backend/**: API REST construida en Node.js + Express. Expone endpoints para servir datos de apuestas y lógica de agente.
- **odds-agent/frontend/**: Aplicación web en React (Vite) para mostrar y comparar cuotas de apuestas de manera visual e interactiva.

```
ScrapOddsAPI/
├── scrapping/           # Scraper y procesamiento de datos (Python)
├── odds-agent/
│   ├── backend/         # Backend Node/Express
│   └── frontend/        # Frontend React/Vite
└── .env                 # Variables de entorno globales (API keys, etc)
```

## Instalación y Setup

### 1. Clona el repositorio

```bash
git clone <your-repository-url>
cd ScrapOddsAPI
```

### 2. Variables de entorno

Crea un archivo `.env` en la raíz con tu API key:

```
ODDS_API_KEY=your_actual_api_key_here
```

### 3. Instala dependencias

- **Frontend y Backend (Node):**
  ```bash
  npm install
  ```
  Esto instalará las dependencias globales y de cada subproyecto.
- **Scrapping (Python):**
  ```bash
  cd scrapping
  pip install -r requirements.txt
  ```

## Comandos de desarrollo

- **Levantar toda la app (frontend + backend):**
  ```bash
  npm run dev
  ```
- **Levantar solo el backend:**
  ```bash
  npm run server --prefix odds-agent/backend
  ```
- **Levantar solo el frontend:**
  ```bash
  npm run dev --prefix odds-agent/frontend
  ```
- **Ejecutar el scrapper:**
  ```bash
  python scrapping/test.py
  ```

## Testing

- **Frontend:**
  ```bash
  npm test --prefix odds-agent/frontend
  ```
- **Backend:**
  ```bash
  npm test --prefix odds-agent/backend
  ```

## Estructura de carpetas

- `scrapping/`: Scripts de scraping y procesamiento de datos (Python)
- `odds-agent/backend/`: API REST y lógica de negocio (Node.js/Express)
- `odds-agent/frontend/`: Interfaz de usuario (React/Vite)
- `.env`: Variables de entorno globales (API keys, etc)

## Dependencias principales

- **Frontend:** React, Vite, TailwindCSS, Vitest, Testing Library
- **Backend:** Express, dotenv, cors, Jest, Supertest
- **Scrapping:** httpx, pandas, python-dotenv, numpy

## Notas

- El archivo `.env` debe estar en la raíz para que tanto backend como scrapping lo encuentren.
- Los datos generados por el scrapping se guardan en `scrapping/` y pueden ser consumidos por el backend o analizados manualmente.
- El frontend consume la API del backend para mostrar los datos de apuestas.

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama de feature
3. Haz tus cambios y tests
4. Abre un Pull Request

---

**Nota:** Este proyecto es para fines educativos. Respeta siempre los términos de uso de las APIs y servicios utilizados.
