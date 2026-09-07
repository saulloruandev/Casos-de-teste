import pytest
from playwright.sync_api import Page, expect
import time


# Sessão validos


def test_valid_login(page:Page):  #entrar no site com usuário bloqueado
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_valid_imagens(page:Page):  #verificar se o usuário tem imagens repetidas
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce") 
    page.click("#login-button") 

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect((page).locator(".title")).to_have_text("Products")    

    page.wait_for_load_state("networkidle")

    produtos = [
        page.locator('[alt="Sauce Labs Backpack"]'),
        page.locator('[alt="Sauce Labs Bike Light"]'),
        page.locator('[alt="Sauce Labs Bolt T-Shirt"]'),
        page.locator('[alt="Sauce Labs Fleece Jacket"]'),
        page.locator('[alt="Sauce Labs Onesie"]'),
        page.locator('[alt="Test.allTheThings() T-Shirt (Red)"]')
    ]

    imagens_vistas = set()
    imagens_repetidas = []

    for produto in produtos:
        src = produto.get_attribute("src")
        alt = produto.get_attribute("alt")

        if src in imagens_vistas:
            imagens_repetidas.append(alt)
        else:
            imagens_vistas.add(src)

    assert len(imagens_repetidas) == 0, f"Produtos com imagem repetida: {imagens_repetidas}"

         
def test_valid_button(page:Page): #verificar se o usuário tem botões de adicionar ao carrinho funcionando corretamente
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect((page).locator(".title")).to_have_text("Products") 

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click("#add-to-cart-sauce-labs-bike-light")
    page.click("#add-to-cart-sauce-labs-bolt-t-shirt")
    page.click("#add-to-cart-sauce-labs-fleece-jacket")
    page.click("#add-to-cart-sauce-labs-onesie")
    page.click('[id="add-to-cart-test.allthethings()-t-shirt-(red)"]')

    page.wait_for_timeout(3000)

    expect((page).locator(".shopping_cart_badge")).to_have_text("6")


def test_valid_button_remove(page:Page): #verificar se o usuário problem_user tem botões de remover do carrinho funcionando corretamente
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.wait_for_load_state("networkidle")

    ids_produtos = [
            "sauce-labs-backpack",
            "sauce-labs-bike-light",
            "sauce-labs-bolt-t-shirt",
            "sauce-labs-fleece-jacket",
            "sauce-labs-onesie",
            "test.allthethings()-t-shirt-(red)"
        ]

    nao_adicionados = []
    nao_removidos = []

    for id_produto in ids_produtos:
        botao_adicionar = page.locator(f'[id="add-to-cart-{id_produto}"]')
        botao_remover = page.locator(f'[id="remove-{id_produto}"]')

        botao_adicionar.click()
        page.wait_for_timeout(500)

        if not botao_remover.is_visible():
            nao_adicionados.append(id_produto)
            continue

        botao_remover.click()
        page.wait_for_timeout(500)

        if not botao_adicionar.is_visible():
            nao_removidos.append(id_produto)

    assert len(nao_removidos) == 0, f"Produtos não removidos: {nao_removidos}"


def test_valid_filtro(page: Page):
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    filtros = ["az", "za", "lohi", "hilo"]
    filtros_ruins = []

    for filtro in filtros:


        produtos_antes = page.locator(".inventory_item").all_text_contents()

        page.select_option(".product_sort_container", filtro)
        page.wait_for_timeout(500)

        produtos_depois = page.locator(".inventory_item").all_text_contents()

        if filtro != "az" and produtos_antes == produtos_depois:
            filtros_ruins.append(filtro)

        

    assert len(filtros_ruins) == 0, f"Os seguintes filtros não alteraram a ordem dos produtos: {filtros_ruins}"



def test_valid_checkout(page:Page): #verificar se o usuário consegue preencher os dados corretamente e não alterar os valores

    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")

    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    page.click("#checkout")

    page.fill("#first-name", "João")
    page.fill("#last-name", "Marcos")
    page.fill("#postal-code", "666777")

    print("first-name:", page.locator("#first-name").input_value())
    print("last-name:", page.locator("#last-name").input_value())
    print("postal-code:", page.locator("#postal-code").input_value())

    expect(page.locator("#first-name")).to_have_value("João")
    expect(page.locator("#last-name")).to_have_value("Marcos")
    expect(page.locator("#postal-code")).to_have_value("666777")

    page.click("#continue")

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")


