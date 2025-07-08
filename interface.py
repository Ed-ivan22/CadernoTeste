import streamlit as st

# --- Dados das Questões ---
questoes_prova = [
    {
        "pergunta": "Qual a capital do Brasil?",
        "opcoes": ["Rio de Janeiro", "São Paulo", "Brasília", "Belo Horizonte"],
        "resposta_correta_index": 2
    },
    {
        "pergunta": "Quem escreveu 'Dom Quixote'?",
        "opcoes": ["William Shakespeare", "Miguel de Cervantes", "Machado de Assis", "Gabriel García Márquez"],
        "resposta_correta_index": 1
    },
    {
        "pergunta": "Quantos continentes existem no mundo?",
        "opcoes": ["5", "6", "7", "4"],
        "resposta_correta_index": 2
    },
    {
        "pergunta": "Qual o maior oceano do mundo?",
        "opcoes": ["Oceano Atlântico", "Oceano Índico", "Oceano Ártico", "Oceano Pacífico"],
        "resposta_correta_index": 3
    },
    {
        "pergunta": "Qual o animal mais rápido do mundo?",
        "opcoes": ["Guepardo", "Falcão Peregrino", "Leão", "Antílope"],
        "resposta_correta_index": 1
    },
    {
        "pergunta": "Qual elemento químico é simbolizado por 'Au'?",
        "opcoes": ["Prata", "Cobre", "Ouro", "Alumínio"],
        "resposta_correta_index": 2
    },
    {
        "pergunta": "Em que ano o homem pisou na Lua pela primeira vez?",
        "opcoes": ["1959", "1969", "1979", "1989"],
        "resposta_correta_index": 1
    },
    {
        "pergunta": "Qual o país com a maior população do mundo (aproximadamente em 2024)?",
        "opcoes": ["Estados Unidos", "China", "Índia", "Indonésia"],
        "resposta_correta_index": 2
    },
    {
        "pergunta": "Qual a cor primária que falta: Azul, Amarelo, ___?",
        "opcoes": ["Verde", "Laranja", "Vermelho", "Roxo"],
        "resposta_correta_index": 2
    },
    {
        "pergunta": "Qual o maior planeta do nosso Sistema Solar?",
        "opcoes": ["Marte", "Terra", "Júpiter", "Saturno"],
        "resposta_correta_index": 2
    }
]

# --- Configuração da Página Streamlit ---
st.set_page_config(layout="centered", page_title="Caderno de Provas")
st.title("📚 Caderno de Provas MVP")
st.markdown("---")

# --- Inicializa o estado da sessão ---
# 'quiz_submetido' controla quando os resultados devem ser mostrados
if 'quiz_submetido' not in st.session_state:
    st.session_state.quiz_submetido = False

# 'respostas_selecionadas' irá armazenar o VALOR da opção escolhida pelo usuário para cada rádio-botão
# A chave de cada rádio-botão será 'q_0', 'q_1', etc. e seu valor será a opção selecionada.
# Não precisamos de um dicionário aninhado para isso.
# O Streamlit armazena automaticamente o valor de um widget em st.session_state[key]
# se uma 'key' for fornecida.

# --- Exibir as Questões ---
st.subheader("Responda às questões abaixo:")

# Itera sobre as questões para criar a interface de rádio-botões
for i, questao in enumerate(questoes_prova):
    st.markdown(f"**{i+1}. {questao['pergunta']}**")
    
    # Pega o VALOR da resposta que o usuário selecionou anteriormente para esta questão (se houver)
    # Isso é crucial para que o st.radio mantenha a seleção após um re-run (como o clique no botão Responder)
    resposta_previa_valor = st.session_state.get(f'q_{i}')
    
    # Encontra o índice da resposta prévia na lista de opções para pré-selecionar o rádio-botão
    initial_index = None
    if resposta_previa_valor in questao['opcoes']:
        initial_index = questao['opcoes'].index(resposta_previa_valor)

    # Cria o rádio-botão para a questão atual
    # O 'key' é fundamental para que o Streamlit salve e recupere o estado de cada widget individual
    st.radio(
        label=f"Opções da Questão {i+1}", # Label interno que pode ser escondido
        options=questao['opcoes'],
        index=initial_index, # Define qual opção estará selecionada inicialmente (do estado anterior)
        key=f'q_{i}', # Chave única para este rádio-botão no st.session_state
        label_visibility="collapsed" # Esconde o label para não duplicar com o markdown da pergunta
    )
    st.markdown("---") # Divisor visual

