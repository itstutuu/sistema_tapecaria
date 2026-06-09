* Texto escrito por mim, traduzido em **markdown** pela Gemini.

# Projeto Integrador I | Big Data para Negócios (Fatec Ipiranga)

# Sistema desenvolvido como um ERP para cadastro de clientes, pedidos e fornecedores.

## 🛠️ Infraestrutura do Software

A arquitetura da solução foi desenhada integrando as seguintes tecnologias:

* **Banco de Dados:** PostgreSQL (armazenamento e modelagem relacional).
* **Back-end:** Python + `PG8000` (conexão e execução de queries no banco).
* **Front-end:** Python + `Tkinter` (construção da interface gráfica).
* **Analytics:** Power BI (desenvolvimento de dashboards para suporte à tomada de decisão).

---

## ⚙️ Funcionalidades

* **CRUD Completo:** Criação, leitura, atualização e deleção de cadastros de clientes, pedidos e fornecedores.
* **Interface Intuitiva:** Operações realizadas por meio de uma GUI (Interface Gráfica do Usuário) amigável e de fácil usabilidade.
* **Histórico de Entidades:** Armazenamento do histórico das entidades relacionadas para auditoria e análise de dados futura.

---

## 📊 Geração de Dados Fictícios (*Mock Data*)

Como o parceiro comercial não possuía uma gestão centralizada da informação, com dados dispersos em cadernetas manuais, WhatsApp e e-mails, foi necessário criar uma estratégia de testes robusta.

Utilizando **Python + biblioteca Faker**, gerei *mock data* (dados fictícios, porém estatisticamente realistas). Essa massa de dados foi fundamental para:

1. Validar e homologar as funcionalidades da aplicação (testes de estresse e consistência).
2. Alimentar e simular os relatórios analíticos no Power BI antes da virada oficial para o ambiente de produção.

---

## 📌 Sobre o Projeto

A iniciativa visa cumprir a missão do **Centro Paula Souza**, que incentiva os estudantes a retornarem o benefício do ensino público à sociedade. Isso é feito aplicando o aprendizado acadêmico na resolução de problemas reais de mercado. O desafio inicial consistiu em prospectar e firmar parceria com um negócio real para implementar, de forma totalmente gratuita, uma solução voltada à inteligência de dados.

Com isso, fechamos uma parceria com a **Tapeçaria Marzorati**, uma empresa de médio porte focada na confecção e conserto de móveis estofados, para o desenvolvimento e aplicação do sistema.