def test_valid_tempo_login(page:Page): #verificar se o tempo de login do usuário
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")

    inicio = time.time()
    page.click("#login-button")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    fim = time.time()

    tempo_gasto = fim - inicio
    assert tempo_gasto < 1, f"O login demorou {tempo_gasto:.2f} segundos"

    expect(page.locator(".title")).to_have_text("Products")


def test_valid_navegação(page:Page): #verificar se o usuário consegue ir do carrinho até pagina principal num tempo aceitável
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")

    inicio = time.time()
    page.click("#continue-shopping")
    fim = time.time()

    tempo_gasto = fim - inicio
    assert tempo_gasto < 1, f"A navegação demorou {tempo_gasto:.2f} segundos"


def test_valid_last_name_visivel(page:Page): #verificar se o usuário consegue preencher os dados
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")

    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    page.click("#checkout")

    page.fill("#first-name", "João")
    page.fill("#last-name", "Marcos")
    page.fill("#postal-code", "666777")

    expect(page.locator("#first-name")).to_have_value("João")
    expect(page.locator("#last-name")).to_have_value("Marcos")
    expect(page.locator("#postal-code")).to_have_value("666777")

    page.click("#continue")

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")


 # Sessão de bugs
def test_invalid_login_locked(page:Page):  #entrar no site com usuário bloqueado
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "locked_out_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")


def test_invalid_problem_user_imagens(page:Page):  #verificar se o usuário problem_user tem imagens repetidas
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "problem_user")
    page.fill("#password", "secret_sauce") 
    page.click("#login-button") 

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect((page).locator(".title")).to_have_text("Products")    

    page.wait_for_load_state("networkidle")

    produtos = [
        page.locator('[alt="Sauce Labs Backpack"]'),
        page.locator('[alt="Sauce Labs Bike Light"]'),
        page.locator('[alt="Sauce Labs Bolt T-Shirt"]'),
        page.locator('[alt="Sauce Labs Fleece Jacket"]'),
        page.locator('[alt="Sauce Labs Onesie"]'),
        page.locator('[alt="Test.allTheThings() T-Shirt (Red)"]')
    ]

    imagens_vistas = set()
    imagens_repetidas = []

    for produto in produtos:
        src = produto.get_attribute("src")
        alt = produto.get_attribute("alt")

        if src in imagens_vistas:
            imagens_repetidas.append(alt)
        else:
            imagens_vistas.add(src)

    assert len(imagens_repetidas) == 0, f"Produtos com imagem repetida: {imagens_repetidas}"

         
def test_invalid_problem_user_button(page:Page): #verificar se o usuário problem_user tem botões de adicionar ao carrinho funcionando corretamente
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "problem_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect((page).locator(".title")).to_have_text("Products") 

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click("#add-to-cart-sauce-labs-bike-light")
    page.click("#add-to-cart-sauce-labs-bolt-t-shirt")
    page.click("#add-to-cart-sauce-labs-fleece-jacket")
    page.click("#add-to-cart-sauce-labs-onesie")
    page.click('[id="add-to-cart-test.allthethings()-t-shirt-(red)"]')

    page.wait_for_timeout(3000)

    expect((page).locator(".shopping_cart_badge")).to_have_text("6")


def test_invalid_problem_user_button_remove(page:Page): #verificar se o usuário problem_user tem botões de remover do carrinho funcionando corretamente
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "problem_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.wait_for_load_state("networkidle")

    ids_produtos = [
            "sauce-labs-backpack",
            "sauce-labs-bike-light",
            "sauce-labs-bolt-t-shirt",
            "sauce-labs-fleece-jacket",
            "sauce-labs-onesie",
            "test.allthethings()-t-shirt-(red)"
        ]

    nao_adicionados = []
    nao_removidos = []

    for id_produto in ids_produtos:
        botao_adicionar = page.locator(f'[id="add-to-cart-{id_produto}"]')
        botao_remover = page.locator(f'[id="remove-{id_produto}"]')

        botao_adicionar.click()
        page.wait_for_timeout(500)

        if not botao_remover.is_visible():
            nao_adicionados.append(id_produto)
            continue

        botao_remover.click()
        page.wait_for_timeout(500)

        if not botao_adicionar.is_visible():
            nao_removidos.append(id_produto)

    assert len(nao_removidos) == 0, f"Produtos não removidos: {nao_removidos}"


