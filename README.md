# SGSSI 23-24

El script ***main.py*** requiere como argumentos la ruta de la carpeta que contiene los bloques candidatos y la ruta del archivo con el que se comparará la primera parte del bloque. La ejecución del código necesita un entorno de ejecución con Python 3.9 o una versión superior.

El comando para ejecutar el script es el siguiente:

```bash
python main.py <FOLDER> <FILE>
```

## Documentación

La función principal del script es **select_best_solution**, que se encarga de encontrar la mejor solución para el bloque. La función **get_candidates_path** es la encargada de buscar los bloques candidatos dentro de la carpeta pasada como parámetro. Para que un candidato sea encontrado, debe tener una estructura de la siguiente manera: "*.[0-9a-f]{2}.txt*". Los dos caracteres entre los puntos deben corresponder al identificador único del minero.

Las funciones **check_file_structure** y **check_prefix_sha256** son las encargadas de validar que los candidatos cumplan todas las restricciones. En concreto, la función **check_prefix_sha256** también retorna la cantidad de ceros que posee el sha256.

La última función, **resolve_collision**, como su nombre indica, es la encargada de resolver colisiones en caso de que dos bloques candidatos tengan la misma cantidad de ceros en sus sha256 correspondientes. Esta función le da prioridad a la solución que ha llegado primero al sistema. Para este caso, sería el archivo que tenga la fecha de modificación más antigua.
