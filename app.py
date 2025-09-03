import gradio as gr
from transformers import pipeline

# Carregando o modelo de IA
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    print(f"Erro ao carregar o modelo de IA: {e}")
    classifier = None

def classify_email(email_content):
    if not classifier:
        return "Erro", "Modelo de IA não disponível.", ""
    
    critical_keywords = [
        "solicitação", "pedido", "suporte", "atualização", "ajuda", "dúvida", 
        "retorno", "problema", "resposta", "preciso de", "necessito de", 
        "gostaria de", "qual o status", "extrato", "documento", "fatura", 
        "senha", "acesso", "conta", "cancelar", "reembolso", "troca"
    ]
    
    email_lower = email_content.lower()
    for keyword in critical_keywords:
        if keyword in email_lower:
            return "PRODUTIVO", "Olá, obrigado pelo seu email. Estamos processando sua solicitação e entraremos em contato em breve com uma atualização.", "Classificação por palavra-chave crítica. Não há análise de IA."

    candidate_labels = ["saudacao", "mensagem de cortesia", "solicitacao"]
    try:
        result = classifier(email_content, candidate_labels=candidate_labels, multi_label=True)
        probabilities_str = ""
        for label, score in zip(result['labels'], result['scores']):
            probabilities_str += f"- {label.capitalize()}: {score:.2f}\n"
        try:
            action_score = result['scores'][result['labels'].index('solicitacao')]
        except ValueError:
            action_score = 0
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

# CSS personalizado
custom_css = """
body, .gradio-container {
    background: linear-gradient(135deg, #FFB347 0%, #FF9900 100%);
}
.gradio-container {
    min-height: 100vh;
}
h1, h2, h3, label {
    color: #FF9900;
}
.gr-button {
    background: #FF9900 !important;
    color: #fff !important;
    border-radius: 8px !important;
    font-weight: bold;
}
#cliente-card, #ia-card {
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 4px 24px rgba(255,153,0,0.15);
    padding: 24px;
    margin: 8px;
}
"""

with gr.Blocks(css=custom_css) as demo:
    
    with gr.Row():
        # Card da Visão do Cliente
        with gr.Column(scale=3):
            with gr.Group(elem_id="cliente-card"):
                gr.Markdown(
                    """
                    <div style="text-align:center; width:100%; margin-bottom:16px;">
                        <h1 style="margin-bottom:0;">Fale Conosco</h1>
                    </div>
                    """
                )           
                email_input = gr.Textbox(lines=8, label="Digite ou copie aqui sua mensagem que teremos prazer em te responder", placeholder="Digite aqui sua dúvida, pedido ou sugestão...")
                classify_btn = gr.Button("Enviar")
                response_out = gr.Textbox(label="Resposta Sugerida", interactive=False)

        # Card dos Bastidores da IA
        with gr.Column(scale=2):
            with gr.Group(elem_id="ia-card"):
                gr.Markdown("### Bastidores da IA")
                category_out = gr.Textbox(label="Categoria", interactive=False)
                gr.Markdown(
                    """
                    <b>Palavras-chave críticas:</b><br>
                    <span style="color:#FF9900;">solicitação, pedido, suporte, atualização, ajuda, dúvida, retorno, problema, resposta, preciso de, necessito de, gostaria de, qual o status, extrato, documento, fatura, senha, acesso, conta, cancelar, reembolso, troca</span>
                    <br><br>
                    <b>Probabilidades da IA:</b>
                    """)
                probabilities_out = gr.Textbox(label="", interactive=False)

    classify_btn.click(
        classify_email, 
        inputs=email_input, 
        outputs=[category_out, response_out, probabilities_out]
    )

demo.launch()