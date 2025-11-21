import os
import subprocess
import argparse
import sys
from pathlib import Path

# La importación de tqdm se hace en runtime después de verificar su existencia.

# --- Funciones de Comprobación de Entorno ---

def check_tqdm():
    """Comprueba si tqdm está instalado. Si no, informa al usuario cómo instalarlo."""
    try:
        global tqdm
        # Importación tardía (lazy import) de tqdm
        from tqdm import tqdm
        globals()['tqdm'] = tqdm  # Hacemos tqdm accesible globalmente
        return True
    except ImportError:
        print("--- REQUISITO: Librería 'tqdm' no encontrada ---")
        print("La librería 'tqdm' es necesaria para la barra de progreso.")
        print("Instale todas las dependencias de Python ejecutando en el Terminal:")
        print("   pip install -r requirements.txt")
        return False

def check_ffmpeg_path():
    """Comprueba si FFmpeg es accesible desde el PATH."""
    print("--- REQUISITO: Comprobación de 'ffmpeg' ---")
    try:
        # Intenta ejecutar ffmpeg para ver si es accesible
        subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True, text=True, encoding='utf-8')
        print("✅ 'ffmpeg' encontrado en el PATH.")
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ 'ffmpeg' NO encontrado en el PATH o no accesible.")
        print("\nINSTRUCCIONES IMPORTANTES:")
        print("1. Descargue FFmpeg (por ejemplo, desde https://ffmpeg.org/download.html).")
        print("2. Descomprima y añada la carpeta 'bin' de FFmpeg a la variable de entorno PATH de Windows.")
        print("3. Reinicie su Terminal (CMD/PowerShell) y vuelva a ejecutar el script.")
        return False

# --- Lógica de Conversión ---

def get_flac_files(root_dir: Path):
    """Busca recursivamente todos los archivos .flac en el directorio dado."""
    return list(root_dir.rglob('*.flac'))

def convert_flac_to_mp3(input_file: Path, output_file: Path, bitrate: str):
    """Ejecuta el comando FFmpeg para la conversión."""
    command = [
        'ffmpeg',
        '-i', str(input_file),
        '-vn',
        '-ar', '44100',
        '-ac', '2',
        '-b:a', f'{bitrate}k',
        str(output_file)
    ]
    
    # El resultado de la conversión se ignora aquí, se maneja el error en main
    subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8')

def mp3Converter():
    """Función principal que maneja los requisitos y la lógica de conversión."""
    
    # 1. Comprobación de Requisitos
    if not check_tqdm():
        sys.exit(1) # Salir si tqdm no se puede instalar
        
    if not check_ffmpeg_path():
        sys.exit(1) # Salir si ffmpeg no está en el PATH

    # 2. Configuración de Argumentos (solo si los requisitos se cumplen)
    parser = argparse.ArgumentParser(
        description="mp3Converter: Convierte recursivamente archivos FLAC a MP3."
    )
    parser.add_argument(
        'source_dir',
        type=str,
        help="Directorio raíz donde buscará los archivos FLAC."
    )
    parser.add_argument(
        '-b', '--bitrate',
        type=int,
        default=320,
        choices=[128, 192, 320],
        help="Bitrate del MP3 de salida (128, 192, 320). Por defecto es 320k."
    )
    
    args = parser.parse_args()
    
    source_path = Path(args.source_dir)
    bitrate_str = str(args.bitrate)

    if not source_path.is_dir():
        print(f"Error: El directorio fuente no existe: {args.source_dir}")
        sys.exit(1)

    # 3. Escaneo y Pre-procesamiento
    print("\n--- Escaneando archivos ---")
    flac_files = get_flac_files(source_path)
    total_files = len(flac_files)
    
    if total_files == 0:
        print(f"No se encontraron archivos .flac en '{source_path}' o sus subdirectorios.")
        return

    print(f"Total de canciones FLAC encontradas: {total_files}")
    print(f"Bitrate de salida: {bitrate_str} kbps")

    # 4. Conversión con Interfaz Interactiva
    print("\n--- Iniciando conversión ---")
    
    # tqdm proporciona la barra de progreso interactiva
    # Nota: tqdm debe estar disponible globalmente gracias a check_tqdm()
    with tqdm(flac_files, desc="Progreso total", unit="canción", ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]") as progress_bar:
        for input_file in progress_bar:
            try:
                output_file = input_file.with_suffix('.mp3')

                # Muestra el nombre del archivo actual sin interferir con la barra
                progress_bar.set_postfix_str(f"Convirtiendo: {input_file.name}")
                
                convert_flac_to_mp3(input_file, output_file, bitrate_str)

            except subprocess.CalledProcessError as e:
                # Si FFmpeg devuelve un error, lo registramos.
                progress_bar.write(f"\n[ERROR] Falló la conversión de {input_file.name}: {e.stderr.strip()}")
            except Exception as e:
                progress_bar.write(f"\n[ERROR] Ocurrió un error inesperado al procesar {input_file.name}: {e}")
                
        progress_bar.set_postfix_str("Finalizado.")

    print("\n--- Conversión completada ---")


if __name__ == "__main__":
    mp3Converter()