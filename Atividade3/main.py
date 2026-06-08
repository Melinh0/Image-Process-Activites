import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
IMAGES = BASE / "images"
Q1_OUT = BASE / "resultados_q1"
Q2_OUT = BASE / "resultados_q2"

IMG1 = Path(r"images\imagem1.jpeg")
IMG2 = Path(r"images\imagem2.jpeg")

def run(cmd):
    print(f'\n$ {" ".join(str(c) for c in cmd)}')
    result = subprocess.run([str(c) for c in cmd], check=True)
    return result

def main():
    for d in [Q1_OUT, Q2_OUT]:
        d.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("QUESTAO 1 - Compressao DCT estilo JPEG")
    print("=" * 60)
    run([
        sys.executable, BASE / "questao1_dct.py",
        "--input", IMG1,
        "--outdir", Q1_OUT
    ])

    print("\n" + "=" * 60)
    print("QUESTAO 2 - Descritores de Imagem")
    print("=" * 60)
    run([
        sys.executable, BASE / "questao2_descritores.py",
        "--inputs", IMG1, IMG2,
        "--labels", "imagem1", "imagem2",
        "--outdir", Q2_OUT
    ])

    print("\n" + "=" * 60)
    print("Todas as questoes processadas com sucesso!")
    print(f"Resultados Q1: {Q1_OUT}")
    print(f"Resultados Q2: {Q2_OUT}")
    print("=" * 60)

if __name__ == "__main__":
    main()