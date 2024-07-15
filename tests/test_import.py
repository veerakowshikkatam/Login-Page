# # test_import.py
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


try:
    from source.subscribe import on_connect
    print("Import successful")
except ImportError as e:
    print(f"Import error: {e}")
