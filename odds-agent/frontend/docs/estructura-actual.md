# Revisión de la Estructura y Componentes del Frontend

## 1. Estructura de Carpetas y Archivos

- **src/**
  - `App.jsx` (componente raíz, contiene lógica y composición)
  - **components/**
    - `Header.jsx` (encabezado)
    - `LoadingSpinner.jsx` (spinner de carga)
    - `MatchCard.jsx` (tarjeta de partido)
    - `OddsComparison.jsx` (comparación detallada de cuotas)
    - `OddsDisplay.jsx` (muestra lista de partidos/cuotas)
    - `SearchForm.jsx` (formulario de búsqueda)
  - **hooks/**
    - `useOddsData.js` (hook personalizado para lógica de cuotas)
  - **services/**
    - `langGraphAgent.js` (servicio para procesamiento de lenguaje natural)
    - `oddsService.js` (servicio para obtención de cuotas, equipos y partidos)
  - `index.css` (estilos globales)
  - `main.jsx` (entrypoint de React)

## 2. Dependencias Principales (`package.json`)

- React 18, ReactDOM 18
- Axios (peticiones HTTP)
- TailwindCSS (estilos)
- Vite (build y dev server)
- Vitest (testing)
- Tipos para React y ReactDOM

## 3. Componentes y Hooks Existentes

- **Componentes:**

  - `Header`: Encabezado con branding y descripción.
  - `LoadingSpinner`: Indicador de carga.
  - `MatchCard`: Tarjeta individual de partido, muestra mejores cuotas y regiones.
  - `OddsComparison`: Tabla detallada de cuotas por resultado y casa de apuestas.
  - `OddsDisplay`: Orquesta la visualización de partidos, permite seleccionar uno para detalle.
  - `SearchForm`: Formulario para buscar partidos, soporta búsqueda natural y directa.

- **Hooks:**

  - `useOddsData`: Maneja estado de cuotas, loading, error, y lógica de búsqueda (incluye integración con servicios).

- **Servicios:**
  - `langGraphAgent`: Procesa queries en lenguaje natural, obtiene sugerencias y valida queries.
  - `oddsService`: Obtiene cuotas, equipos y partidos desde la API.

## 4. Archivos Grandes o con Demasiadas Responsabilidades

- `App.jsx`: Contiene lógica de estado, handlers y composición de componentes. Debería limitarse a composición.
- `OddsDisplay.jsx`: Orquesta lógica de agrupación, ordenamiento y renderizado de partidos y detalles.
- `useOddsData.js`: Centraliza la lógica de negocio para obtención de cuotas, pero está bien abstraído.

---

## Mapa de Componentes (Flujo Principal)

```
App.jsx
 ├─ Header
 ├─ SearchForm
 ├─ LoadingSpinner (condicional)
 ├─ OddsDisplay
 │    ├─ MatchCard (por cada partido)
 │    └─ OddsComparison (si hay partido seleccionado)
```

---

**Este documento resume la estructura y hallazgos actuales del frontend para facilitar la identificación de mejoras y la planificación de refactorizaciones.**
