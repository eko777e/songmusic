import os, re


def errors_chats(id, error_message):
    if os.path.exists("errors_chats.txt"):
        os.remove("errors_chats.txt")
    with open("errors_chats.txt", "a") as file:
        file.write(f"🆔ID: {id}, ❌Xəta: {error_message}\n")


def errors_users(id, error_message):
    if os.path.exists("errors_users.txt"):
        os.remove("errors_users.txt")
    with open("errors_users.txt", "a") as file:
        file.write(f"🆔ID: {id}, ❌Xəta: {error_message}\n")


async def send_errors(client, file_name, chat_id):
    try:
        with open(file_name, 'r') as file:
            if file.read(1):
                file.seek(0)
                await client.send_document(chat_id, file_name)
    except FileNotFoundError:
        pass


def extract_chat_ids(file_path):
    chat_id_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r'🆔ID: (-\d+)', line)
            if match:
                chat_id_list.append(int(match.group(1)))
    return chat_id_list


def extract_user_ids(file_path):
    user_id_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r'🆔ID: (\d+)', line)
            if match:
                user_id_list.append(int(match.group(1)))
    return user_id_list


def remove_errors(file_path, errors_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists(errors_path):
        os.remove(errors_path)
