# Oportunidades de Mejora en el Frontend

## 1. Duplicidad de código y violaciones a DRY

- Agrupación y procesamiento de datos repetidos en MatchCard y OddsComparison. Extraer a helper/hook reutilizable.
- Formateo de fechas repetido. Unificar en utilitario común.

## 2. Componentes con demasiadas responsabilidades

- OddsDisplay.jsx: Orquesta agrupación, ordenamiento, renderizado y lógica de selección. Dividir en subcomponentes y delegar lógica a hooks/helpers.
- App.jsx: Contiene lógica de estado y handlers. Limitar a composición de componentes y delegar lógica a hooks personalizados.

## 3. Consistencia en el uso de hooks y props

- Props anidados y estructuras complejas. Mejorar definición y documentación de props.
- Uso de hooks personalizados correcto, pero dividir si crece la lógica de negocio.

## 4. Experiencia de usuario y flujos

- Textos y mensajes en inglés. Traducir y centralizar en archivo de constantes.
- Accesibilidad: Mejorar descripciones accesibles (aria-labels) en botones y selects.
- Feedback visual: Mensajes de carga y error pueden ser más descriptivos y en español.

## 5. Estructura de carpetas y modularización

- Crear carpeta /utils para helpers y lógica compartida.
- Centralizar textos, opciones de búsqueda rápida y valores estáticos.

## 6. Principios SOLID

- Single Responsibility: Separar responsabilidades en componentes grandes.
- Open/Closed: Facilitar extensión de componentes (ej. nuevos tipos de búsqueda en SearchForm).

---

**Este documento servirá como referencia para priorizar y ejecutar las refactorizaciones y mejoras en el frontend.**
