import sys
import os

# Añadir la carpeta raíz al PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from main.app import main  

if __name__ == "__main__":
    main()