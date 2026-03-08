# ⛪ Relatório de Músicas - ECAD Igreja

Sistema desenvolvido em Python com **Streamlit** para facilitar o registro e a exportação de músicas utilizadas em celebrações religiosas, visando o controle e envio de dados para o ECAD.

## 🚀 Funcionalidades

- **Informações da Celebração:** Registro de data, horário, local e grupo responsável.
- **Biblioteca Integrada:** Busca automática de títulos e compositores a partir de uma base de dados no Google Sheets.
- **Entrada Manual:** Permite adicionar músicas que ainda não constam na biblioteca.
- **Cálculo de Duração:** Conversão automática de minutos e segundos para o formato do relatório.
- **Gestão de Status:** Interface separada para Novos Relatórios, Rascunhos e Finalizados.

## 🛠️ Tecnologias Utilizadas

* [Python](https://www.python.org/)
* [Streamlit](https://streamlit.io/) (Interface Web)
* [Pandas](https://pandas.pydata.org/) (Manipulação de Dados)
* [Streamlit GSheets Connection](https://github.com/streamlit/gsheets-connection) (Integração com Google Sheets)

## 📋 Pré-requisitos

Antes de rodar o projeto, você precisará instalar as dependências:

```bash
pip install -r requirements.txt
