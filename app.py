import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import streamlit as st

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
def load_data():
    return pd.read_csv('03_streaming.csv')


df = load_data()
freq = df['frequencia_uso_mes']

mu = freq.mean()
sigma = freq.std()

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
x_limite = st.sidebar.slider(
    'Acessos por mês',
    int(freq.min()),
    int(freq.max()),
    max(int(freq.min()), min(12, int(freq.max()))),
    label_visibility='collapsed',
)
st.sidebar.caption(
    'Usuários com frequência igual ou abaixo do limite são considerados '
    'na zona de risco.'
)
st.sidebar.markdown('---')
st.sidebar.caption(f'Base analisada · {len(freq):,} registros'.replace(',', '.'))

z_score = (x_limite - mu) / sigma
prob_cancelamento = stats.norm.cdf(z_score)
usuarios_risco = len(freq[freq <= x_limite])
perc_real = (usuarios_risco / len(freq)) * 100

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
metric_columns = st.columns(4)
metrics = (
    ('Média de acessos', f'{mu:.2f}', False),
    ('Desvio padrão', f'{sigma:.2f}', False),
    ('Risco teórico', f'{prob_cancelamento * 100:.1f}%', True),
    ('Risco observado', f'{perc_real:.1f}%', True),
)
for column, (label, value, is_accent) in zip(metric_columns, metrics):
    accent_class = ' metric-card--accent' if is_accent else ''
    column.markdown(
        f"""
        <div class="metric-card{accent_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div style="height:1.6rem"></div>', unsafe_allow_html=True)

with st.container(key='chart_card'):
    st.markdown('<div class="section-heading">Distribuição de uso mensal</div>', unsafe_allow_html=True)

    x_min = min(mu - 3 * sigma, x_limite)
    x_max = max(mu + 3 * sigma, x_limite)
    x_axis = np.linspace(x_min, x_max, 1000)
    fig, ax = plt.subplots(figsize=(11, 4.8))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    ax.plot(
        x_axis,
        stats.norm.pdf(x_axis, mu, sigma),
        label='Distribuição normal',
        color='#635bdb',
        linewidth=2.8,
        zorder=3,
    )
    x_fill = np.linspace(x_min, x_limite, 500)
    ax.fill_between(
        x_fill,
        stats.norm.pdf(x_fill, mu, sigma),
        color='#ef7188',
        alpha=0.24,
        label=f'Zona de risco (≤ {x_limite} acessos)',
    )
    ax.axvline(
        x_limite,
        color='#dc536e',
        linestyle='--',
        linewidth=2,
        label=f'Limiar de alerta: {x_limite}',
    )
    ax.axvline(
        mu,
        color='#26334e',
        linestyle=':',
        linewidth=1.8,
        label=f'Média: {mu:.1f}',
    )

    ax.set_xlabel('Frequência de uso no mês', color='#71809b', labelpad=12)
    ax.set_ylabel('Densidade', color='#71809b', labelpad=10)
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.spines['bottom'].set_color('#e8ebf3')
    ax.tick_params(colors='#71809b', length=0, pad=8)
    ax.grid(axis='y', color='#e8ebf3', linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, loc='upper right', fontsize=9, labelcolor='#53617a')
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

st.markdown('<div style="height:.8rem"></div>', unsafe_allow_html=True)
st.info(
    f'**Como interpretar:** no limite de **{x_limite} acessos**, o escore Z é '
    f'**{z_score:.2f}**. O modelo normal estima **{prob_cancelamento * 100:.2f}%** '
    f'dos usuários nessa faixa; na base observada, são **{perc_real:.2f}%**.'
)
