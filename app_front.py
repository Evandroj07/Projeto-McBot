import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hashlib 
import requests

BASE_URL = "http://127.0.0.1:5000/api"

# --- 0. CONFIGURAÇÃO DE PÁGINA ÚNICA ---
# Deve ser a primeira chamada do script
st.set_page_config(
    page_title="McBot | Dashboard de Projetos MC Sonae",
    page_icon="🤖", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- Paleta de Cores MC Sonae ---
PRIMARY_COLOR = "#E30613"   # Vermelho MC Sonae
SECONDARY_COLOR = "#007bff"  # Azul (Detalhes e Chamada Secundária)
BACKGROUND_COLOR = "#f4f4f4" # Cinza Claro (Fundo do Dashboard)
TEXT_COLOR = "#333333"      # Cinza Escuro (Texto Principal)
ACCENT_COLOR = "#ffc107"    # Amarelo (Para Warnings ou Status)

# --- 1. CONFIGURAÇÃO DE SEGURANÇA E BANCO DE DADOS SIMULADO ---

def hash_password(password):
    # Simula o hashing seguro da senha
    return hashlib.sha256(password.encode()).hexdigest()

# Usuários iniciais (Base de dados simulada)
USUARIOS_DB = {
    "ana.gerente": (hash_password("ana123"), "Gerente"), 
    "juan.diretor": (hash_password("juan123"), "Diretor"), 
    "laura.op": (hash_password("laura123"), "Operacional"), 
    "rafael.bi": (hash_password("rafael123"), "Analista BI") 
}

# Inicialização do st.session_state (para persistência na sessão)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'usuarios_db' not in st.session_state:
    st.session_state['usuarios_db'] = USUARIOS_DB
if 'show_login' not in st.session_state:
    st.session_state['show_login'] = True 


# --- 2. FUNÇÕES DE AUTENTICAÇÃO (INTEGRAÇÃO API REAL) ---

def authenticate(email, password):
    """Tenta fazer login na API Flask"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "senha": password})
        
        if response.status_code == 200:
            data = response.json()
            st.session_state['logged_in'] = True
            st.session_state['token'] = data['access_token'] # Salva o Token
            st.session_state['profile'] = data['user_role']  # Salva a Role (Admin/User)
            st.session_state['username'] = email # Usa o email como nome
            return True
        else:
            return False
    except Exception as e:
        st.error(f"Erro de conexão com a API: {e}")
        return False

def create_user(nome, email, password, profile):
    """Tenta registrar usuário na API Flask"""
    payload = {
        "nome": nome,
        "email": email,
        "senha": password,
        "nome_funcao": "Admin" if profile == "Gerente" or profile == "Diretor" else "User"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if response.status_code == 201:
            return True, "Usuário criado com sucesso!"
        else:
            msg_erro = response.json().get("msg", "Erro desconhecido")
            return False, f"Erro: {msg_erro}"
    except Exception as e:
        return False, f"Erro de conexão: {e}"

# --- 3. CSS EMBUTIDO (FONTE E ESTÉTICA PROFISSIONAL) ---

# 3.1. CSS para a Tela de LOGIN (Mais forte e chamativa)
LOGIN_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
html, body, [class*="st-"], .main {{
    font-family: 'Inter', sans-serif !important;
}}

/* Fundo total da página de login */
.stApp {{
    background-color: #f0f2f6; 
}}
/* Container de Login */
.login-container {{
    max-width: 450px; 
    margin: 80px auto; 
    padding: 40px; 
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25); 
    border-radius: 12px; 
    background-color: #fff; 
    border-left: 10px solid {PRIMARY_COLOR}; /* Borda Vermelha forte */
}}
.login-header {{
    text-align: center; 
    color: {PRIMARY_COLOR}; 
    margin-bottom: 30px;
    font-size: 2.2em; 
    font-weight: 800; 
}}
/* Botões de Ação */
div.stButton > button[kind="primary"], div.stButton > button[kind="secondary"] {{
    width: 100%; 
    height: 3.2em; 
    font-size: 1.1em;
    border-radius: 8px;
    border: none;
    transition: background-color 0.3s;
}}
div.stButton > button[kind="primary"] {{
    background-color: {PRIMARY_COLOR}; 
    color: white; 
}}
div.stButton > button[kind="secondary"] {{
    background-color: {SECONDARY_COLOR}; 
    color: white; 
    margin-top: 15px; /* Espaço para o botão de cadastro */
}}
/* Entrada de Texto */
.stTextInput > div > div > input {{
    border-radius: 6px;
    border: 1px solid #ccc;
    padding: 10px;
}}
</style>
"""

# 3.2. CSS para o DASHBOARD (Elaborado e Detalhado)
DASHBOARD_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
html, body, [class*="st-"], .main {{
    font-family: 'Inter', sans-serif !important;
}}
/* 1. Fundo Principal */
.main {{
    background-color: {BACKGROUND_COLOR};
    color: {TEXT_COLOR};
    padding: 2em 3em; 
}}
/* 2. Sidebar (Mais profissional) */
[data-testid="stSidebar"] {{
    background-color: #ffffff; 
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
}}
/* 3. Título Principal */
h1 {{
    color: {PRIMARY_COLOR}; 
    border-bottom: 3px solid {SECONDARY_COLOR}; 
    padding-bottom: 12px;
    margin-top: 0;
    font-weight: 700;
}}
/* 4. Subtítulos */
h2, h3, h4 {{
    color: {TEXT_COLOR};
    font-weight: 600;
}}
/* 5. Estilo para as métricas KPI (Cards com elevação) */
.stMetric {{
    background-color: #ffffff; 
    padding: 15px;
    border-radius: 8px;
    border-left: 5px solid {SECONDARY_COLOR}; 
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08); 
    transition: transform 0.2s;
}}
.stMetric:hover {{
    transform: translateY(-2px); 
}}
.stMetric > div[data-testid="stMetricValue"] {{
    font-size: 2.5em; 
    font-weight: bold;
    color: {PRIMARY_COLOR}; 
}}
/* 6. Estilo do Feed de Atividades (st.info) */
.stInfo {{
    border-left: 5px solid {ACCENT_COLOR}; /* Amarelo/Laranja para 'info' */
    background-color: #fff8e1; /* Fundo mais suave para info */
    border-radius: 6px;
    box-shadow: none;
    color: {TEXT_COLOR};
    padding: 10px;
}}
/* 7. Esconde lixo */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
</style>
"""

# --- 4. FUNÇÕES DE INTERFACE DE LOGIN E CADASTRO ---

def login_form():
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="seu@email.com")
        password = st.text_input("Senha", type="password", placeholder="Insira sua senha")
        
        submit_button = st.form_submit_button("Entrar no Dashboard", type="primary")

        if submit_button:
            if authenticate(email, password):
                st.success(f"Bem-vindo, {email}! Acesso liberado.")
                st.rerun()
            else:
                st.error("❌ Usuário ou senha incorretos. Tente novamente.")
    
    st.markdown('<div style="text-align: center; margin-top: 25px;">', unsafe_allow_html=True)
    if st.button("Não tem conta? Crie a sua!", key="go_to_register", type="secondary", help="Clique aqui para cadastrar um novo usuário."):
        st.session_state['show_login'] = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f'<p style="text-align: center; margin-top: 20px; font-size: 0.9em; color: #888;">Credenciais de Teste: ana.gerente / ana123</p>', unsafe_allow_html=True)


def register_form():
    # Estiliza o botão de Cadastro
    with st.form("register_form", clear_on_submit=True):
        st.markdown("##### **Defina suas Credenciais**")
        
        # --- CORREÇÃO: Adicionados campos separados para Nome e Email ---
        novo_nome = st.text_input("Nome Completo", placeholder="Ex: Ana Silva")
        novo_email = st.text_input("Email (Login)", placeholder="ana@mcsonae.com")
        novo_password = st.text_input("Senha (mínimo 6 caracteres)", type="password")
        
        perfil_selecionado = st.selectbox(
            "Perfil Desejado:",
            ["Operacional", "Analista BI", "Gerente", "Diretor"]
        )
        
        create_button = st.form_submit_button(label='Finalizar Cadastro', type="primary")

        if create_button:
            # --- CORREÇÃO: Agora enviamos os 4 argumentos que a função pede ---
            if not novo_nome or not novo_email or not novo_password:
                st.warning("Por favor, preencha todos os campos.")
            else:
                success, message = create_user(novo_nome, novo_email, novo_password, perfil_selecionado)
                
                if success:
                    st.balloons()
                    st.success(message + " Você pode fazer login agora.")
                    st.session_state['show_login'] = True 
                    st.rerun() # Atualizado de experimental_rerun() para rerun()
                else:
                    st.error("❌ " + message)
    
    st.markdown('<div style="text-align: center; margin-top: 25px;">', unsafe_allow_html=True)
    if st.button("Já sou cadastrado. Fazer Login.", key="go_to_login", type="secondary", help="Clique aqui para voltar para a tela de Login."):
        st.session_state['show_login'] = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def login_page_master():
    # 1. Esconde a sidebar e aplica CSS de login
    st.markdown('<style>section[data-testid="stSidebar"] {display: none;}</style>', unsafe_allow_html=True)
    st.markdown(LOGIN_CSS, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2: 
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        if st.session_state['show_login']:
            st.markdown(f'<h3 class="login-header">McBot – Acesso Exclusivo</h3>', unsafe_allow_html=True)
            login_form()
        else:
            st.markdown(f'<h3 class="login-header">McBot – Novo Cadastro</h3>', unsafe_allow_html=True)
            register_form()
            
        st.markdown('</div>', unsafe_allow_html=True)


# --- 5. FUNÇÕES DO DASHBOARD (Módulos de Trabalho) ---

# Dados Simulados
df_projetos = pd.DataFrame({
    'Projeto': ['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'],
    'Gerente': ['Ana', 'João', 'Maria', 'Pedro', 'Sofia'],
    'Progresso (%)': [90, 45, 75, 20, 55],
    'Status': ['Concluído', 'Em Andamento', 'Em Andamento', 'Atrasado', 'Em Andamento'],
    'Investimento (K)': [500, 300, 150, 700, 250],
    'Atraso (dias)': [0, 5, 0, 15, 0]
})

# NOTA: Os ícones profissionais são representados por códigos Unicode do Font Awesome.

def dashboard_gerencial():
    st.title(f"Dashboard Geral \uF080 (Perfil: {st.session_state['profile']})") # Icone de gráfico de barras
    st.markdown("##### *Visão em Tempo Real - Status da Equipe*")
    
    projetos_ativos = df_projetos.shape[0]
    conclusao_prazo = f"{df_projetos[df_projetos['Status'] != 'Atrasado'].shape[0] / projetos_ativos * 100:.0f}%"
    acuracia_simulada = "98%"
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="Projetos Ativos", value=projetos_ativos)
    with col2: st.metric(label="Conclusão no Prazo", value=conclusao_prazo, delta="↑ 5% (última semana)")
    with col3: st.metric(label="Média de Acurácia dos Dados", value=acuracia_simulada)
    st.markdown("---")
    st.subheader("Progresso dos Projetos (Detalhado)")
    
    fig_progresso = px.bar(
        df_projetos.sort_values(by='Progresso (%)', ascending=False), x='Projeto', y='Progresso (%)',
        color='Progresso (%)', color_continuous_scale=[PRIMARY_COLOR, SECONDARY_COLOR, "#00cc00"], 
        text='Progresso (%)', height=450, title="Percentual de Conclusão por Projeto"
    )
    fig_progresso.update_layout(plot_bgcolor='white', paper_bgcolor=BACKGROUND_COLOR, title_font_color=TEXT_COLOR)
    st.plotly_chart(fig_progresso, use_container_width=True)
    
    st.markdown("### Status da Equipe (Feed de Atividades)")
    mock_statuses = [
        f"**{datetime.now().strftime('%H:%M')}** | Ana - Progresso de 10% lançado no Projeto Beta.",
        "**08:00** | Laura - Lançamento de dados finalizado para 3 tarefas críticas."
    ]
    for status in mock_statuses: st.info(status)

def painel_executivo():
    st.title("Painel Estratégico \uF200") # Icone de gráfico de linha
    st.subheader("Indicadores Estratégicos (KPIs) para Tomada de Decisão")
    
    total_investido = df_projetos['Investimento (K)'].sum()
    projetos_criticos = df_projetos[df_projetos['Atraso (dias)'] > 0].shape[0]
    roi_simulado = "85%"
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="Investimento Total (Milhares)", value=f"R$ {total_investido:,}", delta="Orçamento: R$ 2.0M")
    with col2: st.metric(label="ROI Simulado", value=roi_simulado, delta="Meta: 90%")
    with col3: 
        st.markdown(f'<p style="color: {PRIMARY_COLOR}; font-size: 0.9em; margin-bottom: -10px;">Projetos Críticos (Atraso)</p>', unsafe_allow_html=True)
        st.metric(label="Projetos Críticos (Atraso)", value=projetos_criticos, delta_color="inverse", delta=f"{projetos_criticos} projetos")
    st.markdown("---")
    st.subheader("Relação Investimento vs. Progresso")
    
    fig_portfolio = px.scatter(
        df_projetos, x='Investimento (K)', y='Progresso (%)', size='Investimento (K)', color='Status',
        color_discrete_map={'Concluído': '#00cc00', 'Em Andamento': SECONDARY_COLOR, 'Atrasado': PRIMARY_COLOR},
        hover_name='Projeto', height=500, title="Análise de Desempenho do Portfólio"
    )
    fig_portfolio.update_layout(paper_bgcolor=BACKGROUND_COLOR)
    st.plotly_chart(fig_portfolio, use_container_width=True)
        
# (CÓDIGO NOVO - COPIE E COLE NO LUGAR DA FUNÇÃO ANTIGA)
def lancamento_dados():
    st.title("Lançamento de Dados \uF044")
    st.subheader("Enviar dados para processamento na API")
    
    # Cria o formulário
    with st.form(key='data_input_form', clear_on_submit=True):
        st.markdown("#### **Registro de Tarefas (Limpeza de Dados)**")
        
        # Campo de texto para digitar o dado "sujo"
        dado_bruto = st.text_area("Insira o texto/dado bruto para processar:", height=100)
        
        # Botão de enviar
        submit_button = st.form_submit_button(label='Processar e Salvar')
        
        if submit_button:
            # 1. Verifica se o campo não está vazio
            if not dado_bruto:
                st.warning("O campo não pode estar vazio.")
            else:
                # 2. Prepara o Token de Segurança (para provar que está logado)
                token = st.session_state.get('token')
                headers = {"Authorization": f"Bearer {token}"}
                
                # 3. Envia para o SEU Backend (API)
                try:
                    response = requests.post(
                        f"{BASE_URL}/dados/processar", 
                        json={"dado": dado_bruto}, 
                        headers=headers
                    )
                    
                    # 4. Verifica a resposta do servidor
                    if response.status_code == 201:
                        # Sucesso! Mostra o dado limpo que voltou da API
                        dado_limpo = response.json()['dado_processado']['dado_limpo']
                        st.success(f"✅ Sucesso! O dado foi limpo e salvo: '{dado_limpo}'")
                    
                    elif response.status_code == 409:
                        st.warning("⚠️ Atenção: Este dado já existe no banco de dados.")
                    
                    elif response.status_code == 403:
                        st.error("🚫 Acesso Negado: Seu usuário não tem permissão de Admin.")
                        
                    elif response.status_code == 401:
                        st.error("🔒 Sessão expirada. Faça login novamente.")
                        
                    else:
                        st.error(f"Erro desconhecido: {response.text}")
                        
                except Exception as e:
                    st.error(f"Não foi possível conectar ao servidor: {e}")
            
def relatorios_customizaveis():
    st.title("Dados do Banco Real (MySQL)")
    
    headers = {"Authorization": f"Bearer {st.session_state.get('token')}"}
    try:
        response = requests.get(f"{BASE_URL}/dados/processados", headers=headers)
        if response.status_code == 200:
            dados = response.json()
            if dados:
                df_real = pd.DataFrame(dados)
                st.dataframe(df_real[['id', 'dado_bruto', 'dado_limpo', 'data_processamento']])
            else:
                st.info("Nenhum dado processado no banco ainda.")
    except:
        st.error("Não foi possível conectar ao Backend.")

def gestao_acesso():
    st.title("Gestão de Acesso \uF023") # Icone de cadeado
    st.subheader("Revisão de Perfis de Usuários (Acesso Restrito)")
    
    if st.session_state['profile'] != "Gerente":
        st.error("🚫 Acesso negado! Apenas o perfil 'Gerente' pode gerenciar usuários.")
        return

    st.markdown("---")
    st.subheader("Lista Completa de Acessos")
    df_users = pd.DataFrame(
        [(user, data[1]) for user, data in st.session_state['usuarios_db'].items()],
        columns=['Usuário (Login)', 'Perfil']
    )
    st.dataframe(df_users, use_container_width=True)


# --- 6. FUNÇÃO PRINCIPAL DO DASHBOARD (Controle de Navegação) ---

def main_app():
    # Aplica o CSS do Dashboard
    st.markdown(DASHBOARD_CSS, unsafe_allow_html=True)
    
    # SIDEBAR - SIMULANDO IMAGEM/LOGO
    
    # Se você tiver um arquivo chamado 'logo_mcbot.png' na mesma pasta, use:
    # st.sidebar.image("logo_mcbot.png", use_column_width=True)
    # st.sidebar.markdown("---")

    # MOCK (Substitua se tiver a imagem):
    st.sidebar.markdown(f'<div style="background-color: {PRIMARY_COLOR}; padding: 15px; border-radius: 5px; text-align: center;">'
                        f'<h2 style="color: white; margin: 0; font-weight: 800;">McBot</h2>'
                        f'<p style="color: #fff; margin: 5px 0 0 0; font-size: 0.9em;">by MC Sonae Projects</p>'
                        f'</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Usuário:** {st.session_state['username']}")
    st.sidebar.markdown(f"**Perfil:** {st.session_state['profile']}")
    st.sidebar.markdown("---")

    # Botão de Logout
    if st.sidebar.button("Sair (Logout)", use_container_width=True, type="secondary"):
        st.session_state['logged_in'] = False
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.header("Módulos de Trabalho")

    modulos = ["Dashboard Geral", "Painel Estratégico", "Lançamento de Dados", "Relatórios BI"]
    
    if st.session_state['profile'] == "Gerente":
        modulos.append("Gestão de Acesso")

    initial_module_map = {"Gerente": 0, "Diretor": 1, "Operacional": 2, "Analista BI": 3}
    initial_index = initial_module_map.get(st.session_state['profile'], 0)
        
    menu_selection = st.sidebar.radio("Selecione o Módulo:", modulos, index=initial_index)

    # Roteamento
    if menu_selection == "Dashboard Geral":
        dashboard_gerencial()
    elif menu_selection == "Painel Estratégico":
        painel_executivo()
    elif menu_selection == "Lançamento de Dados":
        lancamento_dados()
    elif menu_selection == "Relatórios BI": 
        relatorios_customizaveis()
    elif menu_selection == "Gestão de Acesso":
        gestao_acesso()

    st.sidebar.markdown("---")
    st.sidebar.caption("© 2025 McBot. Todos os direitos reservados.")


# --- 7. INÍCIO DO SCRIPT (CONTROLE DE ESTADO) ---
if not st.session_state['logged_in']:
    login_page_master()
else:
    main_app()