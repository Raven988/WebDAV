from webdav3.client import Client
from conf import options


def folder_tree(client, remote_path, indent=0):
    # Получаем список содержимого папки
    contents = client.list(remote_path)

    for item in contents:
        if item.endswith('/'):
            print("  " * indent + f"📁 {item}")
            # Рекурсивно вызываем функцию для отображения содержимого подпапки
            folder_tree(client, remote_path + item, indent + 1)
        elif item.endswith('.pdf'):
            print("  " * indent + f"📙 {item} ")
        elif item.endswith('.json'):
            print("  " * indent + f"📜 {item} ")
        elif item.endswith('.xlsx'):
            print("  " * indent + f"📊 {item} ")
        else:
            print("  " * indent + f"📦 {item} ")


if __name__ == '__main__':
    client = Client(options)
    free_size = client.free()
    print(free_size // 1024 // 1024, 'Mb')
    folder_tree(client, remote_path='/')
