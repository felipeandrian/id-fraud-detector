import os
import argparse
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from google import genai

# 1. Carrega as chaves do arquivo .env
load_dotenv()
AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
AZURE_KEY = os.getenv('AZURE_KEY')
GEMINI_KEY = os.getenv('GEMINI_KEY')

# 2. Inicializa os clientes
azure_client = DocumentAnalysisClient(
    endpoint=AZURE_ENDPOINT, 
    credential=AzureKeyCredential(AZURE_KEY)
)
gemini_client = genai.Client(api_key=GEMINI_KEY)

# 3. Função Principal
def analisar_documento(caminho_imagem):
    print(f"\n 1. Lendo o arquivo '{caminho_imagem}' e enviando para o Azure...")
    
    try:
        with open(caminho_imagem, "rb") as documento:
            poller = azure_client.begin_analyze_document(
                "prebuilt-idDocument", document=documento
            )
            resultado_azure = poller.result()
    except Exception as e:
        print(f" Erro ao ler a imagem ou conectar com o Azure: {e}")
        return

    # Dicionário de tradução
    mapa_campos = {
        "FirstName": "Nome", "LastName": "Sobrenome",
        "DocumentNumber": "Número do Documento", "PersonalNumber": "CPF",
        "DateOfBirth": "Data de Nascimento", "DateOfIssue": "Data de Emissão",
        "DateOfExpiration": "Data de Expiração"
    }

    dados_extraidos = {}
    for doc in resultado_azure.documents:
        for nome_campo, campo in doc.fields.items():
            if campo.value:
                nome_traduzido = mapa_campos.get(nome_campo, nome_campo)
                dados_extraidos[nome_traduzido] = {
                    "valor": campo.value,
                    "confianca": campo.confidence 
                }
    
    print("\n --- DADOS LIDOS DO DOCUMENTO ---")
    for campo, info in dados_extraidos.items():
        print(f"[+] {campo}: {info['valor']} (Confiança: {info['confianca']})")
    print("------------------------------------\n")

    print(" 2. Dados extraídos! Enviando para o Gemini auditar...")
    
    prompt = f"""
    Você é um auditor especialista em prevenção de fraudes. 
    Analise os seguintes dados extraídos de um documento de identidade por um sistema de OCR:
    
    {dados_extraidos}
    
    Regras de análise:
    1. Verifique a pontuação de confiança (confianca) de cada campo. Se a confiança de campos cruciais (como Nome, Sobrenome, Número do Documento, Data de Nascimento) for menor que 0.85, sinalize como ALTA SUSPEITA de adulteração visual.
    2. Analise a coerência lógica e temporal.
    3. Retorne o seu veredito exatamente neste formato:
       - VEREDITO: [APROVADO, SUSPEITO ou FRAUDE]
       - JUSTIFICATIVA: [Explique o motivo em tópicos curtos e diretos]
    """
    
    try:
        resposta_gemini = gemini_client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt
        )
        print("\n" + "="*30)
        print("+] RESULTADO DA AUDITORIA ")
        print("="*30)
        print(resposta_gemini.text)
        
    except Exception as e:
        print(f"\n Ops! Erro ao consultar o Gemini: {e}")

# 4. Configuração do Terminal (Command Line Interface)
if __name__ == "__main__":
    # Cria o interpretador de comandos
    parser = argparse.ArgumentParser(description="Detector de Fraude em Documentos de Identidade")
    parser.add_argument("-i", "--image", required=True, help="Caminho para a imagem do documento (JPG, PNG, PDF)")
    
    # Lê os argumentos digitados
    args = parser.parse_args()
    
    # Verifica se o arquivo realmente existe na máquina antes de tentar abrir
    if not os.path.exists(args.image):
        print(f" Erro: O arquivo '{args.image}' não foi encontrado.")
    else:
        analisar_documento(args.image)
