import json
from pathlib import Path
from datetime import datetime
from fpdf import FPDF

def sanitize(text):
    replacements = {
        '\u2013': '-', '\u2014': '-', '\u2018': "'", '\u2019': "'",
        '\u201c': '"', '\u201d': '"', '\u2026': '...', '\u00e7': 'c',
        '\u00e1': 'a', '\u00e9': 'e', '\u00ed': 'i', '\u00f3': 'o',
        '\u00fa': 'u', '\u00e0': 'a', '\u00e2': 'a', '\u00ea': 'e',
        '\u00f4': 'o', '\u00fc': 'u', '\u00e3': 'a', '\u00f5': 'o',
        '\u00c1': 'A', '\u00c9': 'E', '\u00cd': 'I', '\u00d3': 'O',
        '\u00da': 'U', '\u00c3': 'A', '\u00d5': 'O', '\u00c2': 'A',
        '\u00ca': 'E', '\u00d4': 'O', '\u00c7': 'C',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode('latin-1', errors='replace').decode('latin-1')

SCRIPT_DIR = Path(__file__).resolve().parent
BASE_DIR = SCRIPT_DIR.parent
IMAGES_DIR = BASE_DIR / "images"
Q1_DIR = SCRIPT_DIR / "resultados_q1"
Q2_DIR = SCRIPT_DIR / "resultados_q2"
Q3_DIR = SCRIPT_DIR / "resultados_q3"
OUTPUT_PDF = SCRIPT_DIR / "reports" / "Relatorio_Atividade4.pdf"
CODE_Q1 = SCRIPT_DIR / "questao1_morfologia.py"
CODE_Q2 = SCRIPT_DIR / "questao2_canny_hog.py"
CODE_Q3 = SCRIPT_DIR / "questao3_watershed.py"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

class PDF(FPDF):
    def __init__(self, capture_sections=False):
        super().__init__()
        self.capture_sections = capture_sections
        self.section_pages = []
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', '', 9)
            self.set_text_color(100, 100, 100)
            self.set_y(10)
            self.cell(0, 5, sanitize(f'{self.page_no()}'), align='R')
            self.set_text_color(0, 0, 0)
            self.ln(10)

    def footer(self):
        pass

    def section_title(self, title):
        self.ln(4)
        self.set_fill_color(220, 220, 220)
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, sanitize(title), border=0, ln=1, fill=True)
        self.ln(4)
        if self.capture_sections:
            self.section_pages.append((title, self.page_no()))

    def subsection_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, sanitize(title), ln=1)
        self.ln(2)

    def body_text(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, sanitize(text))
        self.ln(2)

    def add_single_image(self, img_path, caption='', width=120):
        img_path = Path(img_path)
        if not img_path.exists():
            self.set_font('Arial', '', 10)
            self.cell(0, 8, sanitize(f'Imagem nao encontrada: {img_path}'), ln=1)
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
            self.set_font('Arial', 'I', 9)
            self.multi_cell(0, 5, sanitize(caption), align='C')
        self.ln(5)

    def image_grid(self, images, captions=None, cols=2, img_w=80, img_h=60):
        if captions is None:
            captions = [''] * len(images)
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
            img_p = Path(img)
            if img_p.exists():
                self.image(str(img_p), x=current_x, y=current_y, w=img_w, h=img_h)
            else:
                self.rect(current_x, current_y, img_w, img_h)
                self.set_xy(current_x, current_y + img_h / 2)
                self.set_font('Arial', '', 8)
                self.multi_cell(img_w, 4, sanitize('Imagem nao encontrada'), align='C')

            self.set_xy(current_x, current_y + img_h + 2)
            self.set_font('Arial', '', 8)
            self.multi_cell(img_w, 4, sanitize(cap), align='C')

            current_x += img_w + spacing_x
            if (i + 1) % cols == 0:
                current_x = start_x
                current_y += img_h + spacing_y

        self.set_y(current_y + img_h + spacing_y)

    def add_code_file(self, filepath, title):
        filepath = Path(filepath)
        if not filepath.exists():
            self.body_text(f'Arquivo nao encontrado: {filepath}')
            return
        self.subsection_title(title)
        with open(filepath, 'r', encoding='utf-8') as f:
            code_lines = f.readlines()
        self.set_font('Courier', '', 8)
        for line in code_lines:
            line = line.rstrip('\n')
            self.multi_cell(0, 4, sanitize(line) if line else '')
        self.ln(4)
        self.set_font('Arial', '', 11)

