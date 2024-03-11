"""
Modulo para conexion remota a base de datos chroma.
"""

import chromadb
from chromadb.config import Settings
import pandas as pd
from typing import Sequence, Optional


class Client:
    """
    Establece una interfaz para conectarse al servidor de base de datos de chroma
    """
    
    def __init__(self, host:str='localhost', port:int=8000, **kwargs) -> None:
        
        self.database = kwargs.get('database')
        self.database_info = None 
              
        self._port = port
        self._host = host
        
        self.connection_settings = {
            'port': port,
            'host': host
        }
        
        self.client = None
        self.cursor = None
        
        try:
            self.connect()
        except Exception as e:
            print(e)
        
    def connect(self) -> None:
        self.__settings = Settings(anonymized_telemetry=False)
        
        if self.database:
            self.client = chromadb.HttpClient(host=self._host, port=self._port, settings=self.__settings, database=self.database)
        else:
            self.client = chromadb.HttpClient(host=self._host, port=self._port, settings=self.__settings)

        
    def get_database_collections(self) -> Sequence[chromadb.Collection]:
        """
        Devuelve informacion de las colecciones que contiene la base de datos
        
        Ejemplo de uso:
        
        ```python
        client.get_database_collections_info()
        # [collection(name='mi_coleccion1', metadatas= {}), collection(name='mi_coleccion2', metadatas={}), ...]
        
        ```
        
        Esto es equivalente a utilizar el metodo 'list_collections()' de la clase chromadb.HttpClient():
        ```python
        client.list_collections()
        # [collection(name='mi_coleccion1', metadatas= {}), collection(name='mi_coleccion2', metadatas={}), ...]
        
        ```
        """
        return self.client.list_collections()
    
    def get_cursor_info(self, ignore_embeddings:bool=True, n_rows:int=5) -> pd.DataFrame:
        """
        Devuelve un dataframe con informacion relacionada a la coleccion a la cual apunta el cursor.
        
        Por defecto ignora la columna de embeddings para una mejor representacion visual.
        """
        if self.cursor:
            dataframe = pd.DataFrame(self.cursor.peek())
            
            if ignore_embeddings:
                dataframe = dataframe.drop('embeddings', axis=1)
                
            return dataframe.head(n=n_rows)
        
    def set_cursor(self, collection_name:str) -> None:
        """
        Establece un cursor a una collecion dentro de la base de datos.
        
        Este cursor se utiliza para realizar llamados de ```GET, POST, UPDATE, DELETE``` a la coleccion seleccionada
        """
        for collection in self.get_database_collections():

            if collection_name in getattr(collection, 'name'):
                self.cursor = self.client.get_collection(collection_name)
                break
            
        else:
            print('No se ha encontrado al coleccion solicitada.')
        
    def execute_query(self, query_text:str, n_results:int= 5, include:list[str]=['documents', 'metadatas', 'distances']) -> chromadb.QueryResult:
        """
        Ejecuta una query a la coleccion establecida en el cursor.
        Necesita de un cursor.
        Si no existe un cursor, este metodo retornara None
        
        Devuelve:
        ```python
            {'documents': list[str],
            'metadatas': list[dict],
            'ids': list[str]
            }
        ```
        """
        if self.cursor:

            return self.cursor.query(
                query_texts= query_text,
                n_results= n_results,
                include=include
            )
            
    def insert_data(self, data:dict) -> None:
        """
        Inserta un nuevo valor dentro de una coleccion. Necesita de un cursor.
        
        El formato de ```data``` debera ser:
        
        ```python
        data = {
            'document': document,
            'metadata': metadata,
            'id': id
        }
        
        """
        
        try:
            if self.cursor:
                document = data['document']
                metadata = data['metadata']
                id = data['id']
                
                self.cursor.add(
                    documents= document,
                    metadatas= metadata,
                    ids= id
                )
            
        except Exception as e:
            print('No se ha podido agregar el dato a la coleccion.', e)
    
    def update_data(self, data:dict):
        """
        Actualiza un valor dentro de una coleccion. Necesita de un cursor.
        
        El formato de ```data``` debera ser:
        
        ```python
        data = {
            'document': document,
            'metadata': metadata,
            'id': id
        }
        """
        
        if self.cursor:      
            document = data['document']
            metadata = data['metadata']
            id = data['id']            
            
            self.cursor.update(
                ids= id,
                documents= document,
                metadatas= metadata
            )
        
        pass
    
    def delete_data(self, data:dict):
        """
        Elimina un valor dentro de una coleccion. Necesita de un cursor.
        
        El formato de ```data``` debera ser:
        
        ```python
        data = {
            'document': document,
            'metadata': metadata,
            'id': id
        }
        """
        
        if self.cursor:
            id = data['id']
            
            self.cursor.delete(
                ids = id
                )
    
    def disconnect(self):
        """ Desconecta el cliente de la base de datos."""
        # la libreria no provee ningun metodo particular para terminar la conexion a la base de datos
        self.client = None
    

if __name__ == '__main__':

    cliente = Client(database = None)
    
    #database_info = cliente.get_database_collections_info()
    #print(database_info)
    # database_info >>> [Collection(name='coleccion_abc'), Collection(name='coleccion_crm'), ...]

    cliente.set_cursor('monotributo_collection')

    results = cliente.execute_query(
        query_text= 'Que es la recategorizacion?',
        n_results=2
    )

    print(results)
        
    
