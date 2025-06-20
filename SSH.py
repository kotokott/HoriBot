import paramiko

# Параметры подключения
hostname = '[2a03:6f00:4::72cb]'
port = 22
username = 'root'
password = 'am^ioF*aML3F1M'  # Или используйте ключи SSH

# Путь к файлу на локальной машине и на сервере
local_path = 'C:/Hori/Main.py'
remote_path = '/home'

# Создание SSH-клиента
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Подключение к серверу
    ssh_client.connect(hostname, port, username, password)

    # Создание SFTP-сессии
    sftp = ssh_client.open_sftp()

    # Копирование файла
    sftp.put(local_path, remote_path)

    # Закрытие SFTP-сессии и SSH-клиента
    sftp.close()
    ssh_client.close()

    print(f"Файл {local_path} успешно скопирован на {remote_path}")
except Exception as e:
    print(f"Ошибка: {e}")