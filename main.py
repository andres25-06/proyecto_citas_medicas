# main.py
from Vista.vista_login import login
from Vista.vista_principal import vista_principal

def main():
    usuario = login()
    if usuario:
        vista_principal()

if __name__ == "__main__":
    main()

