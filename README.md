# Para armar entorno  

## Levantar venv  

```
$ python -m venv .
```  

## Instalar dependencias  

```
$ ./bin/pip install mysql-connector-python
$ ./bin/pip install "fastapi[standard]"
```  

## Extras  

Para "activar" el venv en el shell actual
```
$ source ./bin/activate # En Mac/Linux
```  
```
C:\> .\Scripts\activate.bat :: En Windows
```  

# Para levantar el programa  

```
$ fastapi dev src/main.py
```  

