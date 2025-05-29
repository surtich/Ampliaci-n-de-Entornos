#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from debate.crew import Debate

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Este archivo principal está pensado para que puedas ejecutar tu
# equipo localmente, así que evita agregar lógica innecesaria aquí.
# Reemplaza con los inputs que quieras probar, se interpolará automáticamente
# la información de las tareas y los agentes.

def run():
    """
    Ejecuta el equipo.
    """
    inputs = {
        'motion': 'Ya no es necesario estudiar DAW porque la IA lo hace todo',
    }
    
    try:
        result = Debate().crew().kickoff(inputs=inputs) # Inicia el equipo con los inputs proporcionados
        print(result.raw)
    except Exception as e:
        raise Exception(f"Ocurrió un error al ejecutar el equipo: {e}")
