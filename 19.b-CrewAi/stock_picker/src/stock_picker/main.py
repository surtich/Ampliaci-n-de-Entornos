#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """
    Ejecuta el equipo de investigación.
    """
    inputs = {
        'sector': 'Tecnología',
        "current_date": str(datetime.now())
    }

    # Crea y ejecuta el equipo
    result = StockPicker().crew().kickoff(inputs=inputs)

    # Imprime el resultado
    print("\n\n=== DECISIÓN FINAL ===\n\n")
    print(result.raw)


if __name__ == "__main__":
    run()
