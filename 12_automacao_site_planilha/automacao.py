import time
import webbrowser

import pyautogui
import pyperclip

pyautogui.FAILSAFE = True


def abrir_site(URL):

    webbrowser.open(URL)
    time.sleep(12)

def fazer_login(EMAIL_LOGIN, SENHA_LOGIN):

    pyautogui.moveTo(836, 532, duration=0.5)
    pyautogui.click()
    pyautogui.write(EMAIL_LOGIN, interval=0.2)

    time.sleep(4)

    pyautogui.moveTo(818, 631, duration=0.5)
    pyautogui.click()
    pyautogui.write(SENHA_LOGIN, interval=0.2)

    try:
        entrar = pyautogui.locateCenterOnScreen("imagens/entrar.png", confidence=0.9)
        pyautogui.moveTo(entrar)
        pyautogui.click()
    except pyautogui.ImageNotFoundException:
        pyautogui.moveTo(959, 803, duration=0.5)
        pyautogui.click()

def colar_texto(texto):

    if texto is None:
        texto = ""

    texto = str(texto)
    pyperclip.copy(texto)
    pyautogui.hotkey("ctrl", "v")

def preencher_formulario(cadastro):

    nome = cadastro["nome"] 
    email = cadastro["email"] 
    telefone = cadastro["telefone"] 
    empresa = cadastro["empresa"] 
    cargo =  cadastro["cargo"] 
    cidade = cadastro["cidade"] 
    estado = cadastro["estado"] 
    observacoes = cadastro["observacoes"]

    pyautogui.moveTo(421, 649, duration=0.5)
    pyautogui.click()
    colar_texto(nome)

    time.sleep(2)
    pyautogui.press("tab")
    colar_texto(email)

    time.sleep(2)
    pyautogui.press("tab")
    colar_texto(telefone)

    time.sleep(2)
    pyautogui.press("tab")
    colar_texto(empresa)

    time.sleep(2)
    pyautogui.press("tab")
    colar_texto(cargo)

    time.sleep(2)
    pyautogui.press("tab")
    colar_texto(cidade)

    pyautogui.press("tab")
    time.sleep(2)
    pyautogui.moveTo(1136, 971)
    pyautogui.click()
    time.sleep(4)
    pyautogui.write(estado)
    time.sleep(2)
    pyautogui.press("enter")

    time.sleep(2)
    pyautogui.press("tab")
    colar_texto(observacoes)

    try:
        add = pyautogui.locateCenterOnScreen("imagens/add.png", confidence=0.9)
        pyautogui.moveTo(add)
        pyautogui.click()
    except pyautogui.ImageNotFoundException:
        pyautogui.moveTo(218, 894, duration=0.5)
        pyautogui.click()


    confirmacao = pyautogui.locateCenterOnScreen("imagens/confirmacao.png", confidence=0.7)

    if confirmacao:
        time.sleep(5)
        pyautogui.scroll(999)
        return True

    time.sleep(5)
    pyautogui.scroll(999)
    return False

    
    
    
