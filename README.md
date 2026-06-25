# Claude Code CLI

A small RAG-powered CLI for asking questions about a codebase.

It indexes source files, stores searchable chunks in a vector database, and lets an LLM answer questions using the retrieved code context.

## What It Does

- Parses code into chunks using Tree-sitter.
- Uses line-based chunks for files like Markdown, YAML, JSON, and TOML.
- Stores chunks in Qdrant or Chroma.
- Supports hybrid Qdrant retrieval: dense semantic search + sparse BM25-style search.
- Exposes a CLI command:

```bash
claude-code-cli
```

## Setup

Install dependencies with `uv`:

```bash
make sync
```

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_key_here
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
```

## Run Locally

Run from this repo with `uv`:

```bash
make run-local
```

Install/reinstall the CLI globally with `pipx`, then run it inside `sample_project`:

```bash
make run
```

After code changes, reinstall the global CLI:

```bash
make pipx-reinstall
```

## CLI Commands

Inside the CLI:

```text
/ask <question>
/show_semantic_index
/exit
```

Example:

```text
/ask where is hybrid retrieval implemented?
```

## Useful Make Commands

```bash
make sync            # install/update local uv environment
make run             # reinstall pipx CLI and run it in sample_project
make run-local       # run locally with uv
make pipx-reinstall  # update global pipx install
make check           # compile-check source files
make clean           # remove __pycache__ folders
```

## Notes

If you switch an existing Qdrant collection from semantic-only to hybrid mode, you may need to recreate the collection and re-index. Hybrid mode needs both dense and sparse vectors, while older semantic-only collections only have dense vectors.
