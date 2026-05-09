import json
from pathlib import Path
from datetime import datetime
from fpdf import FPDF
import io
import sys

def sanitize_text(text):
    replacements = {
        '\u2013': '-',
        '\u2014': '-',
        '\u2018': "'",
        '\u2019': "'",
        '\u201c': '"',
        '\u201d': '"',
        '\u2026': '...',
        '\u00e7': 'c',
        '\u00e1': 'a',
        '\u00e9': 'e',
        '\u00ed': 'i',
        '\u00f3': 'o',
        '\u00fa': 'u',
        '\u00e0': 'a',
        '\u00e2': 'a',
        '\u00ea': 'e',
        '\u00f4': 'o',
        '\u00fc': 'u',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.encode('latin-1', errors='replace').decode('latin-1')
    return text

BASE_DIR = Path(r"C:\Users\yagom\Documents\GitHub\Image-Process-Activites")
IMAGES_DIR = BASE_DIR / "images"
INPUT_IMAGE_Q1 = IMAGES_DIR / "imagem2.jpeg"
INPUT_IMAGE_Q2 = IMAGES_DIR / "imagem3.jpeg"
RESULTS_Q1_DIR = BASE_DIR / "Atividade2" / "resultados_q1"
RESULTS_Q2_DIR = BASE_DIR / "Atividade2" / "resultados_q2"
JSON_Q1 = RESULTS_Q1_DIR / "resultados_q1.json"
JSON_Q2 = RESULTS_Q2_DIR / "resultados_questao2.json"
OUTPUT_PDF = BASE_DIR / "Atividade2" / "reports" / "Relatorio_Atividade2.pdf"

class PDF(FPDF):
    def __init__(self, capture_sections=False):
        super().__init__()
        self.capture_sections = capture_sections
        self.section_pages = []
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Arial", "", 9)
            self.set_text_color(100, 100, 100)
            self.set_y(10)
            self.cell(0, 5, sanitize_text(f"{self.page_no()}"), align="R")
            self.set_text_color(0, 0, 0)
            self.ln(10)

    def footer(self):
        pass

    def section_title(self, title):
        self.ln(4)
        self.set_fill_color(220, 220, 220)
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, sanitize_text(title), border=0, ln=1, fill=True)
        self.ln(4)
        if self.capture_sections:
            self.section_pages.append((title, self.page_no()))

    def subsection_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, sanitize_text(title), ln=1)
        self.ln(2)

    def body_text(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 6, sanitize_text(text))
        self.ln(2)

    def add_single_image(self, img_path, caption="", width=120):
        if not Path(img_path).exists():
            self.set_font("Arial", "", 10)
            self.cell(0, 8, sanitize_text(f"Imagem não encontrada: {img_path}"), ln=1)
            return
        margin = 20
        img_height = width * 0.75
        needed = img_height + 20
        if self.get_y() + needed > 297 - margin:
            self.add_page()
        x = (210 - width) / 2
        self.image(str(img_path), x=x, w=width)
        self.ln(2)
        if caption:
            self.set_font("Arial", "I", 9)
            self.multi_cell(0, 5, sanitize_text(caption), align="C")
        self.ln(5)

    def image_grid(self, images, captions=None, cols=2, img_w=80, img_h=60):
        if captions is None:
            captions = [""] * len(images)
        spacing_x = 8
        spacing_y = 18
        total_width = cols * img_w + (cols - 1) * spacing_x
        start_x = (210 - total_width) / 2
        current_x = start_x
        current_y = self.get_y()

        for i, (img, cap) in enumerate(zip(images, captions)):
            if current_y + img_h + 25 > 270:
                self.add_page()
                current_y = self.get_y()
                current_x = start_x

            self.set_xy(current_x, current_y)
            if Path(img).exists():
                self.image(str(img), x=current_x, y=current_y, w=img_w, h=img_h)
            else:
                self.rect(current_x, current_y, img_w, img_h)
                self.set_xy(current_x, current_y + img_h / 2)
                self.set_font("Arial", "", 8)
                self.multi_cell(img_w, 4, sanitize_text("Imagem não encontrada"), align="C")

            self.set_xy(current_x, current_y + img_h + 2)
            self.set_font("Arial", "", 8)
            self.multi_cell(img_w, 4, sanitize_text(cap), align="C")

            current_x += img_w + spacing_x
            if (i + 1) % cols == 0:
                current_x = start_x
                current_y += img_h + spacing_y

        self.set_y(current_y + img_h + spacing_y)

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_content(pdf, is_capture_pass=False):
    pdf.add_page()
    pdf.section_title("1. Objetivo")
    pdf.body_text(
        "Este trabalho apresenta experimentos de processamento digital "
        "de imagens utilizando técnicas no domínio espacial e no domínio "
        "da frequência. Foram implementados filtros de suavização, "
        "realce e detecção de bordas utilizando convolução manual, além "
        "de filtros baseados na Transformada Rápida de Fourier (FFT). "
        "Também foi realizado um experimento de compressão de imagens "
        "por remoção de coeficientes de baixa magnitude."
    )

    pdf.add_page()
    pdf.section_title("2. Imagens Utilizadas")
    pdf.body_text(
        "As imagens utilizadas estão relacionadas ao tema moda. "
        "As figuras abaixo apresentam as duas imagens principais: "
        "a primeira (imagem2.jpeg) foi usada nos experimentos de "
        "filtragem espacial (Questão 1), e a segunda (imagem3.jpeg) "
        "foi usada nos experimentos de filtragem no domínio da frequência "
        "(Questão 2)."
    )
    images_originals = [str(INPUT_IMAGE_Q1), str(INPUT_IMAGE_Q2)]
    captions_originals = ["Imagem usada na Questão 1 (imagem2.jpeg)", 
                          "Imagem usada na Questão 2 (imagem3.jpeg)"]
    pdf.image_grid(images_originals, captions_originals, cols=2, img_w=80, img_h=60)

    pdf.add_page()
    pdf.section_title("3. Metodologia")
    pdf.body_text(
        "Na filtragem espacial foram utilizados kernels de convolução "
        "implementados manualmente. No domínio da frequência foi aplicada "
        "a FFT 2D, seguida da criação de máscaras ideais circulares "
        "passa-baixa, passa-alta, passa-faixa e rejeita-faixa."
    )

    pdf.add_page()
    pdf.section_title("4. Questão 1 – Filtros Espaciais")
    pdf.body_text(
        "Os filtros espaciais foram aplicados utilizando convolução "
        "manual sobre a imagem em escala de cinza (imagem2.jpeg)."
    )
    kernel_description = {
        "h1": "Média 3x3", "h2": "Gaussiano 5x5", "h3": "Sobel horizontal",
        "h4": "Sobel vertical", "h5": "Prewitt horizontal", "h6": "Prewitt vertical",
        "h7": "Laplaciano centro 4", "h8": "Laplaciano centro 5", "h9": "Emboss",
        "h10": "Média 5x5", "h11": "Unsharp masking"
    }
    stats_q1 = load_json(JSON_Q1)
    filters = ["h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11"]
    images_q1 = []
    captions_q1 = []
    for fname in filters:
        img_path = RESULTS_Q1_DIR / f"q1_{fname}.png"
        images_q1.append(str(img_path))
        captions_q1.append(
            f"{fname}\n{kernel_description[fname]}\n"
            f"min={stats_q1[fname]['min']:.1f} | max={stats_q1[fname]['max']:.1f}"
        )
    pdf.image_grid(images_q1, captions_q1, cols=3, img_w=55, img_h=45)

    pdf.subsection_title("4.1 Análise dos Filtros")
    pdf.body_text(
        "Os filtros de média e gaussiano reduziram ruídos e suavizaram "
        "a imagem. Sobel e Prewitt destacaram bordas horizontais e "
        "verticais. Os filtros Laplacianos enfatizaram regiões de alta "
        "variação de intensidade. O filtro emboss gerou efeito artístico "
        "de relevo e o unsharp masking aumentou a nitidez das texturas."
    )

    pdf.add_page()
    pdf.section_title("5. Questão 2 – Filtragem no Domínio da Frequência")
    pdf.body_text("Foi aplicada a FFT 2D na imagem em escala de cinza (imagem3.jpeg) para análise espectral e aplicação de filtros ideais.")

    pdf.subsection_title("5.1 Espectro de Fourier")
    fft_img = RESULTS_Q2_DIR / "00_fft" / "fft_espectro_centralizado.png"
    pdf.add_single_image(fft_img, "Espectro centralizado da FFT", width=120)

    pdf.subsection_title("5.2 Filtros Passa-Baixa e Passa-Alta")
    radii = [15,30,60]
    for filtro_type, label in [("passabaixa","Passa-Baixa"), ("passaalta","Passa-Alta")]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, sanitize_text(f"Filtro {label}"), ln=1)
        imgs, caps = [], []
        for r in radii:
            mask_path = RESULTS_Q2_DIR / "01_masks" / f"mask_{filtro_type}_r{r}.png"
            result_path = RESULTS_Q2_DIR / "02_filtradas" / f"filtro_{filtro_type}_r{r}.png"
            imgs.extend([str(mask_path), str(result_path)])
            caps.extend([f"Máscara r={r}", f"Resultado r={r}"])
        pdf.image_grid(imgs, caps, cols=2, img_w=80, img_h=60)

    pdf.subsection_title("5.3 Passa-Faixa e Rejeita-Faixa")
    band_pairs = [(10,30), (20,50)]
    imgs_band, caps_band = [], []
    for r1,r2 in band_pairs:
        mask_pf = RESULTS_Q2_DIR / "01_masks" / f"mask_passafaixa_r{r1}_{r2}.png"
        img_pf  = RESULTS_Q2_DIR / "02_filtradas" / f"filtro_passafaixa_r{r1}_{r2}.png"
        mask_rf = RESULTS_Q2_DIR / "01_masks" / f"mask_rejeitafaixa_r{r1}_{r2}.png"
        img_rf  = RESULTS_Q2_DIR / "02_filtradas" / f"filtro_rejeitafaixa_r{r1}_{r2}.png"
        imgs_band.extend([str(mask_pf), str(img_pf), str(mask_rf), str(img_rf)])
        caps_band.extend([
            f"Máscara Passa-Faixa ({r1}-{r2})", f"Resultado Passa-Faixa ({r1}-{r2})",
            f"Máscara Rejeita-Faixa ({r1}-{r2})", f"Resultado Rejeita-Faixa ({r1}-{r2})"
        ])
    pdf.image_grid(imgs_band, caps_band, cols=2, img_w=80, img_h=60)

    pdf.subsection_title("5.4 Compressão por FFT")
    stats_q2 = load_json(JSON_Q2)

    pdf.set_font("Arial", "", 10)
    col_widths = [35,45,50,45]
    headers = ["Percentil","Limiar","Coef. Mantidos","Taxa de zeros"]
    for w,h in zip(col_widths, headers):
        pdf.cell(w, 10, sanitize_text(h), border=1, align="C")
    pdf.ln()
    for comp in stats_q2["compressao"]:
        row = [f"{comp['percentil']}%", f"{comp['limiar']:.1f}", f"{comp['coeficientes_mantidos']}", f"{comp['taxa_zerados']*100:.1f}%"]
        for w,item in zip(col_widths, row):
            pdf.cell(w, 10, sanitize_text(item), border=1, align="C")
        pdf.ln()
    pdf.ln(10)

    comp_paths = {
        "70%": RESULTS_Q2_DIR / "03_compressao" / "compressao_percentil_70.png",
        "85%": RESULTS_Q2_DIR / "03_compressao" / "compressao_percentil_85.png",
        "95%": RESULTS_Q2_DIR / "03_compressao" / "compressao_percentil_95.png"
    }
    imgs_comp = [str(p) for p in comp_paths.values()]
    caps_comp = [f"Compressão {pct}" for pct in comp_paths.keys()]
    pdf.image_grid(imgs_comp, caps_comp, cols=3, img_w=55, img_h=55)

    pdf.subsection_title("5.5 Histogramas Comparativos")
    hist_img = RESULTS_Q2_DIR / "04_histogramas" / "comparativo_histogramas.png"
    pdf.add_single_image(hist_img, "Histogramas comparativos das imagens comprimidas", width=170)

    pdf.add_page()
    pdf.section_title("6. Conclusão")
    pdf.body_text(
        "Os experimentos mostraram como filtros espaciais e no domínio "
        "da frequência podem ser utilizados para suavização, realce, "
        "detecção de bordas e compressão de imagens. As técnicas "
        "implementadas demonstraram boa eficiência visual e permitiram "
        "compreender o impacto das frequências espaciais na qualidade "
        "das imagens."
    )

    pdf.section_title("7. Referências")
    pdf.body_text(
        "GONZALEZ, R. C.; WOODS, R. E. Digital Image Processing.\n"
        "Documentação NumPy FFT.\n"
        "Documentação Pillow.\n"
        "Implementações próprias em Python."
    )

