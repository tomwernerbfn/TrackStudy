import datetime

def save():
    n = ''
    t = ''
    d = ''
    no = ''
    time = datetime.datetime.now()
    
    while True:
        print('save study'.upper())
        print(f'1. Name: {n}')
        print(f'2. Topic: {t}')
        print(f'3. Duration: {d}')
        print(f'4. Notes: {no}')
        print('5. Cancel')
        
        if n != '' and t != '' and d != '' and no != '':
            with open('logs.txt', 'a') as f:
                f.write(f'{time} {n} {t} {d} {no}\n')
                print('New study successfully saved for today!')
                menu()
                break
        else:
            try:
                all_points = float(input('Please fill out all points: '))
            except Exception:
                print('Something went wrong! Please try again.')
                continue
            else:
                if all_points == 1:
                    n = input("Please enter a name (space = '-'): ")
                    continue
                elif all_points == 2:
                    t = input("Please enter a topic of the study (space = '-'): ")
                    continue
                elif all_points == 3:
                    try:
                        duration = float(input('Please enter the time how long you studied for: '))
                    except Exception:
                        print('Please enter a number in minutes!')
                        continue
                    else:
                        d = str(duration)
                        continue
                elif all_points == 4:
                    try:
                        no = input()
                    except Exception:
                        print('Please enter notes!')
                        continue
                    else:
                        continue
                elif all_points == 5:
                    print('Canceled new study.')
                    menu()
                    break
                else:
                    print("Your input wasn't an option to choose from!")
                    continue

def delete_line(a): #REMEMBER: There are no specific line deletion syntaxes!
    with open('logs.txt', 'r') as file:
        lines = file.readlines()
    
    filtered_lines = [line for line in lines if a not in line]
    
    with open('logs.txt', 'w') as file:
        file.writelines(filtered_lines)

def loadDelete():
    while True:
        print('load / delete studies'.upper())
        print('1. Load study')
        print('2. Delete study')
        print('3. Load all')
        print('4. Cancel')

        with open('logs.txt', 'r+') as rf:
            try:
                config = int(input('Please choose an option: '))
            except Exception:
                print('Something went wrong! Please try again.')
                continue
            else:
                if config == 1:
                    date = input('Choose the date of the study (yyyy-mm-dd): ')
                    for line in rf:
                        if date in line:
                            print(line)
                            continue
                    try:
                        if date not in line:
                            print("Couldn't find the study! Please try again.")
                            continue
                    except Exception:
                        print("Couldn't find the study! Please try again.")
                        continue    
                elif config == 2:
                    date = input('Choose the date of the study (yyyy-mm-dd): ')
                    for line in rf:
                        if date in line:
                            print(line)
                            try:
                                delete = input('Are you sure to delete this study? (y/n) ')
                            except Exception:
                                print('Something went wrong! Please try again.')
                                continue
                            else:
                                if delete == 'y':
                                    delete_line(line)
                                    print('Study succesfully deleted.')
                                    menu()
                                    break
                                elif delete == 'n':
                                    print('Canceled deletion.')
                                    menu()
                                    break
                                else:
                                    print("Please enter 'y' for 'yes' or 'n' for 'no'.")
                                    continue
                        else:
                            print("Couldn't find the study! Please try again.")
                            continue
                elif config == 3:
                    for lines in rf:
                        print(lines)
                    menu()
                    break
                elif config == 4:
                    print('Canceled configuration.')
                    menu()
                    break
                else:
                    print("Your input wasn't an option to choose from!")
                    continue

def progression():
    hour = 0
    streak = 0
    check = datetime.date.today()

    with open('logs.txt', 'r') as r:
        lines = r.readlines()
        parts = [line.split() for line in lines if line.strip()]
        dates = {datetime.date.fromisoformat(line[0]): line for line in parts}

        total_mins = sum(float(line[4]) for line in parts)
        hour = round(total_mins / 60, 2)

        while check in dates:
            streak += 1
            check -= datetime.timedelta(days=1)

    # Load today's goal from config.txt
    goal = 'None'
    try:
        with open('config.txt', 'r') as o:
            config_lines = o.readlines()
            for line in config_lines:
                parts = line.split()
                if parts and datetime.date.fromisoformat(parts[0]) == check:
                    goal = parts[1]
                    break
    except FileNotFoundError:
        pass

    while True:
        print('progression'.upper())
        print(f'Total hours studied: {hour}')
        print(f'Current streak: {streak}')
        print(f"Today's study goal: {goal} mins")
        print('1. Set a new goal')
        print('2. Go back')

        try:
            choice = int(input('Choose an option: '))
        except Exception:
            print('Please enter a number!')
            continue

        if choice == 1:
            try:
                gl = float(input('Choose a study goal for today: '))
            except Exception:
                print('Please enter a number in minutes!')
                continue
            else:
                if goal == gl:
                    print('Your input is already the goal for today!')
                    continue
                
                overwrite = input('Overwrite old goal? (y/n) ')
                if overwrite == 'y':
                    try:
                        with open('config.txt', 'r') as o:
                            config_lines = o.readlines()
                        filtered = [l for l in config_lines if str(check) not in l]
                    except FileNotFoundError:
                        filtered = []

                    with open('config.txt', 'w') as o:
                        o.writelines(filtered)
                        o.write(f'{check} {gl}\n')

                    goal = gl
                    print('New goal set!')
                elif overwrite == 'n':
                    print('Overwrite successfully canceled.')
                    menu()
                    break
                else:
                    print("Your input wasn't an option to choose from!")
                    continue

        elif choice == 2:
            menu()
            break
        else:
            print("Your input wasn't an option to choose from!")

def menu():
    with open('logs.txt', 'r') as r:
        lines = r.readlines()
        parts = [line.split() for line in lines if line.strip()]
        dates = {datetime.date.fromisoformat(line[0]): line for line in parts}
        today = datetime.date.today()
        if today in dates:
            x = parts[0][2]
        else:
            x = 'There are no studies from today!'

    while True:
        print('Welcome to TrackStudy!')
        print(f"Today's studies: {x}")
        print('1. Save Study')
        print('2. Load/Delete Study')
        print('3. Progression')
        print('4. Exit')

        try:
            opt = int(input('Choose an option: '))
        except Exception:
            print('Something went wrong! Please try again.')
            continue
        else:
            if opt == 1:
                save()
                break
            elif opt == 2:
                loadDelete()
                break
            elif opt == 3:
                progression()
                break
            elif opt == 4:
                exit = input('Are you sure? (y/n) ')

                if exit == 'y':
                    print('See you soon!')
                    break
                elif exit == 'n':
                    continue
                else:
                    print("Please enter 'y' for 'yes' or 'n' for 'no'.")
            else:
                print("Your input wasn't an option to choose from!")

menu()