def build_content(pdf):
    pdf.add_page()
    pdf.section_title('1. Objetivo')
    pdf.body_text(
        'Esta atividade tem como objetivo introduzir técnicas fundamentais de morfologia matemática '
        'e segmentação de imagens, por meio da implementação prática de operadores que permitem extrair, '
        'separar e estruturar informações relevantes em imagens digitais. Busca-se desenvolver a compreensão '
        'dos efeitos dessas operações na análise de formas, bordas e regiões.'
    )

    pdf.add_page()
    pdf.section_title('2. Imagens Utilizadas')
    pdf.body_text(
        'As imagens utilizadas estão relacionadas ao tema do trabalho final (moda). '
        'Foram empregadas imagens do diretório images/, sendo a imagem1 e imagem2 para a questão 1, '
        'e imagem3 para as questões 2 e 3.'
    )
    img1 = IMAGES_DIR / 'imagem1.jpeg'
    img2 = IMAGES_DIR / 'imagem2.jpeg'
    img3 = IMAGES_DIR / 'imagem3.jpeg'
    pdf.image_grid(
        [str(img1), str(img2), str(img3)],
        ['imagem1.jpeg', 'imagem2.jpeg', 'imagem3.jpeg'],
        cols=3, img_w=55, img_h=45
    )

    pdf.add_page()
    pdf.section_title('3. Metodologia')
    pdf.body_text(
        'Todas as implementações foram realizadas manualmente em Python, sem uso de funções prontas '
        'de bibliotecas para as operações solicitadas. Apenas PIL/Pillow foi utilizada para carregar '
        'e salvar imagens. As operações morfológicas foram implementadas via convolução com elementos '
        'estruturantes. O gradiente e a magnitude foram calculados com operadores de Sobel manuais. '
        'O HOG foi implementado dividindo a imagem em células e construindo histogramas de orientação. '
        'O watershed baseado em marcadores utilizou transformada de distância e crescimento de regiões '
        'com fila de prioridade.'
    )

    pdf.add_page()
    pdf.section_title('4. Questão 1 – Morfologia Matemática')
    pdf.body_text(
        'Foram aplicadas erosão, dilatação, abertura e fechamento em imagens binárias obtidas por '
        'limiarização (threshold=128). Utilizaram-se elementos estruturantes quadrados de tamanhos 3, 5 e 15. '
        'Os resultados são apresentados a seguir para cada imagem.'
    )
    stats_q1 = load_json(Q1_DIR / 'resultados_q1.json')
    for img_name, res in stats_q1.items():
        pdf.subsection_title(f'Imagem: {img_name}')
        pdf.body_text(f'Resultados para diferentes tamanhos de elemento estruturante.')
        for se_size, paths in res.items():
            pdf.set_font('Arial', 'B', 10)
            pdf.cell(0, 6, sanitize(f'SE {se_size}'), ln=1)
            imgs = [paths['eroded'], paths['dilated'], paths['opened'], paths['closed']]
            caps = ['Erosão', 'Dilatação', 'Abertura', 'Fechamento']
            pdf.image_grid(imgs, caps, cols=2, img_w=70, img_h=55)
        pdf.ln(4)

    pdf.add_page()
    pdf.section_title('5. Questão 2 – Canny (passos iniciais) e HOG')
    pdf.body_text(
        'Foram implementados: suavização gaussiana, cálculo do gradiente com Sobel, magnitude e orientação. '
        'Em seguida, o descritor HOG foi calculado com células de 8x8 pixels e 9 bins de orientação (0°-180°). '
        'A visualização do HOG é apresentada como um campo de orientação.'
    )
    pdf.subsection_title('5.1 Imagem original e suavizada')
    orig_q2 = Q2_DIR / 'original.png'
    suav_q2 = Q2_DIR / 'suavizada_gauss.png'
    pdf.image_grid([str(orig_q2), str(suav_q2)], ['Original', 'Suavizada Gauss'], cols=2, img_w=80, img_h=60)

    pdf.subsection_title('5.2 Magnitude do gradiente')
    mag_q2 = Q2_DIR / 'magnitude_visual.png'
    pdf.add_single_image(mag_q2, 'Magnitude do gradiente (visualização)', width=140)

    pdf.subsection_title('5.3 Visualização do HOG')
    hog_q2 = Q2_DIR / 'hog_visualizacao.png'
    pdf.add_single_image(hog_q2, 'Campos de orientação do HOG (células 8x8, 9 bins)', width=140)

    pdf.subsection_title('5.4 Vetor de características HOG')
    stats_q2 = load_json(Q2_DIR / 'resultados_q2.json')
    pdf.body_text(
        f'Dimensão do histograma: {stats_q2["histogram_shape"]} (células altura x largura x bins). '
        f'Foram extraídas {stats_q2["histogram_shape"][0] * stats_q2["histogram_shape"][1] * stats_q2["histogram_shape"][2]} características.'
    )

    pdf.add_page()
    pdf.section_title('6. Questão 3 – Watershed com Marcadores')
    pdf.body_text(
        'A segmentação por watershed foi realizada com base em marcadores obtidos a partir da transformada '
        'de distância sobre uma imagem binária limpa (abertura+fechamento). Os marcadores são os máximos '
        'locais da distância. O crescimento de regiões foi feito utilizando fila de prioridade com base no '
        'gradiente da imagem original.'
    )
    pdf.subsection_title('6.1 Pré-processamento')
    bin_q3 = Q3_DIR / 'binaria.png'
    clean_q3 = Q3_DIR / 'limpa.png'
    dist_q3 = Q3_DIR / 'distancia.png'
    pdf.image_grid([str(bin_q3), str(clean_q3), str(dist_q3)],
                   ['Binária', 'Limpa (abertura+fechamento)', 'Distância'],
                   cols=3, img_w=55, img_h=45)

    pdf.subsection_title('6.2 Marcadores')
    markers_q3 = Q3_DIR / 'marcadores.png'
    pdf.add_single_image(markers_q3, 'Marcadores (máximos locais da distância)', width=140)

    pdf.subsection_title('6.3 Resultado da Watershed')
    ws_q3 = Q3_DIR / 'watershed_resultado.png'
    overlay_q3 = Q3_DIR / 'segmentacao_overlay.png'
    pdf.image_grid([str(ws_q3), str(overlay_q3)],
                   ['Linhas de separação (branco)', 'Sobreposição na original'],
                   cols=2, img_w=80, img_h=60)

    stats_q3 = load_json(Q3_DIR / 'resultados_q3.json')
    pdf.body_text(f'Número de marcadores (objetos) encontrados: {stats_q3["num_markers"]}')

    pdf.add_page()
    pdf.section_title('7. Códigos Implementados')
    pdf.body_text(
        'Os códigos-fonte utilizados para gerar os resultados são apresentados a seguir. '
        'O primeiro implementa as operações morfológicas, o segundo o gradiente e HOG, '
        'e o terceiro a segmentação watershed com marcadores.'
    )
    pdf.add_code_file(CODE_Q1, 'questao1_morfologia.py')
    pdf.add_code_file(CODE_Q2, 'questao2_canny_hog.py')
    pdf.add_code_file(CODE_Q3, 'questao3_watershed.py')

    pdf.add_page()
    pdf.section_title('8. Conclusão')
    pdf.body_text(
        'Os experimentos demonstraram a eficácia das operações morfológicas para limpeza e separação de objetos '
        'em imagens binárias. A abertura e o fechamento foram úteis para remover ruídos e preencher falhas. '
        'O gradiente e o HOG permitiram extrair características estruturais das imagens, úteis para reconhecimento '
        'de padrões. O watershed baseado em marcadores mostrou-se eficaz para separar objetos adjacentes, '
        'desde que os marcadores sejam bem definidos. A qualidade da segmentação depende fortemente do '
        'pré-processamento e da escolha dos marcadores.'
    )

    pdf.add_page()
    pdf.section_title('9. Referências')
    pdf.body_text(
        'GONZALEZ, R. C.; WOODS, R. E. Digital Image Processing. 4. ed. Pearson, 2018.\n'
        'Documentação NumPy e Pillow.\n'
        'Implementações próprias em Python.'
    )

