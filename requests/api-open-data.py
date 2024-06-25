import requests
import pandas as pd

# Função para formatar preço em reais
def formatar_preco_reais(valor):
    if valor is None:
        return 'Preço não disponível'
    else:
        return f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        # return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

# URLs atualizadas
consultarItemMaterial_base_url = 'https://dadosabertos.compras.gov.br/modulo-pesquisa-preco/1_consultarMaterial'
consultarItemServico_base_url = 'https://dadosabertos.compras.gov.br/modulo-pesquisa-preco/3_consultarServico'

def obter_itens(tipo_item, codigo_item_catalogo, pagina, tamanho_pagina):
    url = consultarItemMaterial_base_url if tipo_item == 'Material' else consultarItemServico_base_url
    params = {
        'pagina': pagina,
        'tamanhoPagina':tamanho_pagina,  # Ajuste para 500 itens por página
        'codigoItemCatalogo': codigo_item_catalogo
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            json_response = response.json()
            itens = json_response.get('resultado', [])
            paginas_restantes = json_response.get('paginasRestantes', 0)
            total_paginas = json_response.get('totalPaginas', 0)
            return itens, paginas_restantes, total_paginas
        else:
            print(f"Erro na consulta: {response.status_code}")
            return [], 0
    except Exception as e:
        print(f"Erro ao realizar a requisição: {str(e)}")
        return [], 0
x = 1
while x:
        print("--------------PESQUISA DE PREÇOS DE MATERIAIS E/OU SERVIÇOS----------------\n")    

        # Disclaimer
        print("Localize o código do material ou serviço de forma simples e rápida. https://catalogo.compras.gov.br/cnbs-web/busca\n\n")

        tipo_item = 'Material'
        codigo_item_catalogo =str(input("Código do Item de Catálogo: "))
        if codigo_item_catalogo == -1:
                break

        pagina = int(input("Indique a página para consulta: "))
        tamanho_pagina = 500
        
        if codigo_item_catalogo:  # Verifica se o código do item de catálogo não está vazio
                itens, paginas_restantes, total_paginas = obter_itens(tipo_item, codigo_item_catalogo, pagina, tamanho_pagina)
                if itens:  # Ensure 'itens' is not empty before proceeding
                #st.session_state['itens'] = itens
                #st.session_state['paginas_restantes'] = paginas_restantes
                #st.session_state['total_paginas'] = total_paginas
                        print(f"Total de páginas: {total_paginas}")
                        print(f"Páginas restantes: {paginas_restantes}")            
                else:
                        print("Nenhum item encontrado. Por favor, tente com um código diferente ou verifique a conexão com a API.")
        else:
                print("Por favor, informe o código do item de catálogo para realizar a consulta.")

