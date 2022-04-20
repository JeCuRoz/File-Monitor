# Folder Monitor

A simple tool that watches a folder and run a program or command when a file or folder is created in it.

The application and the command are executed in the foreground, so if you create a second file, the associated command will not be executed until the processing of the first file is finished. 

**Usage:** `python folder_monitor.py [-h] -c COMMAND folder`

**Positional arguments:**

  *folder*               
    Monitored folder.

**Optional arguments:**

  *-h, --help*            
    Show the help message

  *-c COMMAND, --command COMMAND*    
    Required. Command to execute when a new file or folder is created
    If it contains spaces, it must be enclosed in quotation marks.

**Example:**

    python folder_monitor.py testfolder -c 'ls -l'

**Output example:**

    testfolder/NewFile.txt
    Command to execute: ls -l "testfolder/NewFile.txt"
    Success: True
    Exit code: 0
    Command output:
    -rw-r--r-- 1 test test 2 abr 20 14:58 testfolder/NewFile.txt


---


Un sencilla utilidad que permite supervisar una carpeta y ejecutar un comando o programa 
cuando se crea un nuevo fichero o carpeta en ella.

La aplicación y el comando se ejecutan en primer plano, por lo que si crea un segundo fichero no se ejecutará el comando asociado hasta que termine el procesamiento del primero. 

**Uso:** `python folder_monitor.py [-h] -c COMMAND folder`

**Argumentos posicionales:**

  *folder*                
    Carpeta a supervisar.

**Argumentos opcionales:**

  *-h, --help*           
    Muestra el mensaje de ayuda.

  *-c COMMAND, --command COMMAND*     
    Requerido. Acción a realizar cuando se crea un nuevo fichero o carpeta. 
    Si contiene espacios es necesario encerrarlo entre comillas.

**Ejemplo:**

    python folder_monitor.py testfolder -c 'ls -l'

**Ejemplo de salida:**

    testfolder/NewFile.txt
    Command to execute: ls -l "testfolder/NewFile.txt"
    Success: True
    Exit code: 0
    Command output:
    -rw-r--r-- 1 test test 2 abr 20 14:58 testfolder/NewFile.txt
