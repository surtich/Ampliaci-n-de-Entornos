#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from coder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Crear el directorio de salida si no existe
os.makedirs('output', exist_ok=True)

assignment = 'Escribe un programa en Python para calcular los primeros 10,000 términos \
    de esta serie, multiplicando el total por 4: 1 - 1/3 + 1/5 - 1/7 + ...'

def run():
    """
    Ejecuta el equipo.
    """
    inputs = {
        'assignment': assignment,
    }
    
    result = Coder().crew().kickoff(inputs=inputs)
    print(result.raw)
