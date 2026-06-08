import json 
from pathlib import Path 
from datetime import datetime 
from fpdf import FPDF 




def sanitize (text ):
    replacements ={
    '\u2013':'-','\u2014':'-','\u2018':"'",'\u2019':"'",
    '\u201c':'"','\u201d':'"','\u2026':'...','\u00e7':'c',
    '\u00e1':'a','\u00e9':'e','\u00ed':'i','\u00f3':'o',
    '\u00fa':'u','\u00e0':'a','\u00e2':'a','\u00ea':'e',
    '\u00f4':'o','\u00fc':'u','\u00e3':'a','\u00f5':'o',
    '\u00c1':'A','\u00c9':'E','\u00cd':'I','\u00d3':'O',
    '\u00da':'U','\u00c3':'A','\u00d5':'O','\u00c2':'A',
    '\u00ca':'E','\u00d4':'O','\u00c7':'C',
    }
    for old ,new in replacements .items ():
        text =text .replace (old ,new )
    text =text .encode ('latin-1',errors ='replace').decode ('latin-1')
    return text 





SCRIPT_DIR =Path (__file__ ).resolve ().parent 
BASE_DIR =SCRIPT_DIR .parent 
IMAGES_DIR =BASE_DIR /"images"
Q1_DIR =SCRIPT_DIR /"resultados_q1"
Q2_DIR =SCRIPT_DIR /"resultados_q2"
JSON_Q1 =Q1_DIR /"resultados_q1.json"
JSON_Q2 =Q2_DIR /"resultados_q2.json"
OUTPUT_PDF =SCRIPT_DIR /"reports"/"Relatorio_Atividade3.pdf"
CODE_Q1 =SCRIPT_DIR /"questao1_dct.py"
CODE_Q2 =SCRIPT_DIR /"questao2_descritores.py"


def load_json (path ):
    with open (path ,'r',encoding ='utf-8')as f :
        return json .load (f )


def collect_images_from_dir (directory :Path ,exclude_names =None ):
    """Retorna lista de caminhos de todas as imagens .png no diretório,
       excluindo nomes de arquivo especificados (sem extensão ou completos)."""
    if exclude_names is None :
        exclude_names =[]
    images =[]
    for p in directory .glob ("**/*.png"):
        if p .name not in exclude_names :
            images .append (p )
    return sorted (images )





