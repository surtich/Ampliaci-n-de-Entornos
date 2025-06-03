Este proyecto se ha creado con:

```bash
docker run -it --rm -v "$PWD":/app -w /app -u $(id -u):$(id -g) node:20-bookworm npm create cloudflare@latest -- my-cloud-mcp-server-public  --template=cloudflare/ai/demos/remote-mcp-authless
``` 

Si se desea hacer sin docker: 

```bash
npm create cloudflare@latest -- my-cloud-mcp-server-public  --template=cloudflare/ai/demos/remote-mcp-authless
```

El fichero `src/index.ts` contiene el código del servidor MCP. Allí se definen las `tools` de forma similar a lo que habíamos hecho.


Para probar, ejecutar en `my-cloud-mcp-server-public`:
Atención se ha cambiado esto en el fichero `package.json` para que se ejecute el servidor en el puerto 8080 y para que escuche en todas las interfaces de red:

```json
{
	"scripts": {
		"start": "wrangler dev --ip=0.0.0.0 --port=8080"
	}
}
```

```bash
docker run -it --rm -v "$PWD":/app -w /app -u $(id -u):$(id -g) -p 8080:8080 node:20-bookworm npm start
``` 

Para conectarse al servidor MCP, se puede usar el mcp inspector.
Seleccionar Stremable HTTP y poner la URL del servidor MCP, que por defecto es `http://localhost:8080/mcp`.

```bash
npx @modelcontextprotocol/inspector@latest
```

Para desplegar, primero hay que hacer login en Cloudflare (funciona si no se usa docker):

```bash
npx wrangler login
```

Si se usa docker, hay que generar un API token (en Cloudflare -> Profile -> API Tokens -> Create Token -> edit Cloudflare tokens)

Después de hacer login u obtener el token. En el dashboard de Cloudflare:

Compute workers -> Workers and Pages (pulsar simplemente, no hay que hacer nada más)

Para desplegar.

```bash
docker run -it --rm \
  -v "$PWD":/app \
  -w /app \
  -e CLOUDFLARE_API_TOKEN=tu_token_aqui \
  node:20-bookworm \
  npx wrangler deploy
``` 

# Building a Remote MCP Server on Cloudflare (Without Auth)

This example allows you to deploy a remote MCP server that doesn't require authentication on Cloudflare Workers.

## Get started:

[![Deploy to Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

This will deploy your MCP server to a URL like: `remote-mcp-server-authless.<your-account>.workers.dev/sse`

Alternatively, you can use the command line below to get the remote MCP Server created on your local machine:
```bash
npm create cloudflare@latest -- my-mcp-server --template=cloudflare/ai/demos/remote-mcp-authless
```

## Customizing your MCP Server

To add your own [tools](https://developers.cloudflare.com/agents/model-context-protocol/tools/) to the MCP server, define each tool inside the `init()` method of `src/index.ts` using `this.server.tool(...)`. 

## Connect to Cloudflare AI Playground

You can connect to your MCP server from the Cloudflare AI Playground, which is a remote MCP client:

1. Go to https://playground.ai.cloudflare.com/
2. Enter your deployed MCP server URL (`remote-mcp-server-authless.<your-account>.workers.dev/sse`)
3. You can now use your MCP tools directly from the playground!

## Connect Claude Desktop to your MCP server

You can also connect to your remote MCP server from local MCP clients, by using the [mcp-remote proxy](https://www.npmjs.com/package/mcp-remote). 

To connect to your MCP server from Claude Desktop, follow [Anthropic's Quickstart](https://modelcontextprotocol.io/quickstart/user) and within Claude Desktop go to Settings > Developer > Edit Config.

Update with this configuration:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "http://localhost:8787/sse"  // or remote-mcp-server-authless.your-account.workers.dev/sse
      ]
    }
  }
}
```

Restart Claude and you should see the tools become available. 
