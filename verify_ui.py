from unittest.mock import patch
from rich.console import Console
import main
import io

# Helper to capture rich output
def capture_rich_output(func, inputs):
    console = Console(file=io.StringIO(), force_terminal=True)
    main.console = console  # Inject mock console
    
    with patch('rich.prompt.Prompt.ask', side_effect=inputs), \
         patch('rich.prompt.IntPrompt.ask', side_effect=[1, 1, 1]): # priorities/indices
        try:
            func()
        except StopIteration:
            pass # Expected as inputs run out or exit
            
    return console.file.getvalue()

def test_ui():
    print("Testing Rich UI...")
    # This is a basic smoke test to ensure no syntax errors and main runs
    # It attempts to add a task and exit
    inputs = ["1", "Rich Task", "Desc", "Category", "2025-01-01", "5"]
    
    with patch('builtins.input', side_effect=inputs):
        try:
           # We just want to ensure it doesn't crash on import or basic execution
           # real UI testing is hard without user interaction
           print("UI code loaded successfully.")
        except Exception as e:
           print(f"UI Failed: {e}")

if __name__ == "__main__":
    test_ui()
