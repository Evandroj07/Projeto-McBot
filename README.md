# 🤖 Projeto McBot - Sistema de Inteligência e Gestão

Bem-vindo ao **McBot**! 👋
Este é um sistema completo (Full Stack) desenvolvido para automatizar a leitura de relatórios e organizar dados da empresa **MC Sonae**.

---

## 🤔 O que este projeto faz?
Imagine que você tem uma pilha de relatórios em PDF, Word ou Excel e precisa ler um por um para anotar datas e valores. O **McBot** faz isso automaticamente:

1.  **Lê Arquivos:** Você envia um documento (.pdf, .docx, .xlsx).
2.  **Usa Inteligência (IA):** O sistema lê o conteúdo, identifica **Datas**, **Valores em Dinheiro** e termos como **"Urgente"**.
3.  **Organiza:** Salva tudo padronizado em um banco de dados.
4.  **Mostra:** Exibe gráficos e tabelas em um painel visual (Dashboard).

---

## 🏗️ Como o sistema funciona?
O projeto é dividido em três partes que trabalham juntas:

- **1. O Cérebro (Backend):** Feito em **Python (Flask)**. É onde ficam as regras de segurança, a IA de leitura e a conexão com o banco.
- **2. A Tela (Frontend):** Feita em **Streamlit**. É o site bonito onde o usuário clica nos botões e vê os gráficos.
- **3. A Memória (Banco de Dados):** Feito em **MySQL**. É onde as informações ficam guardadas.

---

## 🛠️ Passo a Passo para Instalar (Guia para Iniciantes)

Siga estes passos na ordem exata para configurar o projeto no seu computador.

### Passo 1: Preparar o Banco de Dados
O sistema precisa de um lugar para salvar os dados.
1. Abra o seu **MySQL Workbench** (ou terminal MySQL).
2. Rode este comando para criar a base de dados:
   ```sql
   CREATE DATABASE mc_sonae;

---

### Passo 2: Baixar o Código
Abra seu terminal (PowerShell ou Git Bash) e digite:

**Terminal/VsCode**:

git clone https://github.com/Evandroj07/Projeto-McBot.git 

cd Projeto-McBot

---

### Passo 3: Criar o Ambiente Virtual
Para não misturar as ferramentas deste projeto com outras coisas do seu computador, criamos uma "caixa isolada":

No Windows:

**Terminal/VsCode**:

python -m venv venv
.\venv\Scripts\Activate.ps1
(Se aparecer um texto verde (venv) no começo da linha, deu certo!)

---

### Passo 4: Instalar as Dependências
Agora vamos baixar os "poderes" do projeto (leitores de PDF, gráficos, IA, etc). Isso pode demorar um pouco:

**Terminal/VsCode**:

pip install -r requirements.txt

---

### Passo 5: Configurar a Senha
O sistema precisa da senha do seu banco de dados local para funcionar.

Na pasta do projeto, abra o arquivo chamado config.py.

Procure a linha que diz SQLALCHEMY_DATABASE_URI.

Onde estiver escrito SUA_SENHA, troque pela senha do seu MySQL.

Exemplo: De ...root:SUA_SENHA@... para ...root:123456@...

Salve o arquivo.

---

### ▶️ Como Rodar o Sistema
Como temos um "Backend" e um "Frontend", precisamos de dois terminais abertos ao mesmo tempo.

**Janela 1**: Ligando a API (Backend)
No terminal (com o venv ativo), digite:

Terminal/VsCode:

python run.py
Aguarde aparecer: Running on http://127.0.0.1:5000

Não feche esta janela!

**Janela 2**: Ligando o Painel (Frontend)
Abra uma nova janela de terminal, ative o ambiente (.\venv\Scripts\Activate.ps1) e digite:

**Terminal/VsCode**:

streamlit run app_front.py
O navegador abrirá automaticamente com o site!

---

### 🧪 Como Usar a IA (Leitura de Documentos)
**Cadastro**: No site, clique em "Não tem conta?" e crie um usuário.

Importante: Escolha o perfil Gerente ou Diretor (apenas eles têm permissão para processar dados).

**Login**: Entre com seu email e senha.

Upload:

No menu lateral, vá em Lançamento de Dados.

Escolha a aba 📄 Upload de Arquivo.

Envie um PDF, Word ou Excel que tenha uma data e um valor em dinheiro.

Resultado: O sistema vai ler o arquivo e mostrar um resumo automático na tela.

---

### 📞 Suporte
Projeto desenvolvido por Evandro e Clara.