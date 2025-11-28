# 🤖 Projeto McBot - Sistema Full Stack

Sistema integrado para gestão e processamento de dados da MC Sonae.
O projeto consiste em uma API robusta (Backend) e um Dashboard interativo (Frontend).

## 🛠️ Tecnologias Utilizadas
- **Backend:** Python, Flask, SQLAlchemy, JWT (Segurança).
- **Frontend:** Streamlit, Pandas, Plotly.
- **Banco de Dados:** MySQL.

---

## 🚀 Como Rodar o Projeto

### 1. Pré-requisitos
Certifique-se de ter o Python e o MySQL instalados.
Crie um banco de dados no MySQL chamado `mc_sonae`.

### 2. Instalação
Clone o repositório e instale as dependências:

```bash
# Clone o projeto
git clone [https://github.com/Evandroj07/Projeto-McBot.git](https://github.com/Evandroj07/Projeto-McBot.git)

# Entre na pasta
cd Projeto-McBot

# Crie e ative o ambiente virtual
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Instale as bibliotecas
pip install -r requirements.txt
pip install streamlit requests pandas plotly