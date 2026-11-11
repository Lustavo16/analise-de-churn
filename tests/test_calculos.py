import math
import unittest

from calculos import calcular_risco, densidade_normal, probabilidade_acumulada_normal


class TestesDistribuicaoNormal(unittest.TestCase):
    def setUp(self):
        self.tabela_z = {
            '-1.2': {0.03: 0.1093},
            '-0.0': {0.02: 0.492},
            '0.0': {0.02: 0.508},
            '1.2': {0.03: 0.8907},
        }

    def test_densidade_no_centro_da_curva(self):
        self.assertAlmostEqual(
            densidade_normal(0, 0, 1), 1 / math.sqrt(2 * math.pi)
        )

    def test_consulta_valores_positivos_e_negativos_na_tabela(self):
        self.assertEqual(
            probabilidade_acumulada_normal(1.234, self.tabela_z),
            0.8907,
        )
        self.assertEqual(
            probabilidade_acumulada_normal(-1.234, self.tabela_z),
            0.1093,
        )

    def test_consulta_linha_de_z_negativo_proximo_de_zero(self):
        self.assertEqual(
            probabilidade_acumulada_normal(-0.02, self.tabela_z),
            0.492,
        )

    def test_rejeita_escore_fora_do_intervalo_da_tabela(self):
        with self.assertRaises(ValueError):
            probabilidade_acumulada_normal(4.0, self.tabela_z)


class TestesAnaliseDeRisco(unittest.TestCase):
    def test_calcula_estatisticas_e_risco_observado(self):
        tabela_z = {'0.0': {0.0: 0.5}}
        resultado = calcular_risco([1, 2, 3, 4, 5], limiar=3, tabela_z=tabela_z)

        self.assertEqual(resultado.media, 3)
        self.assertAlmostEqual(resultado.desvio_padrao, math.sqrt(2.5))
        self.assertEqual(resultado.escore_z, 0)
        self.assertEqual(resultado.probabilidade_teorica, 0.5)
        self.assertEqual(resultado.usuarios_em_risco, 3)
        self.assertEqual(resultado.percentual_risco_observado, 60)
        self.assertEqual(resultado.total_usuarios, 5)

    def test_rejeita_dados_vazios_ou_constantes(self):
        tabela_z = {'0.0': {0.0: 0.5}}
        with self.assertRaises(ValueError):
            calcular_risco([], limiar=3, tabela_z=tabela_z)
        with self.assertRaises(ValueError):
            calcular_risco([4, 4, 4], limiar=4, tabela_z=tabela_z)


if __name__ == '__main__':
    unittest.main()
