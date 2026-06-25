import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
import chromadb


from config import config
from context.indexers.factory import get_indexer, get_index_inspector
from llm.factory import get_llm, get_embedder
from observability.logger import get_logger
from agent.orchestrator import handle_query




# Load .env before anything else
load_dotenv(find_dotenv(usecwd=True))


console = Console()
logger = get_logger(__name__)


def get_or_create_index():
   repo_path = str(Path.cwd())
   logger.info(f"Checking index for: {repo_path}")
   console.print(f"[dim]Checking index for {repo_path}...[/dim]")
   return get_indexer()(repo_path)


def initialize():
   """Bootstrap LLM, embedder, and index before the REPL starts."""
   llm = get_llm()
   embedder = get_embedder()
   console.print(f"[dim]LLM: {config['llm']['provider']} / {config['llm']['model']}[/dim]")
   console.print(f"[dim]Embedder: {config['embeddings']['provider']} / {config['embeddings']['model']}[/dim]")


   index = get_or_create_index()
   console.print(f"[green]✓ Ready[/green]\n")
   return llm, embedder, index


def show_agent_response(response: str) -> None:
   """Render the agent's final answer as a distinct CLI block."""
   console.print()
   console.print(Panel(
       Markdown(response),
       title="[bold green]Answer[/bold green]",
       border_style="green",
       padding=(1, 2),
   ))
   console.print()


def run():
   logger.info("Starting Educosys Claude")
   console.print("\n[bold blue]Educosys Claude[/bold blue] — RAG-powered code assistant")


   llm, embedder, index = initialize()
   console.print("Type [bold]'/exit'[/bold] to quit\n")


   while True:
       user_input = Prompt.ask("[bold green]>[/bold green]")


       if not user_input.strip():
           continue
       if user_input.lower() in ("/exit", "/quit"):
           logger.info("Shutting down")
           console.print("[dim]Goodbye![/dim]")
           break
       elif user_input.startswith("/ask "):
           question = user_input.removeprefix("/ask ").strip()
           logger.info(f"Ask command received: {question}")
           console.print(f"[dim]Searching for: {question}...[/dim]")
           response = handle_query(question)
           show_agent_response(response)
       elif user_input == "/show_semantic_index":
           logger.info("Showing semantic index")
           get_index_inspector()(index)
       else:
           logger.warning(f"Unknown command received: {user_input}")
           console.print("[yellow]Unknown command. Try:[/yellow]")
           console.print("  [bold]/ask <question>[/bold]       — ask a question about the codebase")
           console.print("  [bold]/show_semantic_index[/bold]  — show all chunks in the semantic index")


if __name__ == "__main__":
   run()
