import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// Función TypeScript con anotación de tipo (similar a las sugerencias de tipo de Python)
// El `: string` después del parámetro y antes del bloque es la anotación del tipo de retorno
function getSymbolFromName(name: string): string {
  if (["bitcoin", "btc"].includes(name.toLowerCase())) return "BTCUSDT";
  if (["ethereum", "eth"].includes(name.toLowerCase())) return "ETHUSDT";
  // Operador ternario de TypeScript - como `x if condition else y` de Python
  // La comprobación de tipo explícita es necesaria porque TypeScript es más estricto con los tipos
  return typeof name === "string"
    ? name.toUpperCase()
    : String(name).toUpperCase();
}

// Define our MCP agent with tools
export class MyMCP extends McpAgent {
  server = new McpServer({
    name: "Crypto Price MCP",
    version: "1.0.0",
  });

  async init() {
    // Simple addition tool
    this.server.tool(
      "add",
      { a: z.number(), b: z.number() },
      async ({ a, b }) => ({
        content: [{ type: "text", text: String(a + b) }],
      })
    );

    // Registro de herramientas en TypeScript, equivalente al decorador @mcp.tool() de Python
    // En lugar de decoradores de funciones, usamos un patrón de llamada a método común en TypeScript
    this.server.tool(
      // Nombre de la herramienta
      "get_price",
      // Esquema de parámetros usando zod (similar a las sugerencias de tipo de Python pero con validación en tiempo de ejecución)
      { symbol: z.string() },
      // Función de manejador asíncrono (similar a `async def` de Python)
      // La sintaxis de función de flecha es común en TypeScript: `({params}) => { body }`
      async ({ symbol }) => {
        const resolvedSymbol = getSymbolFromName(symbol);
        const url = `https://api.binance.com/api/v3/ticker/price?symbol=${resolvedSymbol}`;
        // fetch está incorporado en Node.js moderno (similar a requests.get de Python)
        const response = await fetch(url);
        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(
            `Error obteniendo el precio para ${resolvedSymbol}: ${response.status} ${errorText}`
          );
        }
        // TypeScript requiere una aserción de tipo (as any) aquí porque la estructura JSON
        // no se conoce en tiempo de compilación (Python no necesita esto)
        const data = (await response.json()) as any;
        const price = data.price;
        // El formato de respuesta de MCP es más explícito en TypeScript debido a la tipificación estática
        return {
          content: [
            {
              type: "text",
              text: `El precio actual de ${resolvedSymbol} es ${price}`,
            },
          ],
        };
      }
    );
  }
}

export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const url = new URL(request.url);

    if (url.pathname === "/sse" || url.pathname === "/sse/message") {
      return MyMCP.serveSSE("/sse").fetch(request, env, ctx);
    }

    if (url.pathname === "/mcp") {
      return MyMCP.serve("/mcp").fetch(request, env, ctx);
    }

    return new Response("Not found", { status: 404 });
  },
};
