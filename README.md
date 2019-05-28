# thermo_images
Repository to thermoimages project

https://www.workana.com/job/processamento-de-imagem-1?dateFrom=2019-05-22&dateTo=2019-05-22&page=1&status=pending

### Projeto:
* 0. Definições de Inputs:(início previsto 20/05 - inicio real 22/05)
    * 0.1 Avaliar as Imagens de Teste
    * 0.2 Definir os padrões de imagens a serem trabalhados
    * 0.3 Criar Script Principal do Projeto
    * 0.4 GATE de Validação(data prevista 22/05)
* 1. Contorno do Corpo (data prevista 23/05)
    * 1.1 Utilizar OpenCV para contorno do corpo;
    * 1.2 Relacionar contorno do corpo com padrões definidos
    * 1.3 Script:
        Input -> Imagem
        Output-> contornos e classificação
    * 1.4 GATE de Validação (data prevista 25/05)
* 2. Segmentação das Áreas
    * 2.1 Pesquisa sobre métodos de segmentação;
    * 2.2 Segmentação por contornos
    * 2.3 Script:
        Input -> Imagem
        Output-> imagens segmentadas
    * 2.4 GATE de validação (data prevista 29/05)
* 3. Atribuição das temperaturas por região (data prevista 30/05):
  * 3.1 Pesquisa sobre métodos de cores e temperatura;
  * 3.2 Teste com luminosidade de para temperatura
  * 3.3 Relacionar Luminosidade e Legenda;
  * 3.4 Script para temperatura média:
      Input-> Imagens
      Output-> CSV com temperatura média por imagem
  * 3.5 GATE de Validação (data prevista 02/06)
* 4. Ajustes Finais (data prevista 03/06):
  * 4.1 Criação de Manual de Uso
  * 4.2 Suporte e teste com cliente
  * 4.3 GATE de Validação (data prevista 05/06)
  
  
# PROJECT EVOLUTION

    0. Definições de Inputs:(início previsto 20/05 - inicio real 22/05)
        0.1 Avaliar as Imagens de Teste;
            [OK] As Imagens Disponíveis são: dorso_costa,dorso_frent, pé , perna_costa e perna_ frente.
            [OK] As dimensões das Imagens são 480x640 sempre?
            [OK] Nas segmentações enviadas não há a divisão da planta do pé.
        0.2 Definir os padrões de imagens a serem trabalhados
            O código vai ser cirado para trabalhar com imagens de 5 tipos:
                - PÉ (dimensão 640x480)
                - DORSO FRONTAL (dimensao 480x640)
                - DORSO POSTERIOR (dimensao 480x640)
                - PERNA FRONTAL (dimensao 480x640)
                - PERNA POSTERIOR (dimensao 480x640)
        0.3 Criar Script Principal do Projeto
            thermo_images/
            ├── .gitignore
            ├── thermo_images/
            |   ├── __init__.py
            |   ├── thermo_images.py
            |   ├── auxiliar.py
            |   ├── classification.py
            |   ├── segmentation.py
            |   ├── temperatures.py
            ├── testes/
            |   ├── testes.py
            |   ├── images/
            ├── LICENSE
            ├── README.md
            ├── requirements.txt
            ├── setup.py
            
            0.3.1 Padrão de Documentação:
                Google Style Python Docstrings
                (https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
        0.4 GATE de Validação(data prevista 22/05)
        
        
    1.Contorno do Corpo (data prevista 23/05)
        1.1 Utilizar OpenCV para contorno do corpo;
        1.2 Relacionar contorno do corpo com padrões definidos;
        1.3 Script: Input -> Imagem Output-> contornos e classificação;
        1.4 GATE de Validação (data prevista 25/05;

# REFERENCES

[1. Contours](https://docs.opencv.org/3.4/d1/d32/tutorial_py_contour_properties.html)

[2. Documentation](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)

[3. Skeletonization](http://opencvpython.blogspot.com/2012/05/skeletonization-using-opencv-python.html)

[4. Topological Skeleton](https://en.wikipedia.org/wiki/Topological_skeleton)


