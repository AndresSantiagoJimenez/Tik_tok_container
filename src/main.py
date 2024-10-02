import os
import ssl
from ftplib import FTP_TLS
from loguru import logger
import logging
from config.settings import settings
from data_processing.file_uploader import asegurar_directorio
from data_processing.sftp_utils import listar_archivos_ftp
from data_processing.sftp_downloader import descargar_tiktok#, validar_y_descomprimir_archivos

def main():
    # Inicio del proceso
    logger.info("Iniciando el proceso...")

    # Asegurarse de que el directorio temporal exista
    asegurar_directorio(settings.DIRECTORIO_TEMPORAL)
    logger.info(f"Directorio temporal asegurado: {settings.DIRECTORIO_TEMPORAL}")

    # Habilitar logging de SSL
    logging.basicConfig(level=logging.DEBUG)

    # Crear un contexto de SSL
    context = ssl.create_default_context()
    context.set_ciphers('HIGH:!aNULL:!MD5')  # Usa cifrados seguros

    # Forzar uso de TLS 1.2
    context.options |= ssl.OP_NO_SSLv2
    context.options |= ssl.OP_NO_SSLv3
    context.options |= ssl.OP_NO_TLSv1
    context.options |= ssl.OP_NO_TLSv1_1

    # Usar el contexto en FTPS
    ftps = FTP_TLS(context=context)

    try:
        # Conectar al servidor FTPS
        logger.info(f"Conectando al servidor FTPS {settings.FTP_HOST}:{settings.FTP_PORT} ...")
        ftps.connect(settings.FTP_HOST, settings.FTP_PORT, timeout=300)

        # Iniciar sesión
        logger.info("Iniciando sesión...")
        ftps.login(settings.FTP_USERNAME, settings.FTP_PASSWORD)
        ftps.prot_p()  # Cambiar a modo de protección de datos
        logger.info("Conexión FTPS establecida correctamente.")

        # Obtener la lista de archivos desde el servidor FTP
        try:
            archivos_remotos = listar_archivos_ftp(ftps, settings.FTP_DIRECTORIO_RAIZ)
            if archivos_remotos:
                logger.info(f"Archivos encontrados: {archivos_remotos}")
                
                # Llamar a la función para descargar solo los archivos de tiktok
                descargar_tiktok(archivos_remotos, ftps, settings.DIRECTORIO_TEMPORAL)
            else:
                logger.warning("No se encontraron archivos en el directorio.")
        except Exception as list_error:
            logger.error(f"Ocurrió un error al listar los archivos: {list_error}")

    except Exception as e:
        logger.error(f"Error conectando al servidor FTPS o durante la descarga: {e}")
    finally:
        # Cerrar la conexión FTPS solo si está abierta
        try:
            ftps.quit()
            logger.info("Conexión FTPS cerrada.")
        except Exception as e:
            logger.error(f"Error cerrando la conexión FTPS: {e}")

    # Fin del proceso
    logger.info("Proceso completado con éxito.")

if __name__ == "__main__":
    main()
