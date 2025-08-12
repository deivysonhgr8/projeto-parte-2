import streamlit as st
from escola import Escola, Aluno, Funcionario

# Inicializa a classe Escola no estado da sessão
if 'escola' not in st.session_state:
    st.session_state.escola = Escola('Construindo o Saber')

st.title(f'Sistema de Gerenciamento da Escola {st.session_state.escola.nome_escola}')

# Sidebar para navegação
st.sidebar.title('Menu')
opcao = st.sidebar.radio('Escolha uma opção:', 
                         ['Cadastrar', 'Listar/Buscar', 'Análises Gráficas'])

if opcao == 'Cadastrar':
    st.header('Cadastramento')
    tipo_cadastro = st.radio('O que você deseja cadastrar?', ['Aluno', 'Funcionário'])

    if tipo_cadastro == 'Aluno':
        st.subheader('Cadastrar Novo Aluno')
        with st.form('form_aluno', clear_on_submit=True):
            nome = st.text_input('Nome do Aluno', key='aluno_nome')
            idade = st.number_input('Idade do Aluno', min_value=0, key='aluno_idade')
            matricula = st.number_input('Matrícula do Aluno', min_value=0, key='aluno_matricula')
            serie = st.text_input('Série do Aluno', key='aluno_serie')
            submit_button = st.form_submit_button('Cadastrar')

            if submit_button:
                if nome and idade is not None and serie:
                    sucesso, mensagem = st.session_state.escola.cadastrar_aluno(nome, int(idade), int(matricula), serie)
                    if sucesso:
                        st.success(mensagem)
                    else:
                        st.error(mensagem)
                else:
                    st.warning('Por favor, preencha todos os campos.')

    else: # tipo_cadastro == 'Funcionário'
        st.subheader('Cadastrar Novo Funcionário')
        with st.form('form_funcionario', clear_on_submit=True):
            nome = st.text_input('Nome do Funcionário', key='func_nome')
            idade = st.number_input('Idade do Funcionário', min_value=0, key='func_idade')
            cargo = st.text_input('Cargo', key='func_cargo')
            tipo_vinculo = st.selectbox('Tipo de Vínculo', ['CLT', 'PJ', 'Contrato', 'Temporário'], key='func_vinculo')
            escolaridade = st.text_input('Escolaridade', key='func_escolaridade')
            submit_button = st.form_submit_button('Cadastrar')

            if submit_button:
                if nome and idade is not None and cargo and tipo_vinculo and escolaridade:
                    sucesso, mensagem = st.session_state.escola.cadastrar_funcionario(nome, int(idade), cargo, tipo_vinculo, escolaridade)
                    if sucesso:
                        st.success(mensagem)
                    else:
                        st.error(mensagem)
                else:
                    st.warning('Por favor, preencha todos os campos.')

elif opcao == 'Listar/Buscar':
    st.header('Listar e Buscar')
    tipo_busca = st.radio('O que você deseja listar/buscar?', ['Alunos', 'Funcionários'])

    termo_busca = st.text_input(f'Buscar {tipo_busca} por nome ou matrícula:')
    
    if st.button('Listar Todos'):
        termo_busca = '' # Limpa o termo de busca para listar todos

    if tipo_busca == 'Alunos':
        st.subheader('Alunos Cadastrados')
        if termo_busca:
            encontrados = st.session_state.escola.buscar_aluno(termo_busca)
            if encontrados:
                for aluno in encontrados:
                    st.markdown(f"---")
                    st.markdown(aluno.exibir_informacoes())
            else:
                st.info('Nenhum aluno encontrado.')
        else:
            if st.session_state.escola.alunos:
                df = st.session_state.escola.gerar_dataframe_alunos()
                st.dataframe(df)
            else:
                st.info('Nenhum aluno cadastrado.')

    else: # tipo_busca == 'Funcionários'
        st.subheader('Funcionários Cadastrados')
        if termo_busca:
            encontrados = st.session_state.escola.buscar_funcionario(termo_busca)
            if encontrados:
                for funcionario in encontrados:
                    st.markdown(f"---")
                    st.markdown(funcionario.exibir_informacoes())
            else:
                st.info('Nenhum funcionário encontrado.')
        else:
            if st.session_state.escola.funcionarios:
                df = st.session_state.escola.gerar_dataframe_funcionarios()
                st.dataframe(df)
            else:
                st.info('Nenhum funcionário cadastrado.')

elif opcao == 'Análises Gráficas':
    st.header('Análises Gráficas')
    st.subheader('Gráfico de Alunos e Funcionários')
    num_alunos = len(st.session_state.escola.alunos)
    num_funcionarios = len(st.session_state.escola.funcionarios)

    if num_alunos > 0 or num_funcionarios > 0:
        dados_quantidades = pd.DataFrame({
            'Categoria': ['Alunos', 'Funcionários'],
            'Quantidade': [num_alunos, num_funcionarios]
        })
        st.bar_chart(dados_quantidades.set_index('Categoria'))
    else:
        st.info("Não há dados suficientes para gerar o gráfico.")

    st.subheader('Gráfico de Alunos por Série')
    if st.session_state.escola.alunos:
        series_count = {}
        for aluno in st.session_state.escola.alunos:
            serie = aluno.serie.upper().strip()
            series_count[serie] = series_count.get(serie, 0) + 1
        
        df_series = pd.DataFrame(list(series_count.items()), columns=['Série', 'Quantidade'])
        st.bar_chart(df_series.set_index('Série'))
    else:
        st.info("Nenhum aluno cadastrado para gerar o gráfico por série.")