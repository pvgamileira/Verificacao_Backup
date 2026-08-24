import os 
import time 

# Caminho principal onde os backups estão armazenados
caminho_pastas_backup = r"C:\Users\BoxPDV\Dropbox\Aplicativos\SQL Backup Master"

def coletar_dados_backup(caminho_base, pastas_ignoradas=None, arquivos_ignorados=None):
    """
    Varre os diretórios e coleta os dados dos arquivos e pastas.
    Os filtros de coleta ignoram arquivos/pastas por correspondência parcial
    (ex: o filtro "MATRIZ" vai ignorar qualquer pasta que tenha "matriz" no nome).
    """
    pastas_ignoradas = pastas_ignoradas or []
    arquivos_ignorados = arquivos_ignorados or []

    lista_arquivos = []
    lista_pastas = []
    
    tempo_atual = time.time()

    for pasta_atual, subpastas, arquivos in os.walk(caminho_base):
        nome_pasta = os.path.basename(pasta_atual)
        
        # FILTRO GLOBAL DE PASTA: se tiver algum termo ignorado, pula a pasta inteira
        if any(ignorado.lower() in nome_pasta.lower() for ignorado in pastas_ignoradas):
            continue

        arquivos_da_pasta = []
        
        for arquivo in arquivos:
            # FILTRO GLOBAL DE ARQUIVO: se tiver algum termo ignorado, pula esse arquivo específico
            if any(ignorado.lower() in arquivo.lower() for ignorado in arquivos_ignorados):
                continue
            
            diretorio_completo = os.path.join(pasta_atual, arquivo)
            
            try:
                tamanho_bytes = os.path.getsize(diretorio_completo)
                tamanho_mb = tamanho_bytes / (1024 * 1024) 
                
                data_modificacao = os.path.getmtime(diretorio_completo)
                dias_passados = (tempo_atual - data_modificacao) / (60 * 60 * 24) 
                
                dados_backup = {
                    "nome": arquivo, 
                    "tamanho_mb": tamanho_mb, 
                    "data": data_modificacao, 
                    'dias_atras': dias_passados, 
                    'pasta': nome_pasta
                }
                lista_arquivos.append(dados_backup)
                arquivos_da_pasta.append(dados_backup)
                
            except OSError:
                continue            
        
        if arquivos_da_pasta:
            # Ordena do mais recente (menos dias_atras) para o mais antigo (mais dias_atras)
            arquivos_da_pasta.sort(key=lambda x: x['dias_atras'])
            arquivo_mais_recente = arquivos_da_pasta[0]['nome']
            arquivo_mais_antigo = arquivos_da_pasta[-1]['nome']
            
            lista_pastas.append({
                'pasta': nome_pasta, 
                'quantidade_total': len(arquivos_da_pasta),
                'arquivo_mais_recente': arquivo_mais_recente,
                'arquivo_mais_antigo': arquivo_mais_antigo
            })
            
    return lista_arquivos, lista_pastas


def aplicar_filtros_arquivos(arquivos, min_dias=None, max_dias=None, min_mb=None, max_mb=None, extensao=None):
    """
    Aplica filtros específicos em uma lista de arquivos, ideal para consultas individuais.
    """
    resultado = arquivos
    
    if min_dias is not None:
        resultado = list(filter(lambda a: a['dias_atras'] >= min_dias, resultado))
    if max_dias is not None:
        resultado = list(filter(lambda a: a['dias_atras'] <= max_dias, resultado))
    if min_mb is not None:
        resultado = list(filter(lambda a: a['tamanho_mb'] >= min_mb, resultado))
    if max_mb is not None:
        resultado = list(filter(lambda a: a['tamanho_mb'] <= max_mb, resultado))
    if extensao is not None:
        resultado = list(filter(lambda a: a['nome'].lower().endswith(extensao.lower()), resultado))
        
    return resultado


def relatorio_mais_antigos(arquivos, top_n=50, **filtros):
    arquivos_filtrados = aplicar_filtros_arquivos(arquivos, **filtros)
    arquivos_filtrados.sort(key=lambda x: x["dias_atras"], reverse=True)
    
    print(f"\n=== ARQUIVOS MAIS ANTIGOS PARA MONITORAR (Top {top_n}) ===")
    for i in arquivos_filtrados[:top_n]:
        print(f"Arquivo: {i['nome']} | Há {i['dias_atras']:.0f} dias | Pasta: {i['pasta']}")


