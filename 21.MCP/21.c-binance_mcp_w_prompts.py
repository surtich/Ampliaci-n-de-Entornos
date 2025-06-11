# mcp dev 21.MCP/21.c-binance_mcp_w_prompts.py

import datetime
from pathlib import Path
from typing import Any

import requests
from mcp.server.fastmcp import FastMCP

THIS_FOLDER = Path(__file__).parent.absolute()
ACTIVITY_LOG_FILE = THIS_FOLDER / "activity.log"

mcp = FastMCP("Binance MCP")


def get_symbol_from_name(name: str) -> str:
    if name.lower() in ["bitcoin", "btc"]:
        return "BTCUSDT"
    elif name.lower() in ["ethereum", "eth"]:
        return "ETHUSDT"
    else:
        return name.upper()


@mcp.prompt()
def executive_summary() -> str:
    """Devuelve un resumen ejecutivo de Bitcoin y Ethereum"""
    return """
    Obtén los precios de los siguientes activos cripto: btc, eth

    Proporcióname un resumen ejecutivo que incluya el 
    resumen en dos oraciones del activo cripto, el precio actual, 
    el cambio de precio en las últimas 24 horas y el cambio porcentual
    en las últimas 24 horas.

    Al usar las herramientas get_price y get_price_price_change,
    usa el símbolo como argumento.
    
    Símbolos: Para bitcoin/btc, el símbolo es "BTCUSDT".
    Símbolos: Para ethereum/eth, el símbolo es "ETHUSDT".
    """


@mcp.prompt()
def crypto_summary(crypto: str) -> str:
    """Devuelve un resumen de un activo cripto"""

    return f"""
    Obtén el precio actual del siguiente activo cripto:
    {crypto}
    y también proporciona un resumen de los cambios de precio en las últimas 24 horas.

    Al usar las herramientas get_price y get_price_price_change, usa el símbolo como argumento.
    Símbolos: Para bitcoin/btc, el símbolo es "BTCUSDT".
    Símbolos: Para ethereum/eth, el símbolo es "ETHUSDT".
    """


@mcp.tool()
def get_price(symbol: str) -> Any:
    """
    Get the current price of a crypto asset from Binance

    Args:
        symbol (str): The symbol of the crypto asset to get the price of

    Returns:
        Any: The current price of the crypto asset
    """
    symbol = get_symbol_from_name(symbol)
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    if response.status_code != 200:
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(
                f"Error getting price change for {symbol}: {response.status_code} {response.text}\n"
            )
        raise Exception(
            f"Error getting price change for {symbol}: {response.status_code} {response.text}"
        )
    else:
        price = response.json()["price"]
        with open(ACTIVITY_LOG_FILE, "a") as f:
            f.write(
                f"Successfully got price change for {symbol}. Current price is {price}. Current time is {datetime.datetime.now(datetime.UTC)}\n"
            )
    return f"The current price of {symbol} is {price}"


@mcp.resource("file://activity.log")
def activity_log() -> str:
    with open(ACTIVITY_LOG_FILE, "r") as f:
        return f.read()


@mcp.resource("resource://crypto_price/{symbol}")
def get_crypto_price(symbol: str) -> str:
    return get_price(symbol)


@mcp.tool()
def get_price_price_change(symbol: str) -> Any:
    """
    Get the price change of the last 24 hours of a crypto asset from Binance

    Args:
        symbol (str): The symbol of the crypto asset to get the price change of

    Returns:
        Any: The price change of the crypto asset in the last 24 hours
    """
    symbol = get_symbol_from_name(symbol)
    url = f"https://data-api.binance.vision/api/v3/ticker/24hr?symbol={symbol}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if not Path(ACTIVITY_LOG_FILE).exists():
        Path(ACTIVITY_LOG_FILE).touch()
    mcp.run(transport="stdio")
