## INSTALL_DEPENDENCIES ##

pip install -r requirements.txt


## START_SERVER ##

Montar la base de datos para produccion:

Uso: chroma run # OPTIONS #

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
