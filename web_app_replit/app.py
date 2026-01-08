from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading
from datetime import datetime
import os
from funcoes_web import gerar_datas, definitiva_web

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
socketio = SocketIO(app, cors_allowed_origins="*")

# Armazenar estado por sessão
sessoes_ativas = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    sessoes_ativas[session_id] = {
        'status': 'conectado',
        'progresso': 0,
        'total': 0,
        'mensagem': 'Conectado',
        'num_downloads': 0
    }
    emit('conectado', {'session_id': session_id})

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in sessoes_ativas:
        del sessoes_ativas[session_id]

@socketio.on('iniciar_extracao')
def iniciar_extracao(data):
    session_id = request.sid
    
    data_inicio = data.get('data_inicio')
    data_fim = data.get('data_fim')
    filtro = data.get('filtro', [
        "form-filtroAcss-dlgFilterPrefs-tableUser-8-j_idt364",
        "form-filtroAcss-dlgFilterPrefs-tableUser-9-j_idt364"
    ])
    
    # Validar datas
    try:
        datetime.strptime(data_inicio, '%d/%m/%Y')
        datetime.strptime(data_fim, '%d/%m/%Y')
    except ValueError:
        emit('erro', {'mensagem': 'Formato de data inválido. Use DD/MM/YYYY'})
        return
    
    # Gerar datas
    datas = gerar_datas(data_inicio, data_fim)
    sessoes_ativas[session_id]['total'] = len(datas)
    sessoes_ativas[session_id]['status'] = 'processando'
    
    emit('progresso_inicio', {'total': len(datas)})
    
    # Executar em thread
    thread = threading.Thread(
        target=executar_extracao,
        args=(session_id, filtro, datas)
    )
    thread.daemon = True
    thread.start()

def executar_extracao(session_id, filtro, datas):
    """Executa a extração em background"""
    try:
        def callback_progresso(msg):
            """Callback para enviar progresso via websocket"""
            socketio.emit('atualizar_progresso', {
                'mensagem': msg,
                'progresso': sessoes_ativas[session_id]['num_downloads']
            }, room=session_id)
        
        # Iniciar threads de extração
        threads = [
            threading.Thread(
                target=definitiva_web,
                args=(filtro[0], datas, session_id, callback_progresso)
            ),
            threading.Thread(
                target=definitiva_web,
                args=(filtro[1], datas, session_id, callback_progresso)
            )
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # Extração completa
        sessoes_ativas[session_id]['status'] = 'concluido'
        socketio.emit('extracao_concluida', {
            'total_baixado': sessoes_ativas[session_id]['num_downloads'],
            'mensagem': 'Extração finalizada com sucesso!'
        }, room=session_id)
        
    except Exception as e:
        sessoes_ativas[session_id]['status'] = 'erro'
        socketio.emit('erro', {
            'mensagem': f'Erro na extração: {str(e)}'
        }, room=session_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
