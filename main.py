# main.py
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import qrcode
import os

app = Flask(__name__)

# Génération du QR code (mais ne pas l'afficher sur le site)
def generate_qr_code():
    url = "https://azitropy1.onrender.com"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    os.makedirs("static", exist_ok=True)
    img.save("static/qr_code.png")

generate_qr_code()

reponses_utilisateurs = {}

questions = [
    "1. Quel est l'agent causal de la tuberculose ?",
    "2. Quel antibiotique est utilisé en première ligne contre le streptocoque A ?",
    "3. Quel est le vecteur du paludisme ?",
    "4. Quelle est la complication la plus grave de la dengue ?",
    "5. Quelle est la durée d'incubation de la rougeole ?",
    "6. Quelle hépatite est principalement transmise par voie fécale-orale ?",
    "7. Quel est le traitement de première intention pour une cystite aiguë simple ?",
    "8. Quelle bactérie est responsable du tétanos ?"
]

choix = [
    ["A. Mycobacterium tuberculosis", "B. Streptococcus pneumoniae", "C. Haemophilus influenzae", "D. Escherichia coli"],
    ["A. Amoxicilline", "B. Gentamicine", "C. Ciprofloxacine", "D. Vancomycine"],
    ["A. Moustique Anopheles", "B. Tique", "C. Mouche Tse-Tse", "D. Puce"],
    ["A. Fièvre hémorragique", "B. Arthrite", "C. Encéphalite", "D. Syndrome grippal"],
    ["A. 7 jours", "B. 14 jours", "C. 10-12 jours", "D. 3-5 jours"],
    ["A. VHB", "B. VHC", "C. VHA", "D. VHE"],
    ["A. Amoxicilline", "B. Fosfomycine", "C. Nitrofurantoïne", "D. Ceftriaxone"],
    ["A. Clostridium tetani", "B. Clostridium difficile", "C. Bacillus anthracis", "D. Neisseria meningitidis"]
]

reponses_correctes = ["A", "A", "A", "A", "C", "C", "C", "A"]
explications = [
    "Mycobacterium tuberculosis est l'agent de la tuberculose.",
    "L'amoxicilline est efficace contre le streptocoque A.",
    "Le moustique Anopheles transmet le paludisme.",
    "La dengue peut évoluer en fièvre hémorragique.",
    "La rougeole a une incubation de 10-12 jours.",
    "Le VHA est transmis par voie fécale-orale.",
    "La nitrofurantoïne est le traitement standard.",
    "Clostridium tetani provoque le tétanos."
]

@app.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        nom = request.form.get('nom')
        if not nom:
            return "Veuillez entrer votre nom."
        maintenant = datetime.now()
        if nom in reponses_utilisateurs and maintenant - reponses_utilisateurs[nom]["time"] < timedelta(hours=2):
            return "Tu as déjà participé."
        answers = [request.form.get(f'q{i}') for i in range(1, 9)]
        reponses_utilisateurs[nom] = {
            "time": maintenant,
            "answers": answers
        }
        return redirect(url_for('merci'))
    return render_template('index.html', questions=questions, choix=choix)

@app.route('/merci')
def merci():
    return render_template('merci.html')

@app.route('/stats', methods=['GET', 'POST'])
def stats():
    if request.method == 'POST':
        password = request.form['password']
        if password != "pr.Achour":
            return "You are not the pr.Achour..."
        now = datetime.now()
        valides = {
            nom: data for nom, data in reponses_utilisateurs.items()
            if now - data['time'] < timedelta(hours=2)
        }
        return render_template(
            'stats.html',
            data=valides,
            correct=reponses_correctes,
            explications=explications,
            questions=questions,
            choix=choix
        )
    return render_template('login_stats.html')
