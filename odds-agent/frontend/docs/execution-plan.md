# 🛠️ Plan Detallado de Refactorización Frontend

> **Nota:** Solo se debe ejecutar una tarea a la vez. Marca el check `[x]` cuando completes cada tarea.

---

## 1. Revisión del Proyecto Actual

- [x] **Revisar la estructura y componentes actuales en `/frontend/`**
  - Complejidad: Baja
  - **Subtareas:**
    - [x] Analizar la estructura de carpetas y archivos.
    - [x] Revisar dependencias en `package.json` y detectar posibles obsoletas o innecesarias.
    - [x] Listar todos los componentes y hooks existentes.
    - [x] Identificar archivos grandes o con demasiadas responsabilidades.
  - **Criterio de aceptación:** Documento con hallazgos y mapa de componentes.

## 2. Identificación de Mejoras

- [x] **Detectar oportunidades de mejora en arquitectura, código y experiencia de usuario**
  - Complejidad: Media
  - **Subtareas:**
    - [x] Identificar duplicidad de código y violaciones a DRY.
    - [x] Detectar componentes con demasiadas responsabilidades (violación de Single Responsibility).
    - [x] Revisar consistencia en el uso de hooks y props.
    - [x] Analizar la experiencia de usuario y flujos de navegación.
    - [x] Proponer mejoras en la estructura de carpetas y modularización.
  - **Criterio de aceptación:** Lista priorizada de mejoras sugeridas.

## 3. Limpieza de `App.jsx`

- [ ] **Extraer toda la lógica de `App.jsx` y dejar solo la importación y composición de componentes**
  - Complejidad: Media
  - **Subtareas:**
    - [ ] Mover hooks personalizados a `/hooks`.
    - [ ] Extraer handlers y lógica de negocio a componentes hijos o hooks.
    - [ ] Dejar en `App.jsx` solo la composición de componentes y el layout general.
    - [ ] Documentar los cambios realizados.
  - **Criterio de aceptación:** `App.jsx` solo importa y compone componentes, sin lógica interna.

## 4. Aplicación del Patrón Builder (si es viable)

- [ ] **Evaluar y aplicar el patrón Builder donde aporte claridad y escalabilidad**
  - Complejidad: Alta
  - **Subtareas:**
    - [ ] Investigar puntos donde la construcción de objetos o configuraciones sea compleja (por ejemplo, armado de queries, configuración de componentes, etc).
    - [ ] Proponer y documentar un ejemplo de implementación del patrón Builder.
    - [ ] Refactorizar el código aplicando el patrón donde sea útil.
    - [ ] Documentar ventajas y posibles limitaciones.
  - **Criterio de aceptación:** Al menos un caso de uso real con patrón Builder implementado y documentado.

## 5. Mejor Componetización y Principios DRY/SOLID

- [ ] **Reestructurar componentes para maximizar reutilización y adherencia a DRY/SOLID**
  - Complejidad: Alta
  - **Subtareas:**
    - [ ] Identificar componentes que pueden dividirse en subcomponentes reutilizables.
    - [ ] Unificar lógica repetida en hooks o utilidades.
    - [ ] Separar responsabilidades en componentes grandes.
    - [ ] Aplicar principios SOLID (especialmente Single Responsibility y Open/Closed).
    - [ ] Documentar la nueva estructura de componentes.
  - **Criterio de aceptación:** Componentes pequeños, reutilizables y bien documentados.

## 6. Aplicar Clean Code

- [ ] **Refactorizar el código para que sea limpio, legible y mantenible**
  - Complejidad: Media
  - **Subtareas:**
    - [ ] Renombrar variables y funciones para mayor claridad.
    - [ ] Eliminar código muerto o no utilizado.
    - [ ] Añadir comentarios útiles solo donde sea necesario.
    - [ ] Limitar la longitud de funciones y componentes.
    - [ ] Asegurar consistencia en el estilo de código (indentación, comillas, etc).
  - **Criterio de aceptación:** Código fácil de leer, entender y mantener.

## 7. Localización: Textos en Español

- [ ] **Traducir todos los textos de la app al español**
  - Complejidad: Baja
  - **Subtareas:**
    - [ ] Identificar todos los textos hardcodeados en los componentes.
    - [ ] Traducir títulos, botones, mensajes de error y ayuda.
    - [ ] Revisar que no queden textos en inglés.
    - [ ] (Opcional) Centralizar textos en un archivo de constantes para facilitar futuras traducciones.
  - **Criterio de aceptación:** Toda la interfaz está en español.

---

¿Te gustaría revisar o modificar este plan antes de comenzar con la ejecución de las tareas? Si tienes sugerencias o quieres agregar/quitar pasos, házmelo saber antes de iniciar.
