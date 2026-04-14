from pathlib import Path
from Questao1 import pencil_sketch
from Questao2 import gamma_correction
from Questao3 import weighted_blend
from Questao4 import apply_all_transformations
from Questao5 import create_mosaic
from Questao6 import quantize

def main():
    base_path = Path("images")
    img1 = base_path / "imagem1.jpeg"
    img2 = base_path / "imagem2.jpeg"
    img3 = base_path / "imagem3.jpeg"
    img4 = base_path / "imagem4.jpeg"

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Executando Questão 1: Esboço a lápis...")
    sketch_output = output_dir / "questao1_sketch.jpg"
    pencil_sketch(str(img1), str(sketch_output), kernel_size=21, sigma=5)
    print(f"  -> Salvo em {sketch_output}")

    print("Executando Questão 2: Correção gama...")
    gammas = [0.5, 1.0, 1.5, 2.0, 2.5]
    for gamma in gammas:
        gamma_output = output_dir / f"questao2_gamma_{gamma}.jpg"
        gamma_correction(str(img2), str(gamma_output), gamma)
        print(f"  -> Gamma {gamma} salvo em {gamma_output}")

    print("Executando Questão 3: Média ponderada...")
    alphas = [0.3, 0.5, 0.7]
    for alpha in alphas:
        blend_output = output_dir / f"questao3_blend_alpha_{alpha}.jpg"
        weighted_blend(str(img1), str(img2), str(blend_output), alpha)
        print(f"  -> Alpha {alpha} salvo em {blend_output}")

    print("Executando Questão 4: Transformações sequenciais...")
    trans_output = output_dir / "questao4_transformed.jpg"
    apply_all_transformations(str(img3), str(trans_output))
    print(f"  -> Salvo em {trans_output}")

    print("Executando Questão 5: Mosaico 4x4...")
    mosaic_output = output_dir / "questao5_mosaic.jpg"
    create_mosaic(str(img4), str(mosaic_output), block_size=4)
    print(f"  -> Salvo em {mosaic_output}")

    print("Executando Questão 6: Quantização...")
    niveis = [256, 64, 32, 16, 8, 4, 2]
    for levels in niveis:
        quant_output = output_dir / f"questao6_quant_{levels}levels.jpg"
        quantize(str(img1), str(quant_output), levels)
        print(f"  -> {levels} níveis salvo em {quant_output}")

    print("\nTodas as questões foram processadas com sucesso!")

if __name__ == "__main__":
    main()