from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

# -----------------
# Configuração da IA
# -----------------
# O pipeline 'zero-shot-classification' é perfeito para o nosso caso.
# Ele classifica um texto em categorias (produtivo/improdutivo) sem precisar ser treinado especificamente para isso.
# O modelo 'facebook/bart-large-mnli' é um dos mais eficientes para essa tarefa.
print("Carregando o modelo de IA... Por favor, aguarde.")
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
    print("Modelo de IA carregado com sucesso!")
except Exception as e:
    print(f"Erro ao carregar o modelo de IA: {e}")
    classifier = None

# -----------------
# Configuração do Flask
# -----------------
app = Flask(__name__)
# O CORS é necessário para permitir que seu frontend (em um domínio diferente)
# possa se comunicar com este backend.
CORS(app)

# -----------------
# Lógica da Aplicação
# -----------------
def process_email(email_text):
    """
    Classifica o email e sugere uma resposta baseada na categoria.
    """
    if not classifier:
        return {"category": "erro", "response": "Modelo de IA não disponível."}

    # As categorias que queremos classificar
    candidate_labels = ["produtivo", "improdutivo"]
    
    # Executa a classificação
    try:
        result = classifier(email_text, candidate_labels=candidate_labels)
        
        # A categoria com o maior score de confiança
        category = result['labels'][0]
        
        # Lógica para gerar a resposta sugerida
        if category == "produtivo":
            suggested_response = "Olá, obrigado pelo seu email. Estamos processando sua solicitação e entraremos em contato em breve com uma atualização."
        else: # categoria "improdutivo"
            suggested_response = "Olá, obrigado pela sua mensagem! Tenha um ótimo dia."
        
        return {"category": category, "response": suggested_response}

    except Exception as e:
        print(f"Erro na classificação ou geração de resposta: {e}")
        return {"category": "erro", "response": "Ocorreu um erro no processamento do email."}

# -----------------
# Rota da API
# -----------------
@app.route('/classify', methods=['POST'])
def classify_email():
    """
    Endpoint da API para receber o conteúdo do email, processar e retornar a classificação.
    """
    # Garante que a requisição é um JSON
    data = request.get_json(silent=True)
    if not data or 'email_content' not in data:
        return jsonify({"error": "Requisição inválida. Envie um JSON com a chave 'email_content'."}), 400

    email_content = data.get('email_content')
    
    # Chama a função de processamento
    result = process_email(email_content)
    
    return jsonify(result)

# -----------------
# Execução
# -----------------
if __name__ == '__main__':
    # Quando você rodar o arquivo, o servidor Flask vai iniciar
    # Em produção, você usaria um servidor como Gunicorn ou uWSGI
    app.run(debug=True)