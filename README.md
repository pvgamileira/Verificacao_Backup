<div align="center">

# 🛡️ Verificação de Backups - SQL Backup Master

**Script Python em lote para monitoramento, auditoria e alerta de rotação de backups SQL.**

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

</div>

---

## 📌 Visão Geral

Este utilitário realiza a varredura automática nos diretórios do **SQL Backup Master** (armazenados no Dropbox ou rede local), coletando informações cruciais sobre retenção, tamanho e idade dos arquivos de backup.

---

## 🚀 Recursos

- 🔍 **Varredura Recursiva**: Coleta tamanho (MB) e idade em dias de todos os arquivos `.zip` / backups.
- 🕒 **Relatório dos Mais Antigos**: Identifica arquivos defasados no sistema.
- 💾 **Relatório dos Mais Pesados**: Monitora os backups que mais ocupam espaço em disco.
- 📁 **Análise por Diretório**: Lista as pastas com maior quantidade de arquivos acumulados.
- 🚨 **Alerta de Excesso**: Emite alertas para pastas que passam do limite ideal (ex: mais de 3 backups por loja), destacando o **mais recente** para restauração e o **mais antigo** para limpeza.

---

## ⚙️ Como Executar

### Pré-requisito
Possuir o **Python 3** instalado.

### Execução
```bash
python verificacao_backup.py
```

---

## 📂 Estrutura do Repositório

```text
.
├── verificacao_backup.py   # Script principal de monitoramento e relatórios
├── .gitignore              # Filtro de arquivos ignorados pelo Git
└── README.md               # Documentação estilizada do projeto
```

---

## 📄 Licença

Este projeto é de uso livre sob a licença MIT.
