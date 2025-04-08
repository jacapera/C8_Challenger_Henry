# Chatbot con Búsqueda en Internet y Respuestas en Streaming

Este proyecto implementa un chatbot de consola con capacidad de búsqueda en Internet, memoria de conversación y respuestas en streaming, cumpliendo con los requerimientos especificados en el challenge.

## Características Principales

1. **Interfaz de Consola**
   - Interfaz interactiva basada en texto
   - Indicadores visuales del estado de la búsqueda y respuesta
   - Formato rico en colores para mejor legibilidad

2. **Memoria de Conversación**
   - Mantiene el historial completo durante la ejecución
   - Utiliza el contexto de las últimas 5 interacciones
   - Permite conversaciones coherentes y contextuales

3. **Búsqueda en Internet**
   - Integración con Serper.dev para búsquedas en Google
   - Procesamiento de los 5 resultados más relevantes
   - Extracción inteligente de contenido de páginas web

4. **Respuestas en Streaming**
   - Generación de respuestas en tiempo real
   - Visualización carácter por carácter
   - Indicadores de progreso durante la búsqueda

5. **Citación de Fuentes**
   - Referencias a las fuentes consultadas
   - Enlaces directos a las páginas originales
   - Títulos descriptivos de las fuentes

## Requisitos Técnicos

- Python 3.8 o superior
- Claves de API:
  - GROQ_API_KEY: Para el modelo de lenguaje (https://console.groq.com)
  - SERPER_API_KEY: Para búsquedas en Internet (https://serper.dev)
- Dependencias principales:
  - groq: Para interacción con el modelo de lenguaje
  - requests: Para peticiones HTTP
  - beautifulsoup4: Para extracción de texto
  - rich: Para interfaz de consola mejorada

## Instalación

1. Clonar el repositorio y navegar al directorio del proyecto:
```bash
cd chatbot_app
```

2. Crear y activar el entorno virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar el archivo `.env`:
```env
# Clave API de Groq - Obtener en https://console.groq.com
GROQ_API_KEY=tu_clave_de_groq_aqui

# Clave API de Serper.dev - Obtener en https://serper.dev
SERPER_API_KEY=tu_clave_de_serper_aqui

# Configuración del modelo de Groq
GROQ_MODEL=llama-3.3-70b-versatile
```

## Uso

1. Iniciar el chatbot:
```bash
python src/main.py
```

2. Hacer preguntas naturalmente. Ejemplo:
```
Tú: ¿Cuál es la capital de Francia?

[Buscando información...]
[Generando respuesta...]

La capital de Francia es París...

Fuentes consultadas:
- Wikipedia: https://es.wikipedia.org/wiki/París
- ...
```

3. Para salir, escribir 'salir'.

## Pruebas Automatizadas

El proyecto incluye pruebas unitarias que verifican:

1. **Inicialización del Chatbot**
   - Verificación de estado inicial
   - Configuración de variables de entorno

2. **Búsqueda en Internet**
   - Integración con Serper.dev
   - Procesamiento de resultados
   - Manejo de errores

3. **Extracción de Texto**
   - Procesamiento de HTML
   - Limpieza de contenido
   - Manejo de codificación

4. **Gestión de Conversación**
   - Mantenimiento del historial
   - Formato de mensajes
   - Roles de usuario y asistente

Para ejecutar las pruebas:
```bash
pytest tests/ -v
```

## Estructura del Proyecto

```
chatbot_app/
├── src/
│   └── main.py          # Lógica principal del chatbot
├── tests/
│   └── test_chatbot.py  # Pruebas unitarias
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Documentación
└── .env               # Configuración de APIs
```

## Características Técnicas Adicionales

- Uso del modelo LLM más reciente de Groq (llama-3.3-70b-versatile)
- Manejo asíncrono de respuestas en streaming
- Sistema de caché para respuestas frecuentes
- Manejo robusto de errores y excepciones
- Formateo inteligente de respuestas

## Limitaciones Conocidas

- El historial de conversación se mantiene solo durante la ejecución
- Requiere conexión a Internet activa
- Las claves API deben ser válidas y tener créditos disponibles
- El modelo puede tener tiempos de respuesta variables 