class PDF (FPDF ):
    def __init__ (self ,capture_sections =False ):
        super ().__init__ ()
        self .capture_sections =capture_sections 
        self .section_pages =[]
        self .set_auto_page_break (auto =True ,margin =20 )

    def header (self ):
        if self .page_no ()>1 :
            self .set_font ('Arial','',9 )
            self .set_text_color (100 ,100 ,100 )
            self .set_y (10 )
            self .cell (0 ,5 ,sanitize (f'{self .page_no ()}'),align ='R')
            self .set_text_color (0 ,0 ,0 )
            self .ln (10 )

    def footer (self ):
        pass 

    def section_title (self ,title ):
        self .ln (4 )
        self .set_fill_color (220 ,220 ,220 )
        self .set_font ('Arial','B',15 )
        self .cell (0 ,10 ,sanitize (title ),border =0 ,ln =1 ,fill =True )
        self .ln (4 )
        if self .capture_sections :
            self .section_pages .append ((title ,self .page_no ()))

    def subsection_title (self ,title ):
        self .set_font ('Arial','B',12 )
        self .cell (0 ,8 ,sanitize (title ),ln =1 )
        self .ln (2 )

    def body_text (self ,text ):
        self .set_font ('Arial','',11 )
        self .multi_cell (0 ,6 ,sanitize (text ))
        self .ln (2 )

    def add_single_image (self ,img_path ,caption ='',width =120 ):
        img_path =Path (img_path )
        if not img_path .exists ():
            self .set_font ('Arial','',10 )
            self .cell (0 ,8 ,sanitize (f'Imagem nao encontrada: {img_path }'),ln =1 )
            return 
        margin =20 
        img_height =width *0.75 
        needed =img_height +20 
        if self .get_y ()+needed >297 -margin :
            self .add_page ()
        x =(210 -width )/2 
        self .image (str (img_path ),x =x ,w =width )
        self .ln (2 )
        if caption :
            self .set_font ('Arial','I',9 )
            self .multi_cell (0 ,5 ,sanitize (caption ),align ='C')
        self .ln (5 )

    def image_grid (self ,images ,captions =None ,cols =2 ,img_w =80 ,img_h =60 ):
        if captions is None :
            captions =['']*len (images )
        spacing_x =8 
        spacing_y =18 
        total_width =cols *img_w +(cols -1 )*spacing_x 
        start_x =(210 -total_width )/2 
        current_x =start_x 
        current_y =self .get_y ()

        for i ,(img ,cap )in enumerate (zip (images ,captions )):
            if current_y +img_h +25 >270 :
                self .add_page ()
                current_y =self .get_y ()
                current_x =start_x 

            self .set_xy (current_x ,current_y )
            img_p =Path (img )
            if img_p .exists ():
                self .image (str (img_p ),x =current_x ,y =current_y ,w =img_w ,h =img_h )
            else :
                self .rect (current_x ,current_y ,img_w ,img_h )
                self .set_xy (current_x ,current_y +img_h /2 )
                self .set_font ('Arial','',8 )
                self .multi_cell (img_w ,4 ,sanitize ('Imagem nao encontrada'),align ='C')

            self .set_xy (current_x ,current_y +img_h +2 )
            self .set_font ('Arial','',8 )
            self .multi_cell (img_w ,4 ,sanitize (cap ),align ='C')

            current_x +=img_w +spacing_x 
            if (i +1 )%cols ==0 :
                current_x =start_x 
                current_y +=img_h +spacing_y 

        self .set_y (current_y +img_h +spacing_y )

    def add_code_file (self ,filepath ,title ):
        filepath =Path (filepath )
        if not filepath .exists ():
            self .body_text (f'Arquivo nao encontrado: {filepath }')
            return 
        self .subsection_title (title )
        with open (filepath ,'r',encoding ='utf-8')as f :
            code_lines =f .readlines ()
        self .set_font ('Courier','',8 )
        for line in code_lines :
            line =line .rstrip ('\n')
            self .multi_cell (0 ,4 ,sanitize (line )if line else '')
        self .ln (4 )
        self .set_font ('Arial','',11 )

    def metrics_table (self ,headers ,col_widths ,rows ):
        self .set_font ('Arial','B',10 )
        for w ,h in zip (col_widths ,headers ):
            self .cell (w ,9 ,sanitize (h ),border =1 ,align ='C')
        self .ln ()
        self .set_font ('Arial','',10 )
        for row in rows :
            for w ,item in zip (col_widths ,row ):
                self .cell (w ,9 ,sanitize (str (item )),border =1 ,align ='C')
            self .ln ()
        self .ln (6 )





