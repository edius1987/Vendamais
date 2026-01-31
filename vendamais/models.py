from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Produto:
    id: Optional[int]
    nome: str
    codigo_barras: str
    preco_compra: float
    preco_venda: float
    estoque: int
    ncm: str
    tributacao: float = 0.0
    
    @property
    def margem_lucro(self) -> float:
        if self.preco_compra == 0:
            return 100.0
        return ((self.preco_venda - self.preco_compra) / self.preco_compra) * 100

@dataclass
class Cliente:
    id: Optional[int]
    nome: str
    documento: str
    telefone: str
    email: str
    endereco: str

@dataclass
class ItemVenda:
    produto: Produto
    quantidade: int
    preco_unitario: float
    
    @property
    def total(self) -> float:
        return self.quantidade * self.preco_unitario

@dataclass
class Venda:
    id: Optional[int]
    cliente: Optional[Cliente]
    itens: List[ItemVenda]
    forma_pagamento: str
    tipo_fiscal: str
    data_hora: Optional[datetime] = None
    
    @property
    def total(self) -> float:
        return sum(item.total for item in self.itens)