def test_invalid_problem_user_filtro(page: Page):
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "problem_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    filtros = ["az", "za", "lohi", "hilo"]
    filtros_ruins = []

    for filtro in filtros:

        produtos_antes = page.locator(".inventory_item").all_text_contents()

        page.select_option(".product_sort_container", filtro)

        produtos_depois = page.locator(".inventory_item").all_text_contents()

        if produtos_antes == produtos_depois:
            filtros_ruins.append(filtro)

    assert len(filtros_ruins) == 0, f"Os seguintes filtros não alteraram a ordem dos produtos: {filtros_ruins}"



def test_invalid_problem_user_checkout(page:Page): #verificar se o usuário problem_user consegue preencher os dados corretamente e não alterar os valores

    page.goto("https://saucedemo.com")
    page.fill("#user-name", "problem_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")

    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    page.click("#checkout")

    page.fill("#first-name", "João")
    page.fill("#last-name", "Marcos")
    page.fill("#postal-code", "666777")

    print("first-name:", page.locator("#first-name").input_value())
    print("last-name:", page.locator("#last-name").input_value())
    print("postal-code:", page.locator("#postal-code").input_value())

    expect(page.locator("#first-name")).to_have_value("João")
    expect(page.locator("#last-name")).to_have_value("Marcos")
    expect(page.locator("#postal-code")).to_have_value("666777")

    page.click("#continue")

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")


def test_invalid_performance_glitch_user_tempo_login(page:Page): #verificar se o tempo de login do usuário performance_glitch_user
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "performance_glitch_user")
    page.fill("#password", "secret_sauce")

    inicio = time.time()
    page.click("#login-button")
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    fim = time.time()

    tempo_gasto = fim - inicio
    assert tempo_gasto < 1, f"O login demorou {tempo_gasto:.2f} segundos"

    expect(page.locator(".title")).to_have_text("Products")


def test_invalid_performance_glitch_user_navegação(page:Page): #verificar se o usuário performance_glitch_user consegue ir do carrinho até pagina principal num tempo aceitável
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "performance_glitch_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")

    inicio = time.time()
    page.click("#continue-shopping")
    fim = time.time()

    tempo_gasto = fim - inicio
    assert tempo_gasto < 1, f"A navegação demorou {tempo_gasto:.2f} segundos"


def test_invalid_error_user_button(page:Page): #verificar se o usuário error_user tem botões de adicionar ao carrinho funcionando corretamente
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "error_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect((page).locator(".title")).to_have_text("Products") 

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click("#add-to-cart-sauce-labs-bike-light")
    page.click("#add-to-cart-sauce-labs-bolt-t-shirt")
    page.click("#add-to-cart-sauce-labs-fleece-jacket")
    page.click("#add-to-cart-sauce-labs-onesie")
    page.click('[id="add-to-cart-test.allthethings()-t-shirt-(red)"]')

    assert page.locator(".shopping_cart_badge").inner_text() == "6", f"O número de itens no carrinho é {page.locator('.shopping_cart_badge').inner_text()}, mas deveria ser 6"


def test_invalid_error_user_last_name_visivel(page:Page): #verificar se o usuário error_user consegue preencher os dados
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "error_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    page.click("#add-to-cart-sauce-labs-backpack")
    page.click(".shopping_cart_link")

    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    page.click("#checkout")

    page.fill("#first-name", "João")
    page.fill("#last-name", "Marcos")
    page.fill("#postal-code", "666777")

    expect(page.locator("#first-name")).to_have_value("João")
    expect(page.locator("#last-name")).to_have_value("Marcos")
    expect(page.locator("#postal-code")).to_have_value("666777")

    page.click("#continue")

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

