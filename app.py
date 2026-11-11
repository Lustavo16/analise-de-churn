import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from calculos import calcular_risco, densidade_normal

st.set_page_config(
    page_title='Análise de Churn | Streaming',
    page_icon='📊',
    layout='wide',
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --ink: #17233c;
        --muted: #71809b;
        --accent: #635bdb;
        --line: #e8ebf3;
        --surface: #ffffff;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 92% 0%, rgba(119, 111, 235, 0.10), transparent 34%),
            #f5f7fc;
        color: var(--ink);
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3, [data-testid="stMetricValue"] {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
    }

    .block-container {
        max-width: 1440px;
        padding-top: 2.4rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #fff;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] [data-testid="stMarkdown"] p {
        color: var(--muted);
        line-height: 1.65;
    }

    .hero {
        padding: 1.75rem 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(226, 230, 242, 0.9);
        border-radius: 22px;
        background: linear-gradient(115deg, #fff 42%, #f0efff 100%);
        box-shadow: 0 12px 34px rgba(32, 45, 80, 0.055);
    }

    .eyebrow {
        margin: 0 0 .55rem;
        color: var(--accent);
        font-size: .73rem;
        font-weight: 700;
        letter-spacing: .13em;
        text-transform: uppercase;
    }

    .hero h1 {
        margin: 0;
        font-size: clamp(1.7rem, 3vw, 2.45rem);
        font-weight: 800;
        letter-spacing: -.045em;
        line-height: 1.15;
    }

    .hero-copy {
        max-width: 720px;
        margin: .7rem 0 0;
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.6;
    }

    .section-heading {
        margin: .3rem 0 1rem;
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.16rem;
        font-weight: 700;
        letter-spacing: -.02em;
    }

    .metric-card {
        min-height: 122px;
        padding: 1.15rem 1.25rem;
        border: 1px solid var(--line);
        border-radius: 16px;
        background: var(--surface);
        box-shadow: 0 7px 22px rgba(32, 45, 80, 0.045);
    }

    .metric-label {
        margin: 0 0 .65rem;
        color: var(--muted);
        font-size: .83rem;
        font-weight: 600;
    }

    .metric-value {
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -.04em;
        line-height: 1.15;
    }

    .metric-card--accent .metric-value {
        color: var(--accent);
    }

    .st-key-chart_card {
        padding: 1.2rem 1.3rem .5rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: var(--surface);
        box-shadow: 0 7px 22px rgba(32, 45, 80, 0.045);
    }

    div[data-testid="stAlert"] {
        border: 1px solid #e2e0ff;
        border-radius: 14px;
        background: #f0efff;
        color: #393777;
    }

    @media (max-width: 768px) {
        .block-container { padding: 1.25rem 1rem 2rem; }
        .hero { padding: 1.35rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def carregar_dados():
    return pd.read_csv('03_streaming.csv')


@st.cache_data
def carregar_tabela_z():
    tabela = pd.read_excel('tabela_normal_Z.xlsx', dtype=str)

    return {
        str(linha.iloc[0]): {
            round(float(coluna), 2): float(valor)
            for coluna, valor in zip(tabela.columns[1:], linha.iloc[1:])
        }
        for _, linha in tabela.iterrows()
    }


dados = carregar_dados()
frequencias = dados['frequencia_uso_mes']
status_assinaturas = dados['status_assinatura']
tabela_z = carregar_tabela_z()

st.sidebar.markdown(
    """
    <p class="eyebrow">Painel de análise</p>
    <h2 style="margin:0; font-family:Manrope,sans-serif; color:#17233c;">
        Parâmetros
    </h2>
    <p>Ajuste o limite mensal para explorar a faixa de atenção.</p>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown('**Limiar de alerta**')
limiar_alerta = st.sidebar.slider(
    'Acessos por mês',
    int(frequencias.min()),
    int(frequencias.max()),
    max(int(frequencias.min()), min(12, int(frequencias.max()))),
    label_visibility='collapsed',
)
st.sidebar.caption(
    'Usuários com frequência igual ou abaixo do limite são considerados '
    'na zona de risco.'
)
st.sidebar.markdown('---')
st.sidebar.caption(
    f'Base analisada · {len(frequencias):,} registros'.replace(',', '.')
)

try:
    analise = calcular_risco(
        frequencias,
        status_assinaturas,
        limiar_alerta,
        tabela_z,
    )
except ValueError as erro:
    st.error(f'Não foi possível calcular os indicadores: {erro}')
    st.stop()

st.markdown(
    f"""
    <section class="hero">
        <p class="eyebrow">Inteligência de produto · Streaming</p>
        <h1>Engajamento & risco de churn</h1>
        <p class="hero-copy">
            Uma leitura da frequência de uso para entender a faixa crítica
            de engajamento, combinando distribuição normal e padronização Z.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-heading">Resumo da análise</div>', unsafe_allow_html=True)
colunas_metricas = st.columns(5)
metricas = (
    ('Média de acessos', f'{analise.media:.2f}', False),
    ('Desvio padrão', f'{analise.desvio_padrao:.2f}', False),
    ('Risco teórico', f'{analise.probabilidade_teorica * 100:.1f}%', True),
    ('Risco observado', f'{analise.percentual_risco_observado:.1f}%', True),
    (
        'Cancelamento na zona de risco',
        f'{analise.probabilidade_cancelamento_na_zona_de_risco * 100:.1f}%',
        True,
    ),
)
for coluna, (rotulo, valor, destacar) in zip(colunas_metricas, metricas):
    classe_destaque = ' metric-card--accent' if destacar else ''
    coluna.markdown(
        f"""
        <div class="metric-card{classe_destaque}">
            <div class="metric-label">{rotulo}</div>
            <div class="metric-value">{valor}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div style="height:1.6rem"></div>', unsafe_allow_html=True)

with st.container(key='chart_card'):
    st.markdown('<div class="section-heading">Distribuição de uso mensal</div>', unsafe_allow_html=True)

    minimo_x = min(
        analise.media - 3 * analise.desvio_padrao,
        limiar_alerta,
    )
    maximo_x = max(
        analise.media + 3 * analise.desvio_padrao,
        limiar_alerta,
    )
    eixo_x = np.linspace(minimo_x, maximo_x, 1000)
    figura, eixo = plt.subplots(figsize=(11, 4.8))
    figura.patch.set_facecolor('white')
    eixo.set_facecolor('white')

    eixo.plot(
        eixo_x,
        np.fromiter(
            (
                densidade_normal(valor, analise.media, analise.desvio_padrao)
                for valor in eixo_x
            ),
            dtype=float,
            count=eixo_x.size,
        ),
        label='Distribuição normal',
        color='#635bdb',
        linewidth=2.8,
        zorder=3,
    )
    eixo_risco_x = np.linspace(minimo_x, limiar_alerta, 500)
    eixo.fill_between(
        eixo_risco_x,
        np.fromiter(
            (
                densidade_normal(valor, analise.media, analise.desvio_padrao)
                for valor in eixo_risco_x
            ),
            dtype=float,
            count=eixo_risco_x.size,
        ),
        color='#ef7188',
        alpha=0.24,
        label=f'Zona de risco (≤ {limiar_alerta} acessos)',
    )
    eixo.axvline(
        limiar_alerta,
        color='#dc536e',
        linestyle='--',
        linewidth=2,
        label=f'Limiar de alerta: {limiar_alerta}',
    )
    eixo.axvline(
        analise.media,
        color='#26334e',
        linestyle=':',
        linewidth=1.8,
        label=f'Média: {analise.media:.1f}',
    )

    eixo.set_xlabel('Frequência de uso no mês', color='#71809b', labelpad=12)
    eixo.set_ylabel('Densidade', color='#71809b', labelpad=10)
    eixo.spines[['top', 'right', 'left']].set_visible(False)
    eixo.spines['bottom'].set_color('#e8ebf3')
    eixo.tick_params(colors='#71809b', length=0, pad=8)
    eixo.grid(axis='y', color='#e8ebf3', linewidth=0.8)
    eixo.set_axisbelow(True)
    eixo.legend(frameon=False, loc='upper right', fontsize=9, labelcolor='#53617a')
    figura.tight_layout()
    st.pyplot(figura, use_container_width=True)
    plt.close(figura)

st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
st.info(
    f'**Como interpretar:** no limite de **{limiar_alerta} acessos**, '
    f'o escore Z é **{analise.escore_z:.2f}**. O modelo normal estima '
    f'**{analise.probabilidade_teorica * 100:.2f}%** dos usuários nessa faixa; '
    f'**{analise.usuarios_em_risco}** usuários '
    f'(**{analise.percentual_risco_observado:.2f}%** da base) estão na zona '
    f'de risco. Desses, **{analise.cancelamentos_na_zona_de_risco}** têm status '
    f'Cancelado (**{analise.probabilidade_cancelamento_na_zona_de_risco * 100:.2f}%**). '
    f'Os status são simulados para demonstração.'
)
