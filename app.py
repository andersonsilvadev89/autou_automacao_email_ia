import gradio as gr
from transformers import pipeline

# Carregando o modelo de IA. A primeira vez que rodar, pode demorar um pouco.
# A plataforma Hugging Face é otimizada para isso, então o download será rápido.
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    print(f"Erro ao carregar o modelo de IA: {e}")
    classifier = None

def classify_email(email_content):
    """
    Classifica o email em produtivo/improdutivo e gera uma resposta sugerida.
    """
    if not classifier:
        return "Erro", "Modelo de IA não disponível."
    
    # Define as categorias que queremos classificar
    candidate_labels = ["produtivo", "improdutivo"]
    
    try:
        # Executa a classificação
        result = classifier(email_content, candidate_labels=candidate_labels)
        
        # Pega a categoria com a maior pontuação de confiança
        category = result['labels'][0]
        
        # Lógica para a resposta sugerida
        if category == "produtivo":
            suggested_response = "Olá, obrigado pelo seu email. Estamos processando sua solicitação e entraremos em contato em breve com uma atualização."
        else:
            suggested_response = "Olá, obrigado pela sua mensagem! Tenha um ótimo dia."
        
        return category.upper(), suggested_response
    
    except Exception as e:
        print(f"Erro na classificação: {e}")
        return "Erro", "Ocorreu um erro ao processar o email."

# Criando a interface com Gradio
iface = gr.Interface(
    fn=classify_email, 
    inputs=gr.Textbox(lines=10, label="Cole o conteúdo do email aqui:"), 
    outputs=[
        gr.Textbox(label="Categoria:"), 
        gr.Textbox(label="Resposta Sugerida:")
    ],
    title="Classificador de Emails com IA",
    description="Uma solução que automatiza a classificação de emails e sugere respostas, liberando tempo da equipe.",
    examples=[
        ["Olá, poderia me dar uma atualização sobre o caso #12345? Estamos aguardando o retorno para o cliente."],
        ["Feliz Natal! Desejo um ótimo ano novo para toda a equipe."],
        ["Qual o status da minha solicitação de suporte técnico? Meu problema ainda não foi resolvido."],
    ]
)

# Lançando a aplicação Gradio
iface.launch()