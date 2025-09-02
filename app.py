import gradio as gr
from transformers import pipeline

# Carregando o modelo de IA
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    print(f"Erro ao carregar o modelo de IA: {e}")
    classifier = None

def classify_email(email_content):
    """
    Classifica o email e sugere uma resposta baseada na categoria.
    """
    if not classifier:
        return "Erro", "Modelo de IA não disponível.", ""
    
    # ---------------------------------------------
    # 1. Verificação de palavras-chave críticas (Regra de Negócio)
    # ---------------------------------------------
    critical_keywords = [
        "solicitação", "pedido", "suporte", "atualização", "ajuda", "dúvida", 
        "retorno", "problema", "resposta", "preciso de", "necessito de", 
        "gostaria de", "qual o status", "extrato", "documento", "fatura", 
        "senha", "acesso", "conta", "cancelar", "reembolso", "troca"
    ]
    
    email_lower = email_content.lower()
    for keyword in critical_keywords:
        if keyword in email_lower:
            # Novo: Retorna a probabilidade como uma string
            return "PRODUTIVO", "Olá, obrigado pelo seu email. Estamos processando sua solicitação e entraremos em contato em breve com uma atualização.", "Classificação por palavra-chave crítica. Não há análise de IA."

    # ---------------------------------------------
    # 2. Classificação por IA com análise de probabilidade
    # ---------------------------------------------
    candidate_labels = ["saudacao", "mensagem de cortesia", "solicitacao"]
    
    try:
        result = classifier(email_content, candidate_labels=candidate_labels, multi_label=True)
        
        # Converte as probabilidades em uma string para exibição
        probabilities_str = ""
        for label, score in zip(result['labels'], result['scores']):
            probabilities_str += f"- {label.capitalize()}: {score:.2f}\n"

        # Encontra o score da categoria 'pedido de acao'
        try:
            action_score = result['scores'][result['labels'].index('solicitacao')]
        except ValueError:
            action_score = 0
            
        # Define um limite de probabilidade para ser considerado produtivo
        if action_score > 0.40:
            final_category = "produtivo"
            suggested_response = "Olá, obrigado pelo seu email. Estamos processando sua solicitação e entraremos em contato em breve com uma atualização."
        else:
            final_category = "improdutivo"
            suggested_response = "Olá, obrigado pela sua mensagem! Tenha um ótimo dia."
        
        return final_category.upper(), suggested_response, probabilities_str
    
    except Exception as e:
        print(f"Erro na classificação: {e}")
        return "Erro", "Ocorreu um erro ao processar o email.", ""

# -----------------
# Interface Gradio
# -----------------
iface = gr.Interface(
    fn=classify_email, 
    inputs=gr.Textbox(lines=10, label="Cole o conteúdo do email aqui:"), 
    outputs=[
        gr.Textbox(label="Categoria:"), 
        gr.Textbox(label="Resposta Sugerida:"),
        gr.Textbox(label="Probabilidades da IA:", interactive=False) # Novo campo
    ],
    title="Classificador de Emails com IA",
    description="Uma solução que automatiza a classificação de emails e sugere respostas, liberando tempo da equipe.",
    examples=[
        ["Olá, qual o status da minha solicitação?"],
        ["Feliz Natal! Desejo um ótimo ano novo para toda a equipe."],
        ["Obrigado por sua ajuda, resolvemos o problema."],
        ["Bom dia, tudo bem com vocês?"],
        ["Gostaria de saber se o problema foi corrigido."]
    ]
)

# Lançando a aplicação Gradio
iface.launch()