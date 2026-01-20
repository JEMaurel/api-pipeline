\# API Ecommerce Pipeline



Pipeline ETL que consume datos desde una API pública, los transforma y los guarda en formato parquet particionado para facilitar análisis posteriores.



---



\## Instalación



```bash

git clone https://github.com/JEMaurel/api-pipeline.git

cd api-pipeline



python -m venv venv

venv\\Scripts\\activate



pip install -r requirements.txt

```



---



\## Configuración



Editar `config.py` con los valores correspondientes:



```python

API\_BASE\_URL = ""

API\_TOKEN = ""

API\_EMAIL = ""

```



---



\## Ejecución



```bash

python main.py

```



---



\## Output generado



El pipeline crea:



```

output/orders/              parquet particionado (order\_year, order\_month)

output/orders\_all.parquet   dataset completo

```



---



\## Estructura del proyecto



```

api-pipeline/

│

├── main.py

├── transform.py

├── save\_data.py

├── config.py

├── requirements.txt

└── README.md

```



---



\## Tecnologías



\- Python 3.10+

\- Pandas

\- Parquet

\- Logging

\- Requests



---



\## Objetivo



Demostrar un flujo ETL básico:



1\. Extract (API + retry)

2\. Transform (enriquecimiento + validaciones)

3\. Load (parquet particionado)



