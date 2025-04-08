# Proceso de Desarrollo del Chatbot

Este documento detalla el proceso de desarrollo colaborativo para la creación del chatbot con capacidad de búsqueda en Internet y respuestas en streaming.

## Iteración de Desarrollo

### 1. Planificación Inicial

Comenzamos analizando los requerimientos del challenge:
- Chatbot de consola
- Memoria de conversación
- Búsqueda en Internet (Serper.dev)
- Respuestas en streaming
- Citación de fuentes

Decidimos usar el modelo de Groq en lugar de OpenAI debido a los requerimientos específicos.

### 2. Estructura del Proyecto

Establecimos la estructura base del proyecto:
```
chatbot_app/
├── src/
│   └── main.py
├── tests/
│   └── test_chatbot.py
├── requirements.txt
├── README.md
└── .env
```

### 3. Desarrollo del Código Principal

#### Implementación Inicial
- Creamos el archivo `main.py` con la lógica base del chatbot
- Implementamos la clase Chatbot con sus métodos principales
- Configuramos el cliente Groq para interactuar con el LLM

#### Ajustes y Correcciones
Durante el desarrollo, nos encontramos con varios desafíos:

1. **Compatibilidad de Groq**:
   - Encontramos problemas con la biblioteca del cliente Groq
   - Cambiamos a una implementación directa usando requests
   - Actualizamos la URL de la API a `/openai/v1/chat/completions`

2. **Streaming de Respuestas**:
   - Mejoramos la función `stream_response` para manejar el formato SSE
   - Implementamos una visualización clara del progreso

3. **Modelo de LLM**:
   - Actualizamos al modelo `llama-3.3-70b-versatile` de Groq
   - Configuramos las variables de entorno para facilitar cambios

### 4. Pruebas Unitarias

Desarrollamos pruebas unitarias que verifican:
- Inicialización correcta del chatbot
- Funcionalidad de búsqueda en Internet
- Extracción de texto de URLs
- Mantenimiento del historial de conversación

Todas las pruebas pasaron exitosamente.

### 5. Corrección de Errores

Identificamos y corregimos varios errores:
1. **Problemas con la API de Groq**:
   - Corregimos la URL base
   - Actualizamos el modelo a uno compatible
   - Mejoramos el manejo de errores

2. **Problemas con el Streaming**:
   - Solucionamos un error con el argumento `flush`
   - Mejoramos la visualización de respuestas

3. **Documentación**:
   - Creamos documentación completa en README.md
   - Documentamos la estructura y uso del proyecto

### 6. Configuración para Despliegue

Finalizamos el proyecto con:
- Archivo `.gitignore` completo
- Documentación detallada
- Instrucciones de instalación y uso
- Pruebas automatizadas

## Aprendizajes Clave

1. **Integración de APIs**:
   Aprendimos a integrar múltiples APIs (Groq y Serper.dev) para crear una experiencia coherente.

2. **Streaming de Respuestas**:
   Implementamos un sistema de streaming que muestra las respuestas en tiempo real.

3. **Extracción de Contenido Web**:
   Desarrollamos técnicas para extraer y limpiar contenido de páginas web.

4. **Manejo de Errores Robusto**:
   Creamos un sistema que maneja graciosamente los errores de API y conectividad.

## Resultado Final

El resultado es un chatbot de consola que:
- Busca información actualizada en Internet
- Genera respuestas basadas en fuentes verificables
- Muestra contenido en tiempo real
- Cita apropiadamente las fuentes utilizadas
- Mantiene una conversación contextual

Este proyecto demuestra cómo se pueden combinar diferentes tecnologías (búsqueda web, LLMs, procesamiento de texto) para crear una herramienta útil y funcional. 