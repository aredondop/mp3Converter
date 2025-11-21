# mp3Converter - Conversor Recursivo de FLAC a MP3 (Windows)

Herramienta en Python diseñada para automatizar la conversión recursiva de archivos de audio FLAC a MP3, manteniendo la estructura de directorios original y ofreciendo un control preciso sobre la calidad (bitrate) de la salida.

---

## Requisitos

El script requiere dos componentes clave para funcionar correctamente:

### 1. Requisitos del Sistema (FFmpeg)

El script utiliza el binario de FFmpeg para realizar la conversión de audio.

* **Instalación de FFmpeg:**
    1.  Descarga la versión más reciente de FFmpeg para Windows (se recomienda el *build* de gyan.dev).
    2.  Descomprime el archivo ZIP en una ubicación permanente, por ejemplo: `C:\ffmpeg`.
    3.  **Añadir al PATH:** Debes añadir la ruta de la carpeta `bin` de FFmpeg a la variable de entorno `PATH` de Windows (ejemplo: `C:\ffmpeg\bin`). Esto permite que el script acceda al comando `ffmpeg` desde cualquier Terminal.

### 2. Requisitos de Python

Necesitas tener Python instalado (versión 3.6 o superior). Las dependencias de Python se instalan a través del archivo `requirements.txt`.

* **Instalación de Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

---

## Uso del Script

El script se ejecuta desde la Terminal de Windows (CMD o PowerShell) y requiere el directorio fuente como primer argumento.

### Estructura de comandos

```bash
python mp3Converter.py [DIRECTORIO_FUENTE] [OPCIONES]
