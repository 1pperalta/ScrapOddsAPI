export const TEXTS = {
  header: {
    title: "Agente de Cuotas Premier League",
    subtitle: "Comparación de cuotas con IA para partidos de la Premier League",
    poweredBy: "Impulsado por Nexa",
    realTimeOdds: "Cuotas en tiempo real",
  },

  search: {
    title: "",
    modeLabel: "Modo de búsqueda:",
    naturalMode: "Lenguaje Natural",
    directMode: "Búsqueda Directa",
    placeholderNatural:
      "Ej: 'Muéstrame las cuotas para Arsenal vs Chelsea este fin de semana'",
    placeholderDirect: "Ej: 'Arsenal vs Chelsea'",
    quickSearchLabel: "Búsquedas rápidas:",
    naturalTipsTitle: "Consejos de Lenguaje Natural:",
    naturalTip1: '¿Cuáles son las cuotas para Arsenal vs Chelsea?',
    naturalTip2: 'Muéstrame las cuotas del próximo partido de Manchester United',
    naturalTip3: 'Dame las mejores cuotas para Liverpool',
    naturalTip4: 'Quiero ver el análisis del partido entre Real Madrid y Barcelona',
    naturalTip5: '¿Qué oportunidades de valor hay para Manchester City?',
    naturalTip6: 'Analiza el rendimiento reciente del Tottenham',
    naturalTip7: 'Muéstrame las mejores apuestas para el Chelsea este fin de semana',
    naturalTip8: '¿Cuál es la mejor cuota para que gane el Arsenal?',
    directTipsTitle: "Consejos de Búsqueda Directa:",
    directTip1: 'Usa el formato: "Equipo A vs Equipo B"',
    directTip2: 'Ejemplos: "Arsenal vs Chelsea", "Man City vs Liverpool"',
    directTip3: 'Puedes buscar clásicos: "Real Madrid vs Barcelona"',
    directTip4: 'Funciona con nombres abreviados: "Man United vs Tottenham"',
    directTip5: 'Intenta: "Liverpool vs Newcastle", "Chelsea vs Brighton"',
  },

  loading: {
    fetchingOdds: "Obteniendo últimas cuotas...",
  },

  error: {
    title: "Error",
  },

  oddsDisplay: {
    title: "Resultados de Cuotas",
    foundMatches: "Encontrados",
    match: "partido",
    matches: "partidos",
    sortByDate: "Ordenar por Fecha",
    sortByHome: "Ordenar por Equipo Local",
    sortByAway: "Ordenar por Equipo Visitante",
    noMatchesFound: "No se encontraron partidos",
    tryDifferentSearch:
      "Intenta buscar un partido diferente o verifica tus términos de búsqueda.",
  },

  matchCard: {
    bookmakers: "casas de apuestas",
    clickForDetails: "Clic para detalles",
    regions: "Regiones:",
  },

  oddsComparison: {
    title: "Comparación Detallada de Cuotas",
    best: "Mejor",
    implied: "implícita",
    bookmaker: "Casa de Apuestas",
    region: "Región",
    odds: "Cuotas",
    impliedPercent: "% Implícito",
    rank: "Rank",
    summaryTitle: "Estadísticas Resumidas",
    totalBookmakers: "Total de Casas de Apuestas",
    regionsCovered: "Regiones Cubiertas",
    outcomesAvailable: "Resultados Disponibles",
  },

  quickSearchOptions: [
    "Arsenal vs Chelsea",
    "Manchester United vs Liverpool",
    "Manchester City vs Tottenham",
    "Newcastle vs Brighton",
  ],

  errors: {
    invalidRequest:
      "Parámetros de solicitud inválidos. Por favor, verifica tu búsqueda.",
    rateLimit:
      "Se excedió el límite de la API. Por favor, intenta de nuevo más tarde.",
    authFailed:
      "Falló la autenticación de la API. Por favor, verifica la configuración.",
    fetchFailed: "Error al obtener cuotas. Por favor, intenta de nuevo.",
    teamsFetchFailed: "Error al obtener la lista de equipos.",
    matchesFetchFailed: "Error al obtener los próximos partidos.",
    queryNotUnderstood:
      "No se pudo entender tu consulta. Intenta ser más específico sobre el partido.",
    agentUnavailable:
      "El agente IA está temporalmente no disponible. Intenta usar la búsqueda directa.",
    noMatchFound:
      "No se pudo encontrar un partido que coincida con tu consulta.",
    noOddsData:
      "No se encontraron datos de cuotas para este partido. Puede que no esté programado o disponible aún.",
    contextError:
      "Los componentes compuestos de SearchForm deben usarse dentro de SearchForm",
  },
};
