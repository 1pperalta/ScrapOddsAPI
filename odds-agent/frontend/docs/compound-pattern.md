# Patrón Compound Components en SearchForm

## ¿Qué es el Patrón Compound?

El patrón Compound Components permite crear componentes flexibles y reutilizables compartiendo estado implícitamente a través de Context API. Los componentes "hijos" trabajan juntos para formar una unidad funcional completa.

## Implementación en SearchForm

### Estructura

```
SearchForm/
├── index.jsx           # Componente principal con Context Provider
├── SearchFormContext.jsx  # Context y hook personalizado
├── ModeToggle.jsx      # Subcomponente: selector de modo de búsqueda
├── Input.jsx           # Subcomponente: campo de entrada
├── QuickSearch.jsx     # Subcomponente: botones de búsqueda rápida
└── HelpText.jsx        # Subcomponente: texto de ayuda contextual
```

### Uso

```jsx
<SearchForm onSearch={fetchOdds} loading={loading}>
  <SearchForm.ModeToggle />
  <SearchForm.Input />
  <SearchForm.QuickSearch />
  <SearchForm.HelpText />
</SearchForm>
```

## Ventajas

### 1. Flexibilidad
- Los consumidores pueden reorganizar los subcomponentes según necesidad
- Pueden omitir subcomponentes que no necesiten
- Pueden agregar elementos personalizados entre subcomponentes

Ejemplo de uso flexible:
```jsx
<SearchForm onSearch={handleSearch} loading={false}>
  <SearchForm.ModeToggle />
  <div className="my-custom-divider" />
  <SearchForm.Input />
  {/* Omitiendo QuickSearch y HelpText */}
</SearchForm>
```

### 2. Separación de Responsabilidades
- Cada subcomponente tiene una única responsabilidad
- Fácil de mantener y testear individualmente
- Código más limpio y organizado

### 3. Estado Compartido Implícito
- Los subcomponentes acceden al estado sin prop drilling
- Usa Context API para compartir estado de forma limpia
- Reduce la complejidad de pasar props manualmente

### 4. Composición Natural
- API intuitiva y fácil de entender
- Se lee como HTML semántico
- Facilita la comprensión del código

## Limitaciones

### 1. Mayor Número de Archivos
- Se crean múltiples archivos para un solo componente
- Puede parecer excesivo para componentes muy simples

### 2. Context API Overhead
- Pequeño overhead de performance por usar Context
- No recomendado si el estado cambia muy frecuentemente (en este caso no aplica)

### 3. Curva de Aprendizaje
- Desarrolladores nuevos deben entender el patrón Compound
- Requiere familiaridad con Context API

## Comparación: Antes vs Después

### Antes (Componente Monolítico)
```jsx
<SearchForm onSearch={fetchOdds} loading={loading} />
```
- **Pros**: Más simple de usar
- **Contras**: Inflexible, no se puede personalizar la estructura

### Después (Patrón Compound)
```jsx
<SearchForm onSearch={fetchOdds} loading={loading}>
  <SearchForm.ModeToggle />
  <SearchForm.Input />
  <SearchForm.QuickSearch />
  <SearchForm.HelpText />
</SearchForm>
```
- **Pros**: Flexible, composable, mantenible
- **Contras**: Más verboso al usar

## Cuándo Usar Este Patrón

✅ **Usar cuando:**
- El componente tiene múltiples partes lógicas que pueden reorganizarse
- Necesitas flexibilidad en la composición
- Los subcomponentes comparten estado
- Quieres mejorar la reusabilidad

❌ **No usar cuando:**
- El componente es muy simple (< 3 partes lógicas)
- La estructura nunca cambiará
- No hay estado compartido entre subcomponentes

## Conclusión

El patrón Compound implementado en `SearchForm` mejora significativamente la mantenibilidad y flexibilidad del código. Permite a los consumidores del componente personalizar la estructura según sus necesidades mientras mantiene la lógica compartida de forma limpia y eficiente.