def main():
    pdf_capture = PDF(capture_sections=True)
    pdf_capture.add_page()
    pdf_capture.set_fill_color(20, 40, 80)
    pdf_capture.rect(0, 0, 210, 55, 'F')
    pdf_capture.set_text_color(255, 255, 255)
    pdf_capture.set_font('Arial', 'B', 22)
    pdf_capture.set_xy(0, 12)
    pdf_capture.cell(210, 12, sanitize('RELATORIO DA ATIVIDADE 4'), align='C')
    pdf_capture.set_font('Arial', 'B', 14)
    pdf_capture.set_xy(0, 27)
    pdf_capture.cell(210, 10, sanitize('Morfologia, Canny, HOG e Watershed'), align='C')
    pdf_capture.set_text_color(0, 0, 0)
    pdf_capture.ln(65)
    pdf_capture.set_font('Arial', '', 13)
    pdf_capture.cell(0, 9, sanitize('Processamento Digital de Imagens'), ln=1, align='C')
    pdf_capture.ln(12)
    pdf_capture.set_font('Arial', '', 12)
    pdf_capture.cell(0, 8, sanitize('Aluno: Yago Melo Da Costa'), ln=1, align='C')
    pdf_capture.cell(0, 8, sanitize('Tema: Moda'), ln=1, align='C')
    pdf_capture.cell(0, 8, sanitize(f'Data: {datetime.now().strftime("%d/%m/%Y")}'), ln=1, align='C')
    build_content(pdf_capture)
    section_pages = pdf_capture.section_pages
    page_of = {title: page for title, page in section_pages}

    pdf = PDF(capture_sections=False)
    pdf.add_page()
    pdf.set_fill_color(20, 40, 80)
    pdf.rect(0, 0, 210, 55, 'F')
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 22)
    pdf.set_xy(0, 12)
    pdf.cell(210, 12, sanitize('RELATORIO DA ATIVIDADE 4'), align='C')
    pdf.set_font('Arial', 'B', 14)
    pdf.set_xy(0, 27)
    pdf.cell(210, 10, sanitize('Morfologia, Canny, HOG e Watershed'), align='C')
    pdf.set_text_color(0, 0, 0)
    pdf.ln(65)
    pdf.set_font('Arial', '', 13)
    pdf.cell(0, 9, sanitize('Processamento Digital de Imagens'), ln=1, align='C')
    pdf.ln(12)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, sanitize('Aluno: Yago Melo Da Costa'), ln=1, align='C')
    pdf.cell(0, 8, sanitize('Tema: Moda'), ln=1, align='C')
    pdf.cell(0, 8, sanitize(f'Data: {datetime.now().strftime("%d/%m/%Y")}'), ln=1, align='C')

    pdf.add_page()
    pdf.section_title('Sumario')
    ordem = [
        '1. Objetivo',
        '2. Imagens Utilizadas',
        '3. Metodologia',
        '4. Questão 1 – Morfologia Matemática',
        '5. Questão 2 – Canny (passos iniciais) e HOG',
        '6. Questão 3 – Watershed com Marcadores',
        '7. Códigos Implementados',
        '8. Conclusão',
        '9. Referências'
    ]
    pdf.set_font('Arial', '', 12)
    for titulo in ordem:
        pagina_real = page_of.get(titulo, '?')
        if isinstance(pagina_real, int):
            pagina_real = pagina_real + 2
        pdf.cell(0, 8, sanitize(f'{titulo} .................... {pagina_real}'), ln=1)
    pdf.ln(5)

    build_content(pdf)

    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT_PDF))
    print(f'\nRelatorio gerado com sucesso:\n{OUTPUT_PDF}')

if __name__ == '__main__':
    main()