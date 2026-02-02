import google.generativeai as genai
import sys

with open("debug_result.txt", "w") as f:
    f.write(f"Python Executable: {sys.executable}\n")
    f.write(f"Genai File: {genai.__file__}\n")
    try:
        f.write(f"Genai Version: {genai.__version__}\n")
    except:
        f.write("Genai Version: Not found\n")

    f.write(f"Genai Attributes: {dir(genai)}\n")

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        f.write("SUCCESS: GenerativeModel found.\n")
    except AttributeError:
        f.write("FAILURE: GenerativeModel not found.\n")
    except Exception as e:
        f.write(f"FAILURE: {e}\n")