def build_content (pdf ,is_capture_pass =False ):



    pdf .add_page ()
    pdf .section_title ('1. Objetivo')
    pdf .body_text (
    'Este trabalho tem como objetivo explorar e consolidar conceitos de compressao, '
    'representacao e descricao de imagens digitais, por meio da implementacao pratica '
    'de tecnicas fundamentais. A Questao 1 implementa uma versao simplificada de '
    'compressao de imagens baseada na Transformada Discreta do Cosseno (DCT), '
    'inspirada no padrao JPEG, analisando as perdas introduzidas no processo. '
    'A Questao 2 desenvolve um conjunto de descritores estatisticos e estruturais '
    'para caracterizar imagens em tons de cinza, comparando diferentes padroes visuais.'
    )




    pdf .add_page ()
    pdf .section_title ('2. Imagens Utilizadas')
    pdf .body_text (
    'As imagens utilizadas estao relacionadas ao tema do trabalho final. '
    'A Figura abaixo apresenta as duas imagens em tons de cinza utilizadas '
    'nos experimentos: imagem1 foi usada na Questao 1 (compressao DCT) e '
    'ambas foram utilizadas na Questao 2 (descritores).'
    )
    img1_orig =IMAGES_DIR /'imagem1.jpeg'
    img2_orig =IMAGES_DIR /'imagem2.jpeg'
    pdf .image_grid (
    [str (img1_orig ),str (img2_orig )],
    ['Imagem 1 (imagem1.jpeg)','Imagem 2 (imagem2.jpeg)'],
    cols =2 ,img_w =80 ,img_h =60 
    )




    pdf .add_page ()
    pdf .section_title ('3. Metodologia')
    pdf .body_text (
    'Todas as transformacoes foram implementadas manualmente em Python, sem uso de '
    'funcoes prontas das bibliotecas. O carregamento e salvamento de imagens utilizou '
    'apenas PIL/Pillow. Os calculos de DCT e IDCT foram feitos com loops explicitamente '
    'baseados na definicao matematica da transformada. Os descritores foram calculados '
    'percorrendo os pixels da imagem via operacoes NumPy basicas. '
    'As bibliotecas matplotlib e fpdf foram usadas apenas para geracao de graficos '
    'e do relatorio, respectivamente.'
    )




    pdf .add_page ()
    pdf .section_title ('4. Questao 1 - Compressao DCT (estilo JPEG)')
    pdf .body_text (
    'A Questao 1 implementa o pipeline de compressao JPEG simplificado: '
    '(1) conversao para tons de cinza, (2) divisao em blocos 8x8, '
    '(3) aplicacao da DCT 2D manual em cada bloco, '
    '(4) quantizacao com a matriz padrao JPEG, '
    '(5) dequantizacao e (6) aplicacao da IDCT 2D para reconstrucao. '
    'Foram testados cinco valores do fator de escala de quantizacao (q_scale): '
    '0.5, 1.0, 2.0, 4.0 e 8.0. '
    'Valores menores preservam mais informacao (qualidade maior), '
    'valores maiores aumentam a compressao e a perda de qualidade.'
    )


    pdf .subsection_title ('4.1 Imagem Original (tons de cinza)')
    orig_gray =Q1_DIR /'original_gray.png'
    pdf .add_single_image (orig_gray ,'Imagem original convertida para tons de cinza',width =110 )


    pdf .subsection_title ('4.2 Imagens Reconstruidas por q_scale')
    q_labels =['0_5','1_0','2_0','4_0','8_0']
    q_names =['q=0.5 (Alta qualidade)','q=1.0 (Padrao JPEG)','q=2.0','q=4.0','q=8.0 (Alta compressao)']
    imgs_rec =[str (Q1_DIR /f'reconstruida_q{t }.png')for t in q_labels ]
    pdf .image_grid (imgs_rec ,q_names ,cols =3 ,img_w =55 ,img_h =45 )


    pdf .subsection_title ('4.3 Imagens de Diferenca (|original - reconstruida|)')
    imgs_diff =[str (Q1_DIR /f'diferenca_q{t }.png')for t in q_labels ]
    pdf .image_grid (imgs_diff ,[f'Diferenca {n }'for n in q_names ],cols =3 ,img_w =55 ,img_h =45 )


    pdf .subsection_title ('4.4 Metricas de Qualidade')
    pdf .body_text (
    'A tabela abaixo apresenta o PSNR (Peak Signal-to-Noise Ratio) e o MAE '
    '(Mean Absolute Error) para cada configuracao de q_scale. '
    'PSNR acima de 40 dB indica qualidade excelente; abaixo de 30 dB, '
    'perda perceptivel significativa.'
    )
    stats_q1 =load_json (JSON_Q1 )
    headers_q1 =['q_scale','PSNR (dB)','MAE']
    widths_q1 =[50 ,70 ,60 ]
    rows_q1 =[]
    for tag in q_labels :
        d =stats_q1 .get (tag ,{})
        rows_q1 .append ([
        str (d .get ('q_scale',tag )),
        f"{d .get ('psnr','-'):.4f}",
        f"{d .get ('mae','-'):.4f}"
        ])
    pdf .metrics_table (headers_q1 ,widths_q1 ,rows_q1 )

    pdf .subsection_title ('4.5 Analise dos Resultados')
    pdf .body_text (
    'Com q_scale=0.5 a quantizacao e mais fina, preservando mais coeficientes '
    'DCT e resultando no maior PSNR. A medida que q_scale aumenta, a matriz de '
    'quantizacao amplifica os passos de arredondamento, descartando mais '
    'informacao de alta frequencia. Isso se manifesta visualmente como '
    'artefatos de bloco (blocky artifacts) e perda de bordas e texturas finas. '
    'As imagens de diferenca evidenciam que as maiores discrepancias concentram-se '
    'nas regioes de alto detalhe, confirmando o comportamento teorico da DCT: '
    'coeficientes de alta frequencia sao os primeiros a ser eliminados. '
    'O artefato de bloco torna-se nitidamente visivel para q_scale >= 4.0.'
    )




    pdf .add_page ()
    pdf .section_title ('5. Questao 2 - Descritores de Imagem')
    pdf .body_text (
    'A Questao 2 implementa um conjunto de descritores para caracterizar '
    'imagens em tons de cinza, combinando medidas estatisticas globais '
    'e informacoes estruturais. Os descritores calculados sao: '
    'media, variancia, desvio padrao, energia, entropia de Shannon '
    'e variacao espacial (diferenca absoluta entre pixels vizinhos '
    'horizontal e vertical).'
    )


    pdf .subsection_title ('5.1 Comparacao Visual das Imagens')
    comp_path =Q2_DIR /'comparativo_imagens.png'
    pdf .add_single_image (comp_path ,'Comparacao visual com descritores',width =160 )



    gray_images =sorted (Q2_DIR .glob ("gray_*.png"))
    if gray_images :
        pdf .subsection_title ('5.2 Imagens Individuais em Tons de Cinza')
        gray_paths =[str (p )for p in gray_images ]
        gray_captions =[p .stem .replace ('gray_','Imagem ')for p in gray_images ]
        pdf .image_grid (gray_paths ,gray_captions ,cols =2 ,img_w =80 ,img_h =60 )


    pdf .subsection_title ('5.3 Histogramas Comparativos')
    hist_path =Q2_DIR /'histogramas_comparativos.png'
    pdf .add_single_image (hist_path ,'Histogramas de intensidade das imagens',width =160 )


    pdf .subsection_title ('5.4 Grafico Radar dos Descritores')
    radar_path =Q2_DIR /'radar_descritores.png'
    pdf .add_single_image (radar_path ,'Grafico radar comparativo dos descritores normalizados',width =130 )


    pdf .subsection_title ('5.5 Tabela de Descritores')
    stats_q2 =load_json (JSON_Q2 )
    labels_q2 =list (stats_q2 .keys ())
    desc_keys =['mean','variance','std','energy','entropy',
    'spatial_variation_horizontal','spatial_variation_vertical','spatial_variation_total']
    desc_names =['Media','Variancia','Desvio Padrao','Energia',
    'Entropia (bits)','Var.Esp. Horiz.','Var.Esp. Vert.','Var.Esp. Total']

    pdf .set_font ('Arial','B',10 )
    col_w_label =50 
    col_w_val =int ((190 -col_w_label )/len (labels_q2 ))
    pdf .cell (col_w_label ,9 ,sanitize ('Descritor'),border =1 ,align ='C')
    for lbl in labels_q2 :
        pdf .cell (col_w_val ,9 ,sanitize (lbl ),border =1 ,align ='C')
    pdf .ln ()
    pdf .set_font ('Arial','',9 )
    for key ,name in zip (desc_keys ,desc_names ):
        pdf .cell (col_w_label ,8 ,sanitize (name ),border =1 )
        for lbl in labels_q2 :
            val =stats_q2 [lbl ].get (key ,'-')
            pdf .cell (col_w_val ,8 ,sanitize (f'{val :.2f}'if isinstance (val ,float )else str (val )),border =1 ,align ='C')
        pdf .ln ()
    pdf .ln (6 )


    pdf .subsection_title ('5.6 Interpretacao dos Resultados')
    pdf .body_text (
    'Os descritores revelam diferencas significativas entre as imagens. '
    'Imagens com alta variacao espacial total possuem grande quantidade de '
    'detalhes e texturas complexas, enquanto regioes com baixa variacao '
    'correspondem a areas homogeneas (como ceu ou fundos uniformes). '
    'A entropia reflete a diversidade do histograma: imagens com distribuicao '
    'de intensidade mais uniforme apresentam maior entropia. '
    'A energia e inversamente relacionada a uniformidade: imagens homogeneas '
    'tendem a concentrar os pixels em poucos niveis, aumentando a energia. '
    'Esses descritores sao uteis em sistemas de recuperacao de imagens, '
    'classificacao de texturas e pre-processamento para algoritmos de '
    'aprendizado de maquina, servindo como vetor de caracteristicas compacto '
    'para diferenciar padroes visuais distintos.'
    )




    pdf .add_page ()
    pdf .section_title ('6. Conclusao')
    pdf .body_text (
    'Os experimentos demonstraram como a DCT permite representar imagens de '
    'forma compacta por meio da concentracao de energia nos coeficientes de '
    'baixa frequencia. A quantizacao introduz perdas controlaveis pelo '
    'parametro q_scale: quanto maior o fator, maior a compressao e mais '
    'intensos os artefatos de bloco. Os descritores estatisticos e estruturais '
    'mostraram-se eficazes para diferenciar imagens com diferentes '
    'caracteristicas visuais, sendo a variacao espacial o indicador mais '
    'sensivel ao nivel de detalhe e textura presentes nas imagens. '
    'Ambas as tecnicas fornecem bases para aplicacoes praticas em '
    'compressao, classificacao e recuperacao de imagens digitais.'
    )




    pdf .add_page ()
    pdf .section_title ('7. Codigos Implementados')
    pdf .body_text (
    'Os codigos-fonte utilizados para gerar os resultados sao apresentados '
    'a seguir. O primeiro arquivo implementa a compressao DCT (Questao 1) '
    'e o segundo implementa os descritores de imagem (Questao 2).'
    )
    pdf .add_code_file (CODE_Q1 ,'questao1_dct.py')
    pdf .add_code_file (CODE_Q2 ,'questao2_descritores.py')




    pdf .add_page ()
    pdf .section_title ('8. Referencias')
    pdf .body_text (
    'GONZALEZ, R. C.; WOODS, R. E. Digital Image Processing. 4. ed. Pearson, 2018.\n'
    'WALLACE, G. K. The JPEG still picture compression standard. '
    'IEEE Transactions on Consumer Electronics, 1992.\n'
    'Documentacao NumPy. Disponivel em: https://numpy.org/doc\n'
    'Documentacao Pillow. Disponivel em: https://pillow.readthedocs.io\n'
    'Implementacoes proprias em Python.'
    )





