"""
Crea una nueva coleccion con los datos del ABC. Para realizar queries a la base de datos ejectuar minimo_caso_de_uso.py
"""

import chromadb
from local_datasets import ABC, CRM

cliente = chromadb.PersistentClient('playground_database')

nombre_coleccion_abc = 'mi_coleccion_abc'
nombre_coleccion_crm = 'mi_coleccion_crm'

print('Creando una coleccion con los datos del abc...')
coleccion_abc = cliente.create_collection(nombre_coleccion_abc)

print('Creando una coleccion con los datos del crm...')
coleccion_crm = cliente.create_collection(nombre_coleccion_crm)


abc, crm = ABC(), CRM()
abc_data, crm_data = abc.get_data(), crm.get_data()

#para limitar la carga de datos a la base
limit = 100

print('\nAsignando valores a la coleccion del abc..')
for count, (document, metadata, id) in enumerate(zip(abc_data['documents'], abc_data['metadatas'], abc_data['ids'])):
    count += 1

    coleccion_abc.add(
        documents= document,
        metadatas= metadata,
        ids = id
    )
    if count%100 == 0:
        print(f'Se han agregados {count} valores a la coleccion')

    if limit and count == limit:
        print('Limite de carga de datos alcanzado. Finalizando ..')
        break

else:
    print('Datos del abc agregados correctamente a la coleccion')


print('\nAsignando valores a la coleccion del crm...')
for count, (document, metadata, id) in enumerate(zip(crm_data['documents'], crm_data['metadatas'], crm_data['ids'])):

    count += 1
    coleccion_abc.add(
        documents= document,
        metadatas= metadata,
        ids = id
    )

    if count%100 == 0:
        print(f'Se han agregados {count} valores a la coleccion')

    if limit and count == limit:
        print('Limite de carga de datos alcanzado. Finalizando ..')
        break

else:
    print('Datos del crm agregados correctamente a la coleccion')
