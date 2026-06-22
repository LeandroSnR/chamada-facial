"""
Diagnóstico de requisitos para a máquina servidora.

Roda checagens leves (sem instalar nada) e imprime um relatório
indicando o que está OK e o que precisa ser ajustado antes de
instalar o servidor (FastAPI + OpenCV + face_recognition/dlib).

Uso:
    python diagnostico_servidor.py
"""

import platform
import shutil
import subprocess
import sys


OK = "[OK]"
ALERTA = "[ALERTA]"
FALHA = "[FALHA]"


def linha(titulo: str) -> None:
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def checar_python() -> None:
    linha("Python")
    versao = sys.version_info
    versao_str = f"{versao.major}.{versao.minor}.{versao.micro}"
    print(f"Versão detectada: {versao_str}")

    if (versao.major, versao.minor) in [(3, 9), (3, 10), (3, 11)]:
        print(f"{OK} Versão compatível com face_recognition/dlib.")
    elif (versao.major, versao.minor) >= (3, 12):
        print(
            f"{ALERTA} Python 3.12+ pode ter problemas de compatibilidade "
            "com versões mais antigas do dlib. Se a instalação do servidor "
            "falhar mais adiante, considere usar Python 3.10 ou 3.11 "
            "(pode instalar em paralelo sem remover o atual)."
        )
    else:
        print(
            f"{FALHA} Versão muito antiga. Recomenda-se Python 3.10 ou 3.11."
        )


def checar_comando(nome: str, comando_versao: list) -> bool:
    caminho = shutil.which(nome)
    if not caminho:
        return False
    try:
        resultado = subprocess.run(
            comando_versao, capture_output=True, text=True, timeout=5
        )
        saida = (resultado.stdout or resultado.stderr).strip().splitlines()[0]
        print(f"{OK} {nome} encontrado: {saida} ({caminho})")
        return True
    except Exception:
        print(f"{OK} {nome} encontrado em {caminho} (não foi possível obter versão)")
        return True


def checar_build_tools() -> None:
    linha("Compilador / Build Tools (necessário para compilar o dlib)")

    sistema = platform.system()
    print(f"Sistema operacional detectado: {sistema}")

    tem_cmake = checar_comando("cmake", ["cmake", "--version"])
    if not tem_cmake:
        print(f"{FALHA} cmake não encontrado. É necessário para compilar o dlib.")

    if sistema == "Windows":
        print(
            f"{ALERTA} No Windows, além do cmake, você precisa do "
            "'Visual Studio Build Tools' (componente 'Desktop development with C++'). "
            "Baixe em: https://visualstudio.microsoft.com/visual-cpp-build-tools/"
        )
    elif sistema == "Linux":
        tem_gcc = checar_comando("gcc", ["gcc", "--version"])
        if not tem_gcc:
            print(
                f"{FALHA} gcc não encontrado. Instale com: "
                "sudo apt install build-essential cmake"
            )
    elif sistema == "Darwin":
        tem_clang = checar_comando("clang", ["clang", "--version"])
        if not tem_clang:
            print(
                f"{FALHA} clang não encontrado. Instale as Command Line Tools: "
                "xcode-select --install"
            )


def checar_ram() -> None:
    linha("Memória RAM")
    try:
        import psutil

        total_gb = psutil.virtual_memory().total / (1024 ** 3)
        print(f"RAM total: {total_gb:.1f} GB")
        if total_gb >= 8:
            print(f"{OK} RAM confortável para o projeto.")
        elif total_gb >= 4:
            print(f"{ALERTA} RAM suficiente, mas no limite. Evite rodar muitos outros programas pesados junto com o servidor.")
        else:
            print(f"{FALHA} RAM abaixo do recomendado (mínimo 4GB).")
    except ImportError:
        print(
            f"{ALERTA} Pacote 'psutil' não instalado, não foi possível medir a RAM automaticamente.\n"
            "  Verifique manualmente (Gerenciador de Tarefas / 'free -h' / 'Sobre este Mac')."
        )


def checar_disco() -> None:
    linha("Espaço em disco")
    try:
        total, usado, livre = shutil.disk_usage(".")
        livre_gb = livre / (1024 ** 3)
        print(f"Espaço livre no disco atual: {livre_gb:.1f} GB")
        if livre_gb >= 5:
            print(f"{OK} Espaço suficiente.")
        elif livre_gb >= 2:
            print(f"{ALERTA} Espaço no limite (recomendado: 5GB+ livres).")
        else:
            print(f"{FALHA} Pouco espaço livre em disco.")
    except Exception as e:
        print(f"{ALERTA} Não foi possível verificar o disco: {e}")


def checar_pip() -> None:
    linha("pip")
    try:
        import pip  # noqa: F401

        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
        )
        print(f"{OK} {resultado.stdout.strip()}")
    except ImportError:
        print(f"{FALHA} pip não encontrado para este interpretador Python.")


def main() -> None:
    print("Diagnóstico de requisitos — servidor de reconhecimento facial")
    print(f"Plataforma: {platform.platform()}")

    checar_python()
    checar_pip()
    checar_build_tools()
    checar_ram()
    checar_disco()

    linha("Resumo")
    print(
        "Revise os itens marcados como [ALERTA] ou [FALHA] acima antes de\n"
        "instalar as dependências do servidor (requirements.txt).\n"
        "Itens [OK] não precisam de ação."
    )


if __name__ == "__main__":
    main()
