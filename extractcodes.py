import sys
from pathlib import Path

SCRIPT_NAME = Path(__file__).name
OUTPUT_FILE = "compiladomobat.txt"
IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "env", ".idea", ".vscode", "dist", "build"}

def should_skip_file(file_path: Path, target_root: Path) -> bool:
    if file_path.name == SCRIPT_NAME:
        return True
    if file_path.name == OUTPUT_FILE:
        return True
    if any(part in IGNORE_DIRS for part in file_path.parts):
        return True
    if file_path.suffix.lower() != '.py':
        return True
    return False

def read_file_content(file_path: Path) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except (UnicodeDecodeError, OSError):
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception as e:
            return f"[Erro ao ler arquivo: {e}]"

def main():
    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1]).resolve()
        if not target_dir.is_dir():
            print(f"Erro: '{target_dir}' não é um diretório válido.")
            sys.exit(1)
    else:
        target_dir = Path.cwd().resolve()

    print(f"Extraindo arquivos .py de: {target_dir}")

    output_path = Path.cwd() / OUTPUT_FILE   # Salva no diretório onde o script foi executado

    with open(output_path, "w", encoding="utf-8") as out:
        for file_path in target_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if should_skip_file(file_path, target_dir):
                continue

            rel_path = file_path.relative_to(target_dir)
            content = read_file_content(file_path)

            out.write(f"{'=' * 80}\n")
            out.write(f"ARQUIVO: {rel_path}\n")
            out.write(f"{'=' * 80}\n")
            out.write(content)
            out.write("\n\n")

    print(f"Compilado salvo em: {output_path}")

if __name__ == "__main__":
    main()