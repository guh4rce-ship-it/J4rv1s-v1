import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import executor_sites  # módulo que criamos

# 🔊 VOZ
engine = pyttsx3.init()
engine.setProperty('rate', 180)

def falar(texto):
    print("Jarvis:", texto)
    engine.say(texto)
    engine.runAndWait()

# 🎤 OUVIR
def ouvir():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Ouvindo...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
        comando = recognizer.recognize_google(audio, language='pt-BR')
        print("Você disse:", comando)
        return comando.lower()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        print("Não entendi o áudio")
        return ""
    except Exception as e:
        print("Erro ao ouvir:", e)
        return ""

# 🧠 ATIVAÇÃO
def ativado(comando):
    return "jarvis" in comando

# 🌐 Dicionários de processos/sites abertos
programas_abertos = {}
sites_abertos = {}

# 🧠 INTERPRETADOR
def interpretar(comando):
    if "youtube" in comando and "fechar" not in comando:
        return "youtube"
    elif "google" in comando and "fechar" not in comando:
        return "google"
    elif "chrome" in comando and "fechar" not in comando:
        return "chrome"
    elif "opera" in comando and "fechar" not in comando:
        return "opera"
    elif "bloco" in comando and "fechar" not in comando:
        return "bloco"
    elif "fechar" in comando:
        return f"fechar_{comando.replace('fechar ', '').strip()}"
    elif "hora" in comando:
        return "hora"
    elif "desligar" in comando:
        return "desligar"
    elif "sair" in comando:
        return "sair"
    else:
        return "desconhecido"

# ⚙️ EXECUTOR
def executar(comando):
    comando = comando.replace("jarvis", "").strip()
    acao = interpretar(comando)

    # 🌐 ABRIR SITES (Chrome via Selenium)
    if acao in ["youtube", "google"]:
        try:
            if acao == "youtube":
                sites_abertos["youtube"] = executor_sites.abrir_site("https://www.youtube.com")
                falar("YouTube aberto")
            elif acao == "google":
                sites_abertos["google"] = executor_sites.abrir_site("https://www.google.com")
                falar("Google aberto")
        except Exception as e:
            falar(f"Erro ao abrir {acao}: {e}")

    # ❌ FECHAR SITES
    elif acao.startswith("fechar_"):
        nome = acao.replace("fechar_", "")
        driver = sites_abertos.get(nome)
        if driver:
            executor_sites.fechar_site(driver)
            sites_abertos.pop(nome)
            falar(f"{nome.capitalize()} fechado")
        else:
            proc = programas_abertos.get(nome)
            if proc:
                proc.terminate()
                programas_abertos.pop(nome)
                falar(f"{nome.capitalize()} fechado")
            else:
                falar(f"{nome.capitalize()} não está aberto pelo Jarvis")

    # 🖥️ ABRIR PROGRAMAS LOCAIS
    elif acao == "chrome":
        try:
            proc = subprocess.Popen([r"C:/Program Files/Google/Chrome/Application/chrome.exe"])
            programas_abertos["chrome"] = proc
            falar("Chrome aberto")
        except Exception as e:
            falar(f"Erro ao abrir Chrome: {e}")

    elif acao == "opera":
        try:
            proc = subprocess.Popen([r"C:/Users/guh4r/AppData/Local/Programs/Opera GX/launcher.exe"])
            programas_abertos["opera"] = proc
            falar("Opera GX aberto")
        except Exception as e:
            falar(f"Erro ao abrir Opera GX: {e}")

    elif acao == "bloco":
        try:
            proc = subprocess.Popen(["notepad.exe"])
            programas_abertos["bloco"] = proc
            falar("Bloco de notas aberto")
        except Exception as e:
            falar(f"Erro ao abrir bloco de notas: {e}")

    # ⏰ HORA
    elif acao == "hora":
        hora = datetime.datetime.now().strftime("%H:%M")
        falar(f"Agora são {hora}")

    # 🔌 DESLIGAR
    elif acao == "desligar":
        falar("Você quer mesmo desligar o computador?")
        confirmacao = ouvir()
        if "sim" in confirmacao:
            falar("Desligando em 5 segundos")
            os.system("shutdown /s /t 5")
        else:
            falar("Cancelado")

    # ❌ SAIR
    elif acao == "sair":
        falar("Encerrando Jarvis")
        exit()

    # 🤖 FALLBACK
    else:
        falar("Não entendi, mas posso aprender isso depois")

# 🚀 START
falar("Jarvis iniciado")

while True:
    comando = ouvir()
    if comando and ativado(comando):
        falar("Estou ouvindo")
        executar(comando)