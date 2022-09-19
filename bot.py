from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import time


api_id = 1
api_hash = '####'
phone = '#####'

all_participants = []
list_users = []

group_list = open('group_list.txt', 'r').read().split()   

client = TelegramClient('bot', api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Please Enter the verification code: '))
    

def check_repeat_user(all_users):
    users = []
    for user in all_users:
        if str(user.username) not in users:
            if user.username != None:
                users.append(str(user.username))
    return users

def write_users(all_users):
    users = check_repeat_user(all_users)

    with open('group_users.txt', '+w', encoding='utf-8') as outfile:
        for user in users:
            outfile.write('{0}\n'.format(user))

def join_groups(group_list):
    for group in group_list:
        try:
            client(JoinChannelRequest(group))
            print(group)
            time.sleep(10)
        except Exception as e:
            print(e)

def main():
    limit = 100
    offset = 0

    join_groups(group_list)

    for group in group_list:
        group = client.get_entity(group)
        while True:
            try:
                participants = client(GetParticipantsRequest(
                    group, ChannelParticipantsSearch(''), offset, limit,
                    hash=0
                ))
                if not participants.users:
                    break
                all_participants.extend(participants.users)
                offset += len(participants.users)
                print(offset)
            except Exception as e:
                print(e)
                break

    write_users(list(all_participants))


if __name__ == "__main__":
    main()