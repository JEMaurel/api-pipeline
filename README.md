Subject: README.md (contenido completo para copiar)



\# Data Pipeline: Extracción, Transformación y Particionado en Parquet



Este proyecto implementa un pipeline ETL en Python que:



1\. Consume datos desde una API externa.

2\. Aplica transformaciones y enriquecimiento (columnas de año y mes).

3\. Persiste el resultado en formato Parquet con particionamiento.

4\. Maneja errores, reintentos y logging.



\## Arquitectura del pipeline



API → Extract → Transform → Load (Parquet partitioned)



\## Módulos principales



\* main.py — Orquestación del pipeline

\* fetch\_data\_with\_retry() — Extracción + retry/backoff

\* transform.py — Transformación de datos

\* save\_data.py — Persistencia en parquet

\* config.py — Configuración/credenciales

\* output/ — Resultados generados



\## Requerimientos



Python >= 3.10



Dependencias principales:



```

pandas

pyarrow

requests

logging

```



\## Instalación



```

git clone https://github.com/tu\_usuario/tu\_repo.git

cd tu\_repo

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

```



\## Configuración



Editar config.py con:



```

API\_BASE\_URL=

API\_TOKEN=

API\_EMAIL=

```



\## Ejecución



```

python main.py

```



\## Output generado



El pipeline crea:



```

output/orders/                 parquet particionado (order\_year, order\_month)

output/orders\_all.parquet      dataset completo

```



Ejemplo de particiones:



```

orders/order\_year=2023/order\_month=04/...

```



\## Logs



Ejemplo típico:



```

INFO Fetching 1000 rows...

INFO Transformación exitosa

INFO Guardando parquet particionado...

INFO Pipeline completado

```



\## Manejo de Errores



Incluye:



\* reintentos automáticos

\* exponential backoff

\* distinción entre errores servidor/cliente

\* timeout controlado

\* logging claro en main



