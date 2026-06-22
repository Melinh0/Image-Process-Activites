import json
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent
ATIV1_DIR = REPO_ROOT / "Atividade1"
ATIV2_DIR = REPO_ROOT / "Atividade2"
ATIV3_DIR = REPO_ROOT / "Atividade3"
ATIV4_DIR = REPO_ROOT / "Atividade4"

OUTPUTS_ATIV1 = ATIV1_DIR / "outputs"
RES_Q1_ATIV2 = ATIV2_DIR / "resultados_q1"
RES_Q2_ATIV2 = ATIV2_DIR / "resultados_q2"
RES_Q1_ATIV3 = ATIV3_DIR / "resultados_q1"
RES_Q2_ATIV3 = ATIV3_DIR / "resultados_q2"
RES_Q1_ATIV4 = ATIV4_DIR / "resultados_q1"
RES_Q2_ATIV4 = ATIV4_DIR / "resultados_q2"
RES_Q3_ATIV4 = ATIV4_DIR / "resultados_q3"

def caminho_relativo(absolute_path: Path) -> str:
    return str(absolute_path.relative_to(REPO_ROOT)).replace("\\", "/")

def listar_imagens(diretorio: Path, padrao: str = "*.jpg") -> list[Path]:
    if not diretorio.exists():
        return []
    return sorted(diretorio.glob(padrao))

