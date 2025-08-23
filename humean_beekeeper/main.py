import sys
import os

# Add project root to path before other imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from humean_beekeeper.beekeeper_operator import BeekeeperOperator

def main():
    """
    Main entry point for the Humean Beekeeper.
    Runs one cycle of the observe-decide-act loop.
    """
    print("--- 🐝 Initializing the Humean Beekeeper 🐝 ---")
    operator = BeekeeperOperator()
    operator.run_once()
    print("\n--- 🐝 Humean Beekeeper cycle complete 🐝 ---")

if __name__ == "__main__":
    main()
