# 🖼️ Image-Process-Activites

Repositório com implementações de técnicas de **Processamento Digital de Imagens** desenvolvidas como atividades acadêmicas. Os experimentos abrangem filtragem espacial e em frequência, transformada DCT, compressão estilo JPEG, descritores de imagem, mosaico, quantização, entre outros.

---

## 📁 Estrutura do Repositório

- `Atividade1/` – Operações básicas (esboço a lápis, correção gama, blend, mosaico, quantização)
- `Atividade2/` – Filtros espaciais (convolução) e filtragem no domínio da frequência (FFT)
- `Atividade3/` – Compressão DCT (JPEG simplificado) e descritores estatísticos de imagem

---

## 📌 Atividade 1 – Operações Fundamentais

Foram implementadas seis tarefas utilizando imagens do diretório `images/`. Os resultados gerados estão na pasta `Atividade1/outputs/`.

### 🖍️ Questão 1 – Esboço a Lápis

![Esboço](Atividade1/outputs/questao1_sketch.jpg)

### 📈 Questão 2 – Correção Gama

- **γ = 0.5**:  
  ![Gamma 0.5](Atividade1/outputs/questao2_gamma_0.5.jpg)
- **γ = 1.0**:  
  ![Gamma 1.0](Atividade1/outputs/questao2_gamma_1.0.jpg)
- **γ = 1.5**:  
  ![Gamma 1.5](Atividade1/outputs/questao2_gamma_1.5.jpg)
- **γ = 2.0**:  
  ![Gamma 2.0](Atividade1/outputs/questao2_gamma_2.0.jpg)
- **γ = 2.5**:  
  ![Gamma 2.5](Atividade1/outputs/questao2_gamma_2.5.jpg)

### 🎚️ Questão 3 – Média Ponderada (Blend)

- **α = 0.3**:  
  ![Blend α=0.3](Atividade1/outputs/questao3_blend_alpha_0.3.jpg)
- **α = 0.5**:  
  ![Blend α=0.5](Atividade1/outputs/questao3_blend_alpha_0.5.jpg)
- **α = 0.7**:  
  ![Blend α=0.7](Atividade1/outputs/questao3_blend_alpha_0.7.jpg)

### 🔄 Questão 4 – Transformações Sequenciais

![Transformações](Atividade1/outputs/questao4_transformed.jpg)

### 🧩 Questão 5 – Mosaico 4×4

![Mosaico](Atividade1/outputs/questao5_mosaic.jpg)

### 🎨 Questão 6 – Quantização

- **256 níveis**:  
  ![Quantização 256](Atividade1/outputs/questao6_quant_256levels.jpg)
- **64 níveis**:  
  ![Quantização 64](Atividade1/outputs/questao6_quant_64levels.jpg)
- **32 níveis**:  
  ![Quantização 32](Atividade1/outputs/questao6_quant_32levels.jpg)
- **16 níveis**:  
  ![Quantização 16](Atividade1/outputs/questao6_quant_16levels.jpg)
- **8 níveis**:  
  ![Quantização 8](Atividade1/outputs/questao6_quant_8levels.jpg)
- **4 níveis**:  
  ![Quantização 4](Atividade1/outputs/questao6_quant_4levels.jpg)
- **2 níveis**:  
  ![Quantização 2](Atividade1/outputs/questao6_quant_2levels.jpg)
---
## 🧪 Atividade 2 – Filtros Espaciais e Frequência

### 🔍 Questão 1 – Filtros Espaciais (Convolução Manual)

Foram aplicados 11 kernels diferentes sobre a imagem `imagem2.jpeg`. Os resultados estão na pasta `Atividade2/resultados_q1/`.

**h1 – Média 3x3**  
![h1](Atividade2/resultados_q1/q1_h1.png)
*Média 3x3 (min=3.6, max=251.7, média=132.5)*

**h2 – Gaussiano 5x5**  
![h2](Atividade2/resultados_q1/q1_h2.png)
*Gaussiano 5x5 (min=4.5, max=251.3, média=132.5)*

