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
coluna `frequencia_uso_mes`. O CSV incluído neste repositório contém dados
sintéticos para demonstração; não substitua por dados pessoais antes de
compartilhar publicamente.

## Estrutura

- `app.py`: interface e cálculos estatísticos
- `03_streaming.csv`: conjunto de dados de demonstração
- `requirements.txt`: dependências Python
- `.streamlit/config.toml`: configuração visual do Streamlit
