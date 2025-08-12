from abc import ABC, abstractmethod
import pandas as pd

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