**h3 – Sobel horizontal**  
![h3](Atividade2/resultados_q1/q1_h3.png)
*Sobel horizontal (min=-943.0, max=983.0, média=0.1)*

**h4 – Sobel vertical**  
![h4](Atividade2/resultados_q1/q1_h4.png)
*Sobel vertical (min=-949.0, max=914.0, média=-0.3)*

**h5 – Prewitt horizontal**  
![h5](Atividade2/resultados_q1/q1_h5.png)
*Prewitt horizontal (min=-700.0, max=731.0, média=0.1)*

**h6 – Prewitt vertical**  
![h6](Atividade2/resultados_q1/q1_h6.png)
*Prewitt vertical (min=-710.0, max=678.0, média=-0.2)*

**h7 – Laplaciano (centro 4)**  
![h7](Atividade2/resultados_q1/q1_h7.png)
*Laplaciano (centro 4) (min=-581.0, max=543.0, média=-0.0)*

**h8 – Laplaciano (centro 5)**  
![h8](Atividade2/resultados_q1/q1_h8.png)
*Laplaciano (centro 5) (min=-579.0, max=772.0, média=132.5)*

**h9 – Emboss**  
![h9](Atividade2/resultados_q1/q1_h9.png)
*Emboss (min=-802.0, max=1102.0, média=132.4)*

**h10 – Média 5x5**  
![h10](Atividade2/resultados_q1/q1_h10.png)
*Média 5x5 (min=6.1, max=251.1, média=132.5)*

**h11 – Unsharp masking**  
![h11](Atividade2/resultados_q1/q1_h11.png)
*Unsharp masking (min=-133.4, max=395.8, média=132.5)*


### 🌐 Questão 2 – Filtragem no Domínio da Frequência (FFT)

A imagem `imagem3.jpeg` foi transformada via FFT 2D e submetida a máscaras ideais. Os resultados estão em `Atividade2/resultados_q2/`.

#### Espectro de Fourier

![Espectro FFT](Atividade2/resultados_q2/00_fft/fft_espectro_centralizado.png)

#### Filtros Passa‑Baixa e Passa‑Alta

**Passa‑Baixa – raio = 15**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_passabaixa_r15.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_passabaixa_r15.png)

**Passa‑Baixa – raio = 30**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_passabaixa_r30.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_passabaixa_r30.png)

**Passa‑Baixa – raio = 60**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_passabaixa_r60.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_passabaixa_r60.png)

**Passa‑Alta – raio = 15**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_passaalta_r15.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_passaalta_r15.png)

**Passa‑Alta – raio = 30**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_passaalta_r30.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_passaalta_r30.png)

**Passa‑Alta – raio = 60**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_passaalta_r60.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_passaalta_r60.png)

#### Filtros Passa‑Faixa e Rejeita‑Faixa

**Passa‑Faixa – 10‑30**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_passafaixa_r10_30.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_passafaixa_r10_30.png)

**Rejeita‑Faixa – 10‑30**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_rejeitafaixa_r10_30.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_rejeitafaixa_r10_30.png)

**Passa‑Faixa – 20‑50**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_passafaixa_r20_50.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_passafaixa_r20_50.png)

**Rejeita‑Faixa – 20‑50**  
Máscara: ![Mask](Atividade2/resultados_q2/01_masks/mask_rejeitafaixa_r20_50.png)  
Resultado: ![Resultado](Atividade2/resultados_q2/02_filtradas/filtro_rejeitafaixa_r20_50.png)

#### Compressão por Percentil da FFT

| Percentil | Limiar | Coef. mantidos | Taxa de zeros |
|-----------|--------|----------------|---------------|
| 70% | 11142.9 | 7200002 | 70.0% |
| 85% | 20266.1 | 3600001 | 85.0% |
| 95% | 46175.9 | 1200001 | 95.0% |

**Compressão 70%**  
![Compressão 70%](Atividade2/resultados_q2/03_compressao/compressao_percentil_70.png)

