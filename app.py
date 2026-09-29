"""API REST de utilidades numericas - desplegable en Render (PaaS).

Endpoints:
  GET /                    -> estado del servicio
  GET /analizar/<n>        -> factorial, primalidad y Fibonacci de n
"""
from flask import Flask, jsonify

app = Flask(__name__)

MAX_N = 500  # limite para evitar consumo excesivo de CPU en el plan gratuito


def factorial(n: int) -> int:
    resultado = 1
    for i in range(2, n + 1):
        resultado *= i
    return resultado


def es_primo(n: int) -> bool:
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@app.route("/")
def inicio():
    return jsonify(servicio="API de utilidades numericas", estado="ok",
                   uso="/analizar/<n> con n entero entre 0 y %d" % MAX_N)


@app.route("/analizar/<int:n>")
def analizar(n):
    if n < 0 or n > MAX_N:
        return jsonify(error="n debe estar entre 0 y %d" % MAX_N), 400
    return jsonify(n=n, factorial=str(factorial(n)),
                   es_primo=es_primo(n), fibonacci=str(fibonacci(n)))


@app.errorhandler(404)
def no_encontrado(_):
    return jsonify(error="ruta no encontrada; use /analizar/<n>"), 404


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
