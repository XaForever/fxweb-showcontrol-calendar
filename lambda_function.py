
from datetime import datetime, timezone, timedelta
from ics import Calendar, Event, Todo
import requests
import csv
from zoneinfo import ZoneInfo
# Set timezone
tz = ZoneInfo("Europe/Paris")

# Define paid days
jours_payes = [
    '2024-12-27',
    '2025-01-29',
    '2025-02-26',
    '2025-03-27',
    '2025-04-28',
    '2025-05-27',
    '2025-06-26',
    '2025-07-29',
    '2025-08-27',
    '2025-09-26',
    '2025-10-29',
    '2025-11-26',
    '2025-12-29'
]

# Define allowed team members
allow_team = {
    '80206109': True,  # Moi
    '1598587': True,   # Matthew
    '81581201': True,  # Louis
    '80207769': True,  # Frank
    '1687718': True,   # Maxime
    '80210450': True,  # Julien
}

def read_planning_csv(filename):
    planning_data = []

    file = requests.get(filename)
    content = file.content.decode('utf-8')
    file.content.decode('utf-8')
    reader = csv.reader(content.splitlines(), delimiter=';')
    for row in reader:
        planning_data.append({
            'Nom': row[0],
            'ID': row[1],
            'Heure': row[2],
            'Jour': row[4:39]  # Days data from column 4 to 38
        })
    
    return planning_data

def create_calendar_for_user(user_id):
    if not user_id:
        return "Utilisateur introuvable"

    if user_id not in allow_team:
        return "Vous n'avez pas autorisé l'accès à votre planning"

    # Create calendar
    cal = Calendar()
    
    # Read planning data
    planning_data = read_planning_csv("https://d2z5bvell1kckp.cloudfront.net/showcontrol/calendar/Planning%20WEB.csv")
    
    # Find user in planning
    user_data = None
    for entry in planning_data:
        if entry['ID'] == user_id:
            user_data = entry
            break
            
    if not user_data:
        return "Utilisateur introuvable"

    # Process each day
    # print(planning_data)
    # start_date = datetime(tz).replace(hour=0, minute=0, second=0, microsecond=0)  # You'll need to implement proper date parsing here
    start_date = datetime.strptime(planning_data[2]['Jour'][0], "%d/%m/%y").replace(tzinfo=tz)
    
    for day_index, day_data in enumerate(user_data['Jour']):
        # print(day_index, day_data)
        if ('CNT1 ' in day_data) or ('CNT2 ' in day_data) or ('CNT 3' in day_data):
            hour = (day_data.replace('CNT1 ', '').replace('CNT2 ', '').replace('CNT 3', ''))

            event = Event()
            event.name = f"PCCR"
            event.begin = start_date + timedelta(days=day_index, hours=(float(hour)))
            event.duration = timedelta(hours=9)
            event.location = "Disneyland Paris, 77700 Chessy, France"
            event.geo=(48.875386739331624, 2.7761106631453574)
            cal.events.add(event)

        if ('PEC1 ' in day_data) or ('PEC2 ' in day_data) or ('PEC3 ' in day_data):
            hour = (day_data.replace('PEC1 ', '').replace('PEC2 ', '').replace('PEC3 ', ''))

            event = Event()
            event.name = f"PECS"
            event.begin = start_date + timedelta(days=day_index, hours=(float(hour)))
            event.duration = timedelta(hours=9)
            event.location = "Walt Disney Studio, 77700 Chessy, France"
            event.geo=(48.86742258851088, 2.779463622350518)
            cal.events.add(event)

        if ('BUR ' in day_data):
            hour = (day_data.replace('BUR ', ''))

            event = Event()
            event.name = f"Bureau"
            event.begin = start_date + timedelta(days=day_index, hours=(float(hour)))
            event.duration = timedelta(hours=9)
            event.location = "Disneyland Paris, 77700 Chessy, France"
            event.geo=(48.864586770409865, 2.779463622350518)
            cal.events.add(event)

        if ('REP ' in day_data):
            hour = (day_data.replace('BUR ', ''))
            event = Event()
            event.name = f"Répétition"
            event.begin = start_date + timedelta(days=day_index, hours=(float(hour)))
            event.duration = timedelta(hours=9)
            event.location = "Disneyland Paris, 77700 Chessy, France"
            event.geo=(48.875386739331624, 2.7761106631453574)
            cal.events.add(event)

        if ('PROG ' in day_data):
            hour = (day_data.replace('PROG ', ''))
            event = Event()
            event.name = f"Programmation"
            event.begin = start_date + timedelta(days=day_index, hours=(float(hour)))
            event.duration = timedelta(hours=9)
            event.location = "Disneyland Paris, 77700 Chessy, France"
            event.geo=(48.875386739331624, 2.7761106631453574)
            cal.events.add(event)

        if ('DEV ' in day_data):
            hour = (day_data.replace('DEV ', ''))
            event = Event()
            event.name = f"Développement"
            event.begin = start_date + timedelta(days=day_index, hours=(float(hour)))
            event.duration = timedelta(hours=9)
            event.location = "Disneyland Paris, 77700 Chessy, France"
            event.geo=(48.875386739331624, 2.7761106631453574)
            cal.events.add(event)
        
        if ('EVE ' in day_data):
            hour = (day_data.replace('EVE ', ''))
            event = Event()
            event.name = f"Evénement"
            event.begin = start_date + timedelta(days=day_index, hours=(float(hour)))
            event.duration = timedelta(hours=9)
            event.location = "Disneyland Paris, 77700 Chessy, France"
            event.geo=(48.875386739331624, 2.7761106631453574)
            cal.events.add(event)

    # Add paid days events
    for paie in jours_payes:
        paie_date = datetime.strptime(paie, '%Y-%m-%d').replace(tzinfo=tz)
        if paie_date > datetime.now(tz):
            event = Event()
            event.name = "Disney Flouzzz Day"
            event.description = "Par ici la monnaie !"
            event.begin = paie_date
            event.duration = timedelta(days=1)
            cal.events.add(event)

    # todo = Todo()
    # todo.name = "Tâche 1"
    # todo.begin = datetime.now(tz)
    # todo.duration = timedelta(hours=1)
    # # todo.description('Tâche 1 à faire')
    # cal.todos.add(todo)

    return str(cal)



def lambda_handler(event, context):
    id = event['queryStringParameters']['id'] 

    if (id == None):
        return {
            'statusCode': 400,
            'body': "Missing ID"
        }
    
    calendar_data = create_calendar_for_user(id)

    return {
        'statusCode': 200,
        'body': calendar_data
    }