**Compressão 85%**  
![Compressão 85%](Atividade2/resultados_q2/03_compressao/compressao_percentil_85.png)

**Compressão 95%**  
![Compressão 95%](Atividade2/resultados_q2/03_compressao/compressao_percentil_95.png)

#### Histogramas Comparativos

![Histogramas](Atividade2/resultados_q2/04_histogramas/comparativo_histogramas.png)

---
## 🗜️ Atividade 3 – Compressão DCT e Descritores de Imagem

### 📷 Questão 1 – Compressão DCT (estilo JPEG)

A imagem `imagem1.jpeg` foi dividida em blocos 8×8, transformada por DCT 2D manual, quantizada com matriz JPEG padrão e reconstruída. Os resultados estão em `Atividade3/resultados_q1/`.

#### Imagem original (tons de cinza)

![Original gray](Atividade3/resultados_q1/original_gray.png)

#### Imagens reconstruídas para diferentes `q_scale`

**q_scale = 0.5 (alta qualidade)** (PSNR = 47.2461 dB, MAE = 0.7153)  
![Reconstruída 0.5 (alta qualidade)](Atividade3/resultados_q1/reconstruida_q0_5.png)  
![Diferença 0.5 (alta qualidade)](Atividade3/resultados_q1/diferenca_q0_5.png)  

**q_scale = 1.0 (padrão JPEG)** (PSNR = 38.5843 dB, MAE = 1.927)  
![Reconstruída 1.0 (padrão JPEG)](Atividade3/resultados_q1/reconstruida_q1_0.png)  
![Diferença 1.0 (padrão JPEG)](Atividade3/resultados_q1/diferenca_q1_0.png)  

**q_scale = 2.0** (PSNR = 35.3761 dB, MAE = 2.8772)  
![Reconstruída 2.0](Atividade3/resultados_q1/reconstruida_q2_0.png)  
![Diferença 2.0](Atividade3/resultados_q1/diferenca_q2_0.png)  

**q_scale = 4.0** (PSNR = 32.0876 dB, MAE = 4.2916)  
![Reconstruída 4.0](Atividade3/resultados_q1/reconstruida_q4_0.png)  
![Diferença 4.0](Atividade3/resultados_q1/diferenca_q4_0.png)  

**q_scale = 8.0 (alta compressão)** (PSNR = 28.7637 dB, MAE = 6.5177)  
![Reconstruída 8.0 (alta compressão)](Atividade3/resultados_q1/reconstruida_q8_0.png)  
![Diferença 8.0 (alta compressão)](Atividade3/resultados_q1/diferenca_q8_0.png)  

### 📊 Questão 2 – Descritores Estatísticos e Estruturais

Foram calculados média, variância, desvio padrão, energia, entropia e variação espacial para as imagens `imagem1.jpeg` e `imagem2.jpeg`. Os gráficos estão em `Atividade3/resultados_q2/`.

#### Comparação visual com descritores

![Comparativo imagens](Atividade3/resultados_q2/comparativo_imagens.png)

#### Imagens em tons de cinza utilizadas

![gray_imagem1](Atividade3/resultados_q2/gray_imagem1.png)  
![gray_imagem2](Atividade3/resultados_q2/gray_imagem2.png)  

#### Histogramas comparativos

![Histogramas Atividade3](Atividade3/resultados_q2/histogramas_comparativos.png)

#### Gráfico radar dos descritores normalizados

![Radar descritores](Atividade3/resultados_q2/radar_descritores.png)

#### Tabela de Descritores

| Descritor | imagem1 | imagem2 |
|-----------|---------|---------|
| Média | 135.1213 | 132.5076 |
| Variância | 5475.6816 | 6514.1655 |
| Desvio padrão | 73.9978 | 80.7104 |
| Energia | 23733.4408 | 24072.4179 |
| Entropia (bits) | 7.4769 | 7.512 |
| Variação espacial total | 4.3851 | 11.9541 |

---
