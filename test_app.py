import unittest
from app import app, factorial, es_primo, fibonacci


class PruebasFunciones(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual(factorial(0), 1)
        self.assertEqual(factorial(5), 120)
        self.assertEqual(factorial(10), 3628800)

    def test_es_primo(self):
        self.assertFalse(es_primo(0))
        self.assertFalse(es_primo(1))
        self.assertTrue(es_primo(2))
        self.assertTrue(es_primo(97))
        self.assertFalse(es_primo(100))

    def test_fibonacci(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)
        self.assertEqual(fibonacci(10), 55)


class PruebasAPI(unittest.TestCase):
    def setUp(self):
        self.c = app.test_client()

    def test_inicio(self):
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["estado"], "ok")

    def test_analizar_valido(self):
        r = self.c.get("/analizar/7")
        self.assertEqual(r.status_code, 200)
        d = r.get_json()
        self.assertEqual(d["factorial"], "5040")
        self.assertTrue(d["es_primo"])
        self.assertEqual(d["fibonacci"], "13")

    def test_fuera_de_rango(self):
        self.assertEqual(self.c.get("/analizar/501").status_code, 400)
        self.assertEqual(self.c.get("/analizar/-3").status_code, 404)

    def test_ruta_inexistente(self):
        self.assertEqual(self.c.get("/otra").status_code, 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
