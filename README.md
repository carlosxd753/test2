Netinventario

Pasos para poder usar la aplicacion:

1) Clonar el repositorio
2) Utilizar estos comandos en la raiz del proyecto:

python3 -m venv .venv
source .venv/bin/activate

3) Instalar la dependencia con este comando:

python -m pip install requests

4) Brindar tus credenciales para poder hacer peticiones a la API de cisco

export CATALYST_USER="usuario"
export CATALYST_PASSWORD="password"

5) Por ultimo ya se podria ejecutar la aplicacion con el siguiente comando:

python netinventario.py
