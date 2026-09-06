import pytest
from playwright.sync_api import Page, expect


def test_login_valido(page:Page):  #entrar no site com usuário válido
    page.goto("https://saucedemo.com")
    page.fill("#user-name", "standard_user")
    page.fill("#password", "secret_sauce")
    page.click("#login-button")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect((page).locator(".title")).to_have_text("Products")


def test_problem_user_image(page:Page):  #verificar se o usuário problem_user tem imagens repetidas
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

    assert len(imagens_repetidas) == 5, f"Produtos com imagem repetida: {imagens_repetidas}"


         
def test_problem_user_button(page:Page): #verificar se o usuário problem_user tem botões de adicionar ao carrinho funcionando corretamente
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

    expect((page).locator(".shopping_cart_badge")).to_have_text("3")


def test_problem_user_button_remove(page:Page): #verificar se o usuário problem_user tem botões de remover do carrinho funcionando corretamente
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
        page.wait_for_timeout(500)  # dá meio segundo pro botão trocar

        if not botao_remover.is_visible():
            nao_adicionados.append(id_produto)
            continue

        botao_remover.click()
        page.wait_for_timeout(500)

        if not botao_adicionar.is_visible():
            nao_removidos.append(id_produto)

    assert len(nao_removidos) == 0, f"Produtos não removidos: {nao_removidos}"