def main():
    pdf_capture = PDF(capture_sections=True)
    pdf_capture.add_page()
    pdf_capture.set_fill_color(30, 30, 30)
    pdf_capture.rect(0, 0, 210, 50, "F")
    pdf_capture.set_text_color(255, 255, 255)
    pdf_capture.set_font("Arial", "B", 24)
    pdf_capture.set_xy(0, 15)
    pdf_capture.cell(210, 10, sanitize_text("RELATÓRIO DA ATIVIDADE 2"), align="C")
    pdf_capture.set_text_color(0, 0, 0)
    pdf_capture.ln(50)
    pdf_capture.set_font("Arial", "", 14)
    pdf_capture.cell(0, 10, sanitize_text("Processamento Digital de Imagens"), ln=1, align="C")
    pdf_capture.cell(0, 10, sanitize_text("Filtragem Espacial e no Domínio da Frequência"), ln=1, align="C")
    pdf_capture.ln(15)
    pdf_capture.set_font("Arial", "", 12)
    pdf_capture.cell(0, 8, sanitize_text("Aluno: Yago Melo Da Costa"), ln=1, align="C")
    pdf_capture.cell(0, 8, sanitize_text("Tema: Moda"), ln=1, align="C")
    pdf_capture.cell(0, 8, sanitize_text(f"Data: {datetime.now().strftime('%d/%m/%Y')}"), ln=1, align="C")
    
    build_content(pdf_capture, is_capture_pass=True)
    
    section_pages = pdf_capture.section_pages
    page_of = {title: page for title, page in section_pages}
    
    pdf = PDF(capture_sections=False)
    pdf.add_page()
    pdf.set_fill_color(30, 30, 30)
    pdf.rect(0, 0, 210, 50, "F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 24)
    pdf.set_xy(0, 15)
    pdf.cell(210, 10, sanitize_text("RELATÓRIO DA ATIVIDADE 2"), align="C")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(50)
    pdf.set_font("Arial", "", 14)
    pdf.cell(0, 10, sanitize_text("Processamento Digital de Imagens"), ln=1, align="C")
    pdf.cell(0, 10, sanitize_text("Filtragem Espacial e no Domínio da Frequência"), ln=1, align="C")
    pdf.ln(15)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, sanitize_text("Aluno: Yago Melo Da Costa"), ln=1, align="C")
    pdf.cell(0, 8, sanitize_text("Tema: Moda"), ln=1, align="C")
    pdf.cell(0, 8, sanitize_text(f"Data: {datetime.now().strftime('%d/%m/%Y')}"), ln=1, align="C")
    
    pdf.add_page()
    pdf.section_title("Sumário")
    ordem = [
        "1. Objetivo",
        "2. Imagens Utilizadas",
        "3. Metodologia",
        "4. Questão 1 – Filtros Espaciais",
        "5. Questão 2 – Filtragem no Domínio da Frequência",
        "6. Conclusão",
        "7. Referências"
    ]
    pdf.set_font("Arial", "", 12)
    for titulo in ordem:
        if titulo in page_of:
            num_pag = page_of[titulo] + 1
            pagina_real = num_pag 
        else:
            pagina_real = "?"
        pdf.cell(0, 8, sanitize_text(f"{titulo} .................... {pagina_real}"), ln=1)
    pdf.ln(5)
    
    build_content(pdf, is_capture_pass=False)
    
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT_PDF))
    print(f"\nRelatório gerado com sucesso:\n{OUTPUT_PDF}")

if __name__ == "__main__":
    main()