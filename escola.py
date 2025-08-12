from abc import ABC, abstractmethod
import pandas as pd
import random
import string
import os

# Interface IPessoa define um contrato
class IPessoa(ABC):
    @abstractmethod
    def exibir_informacoes(self):
        pass

# Refatoração da classe Pessoa com @property para encapsulamento
class Pessoa(IPessoa):
    def __init__(self, nome, idade):
        self._nome = nome
        self._idade = idade

    @property
    def nome(self):
        return self._nome

    @property
    def idade(self):
        return self._idade

    def exibir_informacoes(self):
        # Implementação polimórfica padrão
        return f"Nome: {self.nome} | Idade: {self.idade} anos"

# Herança e polimorfismo na classe Aluno
class Aluno(Pessoa):
    def __init__(self, nome, idade, matricula, serie):
        super().__init__(nome, idade)
        self._matricula = matricula
        self._serie = serie

    @property
    def matricula(self):
        return self._matricula

    @property
    def serie(self):
        return self._serie

    def exibir_informacoes(self):
        # Sobrescrita do método para polimorfismo
        return (
            f"**Aluno**\n"
            f"{super().exibir_informacoes()}\n"
            f"Matrícula: {self.matricula}\n"
            f"Série: {self.serie}"
        )

# Herança e polimorfismo na classe Funcionario
class Funcionario(Pessoa):
    def __init__(self, nome, idade, cargo, tipo_vinculo, escolaridade):
        super().__init__(nome, idade)
        self._cargo = cargo
        self._tipo_vinculo = tipo_vinculo
        self._escolaridade = escolaridade

    @property
    def cargo(self):
        return self._cargo

    @property
    def tipo_vinculo(self):
        return self._tipo_vinculo

    @property
    def escolaridade(self):
        return self._escolaridade

    def exibir_informacoes(self):
        # Sobrescrita do método para polimorfismo
        return (
            f"**Funcionário**\n"
            f"{super().exibir_informacoes()}\n"
            f"Cargo: {self.cargo}\n"
            f"Vínculo: {self.tipo_vinculo}\n"
            f"Escolaridade: {self.escolaridade}"
        )

# Classe Escola adaptada para o Streamlit
class Escola:
    def __init__(self, nome_escola):
        self.nome_escola = nome_escola
        self._alunos = []
        self._funcionarios = []

    @property
    def alunos(self):
        return self._alunos

    @property
    def funcionarios(self):
        return self._funcionarios

    def cadastrar_aluno(self, nome, idade, matricula, serie):
        if len(str(matricula)) != 8:
            return False, 'Erro: A matrícula deve ter exatamente 8 dígitos.'
        if any(aluno.matricula == matricula for aluno in self._alunos):
            return False, f'Erro: A matrícula {matricula} já existe.'
        if any(aluno.nome.lower() == nome.lower() for aluno in self._alunos):
            return False, f'Erro: Já existe um aluno com o nome {nome}.'
        novo_aluno = Aluno(nome, idade, matricula, serie)
        self._alunos.append(novo_aluno)
        return True, 'Aluno cadastrado com sucesso!'

    def cadastrar_funcionario(self, nome, idade, cargo, tipo_vinculo, escolaridade):
        if any(f.nome.lower() == nome.lower() for f in self._funcionarios):
            return False, f'Erro: Já existe um funcionário com o nome {nome}.'
        novo_funcionario = Funcionario(nome, idade, cargo, tipo_vinculo, escolaridade)
        self._funcionarios.append(novo_funcionario)
        return True, 'Funcionário cadastrado com sucesso!'

    def buscar_aluno(self, termo):
        encontrados = [a for a in self._alunos if termo.lower() in a.nome.lower() or str(termo) == str(a.matricula)]
        return encontrados

    def buscar_funcionario(self, termo):
        encontrados = [f for f in self._funcionarios if termo.lower() in f.nome.lower()]
        return encontrados

    def gerar_dataframe_alunos(self):
        data = [{'Nome': a.nome, 'Idade': a.idade, 'Matrícula': a.matricula, 'Série': a.serie} for a in self._alunos]
        return pd.DataFrame(data)

    def gerar_dataframe_funcionarios(self):
        data = [{'Nome': f.nome, 'Idade': f.idade, 'Cargo': f.cargo, 'Vínculo': f.tipo_vinculo, 'Escolaridade': f.escolaridade} for f in self._funcionarios]
        return pd.DataFrame(data)

    def salvar_dados(self):
        # Salva alunos
        if self._alunos:
            df_alunos = self.gerar_dataframe_alunos()
            df_alunos.to_csv('alunos.csv', index=False)
        else:
            if os.path.exists('alunos.csv'):
                os.remove('alunos.csv')
        
        # Salva funcionários
        if self._funcionarios:
            df_funcionarios = self.gerar_dataframe_funcionarios()
            df_funcionarios.to_csv('funcionarios.csv', index=False)
        else:
            if os.path.exists('funcionarios.csv'):
                os.remove('funcionarios.csv')

    def carregar_dados(self):
        try:
            # Carrega alunos
            if os.path.exists('alunos.csv'):
                df_alunos = pd.read_csv('alunos.csv')
                for _, row in df_alunos.iterrows():
                    self.cadastrar_aluno(row['Nome'], row['Idade'], row['Matrícula'], row['Série'])
            
            # Carrega funcionários
            if os.path.exists('funcionarios.csv'):
                df_funcionarios = pd.read_csv('funcionarios.csv')
                for _, row in df_funcionarios.iterrows():
                    self.cadastrar_funcionario(row['Nome'], row['Idade'], row['Cargo'], row['Vínculo'], row['Escolaridade'])
            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False

