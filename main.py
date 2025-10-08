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
    return (
        "Opciones disponibles:<br>"
        "1. ¿Qué es el cambio climático?<br>"
        "2. Causas del cambio climático<br>"
        "3. Consecuencias del cambio climático<br>"
        "4. Cómo podemos prevenirlo<br>"
        "5. Qué son los gases efecto invernadero<br>"
        "6. Qué efectos tiene en los polos<br>"
        "7. Como afecta la agricultura<br>"
        "8. Que pasa con lso oceanos<br>"
        "9. Como afecta a las ciudades<br>"
        "10. Datos curiosos o interesantes"
    )

    
def procesar_mensaje(texto):
    texto = texto.lower().strip()

    if texto == "hola":
        return ("👋 Hola, soy BioCAPTUS. Quiero ayudarte con información sobre el cambio climático.\n\n"
                + menu_opciones())
    
    elif texto == "1":
        return ("🌍 El cambio climatico es la alteracion prolongada del clima terrestre debido a las actividades humanas que emites gases efecto invernadero. Estos gaese atrapan el calor y elevan la temperatira del planeta. Aunque el clima siempre ha cambiado el ritmo actual es alarmante y esta relacionado con la contaminacion y la desforestacion.\n\n"
                "📄 Documento explicativo (ONU): <a href='https://www.un.org/es/climatechange/what-is-climate-change' target='_blank'>Ver aquí</a><br>"
                "🎥 Video corto: <a href='https://youtu.be/vCBeSAOTGA8?t=17' target='_blank'>Ver video</a><br>"
        )
    
    elif texto == "2":
        return ("✅ Entre las principales causas estan la quema de combustibles fosiles, la desforestacion y las actividades industriales. Estas acciones liberan gases como el CO₂ y el metano, que instensifican el efecto inernadero. La agricultura y la ganaderia tambien contribuyen al calentamiento global, liberando gases muy potentes.\n\n"
                "📄 Artículo: <a href='https://ciencia.nasa.gov/cambio-climatico/causas/'_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/shorts/Otxc1mWGPyY?t=14&feature=share' target='_blank'>Ver video</a><br>"
        )
    
    elif texto == "3":
        return ("⚠️ Los efectos del cambio climatico incluyen el derretimiento de los glaciales, aumento del nivel del mar, incendios forestales y fenomentos extremos. Estas consecuencias afectan la vida humanan, los animales y los ecosistemas del planeta. Cada año se intensifican los desastres naturales y se pierden muchos habitas de animales.\n\n"
                "📄 Informe IPCC: <a href='https://climate.ec.europa.eu/climate-change/consequences-climate-change_es' target='_blank'>Leer informe</a><br>"
                "🎥 Video explicativo: <a href='https://www.youtube.com/shorts/OPv4I3yfHBk?t=9&feature=share' target='_blank'>Ver video</a><br>"
        )
    
    elif texto == "4":
        return ("🌱 La prevencion comienza con el uso de energias limpias, como la solar y la eolica, y los cambios de nuestros habitos. Reducir el consumo de plasticos, reciclar y cuidar el agua son acciones cotidianas que marcan la diferencia. Tambien es importante apoyar politicas que protejan el medio ambiente.\n\n"
                "📄 Artículo: <a href='https://accionverde.org.co/medio-ambiente/formas-de-cuidar-el-medio-ambiente/?gad_source=1&gad_campaignid=22925896700&gbraid=0AAAAAplAgf7ptjv_HdD0KYFPWrkR55qjH&gclid=Cj0KCQjwl5jHBhDHARIsAB0YqjzUNp0yihAJnwEYWA0uc24G6XUriLx7XbYviz3EOmVZC69TlZsxr4kaAg49EALw_wcB' target='_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/watch?v=V5w1nqG7KqY' target='_blank'>Ver video</a><br>"
        )
    
    elif texto == "5":
        return ("🌫️ Son gases naturales que ayudan a mantener la Tierra calida, pero en exceso causan calentamiento global. Entre los mas importantes estan el dioxido de carbono, el metano y el oxido nitroso. Su aunmento descontrolado crea un desequilibrio climatico.\n\n"
                "📄 Artículo: <a href='https://www.wwf.org.co/?325754/Que-son-los-Gases-de-Efecto-Invernad' target='_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/shorts/mhlf7EOFkqY?t=2&feature=share' target='_blank'>Ver video</a><br>"
        )
    
    elif texto == "6":
        return ("❄️ Los polos se derriten rapidamente,lo que eleva el nivel del mar y amenaza especies como los son los osos polares y los pinguinos. Ademas, cambia las corrientoes oceanicas, afectando el clima global. Es uno de los impactos mas visibles y preocupantes del calentamiento global\n\n"
                "📄 Artículo: <a href='https://www.csic.es/es/agenda-del-csic/el-cambio-climatico-en-los-polos-dos-especialistas-analizan-las-consecuencias-globales-del-calentamiento-de-los-polos' target='_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/shorts/Li4O8uAru3E?t=21&feature=share' target='_blank'>Ver video</a><br>"
        )
    
    elif texto == "7":
        return ("🌾 El cambio climatico esta modificando los patrones de lluvia y aumentando las sequias, lo que se complica la produccion de alimentos. Los cultivos se enfrentan a plagas nuevas, el suelo pierde nutrientes y las estaciones se vuelven menos predecibles. En algunas zonas, las cosechas se reducen drasticamente, afectando la economia y la seguridad alimentaria. Por eso, se impulsa la agricultura sostenible, con tecnicas que protegen el suelo y reducen el uso de quimicos dañinos.\n\n"
                "📄 Artículo: <a href='https://agriculture.basf.com/ec/es/contenidos-de-agricultura/cambio-climatico-y-agricultura-cual-es-el-impacto' target='_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/watch?v=Z4z2kX9b6pY' target='_blank'>Ver video</a><br>"
        )
    
    elif texto == "8":
        return ("🌊 Los océanos absorben gran parte del claor y de CO₂ generados por el cambio climatico. Esto causa su acidificacion, afectando la vida marina, especialmente los corales, moluscos y peces. Ademas, el aumento de temperatura provoca el blanqueamiento de lso arrecifes y alteera las corrientes oceánicas. Si los océanos se desequilibran, se altera toda la cadena alimenticia marina y, por tanto, la vida humana que depende de ella.\n\n"
                "📄 Artículo: <a href='https://www.nationalgeographic.com/environment/article/oceans' target='_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/watch?v=1f4k7b8k8b8' target='_blank'>Ver video</a><br>"
                )
    
    elif texto == "9":
        return ("🏙️ Las ciudades son responsables de una gran parte de emisiones de gases efecto invernadero, y tambien sufren sus consecuencias. Las olas de claor son cada vez mas intensas, el aire se vuelve mas contaminado y las lluvias torrenciales pueden causar inundaciones. Ademas, el calor ha atrapado por el concreto y los edificios crea el llamado (efecto isla de calor). Las ciudades deben adaptarse con mas zonas verdes, techos solares  y transporte limpio para ser mas sostenibles.\n\n"
                "📄 Artículo: <a href='https://climatepromise.undp.org/es/news-and-stories/las-ciudades-tienen-un-rol-clave-en-la-lucha-contra-el-cambio-climatico-he-aqui-el' target='_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/watch?v=V5w1nqG7KqY' target='_blank'>Ver video</a><br>"
        )
    
    elif texto == "10":
        return ("🌟 Datos curiosos sobre el cambio climático:\n"
                "- El 2020 fue uno de los años más cálidos registrados.\n"
                "- Los océanos absorben alrededor del 30% del CO2 emitido por actividades humanas.\n"
                "- La deforestación contribuye significativamente a las emisiones de GEI.\n\n"
                "📄 Artículo: <a href='https://www.nationalgeographic.com/environment/article/10-facts-about-climate-change' target='_blank'>Leer aquí</a><br>"
                "🎥 Video: <a href='https://www.youtube.com/watch?v=EtW2rrLHs08' target='_blank'>Ver video</a><br>"
        )
    
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



