 ## Proyecto para ejecutar pruebas y empezar a conocer las funcionalidades de Chroma. ##

Dentro de la carpeta 'data' se encuentran los archivos csv con informacion del ABC Consultas Frecuentes y algunas consultas finalizadas del CRM AFIP.

Dentro de la carpeta 'src' se encuentran los archivos.py para procesar los datos deos csv que se encuentran dentro de la carpeta 'data'

Dentro 'src' encontraremos:

    local_datasets.py: es el encargado de cargar y procesar los datos provenientes de los csv del abc y de consultas finalizadas del crm.

    playground_database.py: al ejecutarse crea una base de datos persistente con colecciones que almacenan los datos provenientes de los datasets del ABC y CRM

    query_database.py: contiene los metodos para conectarse a la base de datos previamente creada y realizar queries a la coleccion que se desee.

[IMPORTANTE] Para evitar problemas de importaciones relativas, establecer como directorio raiz '\playground'

Ejemplo de ejecucion de playground_database.py:

 ```<path_to_folder>..\chromadb\playground> python .\src\playground_database.py```
