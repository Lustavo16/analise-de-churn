# Análise de churn

Aplicação interativa em Streamlit para analisar a frequência de uso mensal e
estimar a faixa de risco de cancelamento de assinaturas de streaming.

## Requisitos

- Python 3.10 ou superior
- Git (opcional, para clonar o repositório)

## Configuração no Windows

Abra o PowerShell na pasta do projeto e crie um ambiente virtual:

```powershell
py -m venv .venv
```

Ative o ambiente e instale as dependências:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se a execução de scripts estiver bloqueada no PowerShell, use o Python do
ambiente diretamente:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Executar

Na raiz do projeto:

```powershell
python -m streamlit run app.py
```

Ou, sem ativar o ambiente:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

O Streamlit exibirá o endereço local da aplicação no terminal.

## Dados

O app carrega `03_streaming.csv`, que deve estar na raiz do projeto e conter a
coluna `frequencia_uso_mes`, e usa `tabela_normal_Z.xlsx` para consultar a
probabilidade teórica, arredondando o escore Z para duas casas decimais. Os
arquivos incluídos contêm dados sintéticos e uma tabela Z para demonstração;
não substitua o CSV por dados pessoais antes de compartilhar publicamente.

A coluna `status_assinatura` também contém rótulos simulados, atribuídos para
aproximar as taxas solicitadas. Como a base não tem registros com 0–2 acessos e
tem apenas três registros com 3–8 acessos, não foi possível atingir as metas
nessas duas faixas: a faixa 3–8 ficou com 1 cancelamento (33,3%). As faixas
9–13 e 14+ ficaram com 8,3% e 1,5% de cancelamentos, respectivamente. Esses
rótulos são demonstrativos, não históricos de cancelamentos observados. A
probabilidade de cancelamento na zona de risco é calculada como cancelamentos
com status `Cancelado` nessa zona divididos pelo total de usuários nela.

## Estrutura

- `app.py`: interface Streamlit
- `calculos.py`: cálculos estatísticos sem SciPy, usando a biblioteca padrão do Python
- `03_streaming.csv`: conjunto de dados de demonstração
- `tabela_normal_Z.xlsx`: valores acumulados da tabela Z
- `requirements.txt`: dependências Python
- `.streamlit/config.toml`: configuração visual do Streamlit

## Testes dos cálculos

```powershell
python -m unittest discover -s tests
```
