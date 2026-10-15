--Pipeline de datos sobre fauna marina--

Pipeline automatizado escrito en python que guarda registros de presencia de animales marinos
a traves de la api : [OBIS](https://obis.org), los guarda en una BD de sqlite3 y genera un excel. 
Devuelve 200 registros a eleccion de la api desde 1 de enero de 2020.

--Funcionamiento--

Busca datos de las diferentes especies indicadas a traves de la api, valida que los datos tengan un identificador
y los guarda en el sqlite usando el id como referencia para evitar duplicados. Con ayuda de claude hago que la api gestione 
reintentos y una espera creciente.

en informe.py, uso pandas para procesar los datos y registralos por especie y mes.




