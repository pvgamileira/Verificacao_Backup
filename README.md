# 🛡️ Verificação Proativa de Backups SQL (`Verificacao_Backup`)

![Python](https://img.shields.io/badge/Python%203-Automation%20%26%20SRE-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL Server](https://img.shields.io/badge/SQL%20Server-Backup%20Auditing-CC2927?style=for-the-badge&logo=microsoft-sql-server&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Produ%C3%A7%C3%A3o-10B981?style=for-the-badge)

Ferramenta de automação e auditoria desenvolvida **100% à mão em Python nativo** para monitoramento proativo de rotinas de backup de bancos de dados **SQL Server** sincronizados em nuvem (`SQL Backup Master` / `Dropbox`).

Criado para resolver uma dor real de operação e suporte técnico em ambiente de produção varejista (ERP/PDV), o script transformou a verificação de backups — antes reativa e manual — em um diagnóstico automatizado de retenção, integridade de volume e idade dos arquivos.

---

## 🎯 Problema de Negócio Resolvido

Em operações de varejo com dezenas de lojas e terminais PDV gerando backups diários (`.zip` / `.bak`), duas falhas operacionais são críticas:
1. **Acúmulo excessivo de arquivos antigos**: Pastas de clientes que não rotacionam os arquivos esgotam o armazenamento compartilhado em nuvem e travam novas sincronizações.
2. **Backups defasados ou corrompidos (0 MB)**: Falhas silenciosas no agente de backup só eram descobertas quando a loja sofria sinistro e precisava restaurar o banco.

---

## ⚙️ Funcionalidades Principais

- **Varredura Recursiva Multi-Diretório (`os.walk`)**: Coleta metadados de tamanho (`MB`), timestamp de modificação e idade em dias (`dias_atras`) para cada arquivo e diretório de cliente.
- **Sistema Flexível de Filtros (`**filtros`)**:
  - Exclusão global por correspondência parcial (`pastas_ignoradas`, `arquivos_ignorados`).
  - Filtros granulares por idade mínima/máxima (`min_dias`, `max_dias`), tamanho (`min_mb`, `max_mb`) e extensão (`.zip`, `.bak`).
- **4 Relatórios Operacionais Automatizados**:
  1. `relatorio_mais_antigos`: Identifica arquivos esquecidos ou sem rotação.
  2. `relatorio_mais_pesados`: Aponta bancos com crescimento anômalo de log/dados que exigem manutenção (`DBCC SHRINKFILE` / expurgo).
  3. `relatorio_pastas_com_mais_arquivos`: Ranking de consumo de arquivos por unidade.
  4. `relatorio_alerta_excesso_arquivos`: Alerta imediato para diretórios que ultrapassam a política de retenção ideal (ex: `limite_ideal=3`), já exibindo o nome exato do arquivo mais antigo para remoção rápida e do mais recente para validação.
- **Exportação para Auditoria (`.csv`)**: Função `exportar_relatorio_csv()` utilizando a biblioteca nativa `csv` com codificação `utf-8-sig` (compatível diretamente com Excel).

---

## 🚀 Como Executar

```bash
# Opcional: definir o diretório base via variável de ambiente
set BACKUP_BASE_DIR="C:\Caminho\Para\Backups"

# Executar o diagnóstico
python verificacao_backup.py
```

---

## 👤 Autor

**Paulo Vitor Gamileira Alves**  
- [GitHub](https://github.com/pvgamileira) | [LinkedIn](https://www.linkedin.com/in/paulo-vitor-gamileira-alves-b80b99254/)
