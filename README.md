# Proyecto Final - Sistemas Distribuidos

Se desarollaron dos APIs. 
Una API Rest construida con Python y Flask para gestionar un catálogo de perros disponibles para adopción. Utiliza MongoDB para almacer la información de los perros y un sistemas de cache en Redis para optimizar consultas frecuentes.
Una API Soap construida con Python para gestionar usuarios que pudieran esta intereasdos en adoptar. Utilza Postgres para almacenar la información de los usuarios.

El proyecto implementa contenedores en Docker para la ejecución de ambas APIs, independientes para cada una, la base de datos de Mongo y Postgres, y la cache de Redis. Además, hace uso de volumenes de datps para la persistencia de datos y una red para que los contenedores se comuniquen entre si.
Además, implementa un cluster de Kubernetes utilizando Minikube, dentro del cluster se realizaron las configuraciones necesarias para....

## Características
- SOAP: Operaciones POST y GET para crear unu nuevo usuario y obtener el usuario por su ID.
- REST: Operaciones CRUD (Create, Read, Update, Delete) para crear, leer, actualizar, y borrar datos de perros.
- REST: Filtrar, buscar y ordenar perros por diversos atributos.
- REST: Integración con MongoDb para almacenamiento de Datos.
- REST: Sistema de cache con Redis para la optimización de consultas frecuentes.
- REST: Implementacion de SWAGGER UI para el testeo de los endpoints.
- REST: Acceso a los servicios del API SOAP por medio de Swagger, utiliazando ZEEP como cliente SOAP para llamar directamente los servicios.
- Implementación de contenedores para la ejecución de los componenetes del proyecto.
- Volúmenes en Docker para persistencia de Datos.


## Requisitos previos
- Python 3.x
- Pip (instalador de paquetes de python)
- Docker
- Minikube (para Kubernetes)


## Estructura del proyecto

```bash
.
RestApi/
  controllers
    dog_controller.py
    user_controller.py
  errors
    error_handlers.py
  infrastructure
    mongo.py
    swagger.py
  models
    dog_model.py
  services
    dog_service.py
    user_service.py
    soap_service.py
  static
    swagger.json
  app.py
  config.py
  Dockerfile
  requirements.txt
  README.md
SoapApi/
  controllers
    controller.py
  infrastructure
    postgres.py
  services.py
    services.py
  app.py
  Dockerfile
  requirements.txt
docker-compose.yml
```

## Instalación y ejecución

## Contenedores Docker

Si deseas desplegar el proyecto unicamente en contenedores Docker, sin la utilización de Kubernetes con el cluster en Minikube, sigue las siguientes instrucciones.

### 1. Clona el repositorio en la carpeta deseada

```bash
git clone https://github.com/EmmanuelMoscoso/ProyectoFinal_SD.git

cd

```
### 2. Crea y activa un entorno virtual en tu IDE

**Windows**

```bash

python -m venv venv

source venv/Scripts/activate

```

**Mac y Linux**

```bash
python -m venv venv

source venv/bin/activate
````

### 3. Ejecuta el archivo docker-compose.yml

```bash
docker-compose up --build -d
````

### 4. Ingresa a Swagger para probar los Endpoints

La API estará disponible en http://localhost:5000/swagger

** SI deseas acceder al WSDL del API SOAP, estará disponible en http://localhost:8000/?wsdl


## Cluster de Kubernetes

Para desplegar el proyecto en un cluster con Kubernetes, sigue las siguientes instrucciones:

Paso 1: Crear el Clúster de Kubernetes.
# Iniciar un clúster de Minikube

```bash
minikube start
```

# Crear Namespaces

```bash
kubectl create ns ema-api
kubectl create ns dfpb-databases
```

# Habilitar el Registry

```bash
minikube addons enable registry
```

Paso 3: Aplicar los archivos YAML
# Aplicar los archivos de configuración para la RestApi

```bash
cd RestApi

kubectl apply -f deployment.yaml --namespace ema-api
kubectl apply -f service.yaml --namespace ema-api
kubectl apply -f secrets.yaml --namespace ema-api

kubectl apply -f dogs-data.yaml --namespace dfpb-databases
kubectl apply -f redis.yaml --namespace dfpb-databases
kubectl apply -f mongodb.yaml --namespace dfpb-databases
```

# Aplicar los archivos de configuración para la SoapApi

```bash
cd SoapApi

kubectl apply -f deployment.yaml --namespace ema-api
kubectl apply -f service.yaml --namespace ema-api
kubectl apply -f secrets.yaml --namespace ema-api

kubectl apply -f db-deployment.yaml --namespace dfpb-databases
kubectl apply -f db-service.yaml --namespace dfpb-databases
kubectl apply -f postgres-data.yaml --namespace dfpb-databases
```


## USO

Para probar el API REST, basta con ingresar a la ruta del API y probar los endpoints:

- GET /dogs = Obtener todos los perros
![Alt text](screenshots/REST_get-dogs)
- GET /dogs/{id} = Obtener perro por ID
- GET /dogs/search = Obtener perros por filtros
- POST /dogs = Crear un nuevo perro
- PUT /dogs/{id} = Actualizar información completa de un perro
- PATCH  /dogs/{id} = Actualizar campos específicos por ID
- PATCH /dogs/{id}/adopted = Cambiar estado de un perro a adoptado
- DELETE /dogs/{id} = Borrar un perro por ID
- POST /users = (SOAP) Crear un nuevo usuario con el servicio del API SOAP
- GET /users/{id} = Obtener un usuario por su ID con el servicio del API SOAP

Para probar de manera individual el API SOAP, sin utilizar el API REST, se necesitaran herramientas como CURL o POSTMAN.

En Postman, genera una nueva consulta POST.
En la URL introduce la siguiente ruta: http//localhost:8000/

Para probar el metodo de CREACION de un usuario, en la sección de Body, selecciona RAW y tipo XML.
Ingresa el siguiente texto:

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="soap.api">
<soapenv:Header/>
<soapenv:Body>
    <soap:create_user>
        <soap:name>Max</soap:name>
        <soap:age>32</soap:age>
        <soap:email>max@gmail.com</soap:email>
        <soap:phone>4420123456</soap:phone>
    </soap:create_user>
</soapenv:Body>
</soapenv:Envelope>

Para probar el metodo de OBTENR POR ID un usuario, en la sección de Body, selecciona RAW y tipo XML.
Ingresa el siguiente texto:

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="soap.api">
<soapenv:Header/>
<soapenv:Body>
    <soap:get_user_by_id>
        <soap:user_id>1</soap:user_id>
    </soap:get_user_by_id>
</soapenv:Body>
</soapenv:Envelope>


