#!/usr/bin/env node

/* Para configurar el MCP server localmente
command: npx
args: /home/surtich/projects/Ampliaci-n-de-Entornos/21.MCP/21.d-typescript_mcp
*/

/* Para ejecutar en local
npx .
*/

/* Para ejecutar en remoto
nmm login
npm publish
command: npx
args: surtich-binancemcp
*/

// En TypeScript, usamos importaciones de módulos ES (similar a `from x import y` de Python)
// La extensión `.js` es obligatoria aquí aunque estemos en un archivo `.ts` - esta es una peculiaridad de TypeScript
import {
  McpServer,
  ResourceTemplate,
} from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
// zod es la librería de TypeScript para la comprobación de tipos en tiempo de ejecución, similar a los tipos de Python + comprobaciones en tiempo de ejecución
import { z } from "zod";
// Módulos incorporados de Node.js (como la biblioteca estándar de Python)
import fs from "fs";
import path from "path";

// Importar la versión de package.json
// Necesitamos usar require aquí porque las importaciones JSON necesitan una configuración especial de TypeScript
// eslint-disable-next-line @typescript-eslint/no-var-requires
const { version } = require("../package.json");

// __dirname es la forma de Node.js de obtener el directorio actual (similar a __file__ de Python)
// A diferencia de os.path.join de Python, path.join de Node.js maneja rutas multiplataforma automáticamente
const ACTIVITY_LOG_FILE = path.join(__dirname, "../../activity.log");

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

// Crear una instancia del servidor MCP, similar a FastMCP en Python
// TypeScript usa la sintaxis de objeto literal para la configuración (como los kwargs de Python)
const server = new McpServer({
  name: "Binance MCP",
  version, // Usando la versión de package.json (propiedad de objeto abreviada)
});

// Registro de herramientas en TypeScript, equivalente al decorador @mcp.tool() de Python
// En lugar de decoradores de funciones, usamos un patrón de llamada a método común en TypeScript
server.tool(
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
      // Las operaciones del sistema de archivos de Node.js son síncronas con el sufijo ...Sync
      // (a diferencia de Python donde síncrono es el predeterminado)
      fs.appendFileSync(
        ACTIVITY_LOG_FILE,
        `Error obteniendo el precio para ${resolvedSymbol}: ${response.status} ${errorText}\n`
      );
      throw new Error(
        `Error obteniendo el precio para ${resolvedSymbol}: ${response.status} ${errorText}`
      );
    }
    // TypeScript requiere una aserción de tipo (as any) aquí porque la estructura JSON
    // no se conoce en tiempo de compilación (Python no necesita esto)
    const data = (await response.json()) as any;
    const price = data.price;
    fs.appendFileSync(
      ACTIVITY_LOG_FILE,
      `Se obtuvo el precio para ${resolvedSymbol} con éxito. El precio actual es ${price}. La hora actual es ${new Date().toISOString()}\n`
    );
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

// Patrón similar para el endpoint de cambio de precio
server.tool(
  "get_price_price_change",
  { symbol: z.string() },
  async ({ symbol }) => {
    const resolvedSymbol = getSymbolFromName(symbol);
    const url = `https://data-api.binance.vision/api/v3/ticker/24hr?symbol=${resolvedSymbol}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(
        `Error obteniendo el cambio de precio para ${resolvedSymbol}: ${response.status}`
      );
    }
    const data = (await response.json()) as any;
    return { content: [{ type: "text", text: JSON.stringify(data) }] };
  }
);

// Registro de recursos, similar al manejo de recursos de FastMCP
// TypeScript requiere plantillas y definiciones de tipo más explícitas
server.resource(
  "file://activity.log",
  // ResourceTemplate es una clase de TypeScript que define la interfaz del recurso
  new ResourceTemplate("file://activity.log", { list: undefined }),
  async () => {
    // Patrón de Node.js: verificar la existencia antes de leer
    if (!fs.existsSync(ACTIVITY_LOG_FILE))
      return { contents: [{ uri: "file://activity.log", text: "" }] };
    const text = fs.readFileSync(ACTIVITY_LOG_FILE, "utf-8");
    return { contents: [{ uri: "file://activity.log", text }] };
  }
);

// Recurso dinámico con parámetros URL
// Similar a los recursos dinámicos de FastMCP pero con manejo de tipos explícito
server.resource(
  "resource://crypto_price/{symbol}",
  new ResourceTemplate("resource://crypto_price/{symbol}", { list: undefined }),
  // Los manejadores de recursos reciben URI y variables (como los parámetros de ruta de FastMCP)
  async (uri, variables) => {
    // Se necesita una aserción de tipo porque TypeScript no puede inferir el tipo de la plantilla
    const symbol = variables.symbol as string;
    const resolvedSymbol = getSymbolFromName(symbol);
    const url = `https://api.binance.com/api/v3/ticker/price?symbol=${resolvedSymbol}`;
    const response = await fetch(url);
    if (!response.ok) {
      return {
        contents: [
          {
            uri: uri.href,
            text: `Error obteniendo el precio para ${resolvedSymbol}`,
          },
        ],
      };
    }
    const data = (await response.json()) as any;
    return {
      contents: [
        {
          uri: uri.href,
          text: `El precio actual de ${resolvedSymbol} es ${data.price}`,
        },
      ],
    };
  }
);

// Función principal de inicio del servidor
// TypeScript/Node.js típicamente usa async/await para el inicio (similar a `async main` de Python)
async function startServer() {
  // Asegurarse de que el archivo de registro exista (patrón de Node.js - Python usaría típicamente el modo 'a')
  if (!fs.existsSync(ACTIVITY_LOG_FILE)) {
    fs.writeFileSync(ACTIVITY_LOG_FILE, "");
  }
  // Crear instancia de transporte (equivalente a transport="stdio" en Python)
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`Servidor Binance MCP v${version} iniciado`);
  console.error("Herramientas: get_price, get_price_price_change");
  console.error(
    "Recursos: file://activity.log, resource://crypto_price/{symbol}"
  );
}

// Patrón de manejo de errores en Node.js
// Similar a `if __name__ == "__main__"` de Python pero con manejo de errores de promesas
startServer().catch((err) => {
  console.error("Error al iniciar el servidor:", err);
  process.exit(1);
});
