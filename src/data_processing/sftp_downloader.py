import os
from loguru import logger
from .sftp_utils import listar_archivos_ftp
from ftplib import FTP_TLS
from config.settings import settings  # Asegúrate de que este archivo settings.py existe

def descargar_tiktok(archivos_tiktok, ftps, directorio_local):
    """
    Descarga archivos de las carpetas que contienen 'tiktok', respetando la estructura de carpetas.
    
    Args:
        archivos_tiktok: Lista de archivos que contienen 'tiktok'.
        ftps: Conexión FTPS activa.
        directorio_local: Directorio local donde se almacenarán los archivos.
    """
    if not archivos_tiktok:
        logger.info("No se encontraron archivos en carpetas 'tiktok' para descargar.")
        return

    try:
        for archivo in archivos_tiktok:
            # Generar la ruta local donde se guardará el archivo
            ruta_local = os.path.join(directorio_local, archivo)
            directorio_destino = os.path.dirname(ruta_local)  # Obtener la carpeta destino
            
            # Crear directorios locales si no existen
            if not os.path.exists(directorio_destino):
                os.makedirs(directorio_destino)
                logger.info(f"Directorio creado: {directorio_destino}")

            # Descargar el archivo desde el FTP
            with open(ruta_local, 'wb') as f:
                logger.info(f"Descargando archivo: {archivo} en {ruta_local}")
                ftps.retrbinary(f'RETR {archivo}', f.write)

        logger.info("Descarga completada exitosamente.")

    except Exception as e:
        logger.error(f"Error durante la descarga de archivos: {str(e)}")
        ftps.quit()  # Asegúrate de cerrar la conexión si ocurre un error

    finally:
        try:
            ftps.quit()
            logger.info("Conexión FTPS cerrada.")
        except Exception as e:
            logger.error(f"Error cerrando la conexión FTPS: {str(e)}")
