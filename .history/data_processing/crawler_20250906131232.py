import requests

def obter_reclamacoes(company_id: str, page: int = 1) -> list:
    """
    Obtém as reclamações de uma empresa no ReclameAqui utilizando a API interna.

    Args:
        company_id: ID da empresa no ReclameAqui.
        page: Número da página de reclamações a ser consultada.

    Returns:
        Uma lista de dicionários contendo as reclamações.
    """
    url = f"https://ioapi.reclameaqui.com.br/raichu-io-site-v1/company/{company_id}/claims"
    params = {"page": page}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Verifica se houve erro na requisição

        dados = response.json()
        if dados.get("claims"):
            return dados["claims"]
        else:
            print(f"[INFO] Nenhuma reclamação encontrada na página {page}.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Erro ao acessar a API: {e}")
        return []

if __name__ == "__main__":
    company_id = "santander"  # Substitua pelo ID da empresa desejada
    page = 1  # Número da página que deseja consultar

    reclamacoes = obter_reclamacoes(company_id, page)
    if reclamacoes:
        for i, reclamacao in enumerate(reclamacoes, 1):
            print(f"{i}. {reclamacao['title']}")
            print(f"   {reclamacao['text']}\n")
    else:
        print("[INFO] Nenhuma reclamação encontrada.")