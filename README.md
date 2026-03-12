
# 🛡 ID Fraud Detector: Azure AI & Gemini Cognitive Analysis

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Azure](https://img.shields.io/badge/Azure-Document%20Intelligence-0089D6?logo=microsoft-azure)
![Google Gemini](https://img.shields.io/badge/Google-Gemini%20API-4285F4?logo=google)
![Status](https://img.shields.io/badge/Status-PoC%20Concluída-success)

Uma solução inteligente de **Prova de Conceito (PoC)** projetada para analisar documentos de identidade, extrair dados com precisão e detectar potenciais fraudes utilizando a combinação de Visão Computacional e Inteligência Artificial Generativa.

Esta arquitetura híbrida une o poder de extração e análise estrutural do **Azure Document Intelligence** com o raciocínio lógico avançado do **Google Gemini**. O resultado é um motor cognitivo capaz de auditar documentos de forma automatizada, identificando adulterações visuais e inconsistências de dados.

---

##  Principais Funcionalidades

- **Extração de Dados (OCR) Robusta:** Identifica e estrutura campos-chave (Nome, CPF, Data de Nascimento, etc.) independente do formato da identidade.
- **Detecção de Adulteração Visual:** Utiliza a métrica de *Confidence Score* (Grau de Confiança) do Azure. Pontuações baixas em campos cruciais indicam possíveis sobreposições de texto, edições digitais ou baixíssima resolução.
- **Auditoria Cognitiva (Cross-checking):** O modelo Gemini atua como um inspetor de fraudes, cruzando as informações extraídas para encontrar inconsistências lógicas ou temporais (ex: validade do documento anterior à data de emissão).
- **Interface de Linha de Comando (CLI):** Execução rápida e direta via terminal, facilitando integrações com sistemas legados ou pipelines automatizados.
- **Nuvem e Interatividade:** Inclui um Jupyter Notebook (Google Colab) com interface de upload para testes visuais rápidos sem necessidade de configuração de ambiente local.

---

##  Tecnologias Utilizadas

* **Linguagem:** Python
* **Visão e Extração:** Microsoft Azure AI Document Intelligence (Camada Free F0)
* **Motor Cognitivo (LLM):** Google Gemini 2.5 Flash API (Also Free)
* **Bibliotecas Principais:** `azure-ai-formrecognizer`, `google-genai`, `python-dotenv`

---

##  Como Executar Localmente

### 1. Pré-requisitos
* Python 3.8 ou superior instalado.
* Uma conta no **Microsoft Azure** (com um recurso de Inteligência de Documentos criado e chaves em mãos).
* Uma chave de API gratuita do **Google AI Studio** (Gemini).

### 2. Instalação
Clone este repositório para a sua máquina local:
```bash
git clone [https://github.com/felipeandrian/id-fraud-detector.git](https://github.com/felipeandrian/id-fraud-detector.git)
cd id-fraud-detector

```

Instale as dependências necessárias:

```bash
pip install -r requirements.txt

```

### 3. Configuração de Variáveis de Ambiente

Renomeie o arquivo de exemplo oculto para ativar o ambiente seguro:

```bash
mv .env.example .env

```

Edite o arquivo `.env` gerado e insira suas chaves de API reais:

```env
AZURE_ENDPOINT=[https://seu-recurso.cognitiveservices.azure.com/](https://seu-recurso.cognitiveservices.azure.com/)
AZURE_KEY=sua_chave_azure_aqui
GEMINI_KEY=sua_chave_gemini_aqui

```

##  Uso da CLI (Command Line Interface)

Para analisar um documento, execute o script principal passando o caminho da imagem do documento através do argumento `-i` (ou `--image`). O sistema aceita formatos JPG, PNG e PDF.

```bash
python id-fraud-detector.py -i caminho/para/seu/documento.jpg

```

###  Exemplo de Saída Esperada no Terminal:

```text
[+] 1. Lendo o arquivo 'documento.jpg' e enviando para o Azure...

 --- DADOS LIDOS DO DOCUMENTO ---
[+] Nome: LUIZ (Confiança: 0.551)
[+] Sobrenome: INÁCIO LULA DA SILVA (Confiança: 0.798)
[+] Data de Nascimento: 1945-10-06 (Confiança: 0.866)
[+] Data de Expiração: 2030-12-30 (Confiança: None)
------------------------------------

[+] 2. Dados extraídos! Enviando para o Gemini auditar...

==============================
 [+}️ RESULTADO DA AUDITORIA 
==============================
VEREDITO: SUSPEITO
JUSTIFICATIVA:
- A confiança do campo 'Nome' (0.551) está muito abaixo do limite crítico de 0.85, indicando alta probabilidade de adulteração visual ou sobreposição.
- Não foi possível validar a coerência temporal da Data de Expiração devido à ausência de dados lidos para a Data de Emissão.

```

---

##  Teste Rápido no Google Colab

Se você preferir não configurar o ambiente local agora, pode testar a lógica diretamente na nuvem usando o arquivo `id_fraud_detector_colab.ipynb` incluído neste repositório.
Basta abri-lo no Google Colab, cadastrar suas chaves na aba de **Secrets** e executar as células.

---

##  Aviso Legal e Responsabilidade

*Este projeto é estritamente educacional e configura uma Prova de Conceito (PoC). Não deve ser utilizado como única fonte de verdade em ambientes de produção que lidam com dados sensíveis sem a devida conformidade com leis de proteção de dados (como LGPD/GDPR) e revisões de segurança avançadas.*


## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
