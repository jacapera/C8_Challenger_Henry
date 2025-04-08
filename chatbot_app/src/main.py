import os
from typing import List, Dict
import json
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import html2text
from rich.console import Console
from rich.markdown import Markdown
import time

# Cargar variables de entorno
load_dotenv()

# Configuración de clientes
groq_api_key = os.getenv("GROQ_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")
groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # Modelo actualizado de producción

console = Console()
h = html2text.HTML2Text()
h.ignore_links = True

class Chatbot:
    def __init__(self):
        self.conversation_history = []
        self.groq_headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }

    def search_internet(self, query: str) -> List[Dict]:
        """Realiza una búsqueda en internet usando Serper.dev"""
        headers = {
            "X-API-KEY": serper_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "q": query,
            "num": 5
        }
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=payload
        )
        return response.json().get('organic', [])[:5]

    def extract_text_from_url(self, url: str) -> str:
        """Extrae el texto principal de una URL"""
        try:
            response = requests.get(url, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remover scripts y estilos
            for script in soup(["script", "style"]):
                script.decompose()
                
            text = h.handle(str(soup))
            return text[:2000]  # Limitamos el texto para no sobrecargar el contexto
        except:
            return ""

    def stream_response(self, response):
        """Muestra la respuesta en streaming"""
        full_response = ""
        buffer = ""
        
        try:
            # Procesar la respuesta línea por línea
            for line in response.iter_lines():
                if line:
                    # Decodificar la línea y eliminar el prefijo "data: " si existe
                    try:
                        line = line.decode('utf-8')
                        if line.startswith("data: "):
                            line = line[6:]  # Eliminar el prefijo "data: "
                        
                        # Intentar parsear el JSON
                        if line.strip():
                            json_response = json.loads(line)
                            if 'choices' in json_response and len(json_response['choices']) > 0:
                                delta = json_response['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    content = delta['content']
                                    # Mostrar el contenido directamente
                                    print(content, end="")
                                    full_response += content
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        console.print(f"\n[bold red]Error procesando respuesta: {str(e)}[/bold red]")
                        continue
            
            print("\n")
            return full_response
            
        except Exception as e:
            console.print(f"\n[bold red]Error en stream_response: {str(e)}[/bold red]")
            return ""

    def chat(self, user_input: str):
        """Procesa la entrada del usuario y genera una respuesta"""
        try:
            # Agregar la entrada del usuario al historial
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Realizar búsqueda en internet
            console.print("\n[bold blue]Buscando información...[/bold blue]")
            search_results = self.search_internet(user_input)
            
            # Extraer texto de las URLs
            sources = []
            context = ""
            for result in search_results:
                url = result.get('link')
                if url:
                    text = self.extract_text_from_url(url)
                    if text:
                        context += f"\nFuente ({url}):\n{text}\n"
                        sources.append({"title": result.get('title', ''), "url": url})

            # Preparar el mensaje para el modelo
            system_message = {
                "role": "system",
                "content": """Eres un asistente útil que proporciona respuestas precisas basadas en la información proporcionada.
                Usa el contexto dado para responder las preguntas y cita las fuentes al final de tu respuesta.
                Responde siempre en español."""
            }
            
            context_message = {
                "role": "system",
                "content": f"Contexto de búsqueda:\n{context}"
            }
            
            messages = [system_message, context_message] + self.conversation_history[-5:]
            
            # Generar respuesta usando Groq API
            payload = {
                "model": groq_model,
                "messages": messages,
                "temperature": 0.7,
                "stream": True
            }
            
            console.print("\n[bold blue]Generando respuesta...[/bold blue]")
            
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=self.groq_headers,
                json=payload,
                stream=True
            )
            
            if response.status_code != 200:
                console.print(f"\n[bold red]Error en la API de Groq: {response.status_code}[/bold red]")
                console.print(f"Respuesta: {response.text}")
                return
            
            # Mostrar respuesta en streaming
            full_response = self.stream_response(response)
            
            if not full_response:
                console.print("\n[bold red]No se recibió respuesta del modelo[/bold red]")
                return
            
            # Agregar la respuesta al historial
            self.conversation_history.append({"role": "assistant", "content": full_response})
            
            # Mostrar fuentes
            if sources:
                console.print("\n[bold]Fuentes consultadas:[/bold]")
                for source in sources:
                    console.print(f"- {source['title']}: {source['url']}")
                    
        except Exception as e:
            console.print(f"\n[bold red]Error durante la ejecución: {str(e)}[/bold red]")

def main():
    console.print("[bold green]¡Bienvenido al Chatbot![/bold green]")
    console.print("Escribe 'salir' para terminar la conversación.\n")
    
    chatbot = Chatbot()
    
    while True:
        user_input = console.input("[bold cyan]Tú:[/bold cyan] ")
        
        if user_input.lower() == 'salir':
            console.print("\n[bold green]¡Hasta luego![/bold green]")
            break
            
        chatbot.chat(user_input)

if __name__ == "__main__":
    main()