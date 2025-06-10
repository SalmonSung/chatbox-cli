# chatbox-cli  
chatbox-cli is a command-line interface tool for interacting with LangGraph. It offers seamless support for `interrupt` and resuming graph execution, making it easy to manage your workflows directly from the terminal.
> [!Note]  
> This is a demo version. While all functions work, the codebase is not yet production-ready.

## Features
- Easy CLI interface for running LangGraph-based workflows.  
- Interrupt and resume graph execution effortlessly.
- Easily customizable: implement your own graph logic by replacing `chatbox/core/graph.py`.
## Installation  
To install chatbox-cli in editable (development) mode, run:
```bash
pip install -e .
#or
python -m pip install -e .
```  
After installation, you can launch the CLI tool using one of the following commands:  
```bash
python -m src.chatbox.cli.main chat
chatbox chat
```
