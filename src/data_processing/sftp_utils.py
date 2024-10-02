from ftplib import FTP_TLS
from loguru import logger

def listar_archivos_ftp(ftps, ftp_directorio_raiz='/trends/'):
    archivos_encontrados = []

    try:
        logger.info(f"Cambiando al directorio {ftp_directorio_raiz}...")
        ftps.cwd(ftp_directorio_raiz)  # Cambiar al directorio 'trends'
        
        logger.info(f"Listando archivos en {ftp_directorio_raiz}...")
        
        # Listar archivos y directorios en el directorio 'trends'
        directorios = ftps.nlst()  # Listar archivos y directorios

        for directorio in directorios:
            logger.info(f"Entrando en el directorio: {directorio}")
            ftps.cwd(directorio)  # Cambiar al subdirectorio
            
            # Listar archivos en 'tiktok' si existe
            try:
                ftps.cwd('tiktok')  # Intentar entrar en 'tiktok'
                logger.info(f"Listando archivos en '{directorio}/tiktok'...")
                
                archivos_tiktok = ftps.nlst()  # Listar archivos en 'tiktok'
                for archivo in archivos_tiktok:
                    logger.info(f"Archivo encontrado en 'tiktok': {archivo}")
                    archivos_encontrados.append(f"{directorio}/tiktok/{archivo}")

                # Verificar si 'Weekly Charts' existe dentro de 'tiktok'
                try:
                    ftps.cwd('Weekly Charts')  # Intentar entrar en 'Weekly Charts'
                    logger.info(f"Listando archivos en '{directorio}/tiktok/Weekly Charts'...")
                    
                    archivos_weekly = ftps.nlst()  # Listar archivos en 'Weekly Charts'
                    for archivo in archivos_weekly:
                        logger.info(f"Archivo encontrado en 'Weekly Charts': {archivo}")
                        archivos_encontrados.append(f"{directorio}/tiktok/Weekly Charts/{archivo}")

                    # Volver al directorio anterior
                    ftps.cwd('..')

                except Exception as e:
                    logger.info(f"No se encontró la carpeta 'Weekly Charts' en '{directorio}/tiktok', ignorando... Error: {str(e)}")

                # Volver al directorio anterior (a la carpeta de año/mes)
                ftps.cwd('..')  

            except Exception:
                logger.info(f"No se encontró la carpeta 'Weekly Charts' en {directorio}, ignorando...")

            # Regresar al directorio raíz
            ftps.cwd('..')

    except Exception as e:
        logger.error(f"Error al conectar o procesar archivos FTP: {str(e)}")

    return archivos_encontrados  # Retornar la lista de archivos encontrados
