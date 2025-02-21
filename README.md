# Buscador Inteligente Basado en Embeddings Vectoriales

## Introducción

El objetivo de este proyecto es desarrollar un buscador inteligente que optimice la experiencia del usuario al buscar información pública dentro de las páginas de la AFIP. La iniciativa surge de la necesidad de mejorar la accesibilidad y precisión de las búsquedas en documentos extensos y complejos, utilizando técnicas avanzadas de búsqueda semántica basadas en la vectorización de textos.

## Beneficios de las Búsquedas Semánticas

Las búsquedas semánticas, apoyadas en técnicas de vectorización, ofrecen una mejora significativa respecto a las búsquedas tradicionales por palabras clave. Entre los beneficios destacan:
- **Mayor Precisión:** Al comprender el contexto y el significado de las consultas, se obtienen resultados más relevantes.
- **Eficiencia:** Reducción del tiempo de búsqueda y procesamiento de información.
- **Experiencia de Usuario:** Mejora la interacción del usuario con el sistema, proporcionando respuestas más intuitivas y alineadas con las intenciones de búsqueda.

## Flujo de Trabajo de la Aplicación

![Imagen del flujo de trabajo de la aplicacion](https://github.com/neekoh15/chromadb_app/blob/main/CHROMADB_APP/diagrama.png)

### 1. Base de Datos Vectorial (ChromaDB)
   - **Descripción:** ChromaDB es utilizada como la base de datos vectorial donde se almacenan las representaciones vectoriales de los documentos de consultas frecuentes de AFIP.
   - **Funcionamiento:** Los documentos son preprocesados y convertidos a vectores mediante técnicas de embeddings. Estos vectores son luego almacenados en ChromaDB, permitiendo búsquedas eficientes y precisas.

### 2. Servidor Local de ChromaDB
   - **Configuración:** ChromaDB se despliega como un servidor local, que gestiona las peticiones de búsqueda y recuperación de datos.
   - **Ventajas:** Al operar localmente, se mejora la velocidad de respuesta y se asegura la integridad y seguridad de los datos manejados.

### 3. Aplicación Frontend con Flask
   - **Interfaz de Usuario:** Flask se utiliza para crear una interfaz web donde los usuarios pueden ingresar sus consultas de búsqueda.
   - **Conexión al Servidor:** La aplicación Flask actúa como cliente HTTP, enviando las peticiones al servidor local de ChromaDB.
   - **Proceso de Búsqueda:**
     1. **Ingreso de Consulta:** El usuario ingresa una consulta en la interfaz web.
     2. **Vectorización de la Consulta:** La consulta es convertida a su representación vectorial.
     3. **Petición a ChromaDB:** El vector resultante se envía al servidor de ChromaDB.
     4. **Recuperación de Resultados:** ChromaDB realiza la búsqueda en la base de datos vectorial y retorna los documentos más relevantes.
     5. **Presentación de Resultados:** Los documentos relevantes son presentados al usuario en la interfaz web.


# CONFIGURACIÓN DEL PROYECTO

## INSTALL_DEPENDENCIES ##

pip install -r requirements.txt


## START_SERVER ##

Montar la base de datos para produccion:

Uso: chroma run [<b>OPTIONS</b>]

  Monta un servidor de chroma

  Opciones:
  
    --path TEXT      El path a la base de datos.  [default: ./chroma_data]
    
    --host TEXT      El host desde donde se escuchara. Default: localhost  [default: localhost]
    
    --log-path TEXT  El path a la carpeta de logs.  [default: chroma.log]
    
    --port INTEGER   El puerto donde correra el servidor.  [default: 8000]


  Para montar correctamente el servidor local de chroma para este proyecto ejecutar:
  
    chroma run --path './database' --host '127.0.0.1' --port 8000 --log-path './logs/chroma.log'

  '--log-path' solo es soportado en la ultima version de chromadb, asegurarse de tenerla instalada:
  
    pip install --upgrade chromadb


# FUTURAS IMPLEMENTACIONES DE MEJORAS DEL SISTEMA

## Sistema de aprendizaje continuo

![Imagen del marco de aprendizaje del sistema](https://github.com/neekoh15/chromadb_app/blob/main/CHROMADB_APP/aprendizaje.png)


## Sistema RAG (Retrieval-Augmented Generation)

![Sistema RAG](https://github.com/neekoh15/chromadb_app/blob/main/CHROMADB_APP/rag.png)

La finalidad última del proyecto es generar un sistema RAG. Un sistema RAG combina la recuperación de información (retrieval) con la generación de texto (generation). Este sistema no solo busca documentos relevantes, sino que también puede generar respuestas coherentes y contextualmente precisas basadas en la información recuperada. 

### Impacto en la Experiencia de Usuario

- **Mejora de Precisión:** Al combinar la recuperación de documentos con la generación de texto, el sistema proporciona respuestas más precisas y detalladas.
- **Interacción Natural:** Los usuarios interactúan con el sistema de manera más natural, recibiendo respuestas completas y contextualmente relevantes, similar a una conversación humana.
- **Eficiencia en la Búsqueda:** El sistema reduce el esfuerzo del usuario al proporcionar directamente la información relevante sin necesidad de buscar en múltiples documentos.