# --- Botão Responder ---
# Quando este botão é clicado, ele altera o estado 'quiz_submetido' para True
# e força uma nova execução do script para mostrar os resultados.
if st.button("Responder Prova", type="primary", use_container_width=True):
    st.session_state.quiz_submetido = True
    st.balloons() # Pequena animação de balões!
    # st.rerun() # Opcional: pode ser omitido se o código abaixo já for renderizado condicionalmente
    #              mas ajuda a garantir que a tela de resultados apareça "na hora".

# --- Exibir Resultados (apenas se o quiz foi submetido) ---
if st.session_state.quiz_submetido:
    st.markdown("## ✅ Gabarito e Suas Respostas")
    st.info("Sua pontuação e o gabarito detalhado estão abaixo.")
    
    pontuacao = 0
    
    for i, questao in enumerate(questoes_prova):
        pergunta = questao['pergunta']
        opcoes = questao['opcoes']
        resposta_correta_index = questao['resposta_correta_index']
        resposta_correta_texto = opcoes[resposta_correta_index]
        
        # Obtém a resposta do usuário diretamente do st.session_state usando a chave do widget
        # Se o usuário não selecionou nada, o valor será None
        resposta_usuario_selecionada = st.session_state.get(f'q_{i}')
        
        st.markdown(f"### {i+1}. {pergunta}")
        
        # Encontra o índice da resposta selecionada pelo usuário nas opções da questão
        indice_usuario = -1 # Valor padrão se nada for selecionado ou valor inválido
        if resposta_usuario_selecionada in opcoes:
            indice_usuario = opcoes.index(resposta_usuario_selecionada)

        # Exibir opções e destacar a correta e a do usuário
        for j, opcao in enumerate(opcoes):
            if j == resposta_correta_index:
                # Resposta correta
                st.markdown(f"- **<span style='color: green;'>{opcao} (Correta)</span>**", unsafe_allow_html=True)
            elif j == indice_usuario and j != resposta_correta_index:
                # Resposta do usuário, se estiver errada
                st.markdown(f"- <span style='color: red;'>{opcao} (Sua Resposta Incorreta)</span>", unsafe_allow_html=True)
            else:
                # Outras opções não selecionadas ou incorretas
                st.write(f"- {opcao}")
        
        # Feedback de acerto ou erro para cada questão
        if indice_usuario == resposta_correta_index:
            pontuacao += 1
            st.success("✅ Você acertou!")
        else:
            if resposta_usuario_selecionada is not None: # Verifica se algo foi selecionado, mesmo que errado
                st.error(f"❌ Você errou. Sua resposta: '{resposta_usuario_selecionada}'")
            else:
                st.warning("❓ Você não respondeu a esta questão.")
        st.markdown("---") # Divisor após cada questão no resultado

    st.markdown(f"## Sua Pontuação Final: {pontuacao} de {len(questoes_prova)}")
    if pontuacao == len(questoes_prova):
        st.snow() # Neve para pontuação perfeita! (Ou st.balloons() novamente)
        st.success("🎉 Parabéns! Você acertou todas as questões!")
    elif pontuacao >= len(questoes_prova) / 2:
        st.info("👍 Bom trabalho! Você se saiu bem.")
    else:
        st.error("😔 Continue estudando! Há espaço para melhorias.")

    # Botão para refazer o quiz
    if st.button("Refazer a Prova", type="secondary", use_container_width=True):
        st.session_state.quiz_submetido = False
        # Não precisamos limpar as respostas explicitamente aqui,
        # pois cada st.radio será re-inicializado com `index=None` por padrão
        # na próxima execução se não houver um `st.session_state[key]` prévio.
        # No entanto, se o `index` for explicitamente lido e aplicado,
        # limpar o estado das respostas pode ser útil para um "reset completo".
        # Para garantir que as opções não venham pre-selecionadas na próxima rodada:
        for i in range(len(questoes_prova)):
            if f'q_{i}' in st.session_state:
                del st.session_state[f'q_{i}']
        st.rerun() # Reinicia a página para o estado inicial sem as respostas submetidas