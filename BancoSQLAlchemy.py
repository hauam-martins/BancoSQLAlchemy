import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, func
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "cliente"
    #atributos
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    conta = relationship(
    "Conta", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Cliente(id={self.id}, name={self.name}, cpf={self.cpf})"

class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    saldo = Column(Integer)

    cliente = relationship(
        "Cliente", back_populates ="conta")

    def __repr__(self):
        return f"Conta(id={self.id}, Numero{self.num})"

print(Cliente.__tablename__)
print(Conta.__tablename__)

# conexão com o banco de dados
engine = create_engine("sqlite://")

# criando as classes como tabelas no banco
Base.metadata.create_all(engine)


# insvetiga o esquema do banco
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("cliente"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    juliana = Cliente(
        name='Juliana',
        cpf= 12345658,
        conta=[Conta(Conta= 11115)]
    )

    sandy = Cliente(
        name='sandy',
        cpf= 7945865,
        conta=[Conta(Conta= 8856)]
    )


    # enviando para o banco de dados (persistência de dadosP
    session.add_all([juliana, sandy])
    session.commit()

stmt = select(Cliente).where(Cliente.name.in_(['Juliana', 'sandy']))
print('Recuperando usuários a partir de condição de filtragem matchin')
for cliente in session.scalars(stmt):
    print(cliente)

stmt_conta = select(Conta).where(Conta.cliente.in_([2]))
print('\nRecuperando a conta de Sandy')
for conta in session.scalars(stmt_conta):
    print(conta)


stmt_order = select(Cliente).order_by(Cliente.cpf.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(Cliente.cpf, Conta.num).join_from(Conta, Cliente)
for result in session.scalars(stmt_join):
    print("\n", result)

