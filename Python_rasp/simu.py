from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita o CORS para todas as rotas

# Status inicial dos dispositivos
ar_condicionado_ligado = False
projetor_ligado = False
lampadas = {
    "coluna1": False,
    "coluna2": False,
    "coluna3": False
}
temperatura_ar_condicionado = 25  # Temperatura inicial

@app.route('/enviar-comando', methods=['POST'])
def enviar_comando():
    global ar_condicionado_ligado, projetor_ligado, lampadas, temperatura_ar_condicionado

    # Recebe o comando enviado pelo JavaScript
    comando = request.json.get('comando')

    # Processa o comando
    if comando == 'ligarArCondicionado':
        ar_condicionado_ligado = True
        resposta = "Ar condicionado ligado."
    elif comando == 'desligarArCondicionado':
        ar_condicionado_ligado = False
        resposta = "Ar condicionado desligado."
    elif comando == 'ligarProjetor':
        projetor_ligado = True
        resposta = "Projetor ligado."
    elif comando == 'desligarProjetor':
        projetor_ligado = False
        resposta = "Projetor desligado."
    elif comando.startswith('ligarLampadas:'):
        coluna = comando.split(':')[1]
        if coluna in lampadas:
            lampadas[coluna] = True
            resposta = f"Lâmpadas da {coluna} ligadas."
        else:
            resposta = "Coluna de lâmpadas desconhecida."
    elif comando.startswith('desligarLampadas:'):
        coluna = comando.split(':')[1]
        if coluna in lampadas:
            lampadas[coluna] = False
            resposta = f"Lâmpadas da {coluna} desligadas."
        else:
            resposta = "Coluna de lâmpadas desconhecida."
    elif comando == 'aumentarTemperatura':
        if temperatura_ar_condicionado < 30:
            temperatura_ar_condicionado += 1
            resposta = f"Temperatura do ar condicionado aumentada para {temperatura_ar_condicionado}°C."
        else:
            resposta = "A temperatura máxima foi atingida."
    elif comando == 'diminuirTemperatura':
        if temperatura_ar_condicionado > 16:
            temperatura_ar_condicionado -= 1
            resposta = f"Temperatura do ar condicionado diminuída para {temperatura_ar_condicionado}°C."
        else:
            resposta = "A temperatura mínima foi atingida."
    else:
        resposta = "Comando desconhecido."

    return jsonify({"resposta": resposta})

@app.route('/status-dispositivos', methods=['GET'])
def status_dispositivos():
    global ar_condicionado_ligado, projetor_ligado, lampadas, temperatura_ar_condicionado

    status = {
        "ar_condicionado": ar_condicionado_ligado,
        "projetor": projetor_ligado,
        "lampadas": lampadas,
        "temperatura_ar_condicionado": temperatura_ar_condicionado
    }

    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True)