# Função para simular dados e popular a escola
def simular_dados(escola, num_alunos=100, num_funcionarios=100):
    # Dados para geração aleatória
    nomes_comuns = ['Ana', 'Bruno', 'Carla', 'Daniel', 'Eduarda', 'Felipe', 'Gabriela', 'Henrique', 'Isabela', 'João', 'Letícia', 'Marcos', 'Natália', 'Otávio', 'Patrícia', 'Ricardo', 'Sofia', 'Thiago', 'Vitória', 'Pedro']
    sobrenomes_comuns = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Pereira', 'Ferreira', 'Lima', 'Rodrigues', 'Almeida', 'Costa']
    series_options = ['6º ano', '7º ano', '8º ano', '9º ano', '1ª série', '2ª série', '3ª série']
    cargos = ['Professor', 'Secretário', 'Limpeza', 'Porteiro', 'Bibliotecário', 'Merendeira'] # 'Coordenador' removido para ser adicionado manualmente
    tipos_vinculo = ['CLT', 'PJ', 'Contrato', 'Temporário']
    escolaridade_options = ['Sem escolaridade', 'Ensino fundamental incompleto', 'Ensino fundamental completo', 'Ensino médio incompleto', 'Ensino médio completo', 'Ensino superior incompleto', 'Ensino superior completo', 'Mestrado', 'Doutorado']

    # Gerar alunos
    matriculas_usadas = set()
    for i in range(num_alunos):
        nome = f"{random.choice(nomes_comuns)} {random.choice(sobrenomes_comuns)}"
        idade = random.randint(11, 18)
        
        matricula = 0
        while True:
            matricula = random.randint(10000000, 99999999)
            if matricula not in matriculas_usadas:
                matriculas_usadas.add(matricula)
                break
        
        serie = random.choice(series_options)
        escola.cadastrar_aluno(nome, idade, matricula, serie)

    # Gerar o único coordenador
    nome_coordenador = f"Maria {random.choice(sobrenomes_comuns)}"
    idade_coordenador = random.randint(30, 60)
    escolaridade_coordenador = random.choice(['Ensino superior completo', 'Mestrado', 'Doutorado'])
    escola.cadastrar_funcionario(nome_coordenador, idade_coordenador, 'Coordenador', 'CLT', escolaridade_coordenador)

    # Gerar os demais funcionários
    for i in range(num_funcionarios - 1):
        nome = f"{random.choice(nomes_comuns)} {random.choice(sobrenomes_comuns)}"
        idade = random.randint(25, 60)
        cargo = random.choice(cargos)
        tipo_vinculo = random.choice(tipos_vinculo)
        escolaridade = random.choice(escolaridade_options)
        escola.cadastrar_funcionario(nome, idade, cargo, tipo_vinculo, escolaridade)