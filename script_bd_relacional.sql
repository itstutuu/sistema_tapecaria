SET DATESTYLE TO SQL, DMY;
SELECT current_date, current_timestamp;

DROP TABLE IF EXISTS cliente CASCADE;
CREATE TABLE cliente(
	id_cliente SERIAL PRIMARY KEY,
	nome_cliente VARCHAR(60) NOT NULL,
	fone_cliente NUMERIC(13) NOT NULL,
	email_cliente VARCHAR(50),
	whats_cliente NUMERIC(13),
	sexo_cliente CHAR(14) CHECK(sexo_cliente IN ('Masculino', 'Feminino', 'Não Atribuído')),
	cpfcnpj_cliente VARCHAR(14), -- Evita muitas linhas vazias
	tipo_cliente VARCHAR(15) CHECK(tipo_cliente IN ('Pessoa Física', 'Pessoa Jurídica')),
	end_cliente VARCHAR(225)
);
DROP TABLE IF EXISTS pedido CASCADE;
CREATE TABLE pedido(
	id_pedido SERIAL PRIMARY KEY,
	id_cliente INTEGER NOT NULL,
	valor_pedido NUMERIC(7,2) NOT NULL,
	quant_pedido NUMERIC(7) NOT NULL DEFAULT(1), -- Quantidade total de móveis no pedido
	prazo_entrega DATE,
	data_pedido DATE NOT NULL DEFAULT(current_date),
	descricao_pedido VARCHAR(350) NOT NULL,
	status_pedido VARCHAR(50) DEFAULT 'Em andamento', -- Em andamento, Finalizado, Cancelado 
	FOREIGN KEY(id_cliente) REFERENCES cliente(id_cliente)
);
DROP TABLE IF EXISTS movel CASCADE;
CREATE TABLE movel(
	id_movel int NOT NULL,
	id_pedido INTEGER NOT NULL,
	tipo_movel VARCHAR(25) NOT NULL,
	tipo_servico CHAR(1) NOT NULL CHECK(tipo_servico IN ('C', 'R')), -- Confecção, Reparo
	tecido VARCHAR(20) NOT NULL,
	cor VARCHAR(15) NOT NULL,
	material_movel VARCHAR(15),
	material_estof VARCHAR(15),
	quant_movel SMALLINT NOT NULL DEFAULT 1, -- Quantidade de móveis idênticos. Ex.: Sofá azul X4
	valor_movel NUMERIC(5,2), -- Valor de 1 unidade de móvel idêntico
	valor_total NUMERIC(5,2) GENERATED ALWAYS AS (valor_movel*quant_movel) STORED,
	PRIMARY KEY(id_movel, id_pedido),
	FOREIGN KEY(id_pedido) REFERENCES pedido(id_pedido)
);
DROP TABLE IF EXISTS fornecedor CASCADE;
CREATE TABLE fornecedor(
	id_forn int PRIMARY KEY NOT NULL,
	CNPJ_forn CHAR(14) UNIQUE NOT NULL,
	nome_forn VARCHAR(100) NOT NULL,
	tipo_forn VARCHAR(30),
	fone_forn CHAR(13),
	email_forn VARCHAR(50),
	end_forn VARCHAR(255)
);
DROP TABLE IF EXISTS compra CASCADE;
CREATE TABLE compra(
	id_compra int PRIMARY KEY NOT NULL,
	id_forn INTEGER NOT NULL,
	valor_compra NUMERIC(7,2),
	descricao_compra VARCHAR(300),
	data_compra DATE NOT NULL,
	FOREIGN KEY(id_forn) REFERENCES fornecedor(id_forn)
);
DROP TABLE IF EXISTS material CASCADE;
CREATE TABLE material(
	id_material int PRIMARY KEY,
	id_movel INTEGER NOT NULL,
	id_pedido INTEGER NOT NULL,
	id_forn INTEGER NOT NULL,
	id_compra INTEGER NOT NULL,
	--num_fatura VARCHAR(50)--
	nome_material VARCHAR(35) NOT NULL,
	quant_material NUMERIC(10,2) NOT NULL,
	unid_medida VARCHAR(10) DEFAULT 'unidade',
	custo_unid NUMERIC(5,2) NOT NULL,
	custo_total NUMERIC(7,2)
	GENERATED ALWAYS AS (quant_material*custo_unid) STORED,
	data_compra DATE DEFAULT(current_date),
	FOREIGN KEY(id_movel, id_pedido) REFERENCES movel(id_movel, id_pedido),
	FOREIGN KEY(id_forn) REFERENCES fornecedor(id_forn),
	FOREIGN KEY(id_compra) REFERENCES compra(id_compra)
);
DROP TABLE IF EXISTS pagamento CASCADE;
CREATE TABLE pagamento(
	id_pagamento int NOT NULL,
	id_pedido INTEGER NOT NULL,
	valor_pagamento NUMERIC(7,2),
	data_pagamento DATE NOT NULL,
	status_pagamento CHAR(1) CHECK(status_pagamento IN ('P','N')), -- Pago, Não pago
	PRIMARY KEY(id_pagamento, id_pedido),
	FOREIGN KEY(id_pedido) REFERENCES pedido(id_pedido)
);
-- select * from material
-- select * from pagamento
-- select * from fornecedor
-- select * from movel
-- select * from pedido
-- select * from cliente
-- select * from compra

-- SELECT p.id_pedido, p.id_cliente, p.data_pedido, p.prazo_entrega, p.descricao_pedido, c.nome_cliente FROM pedido p LEFT OUTER JOIN cliente c
-- ON (p.id_cliente=c.id_cliente)
-- ORDER BY p.id_pedido;

-- SELECT c.nome_cliente AS Cliente, fone_cliente AS Telefone, p.descricao_pedido AS Pedido, quant_pedido AS Quantidade,
-- valor_pedido AS Valor_total, status_pedido AS Status
-- FROM cliente c LEFT OUTER JOIN pedido p ON (p.id_cliente=c.id_cliente)
-- ORDER BY id_pedido ASC;