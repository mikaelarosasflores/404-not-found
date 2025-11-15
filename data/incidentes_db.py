import sqlite3

con = sqlite3.connect("mensajes.db", check_same_thread=False)
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS PERSONAS (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  chat_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  nombre TEXT,
  edad INTEGER,
  leve_count INTEGER NOT NULL DEFAULT 0,
  moderado_count INTEGER NOT NULL DEFAULT 0,
  grave_count INTEGER NOT NULL DEFAULT 0,
  creado_en TEXT NOT NULL DEFAULT (DATETIME('now')),
  actualizado_en TEXT NOT NULL DEFAULT (DATETIME('now')),
  UNIQUE(chat_id, user_id)
)""")

cur.execute("""
CREATE TABLE IF NOT EXISTS INCIDENTES (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  persona_id INTEGER NOT NULL,
  mensaje_id INTEGER NOT NULL,
  texto TEXT,
  tipo_entrada TEXT NOT NULL,
  nivel TEXT NOT NULL,
  fecha_hora TEXT NOT NULL DEFAULT (DATETIME('now')),
  UNIQUE(persona_id, mensaje_id),
  FOREIGN KEY(persona_id) REFERENCES PERSONAS(id) ON DELETE CASCADE
)""")
con.commit()

def upsert_persona(chat_id: int, user_id: int, nombre: str | None = None, edad: int | None = None) -> int:
    row = cur.execute(
        "SELECT id, nombre, edad FROM PERSONAS WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    ).fetchone()
    if not row:
        cur.execute(
            "INSERT INTO PERSONAS (chat_id, user_id, nombre, edad) VALUES (?, ?, ?, ?)",
            (chat_id, user_id, nombre, edad)
        )
        con.commit()
        return int(cur.execute("SELECT last_insert_rowid()").fetchone()[0])
    pid, n0, e0 = row
    sets, args = [], []
    if nombre and nombre != n0:
        sets.append("nombre=?"); args.append(nombre)
    if isinstance(edad, int) and edad != e0:
        sets.append("edad=?"); args.append(edad)
    if sets:
        sets.append("actualizado_en=DATETIME('now')")
        cur.execute(f"UPDATE PERSONAS SET {', '.join(sets)} WHERE id=?", (*args, pid))
        con.commit()
    return int(pid)

def registrar_incidente(persona_id: int, mensaje_id: int, texto: str, tipo_entrada: str, nivel: str) -> None:
    try:
        cur.execute(
            "INSERT INTO INCIDENTES (persona_id, mensaje_id, texto, tipo_entrada, nivel) VALUES (?, ?, ?, ?, ?)",
            (persona_id, mensaje_id, texto, tipo_entrada, nivel)
        )
        con.commit()
    except sqlite3.IntegrityError:
        pass

def incrementar_conteo(persona_id: int, nivel: str) -> None:
    if nivel == "leve":
        cur.execute("UPDATE PERSONAS SET leve_count=leve_count+1, actualizado_en=DATETIME('now') WHERE id=?", (persona_id,))
    elif nivel == "moderado":
        cur.execute("UPDATE PERSONAS SET moderado_count=moderado_count+1, actualizado_en=DATETIME('now') WHERE id=?", (persona_id,))
    elif nivel == "grave":
        cur.execute("UPDATE PERSONAS SET grave_count=grave_count+1, actualizado_en=DATETIME('now') WHERE id=?", (persona_id,))
    con.commit()

def obtener_conteos(persona_id: int) -> tuple[int, int, int]:
    row = cur.execute(
        "SELECT leve_count, moderado_count, grave_count FROM PERSONAS WHERE id=?",
        (persona_id,)
    ).fetchone()
    if not row:
        return (0, 0, 0)
    return int(row[0]), int(row[1]), int(row[2])