from langchain_core.tools import tool

@tool
def python_repl(code: str) -> str:
    """
    A Python shell. Use this to execute python commands. 
    Input should be a valid python command. 
    If you want to see the output of a value, you should print it out with `print(...)`.
    """
    import sys
    from io import StringIO
    
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    
    try:
        # Provide a safe-ish environment
        exec(code, {"__builtins__": __builtins__}, {})
        sys.stdout = old_stdout
        output = mystdout.getvalue()
        return output if output else "Executed successfully with no output."
    except Exception as e:
        sys.stdout = old_stdout
        return f"Failed to execute. Error: {repr(e)}"
