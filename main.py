from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de base de datos (archivo SQLite en la carpeta del proyecto)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definición del modelo Card
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Card {self.titulo}>'

# Crear tablas en la base de datos si no existen
with app.app_context():
    db.create_all()
    if not Card.query.first():
        ejemplo1 = Card(titulo="Primera tarjeta", descripcion="Este es un ejemplo.")
        ejemplo2 = Card(titulo="Segunda tarjeta", descripcion="Otra tarjeta de prueba.")
        db.session.add_all([ejemplo1, ejemplo2])
        db.session.commit()

# Historial de chat en memoria
historial = []

# --- FUNCIONES DE BOT --- #
def menu_opciones():
    return ("\nOpciones disponibles:\n"
            "1. ¿Qué es el cambio climático?\n"
            "2. ¿Cómo podemos ayudar?\n"
            "3. Consecuencias principales\n")

def procesar_mensaje(texto):
    texto = texto.lower().strip()

    if texto == "hola":
        return ("👋 Hola, soy BioCAPTUS. Quiero ayudarte con información sobre el cambio climático.\n\n"
                + menu_opciones())
    
    elif texto == "1":
        return ("🌍 El cambio climático es la variación de las condiciones del clima a largo plazo.\n\n"
                "📄 Documento explicativo (ONU): <a href='https://www.un.org/es/climatechange/what-is-climate-change' target='_blank'>Ver aquí</a><br>"
                "🎥 Video corto: <a href='https://www.youtube.com/watch?v=EtW2rrLHs08' target='_blank'>Ver video</a><br>"
                "📚 Guía completa (PDF): <a href='https://unfccc.int/resource/docs/publications/cc_guide.pdf' target='_blank'>Descargar</a><br><br>"
                + menu_opciones())
    
    elif texto == "2":
        return ("✅ Podemos ayudar reduciendo el consumo de energía, reciclando y usando transporte sostenible.\n\n"
                "📄 Artículo: <a href='https://www.nationalgeographic.com/environment/article/how-to-help' target='_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/watch?v=V5w1nqG7KqY' target='_blank'>Ver video</a><br>"
                "📚 Guía práctica (PDF): <a href='https://ec.europa.eu/clima/sites/clima/files/docs/0108/guide_es.pdf' target='_blank'>Descargar</a><br><br>"
                + menu_opciones())
    
    elif texto == "3":
        return ("⚠️ Consecuencias del cambio climático: aumento de temperaturas, deshielo de glaciares y fenómenos extremos.\n\n"
                "📄 Informe IPCC: <a href='https://www.ipcc.ch/' target='_blank'>Leer informe</a><br>"
                "🎥 Video explicativo: <a href='https://www.youtube.com/watch?v=H1t2t5t0FJk' target='_blank'>Ver video</a><br>"
                "📚 Documento PDF (impactos en Latinoamérica): <a href='https://repositorio.cepal.org/bitstream/handle/11362/37312/S1420651_es.pdf' target='_blank'>Descargar</a><br><br>"
                + menu_opciones())
    
    else:
        return "Por favor escribe 'hola' para comenzar o elige una opción válida (1, 2 o 3)."

# --- RUTAS --- #
@app.route("/")
def home():
    return render_template("index.html", historial=historial)

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form["message"]

    # Procesar con el bot
    response = procesar_mensaje(user_message)

    # Guardar conversación en el historial
    historial.append(("usuario", user_message))
    historial.append(("bot", response))

    return render_template("index.html", historial=historial)

@app.route("/cards")
def cards():
    cards = Card.query.order_by(Card.id).all()
    return render_template("card.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=True)



