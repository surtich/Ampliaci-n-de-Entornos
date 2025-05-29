#!/usr/bin/env python
# src/financial_researcher/main.py
import os
from financial_researcher.crew import ResearchCrew

# Crea el directorio de salida si no existe
os.makedirs('output', exist_ok=True)

def run():
    """
    Ejecuta el equipo de investigación.
    """
    inputs = {
        'company': 'Google',
    }

    # Crea y ejecuta el equipo
    result = ResearchCrew().crew().kickoff(inputs=inputs)

    # Imprime el resultado
    print("\n\n=== INFORME FINAL ===\n\n")
    print(result.raw)

    print("\n\nEl informe ha sido guardado en output/report.md")

if __name__ == "__main__":
    run()
