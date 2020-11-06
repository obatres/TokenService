# Servicio
###  Tokens Service
    Parametros:
>    - id
>    - secret
**Respuesta: [Codigo: 201]
    {
      "jwt": "[Token]"
     }
>Rutas: http://35.225.47.35:5001/
>Metodos:
  POST

## Anexos
## Documentacion de herramientas utilizadas
> *Python: https://www.python.org/
> Flask: https://pypi.org/project/Flask/
> Travis: https://travis-ci.com/
> JWT: https://jwt.io/

## Historial de versiones
* 1.0
  * *CAMBIO: Creacion de contenedores, de servidor y pruebas unitarias, contruccion del codigo interpretado en Travis. 

* 1.0.1
  * *CAMBIO:  Agregado un requerimiento en el archivo de requerimientos, para la construccion del contenedor. 
 * 1.0.2
   * *CAMBIO: Log de actividad
* 1.1
  * *CAMBIO: contruccion del contenedor por medio de jenkins
      