def carregar_json(caminho: Path) -> dict:
    if not caminho.exists():
        return {}
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def gerar_readme() -> None:
    print("📝 Gerando README.md...")

    readme = f"""# 🖼️ Image-Process-Activites

Repositório com implementações de técnicas de **Processamento Digital de Imagens** desenvolvidas como atividades acadêmicas. Os experimentos abrangem filtragem espacial e em frequência, transformada DCT, compressão estilo JPEG, descritores de imagem, mosaico, quantização, morfologia matemática, detecção de bordas, HOG e segmentação por watershed.

**Data de geração do relatório:** {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}

---

## 📁 Estrutura do Repositório

- `Atividade1/` – Operações básicas (esboço a lápis, correção gama, blend, mosaico, quantização)
- `Atividade2/` – Filtros espaciais (convolução) e filtragem no domínio da frequência (FFT)
- `Atividade3/` – Compressão DCT (JPEG simplificado) e descritores estatísticos de imagem
- `Atividade4/` – Morfologia matemática, Canny (gradiente), HOG e segmentação por watershed

---

"""

    readme += """## 📌 Atividade 1 – Operações Fundamentais

"""
    readme += """Foram implementadas seis tarefas utilizando imagens do diretório `images/`. Os resultados gerados estão na pasta `Atividade1/outputs/`.

"""

    readme += """### 🖍️ Questão 1 – Esboço a Lápis

"""
    sketch = OUTPUTS_ATIV1 / "questao1_sketch.jpg"
    if sketch.exists():
        readme += f"""![Esboço]({caminho_relativo(sketch)})

"""
    else:
        readme += """*Imagem não encontrada. Execute `main.py` da Atividade1 para gerar.*

"""

    readme += """### 📈 Questão 2 – Correção Gama

"""
    gammas = [0.5, 1.0, 1.5, 2.0, 2.5]
    imgs_gamma = [OUTPUTS_ATIV1 / f"questao2_gamma_{g}.jpg" for g in gammas]
    for g, img in zip(gammas, imgs_gamma):
        if img.exists():
            readme += f"""- **γ = {g}**:  
  ![Gamma {g}]({caminho_relativo(img)})
"""
        else:
            readme += f"""- γ = {g}: (imagem não disponível)
"""
    readme += """
"""

    readme += """### 🎚️ Questão 3 – Média Ponderada (Blend)

"""
    alphas = [0.3, 0.5, 0.7]
    imgs_blend = [OUTPUTS_ATIV1 / f"questao3_blend_alpha_{a}.jpg" for a in alphas]
    for a, img in zip(alphas, imgs_blend):
        if img.exists():
            readme += f"""- **α = {a}**:  
  ![Blend α={a}]({caminho_relativo(img)})
"""
        else:
            readme += f"""- α = {a}: (não disponível)
"""
    readme += """
"""

    readme += """### 🔄 Questão 4 – Transformações Sequenciais

"""
    trans = OUTPUTS_ATIV1 / "questao4_transformed.jpg"
    if trans.exists():
        readme += f"""![Transformações]({caminho_relativo(trans)})

"""
    else:
        readme += """*Imagem não encontrada.*

"""

    readme += """### 🧩 Questão 5 – Mosaico 4×4

"""
    mosaic = OUTPUTS_ATIV1 / "questao5_mosaic.jpg"
    if mosaic.exists():
        readme += f"""![Mosaico]({caminho_relativo(mosaic)})

"""
    else:
        readme += """*Imagem não encontrada.*

"""

    readme += """### 🎨 Questão 6 – Quantização

"""
    niveis = [256, 64, 32, 16, 8, 4, 2]
    imgs_quant = [OUTPUTS_ATIV1 / f"questao6_quant_{n}levels.jpg" for n in niveis]
    for n, img in zip(niveis, imgs_quant):
        if img.exists():
            readme += f"""- **{n} níveis**:  
  ![Quantização {n}]({caminho_relativo(img)})
"""
        else:
            readme += f"""- {n} níveis: (não disponível)
"""
    readme += """---
"""

    readme += """## 🧪 Atividade 2 – Filtros Espaciais e Frequência

"""
    readme += """### 🔍 Questão 1 – Filtros Espaciais (Convolução Manual)

"""
    readme += """Foram aplicados 11 kernels diferentes sobre a imagem `imagem2.jpeg`. Os resultados estão na pasta `Atividade2/resultados_q1/`.

"""
    filtros = ["h1", "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "h11"]
    nomes = [
        "Média 3x3", "Gaussiano 5x5", "Sobel horizontal", "Sobel vertical",
        "Prewitt horizontal", "Prewitt vertical", "Laplaciano (centro 4)",
        "Laplaciano (centro 5)", "Emboss", "Média 5x5", "Unsharp masking"
    ]
    json_q1 = carregar_json(RES_Q1_ATIV2 / "resultados_q1.json")
    for fname, nome in zip(filtros, nomes):
        img = RES_Q1_ATIV2 / f"q1_{fname}.png"
        if img.exists():
            minv = json_q1.get(fname, {}).get("min", "?")
            maxv = json_q1.get(fname, {}).get("max", "?")
            meanv = json_q1.get(fname, {}).get("mean", "?")
            legenda = f"{nome} (min={minv:.1f}, max={maxv:.1f}, média={meanv:.1f})"
            readme += f"""**{fname} – {nome}**  
"""
            readme += f"""![{fname}]({caminho_relativo(img)})
"""
            readme += f"""*{legenda}*

"""
        else:
            readme += f"""- {fname}: resultado não encontrado
"""
    readme += """
"""

    readme += """### 🌐 Questão 2 – Filtragem no Domínio da Frequência (FFT)

"""
    readme += """A imagem `imagem3.jpeg` foi transformada via FFT 2D e submetida a máscaras ideais. Os resultados estão em `Atividade2/resultados_q2/`.

"""
    fft_img = RES_Q2_ATIV2 / "00_fft" / "fft_espectro_centralizado.png"
    if fft_img.exists():
        readme += """#### Espectro de Fourier

"""
        readme += f"""![Espectro FFT]({caminho_relativo(fft_img)})

"""
    readme += """#### Filtros Passa‑Baixa e Passa‑Alta

"""
    for tipo, label in [("passabaixa", "Passa‑Baixa"), ("passaalta", "Passa‑Alta")]:
        for r in [15, 30, 60]:
            mask = RES_Q2_ATIV2 / "01_masks" / f"mask_{tipo}_r{r}.png"
            result = RES_Q2_ATIV2 / "02_filtradas" / f"filtro_{tipo}_r{r}.png"
            if mask.exists() and result.exists():
                readme += f"""**{label} – raio = {r}**  
"""
                readme += f"""Máscara: ![Mask]({caminho_relativo(mask)})  
"""
                readme += f"""Resultado: ![Resultado]({caminho_relativo(result)})

"""
            else:
                readme += f"""*{label} r={r}: arquivos não encontrados*

"""
    readme += """#### Filtros Passa‑Faixa e Rejeita‑Faixa

"""
    for r1, r2 in [(10, 30), (20, 50)]:
        for ft, nome in [("passafaixa", "Passa‑Faixa"), ("rejeitafaixa", "Rejeita‑Faixa")]:
            mask = RES_Q2_ATIV2 / "01_masks" / f"mask_{ft}_r{r1}_{r2}.png"
            result = RES_Q2_ATIV2 / "02_filtradas" / f"filtro_{ft}_r{r1}_{r2}.png"
            if mask.exists() and result.exists():
                readme += f"""**{nome} – {r1}‑{r2}**  
"""
                readme += f"""Máscara: ![Mask]({caminho_relativo(mask)})  
"""
                readme += f"""Resultado: ![Resultado]({caminho_relativo(result)})

"""
            else:
                readme += f"""*{nome} ({r1}‑{r2}): arquivos não encontrados*

"""
    readme += """#### Compressão por Percentil da FFT

"""
    json_q2 = carregar_json(RES_Q2_ATIV2 / "resultados_questao2.json")
    compress_data = json_q2.get("compressao", [])
    if compress_data:
        readme += """| Percentil | Limiar | Coef. mantidos | Taxa de zeros |
"""
        readme += """|-----------|--------|----------------|---------------|
"""
        for comp in compress_data:
            pct = comp.get("percentil", "?")
            limiar = comp.get("limiar", "?")
            mantidos = comp.get("coeficientes_mantidos", "?")
            taxa = comp.get("taxa_zerados", 0) * 100
            readme += f"""| {pct}% | {limiar:.1f} | {mantidos} | {taxa:.1f}% |
"""
        readme += """
"""
    for pct in [70, 85, 95]:
        img_comp = RES_Q2_ATIV2 / "03_compressao" / f"compressao_percentil_{pct}.png"
        if img_comp.exists():
            readme += f"""**Compressão {pct}%**  
"""
            readme += f"""![Compressão {pct}%]({caminho_relativo(img_comp)})

"""
        else:
            readme += f"""*Imagem compressão {pct}% não encontrada*

"""
    hist_comp = RES_Q2_ATIV2 / "04_histogramas" / "comparativo_histogramas.png"
    if hist_comp.exists():
        readme += """#### Histogramas Comparativos

"""
        readme += f"""![Histogramas]({caminho_relativo(hist_comp)})

"""
    readme += """---
"""

    readme += """## 🗜️ Atividade 3 – Compressão DCT e Descritores de Imagem

"""
    readme += """### 📷 Questão 1 – Compressão DCT (estilo JPEG)

"""
    readme += """A imagem `imagem1.jpeg` foi dividida em blocos 8×8, transformada por DCT 2D manual, quantizada com matriz JPEG padrão e reconstruída. Os resultados estão em `Atividade3/resultados_q1/`.

"""
    orig_gray = RES_Q1_ATIV3 / "original_gray.png"
    if orig_gray.exists():
        readme += """#### Imagem original (tons de cinza)

"""
        readme += f"""![Original gray]({caminho_relativo(orig_gray)})

"""
    readme += """#### Imagens reconstruídas para diferentes `q_scale`

"""
    q_labels = ["0_5", "1_0", "2_0", "4_0", "8_0"]
    q_names = ["0.5 (alta qualidade)", "1.0 (padrão JPEG)", "2.0", "4.0", "8.0 (alta compressão)"]
    stats_dct = carregar_json(RES_Q1_ATIV3 / "resultados_q1.json")
    for tag, nome in zip(q_labels, q_names):
        rec_img = RES_Q1_ATIV3 / f"reconstruida_q{tag}.png"
        diff_img = RES_Q1_ATIV3 / f"diferenca_q{tag}.png"
        psnr = stats_dct.get(tag, {}).get("psnr", "-")
        mae = stats_dct.get(tag, {}).get("mae", "-")
        readme += f"""**q_scale = {nome}** (PSNR = {psnr} dB, MAE = {mae})  
"""
        if rec_img.exists():
            readme += f"""![Reconstruída {nome}]({caminho_relativo(rec_img)})  
"""
        if diff_img.exists():
            readme += f"""![Diferença {nome}]({caminho_relativo(diff_img)})  
"""
        readme += """
"""

    readme += """### 📊 Questão 2 – Descritores Estatísticos e Estruturais

"""
    readme += """Foram calculados média, variância, desvio padrão, energia, entropia e variação espacial para as imagens `imagem1.jpeg` e `imagem2.jpeg`. Os gráficos estão em `Atividade3/resultados_q2/`.

"""
    comp_visual = RES_Q2_ATIV3 / "comparativo_imagens.png"
    if comp_visual.exists():
        readme += """#### Comparação visual com descritores

"""
        readme += f"""![Comparativo imagens]({caminho_relativo(comp_visual)})

"""
    gray1 = RES_Q2_ATIV3 / "gray_imagem1.png"
    gray2 = RES_Q2_ATIV3 / "gray_imagem2.png"
    if gray1.exists() or gray2.exists():
        readme += """#### Imagens em tons de cinza utilizadas

"""
        if gray1.exists():
            readme += f"""![gray_imagem1]({caminho_relativo(gray1)})  
"""
        if gray2.exists():
            readme += f"""![gray_imagem2]({caminho_relativo(gray2)})  
"""
        readme += """
"""
    hist_ativ3 = RES_Q2_ATIV3 / "histogramas_comparativos.png"
    if hist_ativ3.exists():
        readme += """#### Histogramas comparativos

"""
        readme += f"""![Histogramas Atividade3]({caminho_relativo(hist_ativ3)})

"""
    radar = RES_Q2_ATIV3 / "radar_descritores.png"
    if radar.exists():
        readme += """#### Gráfico radar dos descritores normalizados

"""
        readme += f"""![Radar descritores]({caminho_relativo(radar)})

"""
    desc_json = carregar_json(RES_Q2_ATIV3 / "resultados_q2.json")
    if desc_json:
        readme += """#### Tabela de Descritores

"""
        readme += """| Descritor | imagem1 | imagem2 |
"""
        readme += """|-----------|---------|---------|
"""
        for chave, rotulo in [
            ("mean", "Média"),
            ("variance", "Variância"),
            ("std", "Desvio padrão"),
            ("energy", "Energia"),
            ("entropy", "Entropia (bits)"),
            ("spatial_variation_total", "Variação espacial total")
        ]:
            v1 = desc_json.get("imagem1", {}).get(chave, "-")
            v2 = desc_json.get("imagem2", {}).get(chave, "-")
            readme += f"""| {rotulo} | {v1} | {v2} |
"""
        readme += """
"""
    readme += """---
"""

    readme += """## 🧬 Atividade 4 – Morfologia, Gradiente, HOG e Watershed

"""
    readme += """### 🧩 Questão 1 – Operações Morfológicas

"""
    readme += """Foram aplicadas erosão, dilatação, abertura e fechamento em imagens binárias (limiarizadas) com elementos estruturantes de tamanhos 3, 5 e 15. Os resultados estão em `Atividade4/resultados_q1/`.

"""
    stats_q1_at4 = carregar_json(RES_Q1_ATIV4 / "resultados_q1.json")
    for img_name, res in stats_q1_at4.items():
        readme += f"""#### Imagem: {img_name}

"""
        for se_size, paths in res.items():
            readme += f"""**SE = {se_size}**  
"""
            for op, path in paths.items():
                if Path(path).exists():
                    readme += f"""{op.capitalize()}: ![Imagem]({caminho_relativo(Path(path))})  
"""
            readme += """
"""

    readme += """### 📐 Questão 2 – Canny (Gradiente) e HOG

"""
    readme += """Foram implementados: suavização gaussiana, cálculo do gradiente com Sobel (magnitude e orientação) e descritor HOG com células 8×8 e 9 bins. Os resultados estão em `Atividade4/resultados_q2/`.

"""
    orig_q2 = RES_Q2_ATIV4 / "original.png"
    if orig_q2.exists():
        readme += """#### Imagem original

"""
        readme += f"""![Original]({caminho_relativo(orig_q2)})

"""
    suav_q2 = RES_Q2_ATIV4 / "suavizada_gauss.png"
    if suav_q2.exists():
        readme += """#### Suavização Gaussiana

"""
        readme += f"""![Suavizada]({caminho_relativo(suav_q2)})

"""
    mag_q2 = RES_Q2_ATIV4 / "magnitude_visual.png"
    if mag_q2.exists():
        readme += """#### Magnitude do gradiente

"""
        readme += f"""![Magnitude]({caminho_relativo(mag_q2)})

"""
    hog_q2 = RES_Q2_ATIV4 / "hog_visualizacao.png"
    if hog_q2.exists():
        readme += """#### Visualização HOG

"""
        readme += f"""![HOG]({caminho_relativo(hog_q2)})

"""
    stats_q2_at4 = carregar_json(RES_Q2_ATIV4 / "resultados_q2.json")
    if stats_q2_at4:
        readme += f"""**Dimensão do histograma:** {stats_q2_at4.get('histogram_shape', 'N/A')}  
"""
        readme += f"""**Número de características:** {stats_q2_at4.get('histogram_shape', [0,0,0])[0] * stats_q2_at4.get('histogram_shape', [0,0,0])[1] * stats_q2_at4.get('histogram_shape', [0,0,0])[2]}

"""

    readme += """### 🚰 Questão 3 – Segmentação por Watershed

"""
    readme += """A segmentação utilizou marcadores obtidos a partir da transformada de distância sobre imagem binária limpa (abertura+fechamento). Os resultados estão em `Atividade4/resultados_q3/`.

"""
    bin_q3 = RES_Q3_ATIV4 / "binaria.png"
    if bin_q3.exists():
        readme += """#### Imagem binária

"""
        readme += f"""![Binária]({caminho_relativo(bin_q3)})

"""
    clean_q3 = RES_Q3_ATIV4 / "limpa.png"
    if clean_q3.exists():
        readme += """#### Imagem limpa (após abertura+fechamento)

"""
        readme += f"""![Limpa]({caminho_relativo(clean_q3)})

"""
    dist_q3 = RES_Q3_ATIV4 / "distancia.png"
    if dist_q3.exists():
        readme += """#### Transformada de distância

"""
        readme += f"""![Distância]({caminho_relativo(dist_q3)})

"""
    markers_q3 = RES_Q3_ATIV4 / "marcadores.png"
    if markers_q3.exists():
        readme += """#### Marcadores (máximos locais)

"""
        readme += f"""![Marcadores]({caminho_relativo(markers_q3)})

"""
    ws_q3 = RES_Q3_ATIV4 / "watershed_resultado.png"
    if ws_q3.exists():
        readme += """#### Resultado da watershed (linhas de separação)

"""
        readme += f"""![Watershed]({caminho_relativo(ws_q3)})

"""
    overlay_q3 = RES_Q3_ATIV4 / "segmentacao_overlay.png"
    if overlay_q3.exists():
        readme += """#### Sobreposição na imagem original

"""
        readme += f"""![Overlay]({caminho_relativo(overlay_q3)})

"""
    stats_q3_at4 = carregar_json(RES_Q3_ATIV4 / "resultados_q3.json")
    if stats_q3_at4:
        readme += f"""**Número de marcadores encontrados:** {stats_q3_at4.get('num_markers', 'N/A')}

"""

    readme += """---
"""

    readme_path = REPO_ROOT / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"✅ README.md gerado com sucesso em {readme_path}")

if __name__ == "__main__":
    gerar_readme()