"""
Interfaz para el manejo de base de datos.

Permite la creacion, actualizacion, eliminacion y retribucion de colecciones y base de datos
"""

import chromadb
import importlib
import pandas as pd 
from typing import Sequence

from local_datasets import ABC, CRM, MONOTRIBUTO


class Database():
    """
    Interfaz de administracion de la base de datos
    """
    def __init__(self, database_path:str='./database', persistent=True) -> None:
        
        self.database_path = database_path
        self.collections = []
        self.collections_names = []
        
        self.__package = importlib.import_module('chromadb.config')
        self.__settings = getattr(self.__package, 'Settings')
        
        if persistent:
            self.client = chromadb.PersistentClient(database_path, self.__settings(anonymized_telemetry=False))
            self.collections = self.client.list_collections()
            
        else:
            self.client = chromadb.Client(database_path, self.__settings(anonymized_telemetry=False))
         
    def get_database_collections(self) -> dict[Sequence[chromadb.Collection], list[str]]:
        """
        Devuelve informacion de las colecciones que contiene la base de datos
        """
        
        return {
            'collections': self.client.list_collections(),
            'names': [collection.name for collection in self.client.list_collections()],
                }
    
    def get_collection(self, collection_name:str) -> chromadb.Collection:
        """
        Devuelve la coleccion solicitada. Si la coleccion no existe, devuelve None.
        """
        for collection in self.client.list_collections():

            if collection_name in getattr(collection, 'name'):
                return collection
        
        else:
            print('No se ha encontrado la coleccion solicitada.')
            return None

    
    def get_collection_info(self, collection_name:str, skip_embeddings=True) -> pd.DataFrame:
        """
        Devuelve y muestra en consola los primeros 10 valores de la coleccion solicitada.
        Por defecto ignora la columna de 'embeddings'.
        """

        collection = self.get_collection(collection_name)
        
        if collection:

            df = pd.DataFrame(collection.peek())
            
            if skip_embeddings:
                df = df.drop('embeddings', axis=1)
            
            print(f'Informacion de la coleccion {collection_name}: \nPrimeras {len(df)} de {collection.count()} filas\n', df, '\n')
            
            return df
                
    
    def query_collection(self, collection_name:str, query_text:str, n_results:int=5) -> chromadb.QueryResult:
        """
        Realiza una consulta a la coleccion solicitada.
            - collection_name: nombre de la coleccion que se quiere consultar
            - query_text: consulta
            - n_results: cantidad de resultados a retribuir
        """
        collection = self.get_collection(collection_name)
        
        if collection:
            response = collection.query(
                query_texts = query_text,
                n_results= n_results
            )
            return response
        
        else:
            # error handling
            return None
     
    def create_collection(self, collection_name:str) -> chromadb.Collection:
        """Metodo simple para crear una coleccion vacia. Si la coleccion ya existe, devuelve None"""

        for collection in self.client.list_collections():
            if collection_name in getattr(collection, 'name'):
                print('No es posible crear la coleccion. Coleccion ya existente dentro de la base de datos.')
                return None
        else:
            nueva_coleccion = self.client.create_collection(collection_name)
            print(f'Coleccion "{collection_name}" creada exitosamente')

            return nueva_coleccion
   
    def build_collection(self, dataset_data:dict) -> chromadb.Collection:
        """
        Crea una coleccion a partir de un diccionario de datos proveniente de un dataset.
        
        Si la coleccion ya existe, devuelve None.
        """

        progress_bar = getattr(importlib.import_module('utilities'), 'progress_bar')

        try:
            collection_name:str = dataset_data['collection_name']
            documents:list = dataset_data['documents']
            metadatas:list = dataset_data['metadatas']
            ids:list = dataset_data['ids']
            total_docs = dataset_data['count']
            count = 0
            
            collection = self.create_collection(collection_name)

            if collection:
                print(f'\nSe añadiran {total_docs} documentos a la coleccion {collection_name}')
                print('Añadiendo documentos a la coleccion... ')   
                    
                for document, metadata, id in zip(documents, metadatas, ids):
                
                    collection.add(
                        documents= document,
                        metadatas= metadata,
                        ids= id
                    )
                    progress_bar(count, total_docs)
                    count += 1

                else:
                    
                    progress_bar(count, total_docs)

                    print('Documentos añadidos a la coleccion exitosamente\n')

                    return collection
                
        except Exception as e:
            print('No se ha podido crear la coleccion. ', e)
            input(' ** ENTER TO CONTINUE **')
    
    def delete_collection(self, collection_name:str, ignore_warnings=False) -> None:
        """
        Elimina una coleccion. Por defecto solicitara una confirmacion manual para elimar la coleccion, aunque se puede deshabilitar
        modificando el parametro 'ignore_warnings'.
        """
        print('\nEstá a punto de eliminar una collecion')
        
        if not ignore_warnings:
            i = input('Desea continuar? y/n: ')
            if i == 'y':
                
                collection = self.get_collection(collection_name=collection_name)

                if collection:
                    self.client.delete_collection(collection.name)
            else:
                print('Operacion abortada.')
                
        else:
            try:
                self.client.delete_collection(collection_name)
                print('Coleccion eliminada exitosamente')
            except Exception as e:
                print('No se ha podido eliminar la coleccion. ', e)
            
    def force_mount(self, port:int=8000, host:str='localhost', log_path:str='logs/chroma.log'):
        """ De manera forzada establece un servidor chroma local de la base de datos junto con un registro de logs a la misma
        
        Por defecto el servidor se establece en ```http://localhost:8000```
        
        """
        import os        
        
        os.system(
            f'chroma run --path {self.database_path} --host {host} --port {port} --log-path {log_path}'
            )
        
    def __del__(self):
        print('Conexion a database finalizada') 
        

if __name__ == '__main__':
    
    database = Database()
    
    #abc, crm, monotributo = ABC(), CRM(), MONOTRIBUTO()
    
    #abc_data, crm_data, monotributo_data = abc.get_data(), crm.get_data(), monotributo.get_data()

    #database.delete_collection(abc_data['collection_name'], ignore_warnings=True)
    #database.delete_collection(crm_data['collection_name'], ignore_warnings=True)
    #database.delete_collection(monotributo_data['collection_name'], ignore_warnings=True)

    #database.build_collection(dataset_data=abc_data)
    #database.build_collection(dataset_data=crm_data)
    #database.build_collection(dataset_data=monotributo_data)
    
    
    #database.get_collection_info(abc.collection_name)
    #database.get_collection_info(crm.collection_name)
    
    database.force_mount()
