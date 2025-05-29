#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Crear el directorio de salida si no existe
os.makedirs('output', exist_ok=True)

requirements = """
Un sistema simple de gestión de cuentas para una plataforma de simulación de trading.
El sistema debe permitir a los usuarios crear una cuenta, depositar fondos y retirar fondos.
El sistema debe permitir a los usuarios registrar que han comprado o vendido acciones, proporcionando una cantidad.
El sistema debe calcular el valor total del portafolio del usuario y las ganancias o pérdidas desde el depósito inicial.
El sistema debe poder reportar las tenencias del usuario en cualquier momento.
El sistema debe poder reportar las ganancias o pérdidas del usuario en cualquier momento.
El sistema debe poder listar las transacciones que el usuario ha realizado con el tiempo.
El sistema debe evitar que el usuario retire fondos que dejen un balance negativo, 
o compre más acciones de las que puede pagar, o venda acciones que no posee.
El sistema tiene acceso a una función get_share_price(símbolo) que devuelve el precio actual de una acción, e incluye una implementación de prueba que devuelve precios fijos para AAPL, TSLA, GOOGL.
"""
module_name = "accounts"
class_name = "Account"

def run():
    """
    Ejecuta el equipo de ingeniería de software.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Crear y ejecutar el equipo
    result = EngineeringTeam().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
