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
    Or you can just add your name behind when you start it:
    python3 dice_roller.py sn0w
    Or by pressing ctrl + c
    '''
    all_os_clear(platform.system())
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
    sim_login()

def sim_login():
    ''' This will show automatically when starting the script.
    Same as above except you can only comment out or delete it,
    '''
    user_name = ''
    err = 0
    while (len(user_name) < 1):
        if (err >= 3):
            print('Unable to set name, try again')
            exit()
        user_name = input('USER: ')
        err += 1
    print(f'Welcome, {user_name}\n')
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

def results_to_string(results, sides, amount, mod, comp):
    ''' Generates a string based on the roll.
    '''
    disc_results = []
    print(f'MOD:\t{mod}  |  COM:\t{comp}\nDIE:\t{sides}  |  ANT:\t{amount}\n\n')
    disc_results.append(str(f'\nMOD:\t{mod}  |  COM:\t{comp}\nDIE:\t{sides}  |  ANT:\t{amount}\n\n'))
    results = dice_roller(int(sides), int(amount), int(mod))
    results = list_shuffle(results)
    for result in results:
        if ((result - int(mod)) == 20 and int(sides) == 20):
            print(f'CRITICAL HIT!!! ({result}) ({mod})')
            disc_results.append(f'CRITICAL HIT!!! ({result}) ({mod})\n')
            continue
        elif ((result - int(mod)) == 1 and int(sides) == 20):
            print(f'CRITICAL FAIL!! ({result}) ({mod})')
            disc_results.append(f'CRITICAL FAIL!! ({result}) ({mod})\n')
            continue
        if (comp):
            if (result >= int(comp)):
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
    ''' Clears terminal dependent on the current OS
    '''
    if (OS == 'Windows'):
        os.system('cls')
    elif (OS == 'Linux' or OS == 'Darwin'):
        os.system('clear')

if __name__ == "__main__":
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
    try: 
        user_name = sys.argv[1]
    except:
        startup()
    while(True):
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
                if (not input_sides and not input_amount or input_amount == '0'):
                    print('ERR: You must add the dice and the amount')
                    print('EX: 20 1\n')
                    time.sleep(0.5)
                    all_os_clear(platform.system())
                    continue
            except:
                pass
            try:
                send_disc_msg(results_to_string(results, input_sides, input_amount, input_modifier, input_compare), user_name, webhook_id, webhook_token, bot_name)
                print('Sent to discord...')
            except:
                print('Unable to send to discord...')
            input('Press Enter to continue...')
            all_os_clear(platform.system())
