import requests

# def formatar_preco_reais(valor):
#     if valor is None:
#         return 'Preço não disponível'
#     else:
#         return f'{valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        # return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

consultarItemMaterial_base_url = 'https://dadosabertos.compras.gov.br/modulo-pesquisa-preco/1_consultarMaterial'

def obter_itens(codigo_item_catalogo):
    url = consultarItemMaterial_base_url
    pagina = 1
    params = {
        'pagina': pagina,
        'tamanhoPagina': 500,
        'codigoItemCatalogo': codigo_item_catalogo
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            json_response = response.json()
            itens = json_response.get('resultado', [])
            paginas_restantes = json_response.get('paginasRestantes', 0)
            while(paginas_restantes != 0):
                pagina = pagina + 1
                params = {
                    'pagina': pagina,
                    'tamanhoPagina': 500,
                    'codigoItemCatalogo': codigo_item_catalogo
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    json_response = response.json()
                    itens = itens + json_response.get('resultado', [])
                paginas_restantes = json_response.get('paginasRestantes', 0)
            return itens
        else:
            print(f"Erro na consulta: {response.status_code}")
            return [], 0
    except Exception as e:
        print(f"Erro ao realizar a requisição: {str(e)}")
        return [], 0