def main ():

    pdf_capture =PDF (capture_sections =True )
    pdf_capture .add_page ()
    pdf_capture .set_fill_color (20 ,40 ,80 )
    pdf_capture .rect (0 ,0 ,210 ,55 ,'F')
    pdf_capture .set_text_color (255 ,255 ,255 )
    pdf_capture .set_font ('Arial','B',22 )
    pdf_capture .set_xy (0 ,12 )
    pdf_capture .cell (210 ,12 ,sanitize ('RELATORIO DA ATIVIDADE 3'),align ='C')
    pdf_capture .set_font ('Arial','B',14 )
    pdf_capture .set_xy (0 ,27 )
    pdf_capture .cell (210 ,10 ,sanitize ('Compressao DCT e Descritores de Imagem'),align ='C')
    pdf_capture .set_text_color (0 ,0 ,0 )
    pdf_capture .ln (65 )
    pdf_capture .set_font ('Arial','',13 )
    pdf_capture .cell (0 ,9 ,sanitize ('Processamento Digital de Imagens'),ln =1 ,align ='C')
    pdf_capture .ln (12 )
    pdf_capture .set_font ('Arial','',12 )
    pdf_capture .cell (0 ,8 ,sanitize ('Aluno: Yago Melo Da Costa'),ln =1 ,align ='C')
    pdf_capture .cell (0 ,8 ,sanitize ('Tema: Moda'),ln =1 ,align ='C')
    pdf_capture .cell (0 ,8 ,sanitize (f"Data: {datetime .now ().strftime ('%d/%m/%Y')}"),ln =1 ,align ='C')
    build_content (pdf_capture ,is_capture_pass =True )
    section_pages =pdf_capture .section_pages 
    page_of ={title :page for title ,page in section_pages }


    pdf =PDF (capture_sections =False )
    pdf .add_page ()
    pdf .set_fill_color (20 ,40 ,80 )
    pdf .rect (0 ,0 ,210 ,55 ,'F')
    pdf .set_text_color (255 ,255 ,255 )
    pdf .set_font ('Arial','B',22 )
    pdf .set_xy (0 ,12 )
    pdf .cell (210 ,12 ,sanitize ('RELATORIO DA ATIVIDADE 3'),align ='C')
    pdf .set_font ('Arial','B',14 )
    pdf .set_xy (0 ,27 )
    pdf .cell (210 ,10 ,sanitize ('Compressao DCT e Descritores de Imagem'),align ='C')
    pdf .set_text_color (0 ,0 ,0 )
    pdf .ln (65 )
    pdf .set_font ('Arial','',13 )
    pdf .cell (0 ,9 ,sanitize ('Processamento Digital de Imagens'),ln =1 ,align ='C')
    pdf .ln (12 )
    pdf .set_font ('Arial','',12 )
    pdf .cell (0 ,8 ,sanitize ('Aluno: Yago Melo Da Costa'),ln =1 ,align ='C')
    pdf .cell (0 ,8 ,sanitize ('Tema: Moda'),ln =1 ,align ='C')
    pdf .cell (0 ,8 ,sanitize (f"Data: {datetime .now ().strftime ('%d/%m/%Y')}"),ln =1 ,align ='C')


    pdf .add_page ()
    pdf .section_title ('Sumario')
    ordem =[
    '1. Objetivo',
    '2. Imagens Utilizadas',
    '3. Metodologia',
    '4. Questao 1 - Compressao DCT (estilo JPEG)',
    '5. Questao 2 - Descritores de Imagem',
    '6. Conclusao',
    '7. Codigos Implementados',
    '8. Referencias',
    ]
    pdf .set_font ('Arial','',12 )
    for titulo in ordem :
        pagina_real =page_of .get (titulo ,'?')
        if isinstance (pagina_real ,int ):
            pagina_real =pagina_real +2 
        pdf .cell (0 ,8 ,sanitize (f'{titulo } .................... {pagina_real }'),ln =1 )
    pdf .ln (5 )

    build_content (pdf ,is_capture_pass =False )

    OUTPUT_PDF .parent .mkdir (parents =True ,exist_ok =True )
    pdf .output (str (OUTPUT_PDF ))
    print (f'\nRelatorio gerado com sucesso:\n{OUTPUT_PDF }')


if __name__ =='__main__':
    main ()