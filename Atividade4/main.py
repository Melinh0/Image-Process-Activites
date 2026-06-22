import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
IMAGES = BASE / "images"

Q1_OUT = BASE / "resultados_q1"
Q2_OUT = BASE / "resultados_q2"
Q3_OUT = BASE / "resultados_q3"

IMG1 = IMAGES / "imagem1.jpeg"
IMG2 = IMAGES / "imagem2.jpeg"
IMG3 = IMAGES / "imagem3.jpeg"

def run(cmd):
    print(f'\n$ {" ".join(str(c) for c in cmd)}')
    subprocess.run([str(c) for c in cmd], check=True)

def main():
    for d in [Q1_OUT, Q2_OUT, Q3_OUT]:
        d.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("QUESTAO 1 - Morfologia Matematica")
    print("=" * 60)
    run([
        sys.executable, BASE / "questao1_morfologia.py",
        "--inputs", IMG1, IMG2,
        "--outdir", Q1_OUT
    ])

    print("\n" + "=" * 60)
    print("QUESTAO 2 - Canny (passos iniciais) e HOG")
    print("=" * 60)
    run([
        sys.executable, BASE / "questao2_canny_hog.py",
        "--input", IMG3,
        "--outdir", Q2_OUT
    ])

    print("\n" + "=" * 60)
    print("QUESTAO 3 - Watershed com marcadores")
    print("=" * 60)
    run([
        sys.executable, BASE / "questao3_watershed.py",
        "--input", IMG3,
        "--outdir", Q3_OUT
    ])

    print("\n" + "=" * 60)
    print("Todas as questoes processadas com sucesso!")
    print(f"Resultados Q1: {Q1_OUT}")
    print(f"Resultados Q2: {Q2_OUT}")
    print(f"Resultados Q3: {Q3_OUT}")
    print("=" * 60)

if __name__ == "__main__":
    main()