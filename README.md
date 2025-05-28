Titulo do Projeto: FoxTower
Autores: João Pedro Medicini, Luan Miguel Ferraro Pereira, Luis Felipe Carreira Rosa.
Link do vídeo do jogo rodando: https://youtu.be/Q-YBm0VWgJo?si=1ZqTZUpifLlzpVx9

Para rodar o jogo, rode a pasta principal.py
para jogar use o botão esquerdo e direito do mouse para ataque e espaço para o ataque especial, o c para ativação do escudo e o g para o consumo de poções.


Estruturas Bases das classes(Dragão,inimigolonge e mago) feito com auxilio de GPT, principalmente para um aprendizado efeitivo do funcionamento do pygame, porém todos os incrementos feitos posteriormente foram feitos sem o auxilio de IA:
Criação da classe mago(20%-40% IA): https://chatgpt.com/c/6829d38a-5448-8004-acc5-1dc42602a92f(a partir da mensagem "adicione vida ao mago e a cada um dos inimigos assim como dano aos seus ataques" nao foi utilizado)
Criação da classe Dragão e da Classe longo_alcance(20% IA e 60-70% IA respectivamente): https://chatgpt.com/c/682b8235-f80c-8004-87b0-74d9e08d8734(muito do conteudo não foi utilizado)

Chatgpt também foi utilizado no auxilio de estruturas pontuais e correção erros cujo demorariam para ser consertados ou encontrados:
construção do escudo do personagem(60% IA): https://chatgpt.com/c/6834bcf7-e8b8-8004-83ab-0993fb924fe3
hitbox do dragão(60% IA): https://chatgpt.com/c/68367943-1b9c-800b-8d10-eca7eeeae9a0

Chatgpt também foi utilizado para criação de imagens como inicio e fim de jogo:
https://chatgpt.com/c/6836fa8e-a0d8-800b-b7cb-d63deddcddb5

imagem do protagonista do jogo foi criado por Chatgpt mas animada manualmente por Luís Felipe: https://chatgpt.com/share/68379533-ecc4-8002-9561-e0d0ca1b6e8b
Tela inicial criada por Chatgpt: https://chatgpt.com/share/68379576-31d0-8002-ab9b-565e9e14e23f
Inimigos pego de repôsitorio online gratis: 
- Slime: https://stealthix.itch.io/animated-slimes
- Boss: https://luizmelo.itch.io/evil-wizard-2
- Bixo voador: https://pixfinity.itch.io/the-dungeon-pack-1
Mapa feito com itens de repôsitorio online gratis: https://cainos.itch.io/pixel-art-top-down-basic
Mapa 2 feito com imagem gerada por ia: https://chat.insper.tech/c/feee4ef7-4d5c-4c0e-b25e-ecad00ffeff3

Função def cortar_spritesheet feito 100% por ia. Ela pega uma imagem cheia de sprites e recorta ela em pedaços e cada pedaço é adicionado dentro de uma lista para ser usada na movimentação do personagem.
Sistema de animação do boss feito 100% por ia.

As músicas e efeitos sonoros utilizados no jogo foram retirados dos seguintes locais:
-musica do campo:https://music.youtube.com/watch?v=Jo8pgqc5rNc&si=J2Qkgp4EgIjcatV7
-música do castelo:https://youtu.be/ai31C3hJXSs?si=X1bb66LJVO5D4XKY
-efeitos sonoros em geral foram retirados dos sites:
.https://mixkit.co/free-sound-effects/discover/gulp/
.https://freesound.org/search/?q=gulp

Observação: o nome de cada arquivo representa sua função principal, declarar assets em assets.py, contantes em contes.py e classes em classes.py

