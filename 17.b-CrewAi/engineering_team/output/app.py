import gradio as gr
from accounts import Account, InsufficientFundsError, InsufficientSharesError, get_share_price

# Inicializar la cuenta del usuario
account = Account("user123", initial_deposit=10000.0)

def actualizar_estado():
    balance = account.get_balance()
    holdings = account.get_holdings()
    portfolio_value = account.get_portfolio_value(get_share_price)
    profit_loss = account.get_profit_loss(get_share_price)
    transactions = account.get_transactions()

    holdings_str = ""
    for symbol, quantity in holdings.items():
        holdings_str += f"{symbol}: {quantity}\n"

    transactions_str = ""
    for transaction in transactions:
        transactions_str += f"{transaction}\n"
    
    return balance, holdings_str, portfolio_value, profit_loss, transactions_str


def depositar(amount):
    try:
        amount = float(amount)
        account.deposit(amount)
        return actualizar_estado()
    except ValueError:
        return "Cantidad inválida", "", "", "", ""

def retirar(amount):
    try:
        amount = float(amount)
        account.withdraw(amount)
        return actualizar_estado()
    except ValueError:
        return "Cantidad inválida", "", "", "", ""
    except InsufficientFundsError:
        return "Fondos insuficientes", "", "", "", ""

def comprar(symbol, quantity):
    try:
        quantity = int(quantity)
        account.buy(symbol, quantity, get_share_price)
        return actualizar_estado()
    except ValueError:
        return "Cantidad inválida", "", "", "", ""
    except InsufficientFundsError:
        return "Fondos insuficientes", "", "", "", ""

def vender(symbol, quantity):
    try:
        quantity = int(quantity)
        account.sell(symbol, quantity, get_share_price)
        return actualizar_estado()
    except ValueError:
        return "Cantidad inválida", "", "", "", ""
    except InsufficientSharesError:
        return "No tienes suficientes acciones", "", "", "", ""

with gr.Blocks() as demo:
    gr.Markdown("# Simulador de Trading Simple")

    with gr.Row():
        with gr.Column():
            deposito_input = gr.Number(label="Depositar")
            deposito_button = gr.Button("Depositar")

            retiro_input = gr.Number(label="Retirar")
            retiro_button = gr.Button("Retirar")

            simbolo_compra = gr.Text(label="Símbolo (AAPL, TSLA, GOOGL)")
            cantidad_compra = gr.Number(label="Cantidad a comprar")
            compra_button = gr.Button("Comprar")

            simbolo_venta = gr.Text(label="Símbolo (AAPL, TSLA, GOOGL)")
            cantidad_venta = gr.Number(label="Cantidad a vender")
            venta_button = gr.Button("Vender")

        with gr.Column():
            balance_output = gr.Number(label="Balance")
            holdings_output = gr.Textbox(label="Tenencias")
            portfolio_value_output = gr.Number(label="Valor del Portafolio")
            profit_loss_output = gr.Number(label="Ganancia/Pérdida")
            transactions_output = gr.Textbox(label="Transacciones")
            
    estado_inputs = [balance_output, holdings_output, portfolio_value_output, profit_loss_output, transactions_output]


    deposito_button.click(depositar, inputs=deposito_input, outputs=estado_inputs)
    retiro_button.click(retirar, inputs=retiro_input, outputs=estado_inputs)
    compra_button.click(comprar, inputs=[simbolo_compra, cantidad_compra], outputs=estado_inputs)
    venta_button.click(vender, inputs=[simbolo_venta, cantidad_venta], outputs=estado_inputs)
    
    demo.load(actualizar_estado, outputs=estado_inputs) # Cargar estado inicial

demo.launch()
