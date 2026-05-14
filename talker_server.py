from flask import Flask, request, send_file, jsonify, send_from_directory
import talker
from langchain_ollama import ChatOllama
import json
import mysql.connector

# talk = Talker()

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return send_from_directory("static","index.html")


@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = data.get("user", "")

    if not question:
        return jsonify({"error": "Nessuna domanda ricevuta"}),500

    try:
        # 1. genera SQL
        sql = genera_sql(question)

        # 2. esegui Nessuna domanda ricevuta
        risultati = esegui_query(sql)

        # 3. genera risposta naturale
        risposta = genera_risposta(question, risultati)

        # 4. risposta finale
        return jsonify({
            "ai": risposta,
            "sql": sql,                # opzionale (debug)
            "risultati_raw": risultati # opzionale (debug)
        }),200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500



# =========================
# DATABASE
# =========================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="RicetteDB"
    )


# =========================
# MODELLO LLM
# =========================
llm = ChatOllama(
    model="gemma4:e4b",
    temperature=0,
    reasoning=False
)


# =========================
# SCHEMA DATABASE
# =========================
SCHEMA = """
DATABASE: RicetteDB

TABELLE:

Categoria(
    ID INT PRIMARY KEY,
    NOME VARCHAR
)

Ricetta(
    ID INT PRIMARY KEY,
    NOME VARCHAR,
    DESCRIZIONE TEXT,
    TEMPO INT,
    DIFFICOLTA VARCHAR,
    CATEGORIA INT
)

Ingredienti(
    ID INT PRIMARY KEY,
    NOME VARCHAR
)

RicetteIngredienti(
    RICETTA INT,
    INGREDIENTE INT,
    QTA DECIMAL,
    U_MISURA VARCHAR
)

Preparazione(
    ID INT PRIMARY KEY,
    DESCRIZIONE TEXT,
    PROGRESSIVO INT,
    RICETTA INT
)

REGOLE:
- Usa sempre JOIN espliciti
- Usa alias (r, c, i, ri, p)
- NON usare SELECT *
- NON SERVE SCRIVERE UN MESSAGGIO DI RISPOSTA,SCRIVI DIRETTAMENTE IL QUERY SQL
"""


# =========================
# GENERAZIONE SQL
# =========================
def genera_sql(question: str) -> str:
    prompt = f"""
Sei un assistente SQL.
Converti la domanda dell'utente in SQL.

Regole:
1. Restituisci solo SQL
2. Solo SELECT
3. Non usare INSERT, UPDATE, DELETE, DROP

Schema database:
{SCHEMA}
"""

    messages = [
        ("system", prompt),
        ("human", question)
    ]

    response = llm.invoke(messages)

    sql = response.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()

    if not sql.lower().startswith("select"):
        raise Exception("Query non valida: " + sql)

    return sql


# =========================
# ESECUZIONE QUERY
# =========================
def esegui_query(sql: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(sql)
    risultati = cursor.fetchall()

    cursor.close()
    conn.close()

    return risultati


# =========================
# GENERAZIONE RISPOSTA TESTUALE
# =========================
def genera_risposta(question: str, risultati: list) -> str:
    risultati_str = json.dumps(risultati, indent=2, ensure_ascii=False)

    prompt = f"""
Sei un assistente che risponde in linguaggio naturale, umano, no sql, no codice.

Domanda utente:
{question}

Risultati della query:
{risultati_str}

Regole:
- Rispondi ESCLUSIVAMENTE IN italiano
- Non mostrare SQL
- Spiega i risultati in modo chiaro
- Se non ci sono risultati, dillo esplicitamente
- Se ci sono più elementi, elencali in modo naturale
-NON RISPONDERE IN INGLESE.
-MOSTRA SOLO TESTO NATURALE NON CODICE SQL,QUERY ECC.
"""

    messages = [
        ("system", prompt),
        ("human", "Genera la risposta")
    ]

    response = llm.invoke(messages)
    return response.content.strip()



if __name__ == '__main__':
    app.run(port=8080)