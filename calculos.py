from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP
from math import exp, fsum, isfinite, pi, sqrt
from typing import Mapping


@dataclass(frozen=True)
class AnaliseRisco:
    media: float
    desvio_padrao: float
    escore_z: float
    probabilidade_teorica: float
    usuarios_em_risco: int
    percentual_risco_observado: float
    total_usuarios: int


def probabilidade_acumulada_normal(
    escore_z: float,
    tabela_z: Mapping[str, Mapping[float, float]],
) -> float:
    """Arredonda o escore a centésimos e consulta a probabilidade na tabela Z."""
    if not tabela_z:
        raise ValueError('A tabela Z está vazia.')

    escore_arredondado = Decimal(str(escore_z)).quantize(
        Decimal('0.01'),
        rounding=ROUND_HALF_UP,
    )
    valores_linhas = [Decimal(rotulo) for rotulo in tabela_z]
    valores_colunas = {
        Decimal(str(coluna))
        for linha in tabela_z.values()
        for coluna in linha
    }
    if not valores_colunas:
        raise ValueError('A tabela Z não contém colunas de centésimos.')

    menor_escore = min(valores_linhas) - max(valores_colunas)
    maior_escore = max(valores_linhas) + max(valores_colunas)
    if escore_arredondado < menor_escore or escore_arredondado > maior_escore:
        raise ValueError(
            f'O escore Z {escore_arredondado} está fora do intervalo da tabela '
            f'({menor_escore} a {maior_escore}).'
        )

    escore_absoluto = abs(escore_arredondado)
    linha_absoluta = (
        (escore_absoluto * 10).to_integral_value(rounding=ROUND_DOWN)
        / Decimal(10)
    )
    sinal_linha = '-' if escore_arredondado < 0 else ''
    rotulo_linha = f'{sinal_linha}{linha_absoluta:.1f}'
    rotulo_coluna = float(escore_absoluto - linha_absoluta)

    try:
        return tabela_z[rotulo_linha][rotulo_coluna]
    except KeyError as erro:
        raise ValueError(
            f'O escore Z {escore_arredondado} não foi encontrado na tabela.'
        ) from erro


def densidade_normal(valor: float, media: float, desvio_padrao: float) -> float:
    """Calcula a densidade da distribuição normal em um valor."""
    if desvio_padrao <= 0:
        raise ValueError('O desvio padrão precisa ser maior que zero.')

    escore_z = (valor - media) / desvio_padrao
    return exp(-0.5 * escore_z**2) / (desvio_padrao * sqrt(2 * pi))


def calcular_risco(
    frequencias: Iterable[float],
    limiar: float,
    tabela_z: Mapping[str, Mapping[float, float]],
) -> AnaliseRisco:
    """Calcula estatísticas amostrais e riscos teórico e observado."""
    valores = [float(valor) for valor in frequencias]
    if not valores:
        raise ValueError('A lista de frequências está vazia.')
    if len(valores) < 2:
        raise ValueError('São necessários pelo menos dois registros.')
    if not isfinite(limiar) or any(not isfinite(valor) for valor in valores):
        raise ValueError('As frequências e o limiar precisam ser valores finitos.')

    total_usuarios = len(valores)
    media = fsum(valores) / total_usuarios
    variancia = fsum(
        (valor - media) ** 2 for valor in valores
    ) / (total_usuarios - 1)
    desvio_padrao = sqrt(variancia)
    if desvio_padrao == 0:
        raise ValueError(
            'Não é possível ajustar a distribuição normal: '
            'todas as frequências são iguais.'
        )

    escore_z = (limiar - media) / desvio_padrao
    usuarios_em_risco = sum(valor <= limiar for valor in valores)

    return AnaliseRisco(
        media=media,
        desvio_padrao=desvio_padrao,
        escore_z=escore_z,
        probabilidade_teorica=probabilidade_acumulada_normal(escore_z, tabela_z),
        usuarios_em_risco=usuarios_em_risco,
        percentual_risco_observado=usuarios_em_risco / total_usuarios * 100,
        total_usuarios=total_usuarios,
    )
