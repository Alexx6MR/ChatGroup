import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Cambia el nivel según sea necesario
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='log/server.log',  # Archivo donde se guardarán los logs
        filemode='a'  # Modo de apertura del archivo: 'a' para agregar
    )
