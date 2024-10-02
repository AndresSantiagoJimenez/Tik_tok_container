import os

class Settings:
    # AWS S3
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    BUCKET_NAME = 'sns-amazonmusic-trends'  # Nombre del bucket de salida
    #S3_PREFIX = 'raw/'  # Prefijo en S3
    #S3_PREFIX_RAW = 'src/sales/'  # Prefijo en S3 para raw

    # FTP
    FTP_HOST = 'ftp.merlinnetwork.org'
    FTP_PORT = int(os.getenv('FTP_PORT', 21))  # Puerto FTP (predeterminado: 21)
    FTP_USERNAME = os.getenv('FTP_USERNAME')
    FTP_PASSWORD = os.getenv('FTP_PASSWORD')
    FTP_DIRECTORIO_RAIZ = '/trends/'  # Directorio raíz en FTP

    # Verificación de variables de entorno críticas
    if not FTP_USERNAME or not FTP_PASSWORD:
        raise ValueError("Las variables de entorno FTP_USERNAME y FTP_PASSWORD deben estar definidas")

    # Directorios
    DIRECTORIO_TEMPORAL = 'src/Data'
    

settings = Settings()