def relatorio_mais_pesados(arquivos, top_n=50, **filtros):
    arquivos_filtrados = aplicar_filtros_arquivos(arquivos, **filtros)
    arquivos_filtrados.sort(key=lambda x: x["tamanho_mb"], reverse=True)
    
    print(f"\n=== ARQUIVOS MAIS PESADOS (Top {top_n}) ===")
    for i in arquivos_filtrados[:top_n]:
        print(f"Arquivo: {i['nome']} | Tamanho: {i['tamanho_mb']:.2f}MB | Pasta: {i['pasta']}")


def relatorio_pastas_com_mais_arquivos(pastas, min_arquivos=None, top_n=20):
    resultado = pastas
    if min_arquivos is not None:
        resultado = list(filter(lambda p: p['quantidade_total'] >= min_arquivos, resultado))
        
    resultado.sort(key=lambda x: x["quantidade_total"], reverse=True)
    
    print(f"\n=== DIRETÓRIOS COM MAIS ARQUIVOS (Top {top_n}) ===")
    for p in resultado[:top_n]:
        print(f"Diretório: {p['pasta']} | Quantidade total de arquivos: {p['quantidade_total']}")


def relatorio_alerta_excesso_arquivos(arquivos, limite_ideal=3, **filtros):
    """
    Exibe um alerta para pastas que excedem a quantidade ideal de arquivos.
    """
    arquivos_filtrados = aplicar_filtros_arquivos(arquivos, **filtros)
    
    # Agrupa os arquivos por pasta
    arquivos_por_pasta = {}
    for a in arquivos_filtrados:
        pasta = a['pasta']
        if pasta not in arquivos_por_pasta:
            arquivos_por_pasta[pasta] = []
        arquivos_por_pasta[pasta].append(a)
        
    print(f"\n=== ALERTA: PASTAS COM EXCESSO DE ARQUIVOS (Acima de {limite_ideal}) ===")
    
    pastas_com_excesso = {p: arqs for p, arqs in arquivos_por_pasta.items() if len(arqs) > limite_ideal}
    
    if not pastas_com_excesso:
        print("Tudo certo! Nenhuma pasta passou do limite ideal.")
    else:
        for pasta, arqs in pastas_com_excesso.items():
            excedente = len(arqs) - limite_ideal
            # Ordena do mais recente para o mais antigo
            arqs.sort(key=lambda x: x['dias_atras'])
            mais_recente = arqs[0]['nome']
            mais_antigo = arqs[-1]['nome']
            
            print(f"ALERTA: Diretório '{pasta}' possui {len(arqs)} arquivos ({excedente} a mais)")
            print(f"  -> Copie para buscar o MAIS RECENTE: {mais_recente}")
            print(f"  -> Copie para buscar o MAIS ANTIGO : {mais_antigo}")
            print("-" * 60)


# ====================================================================================
# ÁREA DE EXECUÇÃO E EXIBIÇÃO DE RELATÓRIOS
# ====================================================================================

if __name__ == "__main__":
    # 1. Filtros Globais (Exclusão por palavra-chave - não precisa mais ser o nome exato)
    pastas_para_ignorar = ['MATRIZ'] 
    arquivos_para_ignorar = [
        'PDV-20250730080006', 
        'PDV_FILIAL-20250730080047'
    ]
    
    print("Iniciando varredura...")
    dados_coletados, pastas_coletadas = coletar_dados_backup(
        caminho_pastas_backup, 
        pastas_ignoradas=pastas_para_ignorar,
        arquivos_ignorados=arquivos_para_ignorar
    )

    # -----------------------------------------------------------------------------
    # 2. Consultas usando filtros específicos para CADA RELATÓRIO
    # Você pode usar os filtros: min_dias, max_dias, min_mb, max_mb, extensao
    # -----------------------------------------------------------------------------
    
    # Consulta 1: Arquivos mais antigos (Exemplo: apenas arquivos que tenham mais de 5MB)
    relatorio_mais_antigos(dados_coletados, top_n=50, min_mb=0)

    # Consulta 2: Arquivos mais pesados (Exemplo: apenas da extensão .zip e com mais de 7 dias)
    relatorio_mais_pesados(dados_coletados, top_n=50, extensao='.zip', min_dias=0)

    # Consulta 3: Pastas com mais arquivos (Exemplo: apenas pastas que tem no mínimo 2 arquivos)
    relatorio_pastas_com_mais_arquivos(pastas_coletadas, top_n=20, min_arquivos=1)

    # Consulta 4: ALERTA de pastas que passam do limite (O ideal é ter apenas 3 arquivos)
    # ATENÇÃO: Agora passando 'dados_coletados' como você queria!
    relatorio_alerta_excesso_arquivos(dados_coletados, limite_ideal=3)
