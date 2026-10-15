import logging
import sqlite3
import time

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

API_URL = "https://api.obis.org/v3/occurrence"
ESPECIES = [
    "Delphinus delphis",       # delfín común
    "Caretta caretta",         # tortuga boba
    "Balaenoptera physalus",   # rorcual común
    "Tursiops truncatus",      # delfín mular
    "Physeter macrocephalus",  # cachalote
    "Chelonia mydas",          # tortuga verde
]


def fetch_sightings(especie, reintentos=3):
    params = {"scientificname": especie, "size": 200, "startdate": "2020-01-01"}
    for intento in range(1, reintentos + 1):
        try:
            r = requests.get(API_URL, params=params, timeout=30)
            r.raise_for_status()
            return r.json().get("results", [])
        except requests.RequestException as e:
            logging.warning("Fallo %s (intento %d/%d): %s", especie, intento, reintentos, e)
            time.sleep(2 ** intento)  # espera creciente
    logging.error("No se pudo obtener %s", especie)
    return []


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS avistamientos (
            id TEXT PRIMARY KEY,
            especie TEXT,
            fecha TEXT,
            lat REAL,
            lon REAL
        )
    """)


def save(conn, especie, resultados):
    nuevos = 0
    for r in resultados:
        if "id" not in r or r.get("decimalLatitude") is None:
            continue  # validación básica: descartar datos incompletos
        cur = conn.execute(
            "INSERT OR IGNORE INTO avistamientos VALUES (?,?,?,?,?)",
            (r["id"], especie, r.get("eventDate"), r["decimalLatitude"], r["decimalLongitude"]),
        )
        nuevos += cur.rowcount
    conn.commit()
    return nuevos


if __name__ == "__main__":
    conn = sqlite3.connect("fauna_marina.db")
    init_db(conn)
    for e in ESPECIES:
        datos = fetch_sightings(e)
        logging.info("%s: %d recibidos, %d nuevos", e, len(datos), save(conn, e, datos))