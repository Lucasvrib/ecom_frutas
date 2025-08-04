import csv

# ===========================
# Função: carregar_produtos
# Lê os dados do CSV e carrega na memória como uma lista de dicionários
# ===========================
def carregar_produtos(caminho):
    """
    Lê um arquivo CSV com os produtos e retorna uma lista de dicionários,
    cada um representando um produto com nome, categoria, tipo e preço.
    
    Parâmetros:
        caminho (str): caminho para o arquivo CSV

    Retorna:
        list: lista de produtos
    """
    produtos = [] # Cria uma lista vazia para armazenar os produtos.
    with open(caminho, newline="", encoding="utf-8") as arquivo: #Abre o arquivo CSV no modo leitura com codificação UTF-8.
        leitor = csv.DictReader(arquivo)  # Constrói um leitor que transforma cada linha do CSV em um dicionário.
        for linha in leitor: #Itera sobre cada linha (produto) no arquivo.
            # Cria dicionário com dados do produto e converte o preço para float
            produtos.append({ #Adiciona à lista de produtos um dicionário com nome, categoria, tipo e preço (convertido para float).
                "nome": linha["nome"],
                "categoria": linha["categoria"],
                "tipo": linha["tipo"],  # unidade ou peso
                "preco": float(linha["preco"])
            })
    return produtos

# ===========================
# Função: mostrar_produtos
# Exibe os produtos disponíveis no terminal com seus detalhes
# ===========================
def mostrar_produtos(produtos):
    """
    Exibe uma lista de produtos no terminal, com índice, nome, categoria, preço e unidade de venda.
    """
    print("\nLista de Produtos Disponíveis:\n")
    for i, produto in enumerate(produtos, 1): # Gera índices a partir de 1
        # Define se o produto é vendido por peso ou unidade
        tipo = "kg" if produto["tipo"] == "peso" else "unidade" # Ajusta a descrição para peso ou unidade
        print(f"{i}. {produto['nome']} ({produto['categoria']}) - R$ {produto['preco']:.2f} por {tipo}") # Exibe cada produto com nome, categoria, preço formatado e tipo.
    print()


# ===========================
# Função: adicionar_ao_carrinho
# Permite ao usuário escolher um produto e adicioná-lo ao carrinho
# ===========================
def adicionar_ao_carrinho(produtos, carrinho):
    """
    Solicita ao usuário que escolha um produto e a quantidade desejada.
    Valida a entrada e adiciona o item ao carrinho com cálculo do total.
    
    Parâmetros:
        produtos (list): lista de produtos disponíveis
        carrinho (list): lista que representa o carrinho de compras
    """
    mostrar_produtos(produtos) # Mostra os produtos disponíveis.
    escolha = input("Digite o número do produto que deseja adicionar ao carrinho: ").strip() # Solicita ao usuário que digite o número do produto.

    # Verifica se o valor digitado é um número dentro da faixa válida
    if not escolha.isdigit() or not (1 <= int(escolha) <= len(produtos)): # Valida se é um número válido.
        print("Opção inválida. Tente novamente.\n")
        return

    # Obtém o produto escolhido (ajusta índice, pois começa em 1 no menu)
    produto = produtos[int(escolha) - 1]

    # Pergunta a quantidade desejada conforme o tipo de venda do produto
    if produto["tipo"] == "peso": # Identifica o tipo do produto (peso ou unidade).
        quantidade = input(f"Quantos quilos de {produto['nome']} você deseja? ") # Pergunta a quantidade adequada ao tipo de produto.
    else:
        quantidade = input(f"Quantas unidades de {produto['nome']} você deseja? ")

    try: # Tenta converter a quantidade para float e valida se é positiva.
        quantidade = float(quantidade)
        if quantidade <= 0:
            raise ValueError
    except ValueError:
        print("Quantidade inválida. Por favor, insira um valor numérico positivo.\n")
        return

    # Calcula o total do item e adiciona ao carrinho
    total_item = quantidade * produto["preco"]
    carrinho.append({ # Adiciona um dicionário com os detalhes do item ao carrinho.
        "nome": produto["nome"],
        "categoria": produto["categoria"],
        "tipo": produto["tipo"],
        "preco_unitario": produto["preco"],
        "quantidade": quantidade,
        "total": total_item
    })

    print(f"{produto['nome']} adicionado ao carrinho com sucesso!\n")


# ===========================
# Função: finalizar_compra
# Gera a nota fiscal da compra e salva em um arquivo de texto
# ===========================
def finalizar_compra(carrinho):
    """
    Calcula o total da compra, gera e salva a nota fiscal em um arquivo de texto.
    
    Parâmetros:
        carrinho (list): lista de itens adicionados pelo usuário
    """
    print("\nGerando sua nota fiscal...\n")
    total_geral = sum(item["total"] for item in carrinho)  # Soma os totais dos itens
    nome_arquivo = "nota_fiscal.txt"

    # Abre o arquivo e escreve os detalhes da nota fiscal
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("===== NOTA FISCAL DO MINI MERCADO =====\n\n") # Escreve cabeçalho da nota fiscal.
        for item in carrinho: # Itera pelos itens do carrinho
            tipo = "kg" if item["tipo"] == "peso" else "unid."
            f.write(
                f"{item['nome']} ({item['categoria']}) - {item['quantidade']} {tipo} x " # Escreve o nome, categoria, quantidade, preço unitário e total de cada item
                f"R$ {item['preco_unitario']:.2f} = R$ {item['total']:.2f}\n"
            )
        f.write(f"\nTOTAL DA COMPRA: R$ {total_geral:.2f}\n") # Escreve o total geral da compra.
        f.write("\nObrigado por comprar com a gente! Volte sempre!")

    print(f"Compra finalizada com sucesso!")
    print(f"Total: R$ {total_geral:.2f}")
    print(f"Nota fiscal salva como '{nome_arquivo}'\n") # Imprime mensagem no terminal com o valor final e nome do arquivo.


# ===========================
# Função principal: main
# Controla o fluxo do programa com o menu e interações do usuário
# ===========================
def main():
    """
    Função principal que gerencia o fluxo do programa:
    - Carrega os produtos
    - Exibe o menu principal
    - Permite comprar, finalizar ou sair
    """
    produtos = carregar_produtos("produtos.csv")  # Lê os produtos do CSV
    carrinho = []  # Lista vazia representando o carrinho
    primeira_compra = True  # Indica se é a primeira vez no menu

    print("Bem-vindo(a) ao Mini Mercado!\n")

    while True:
        print("\nMENU PRINCIPAL")
        # Muda o texto da opção conforme já houve compra ou não
        if primeira_compra:
            print("1 - Comprar")
        else:
            print("1 - Continuar comprando")
        print("2 - Finalizar compra")
        print("3 - Sair sem comprar")

        opcao = input("\nDigite o número da opção desejada: ").strip()

        if opcao == "1": # Adiciona ao carrinho. Altera o texto da opção após a primeira compra.
            adicionar_ao_carrinho(produtos, carrinho)
            primeira_compra = False
        elif opcao == "2": # Finaliza compra se o carrinho tiver itens. Caso contrário, avisa.
            if carrinho:
                finalizar_compra(carrinho)
            else:
                print("Seu carrinho está vazio! Adicione produtos antes de finalizar.")
            break  # Encerra o loop principal
        elif opcao == "3": # Encerra o programa sem finalizar compra.
            print("\nAté logo! Agradecemos sua visita.")
            break
        else:
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.\n") # Valida a opção do menu.


# ===========================
# Execução do programa
# ===========================
if __name__ == "__main__":
    main()  # Inicia o programa
