import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

print("Verifying imports...")

try:
    from core import models, geometry, camera
    print("Imported core modules")
    
    from rendering import renderer, shader
    print("Imported rendering modules")
    
    from shapes import equation, primitive
    print("Imported shapes modules")
    
    from app import window, config
    print("Imported app modules")
    
    from utils import math
    print("Imported utils modules")
    
    print("All imports successful!")
except Exception as e:
    print(f"Import failed: {e}")
    sys.exit(1)
