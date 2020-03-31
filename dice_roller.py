from discord import Embed, Webhook, RequestsWebhookAdapter
import requests
import platform
import random
import time
import sys
import os


def startup():
    ''' This function is just for fun, to remove the startup screen
    simply comment it out in __main__ or delete the entire thing.
    Or you can just add something behind when you start it:
    python3 dice_roller.py 1
    Or by pressing ctrl + c
    '''
    title = '\n' + \
            '____ ____ _    _    ____ ____ \n' + \
            '|__/ |  | |    |    |___ |__/ \n' + \
            '|  \ |__| |___ |___ |___ |  \ \n\n' + \
            '-' * 29 + '\n'
    try:
        for char in title:
            print(char, end = '', flush = True)
            time.sleep(.1)
    except KeyboardInterrupt:
        all_os_clear(platform.system())
        print(title)
        time.sleep(.1)

def sim_login(user_name):
    ''' This will show automatically when starting the script.
    Same as above except you can only comment out or delete it,
    '''
    err = 0
    while (len(user_name) < 1):
        if (err >= 3):
            print('Unable to set name, try again')
            exit()
        user_name = input('USER: ')
        err += 1
    print(f'Welcome, {user_name}')
    time.sleep(0.2)
    return user_name

def dice_roller(dice = 0, amount = 0, modifier = 0):
    ''' Generates a random seed based on ((time + time) / 10) % (time * 2)
    thus assuring more randomness, which is completely useless in this case but fun.
    It will then select a number in the range between 1 and the sides of the die.
    '''
    dice_results = []
    seed = 0
    t_r = 0
    random.seed(((time.time() + time.time()) / 10) % (time.time() * 2))
    for i in range(amount):
        t_r = random.randrange(1, (dice + 1))
        dice_results.append((t_r + modifier))
    return dice_results

def list_shuffle(_list):
    ''' Just for futher randomness, the list with roll results will be
    randomly shuffled in a range between 1 to 5-1000.
    - Uncomment c and print for feedback on how many times it was
    shuffled.
    '''
    #c = 0
    for i in range(1, (random.randrange(5, 1000))):
        #c += 1
        random.shuffle(_list)
    #print(f'Shuffled {c} times!')
    return _list

def results_to_string(results):
    ''' Generates a string based on the roll
    '''
    disc_results = []
    print(f'MOD:\t{input_modifier}  |  COM:\t{input_compare}\nDIE:\t{input_sides}  |  ANT:\t{input_amount}\n\n')
    disc_results.append(str(f'\nMOD:\t{input_modifier}  |  COM:\t{input_compare}\nDIE:\t{input_sides}  |  ANT:\t{input_amount}\n\n'))
    results = dice_roller(int(input_sides), int(input_amount), int(input_modifier))
    results = list_shuffle(results)
    for result in results:
        if ((result - int(input_modifier)) == 20 and int(input_sides) == 20):
            print(f'CRITICAL HIT!!! ({result}) ({input_modifier})')
            disc_results.append(f'CRITICAL HIT!!! ({result}) ({input_modifier})\n')
            continue
        elif ((result - int(input_modifier)) == 1 and int(input_sides) == 20):
            print(f'CRITICAL FAIL!! ({result}) ({input_modifier})')
            disc_results.append(f'CRITICAL FAIL!! ({result}) ({input_modifier})\n')
            continue
        if (input_compare):
            if (result >= int(input_compare)):
                print(f'HIT! ({result})')
                disc_results.append(f'HIT! ({result})\n')
            else:
                print(f'MISS! ({result})')
                disc_results.append(f'MISS! ({result})\n')
        else:
            print(f'You rolled a {result}!')
            disc_results.append(f'You rolled a {result}!\n')
    return disc_results

def send_disc_msg(text, name, ID, token, bot_name):
    ''' Sends a message to a discord chat so that everyone
    can see the roll.
    '''
    phrases = ['Sick plastic toss my dude', 'TUBULAR', 'Radical roll!!!', 'Just stop...']
    # To add a phrase, simply add it to the list above. To add a colour add it to the list below.
    # To remove either simply remove them from the list.
    colours = [0xffffff, 0x000000, 0x009c29, 0xff00ea, 0xff0000, 0xfff200]
    text = ''.join(text)
    embed = Embed(title=f"{name}'s roll", color = (random.choice(colours)))
    embed.add_field(name = (random.choice(phrases)), value = text, inline = True)
    webhook = Webhook.partial(ID, token, adapter = RequestsWebhookAdapter())
    webhook.send(username = bot_name, embed = embed)

def all_os_clear(OS):
    if (OS == 'Windows'):
        os.system('cls')
    elif (OS == 'Linux' or OS == 'Darwin'):
        os.system('clear')

if __name__ == "__main__":
    try: 
        sys.argv[1]
    except:
        startup()
    webhook_id = 0 # Switch with discord webhook id
    webhook_token = '' # Switch with discord webhook token
    bot_name = 'Roller-Bot'
    user_input = ''
    user_name = ''
    input_sides = 0
    input_amount = 0
    input_modifier = 0
    input_compare = 0
    results = []
    while(True):
        if (user_name == ''):
            user_name = sim_login(user_name)
        print(f'---------- {bot_name} - {user_name} ----------\n' + \
            '\tUsage: diceType howMany [optional] modifier compareTo\n' + \
            '\tExample: 20 1\n' + \
            '\t         10 5 2 16\n' + \
            'Die: 4, 6, 8, 10, 12, 20\n' + \
            'q - quit\n')
        user_input = input(' > ')
        if ('q' in user_input.lower() or 'quit' in user_input.lower()):
            break
        else:
            t_inp = user_input.split(' ')
            t_inp = list(filter(None, t_inp))
            try:
                if (len(t_inp) == 4):
                    input_sides, input_amount, input_modifier, input_compare = t_inp
                elif (len(t_inp) == 3):
                    input_sides, input_amount, input_modifier = t_inp
                elif (len(t_inp) == 2):
                    input_sides, input_amount, = t_inp
            except:
                pass
            try:
                send_disc_msg(results_to_string(results), user_name, webhook_id, webhook_token, bot_name)
                print('Sent to discord...')
            except:
                print('Unable to send to discord...')
            input('Press Enter to continue...')
            all_os_clear(platform.system())
