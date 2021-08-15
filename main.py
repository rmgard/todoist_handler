import requests, uuid, json, datetime
from bs4 import BeautifulSoup
import todoist

econ_week_ed_url = 'https://www.economist.com/weeklyedition/archive'
econ_week_ed_page = requests.get(econ_week_ed_url)

soup = BeautifulSoup(econ_week_ed_page.content, 'html.parser')
results = soup.find(id='content')
# job_elems = results.find_all('div', class_='layout-edition-collection ds-layout-grid ds-layout-grid--edged')
ed_elems = results.find_all('div', class_='edition-teaser')
# ed_names = resultpython replace all values in a files.find_all('span', class_='edition-teaser__headline')
# ed_dates = results.find_all('time', class_='edition-teaser__subheadline')

for ed_elem in ed_elems:
    ed_name = ed_elem.find('span', class_='edition-teaser__headline')
    # ed_date = ed_elem.find('time', class_='edition-teaser__subheadline')
    # print(ed_name.text)
    # print(ed_date.text)

recent_ed = ed_elems[0].find('span', class_='edition-teaser__headline').text
edition_store_file = open('/home/ryan/Projects/todoist_handler/recent_ed.txt', 'r+')
recent_ed_data = edition_store_file.read()

if recent_ed != recent_ed_data:
    edition_store_file.truncate(0)
    edition_store_file.close()
    edition_store_file = open('/home/ryan/Projects/todoist_handler/recent_ed.txt', 'w')
    edition_store_file.write(recent_ed.strip())

else:
    print('getting out of here')
    exit()

edition_store_file.close()


# get all projects
api = todoist.TodoistAPI('81e0c2bbf867435192ee15ba0fd5a5e28e8b9265')
api.sync()
project_info = api.state['projects']
label_info = api.state['labels']
for label in label_info:
    print(f'{label["name"]} has id: {label["id"]}')
# print(api.state['projects'])

if datetime.datetime.today().weekday() == 3:
    due_string = 'next thur'
else:
    due_string = 'thur'

ed_structure = ['The World This Week',
                'Leaders',
                'Letters',
                'United States',
                'The Americas',
                'Asia',
                'China',
                'Middle East and Africa',
                'Europe',
                'Britain',
                'International',
                'Business',
                'Finance and Economics',
                'Science and Technology',
                'Books and Arts',
                'Graphic Detail',
                'Obituary']

# add tasks
r = requests.post(
    "https://api.todoist.com/rest/v1/tasks",
    data=json.dumps({'content': ed_elems[0].find('span', class_='edition-teaser__headline').text,
                     'project_id': 2198220182,
                     'label_ids': [2151126910, 2154459061],
                     'due_string': due_string}),
    headers={
        'Content-Type': 'application/json',
        'X-Request-Id': str(uuid.uuid4()),
        'Authorization': 'Bearer 81e0c2bbf867435192ee15ba0fd5a5e28e8b9265'
    }
).json()


for section in ed_structure:
    requests.post(
        "https://api.todoist.com/rest/v1/tasks",
        data=json.dumps({'content': section,
                         'project_id': 2198220182,
                         'parent_id': r['id'],
                         'label_ids': [2151126910]}),
        headers={
            'Content-Type': 'application/json',
            'X-Request-Id': str(uuid.uuid4()),
            'Authorization': 'Bearer 81e0c2bbf867435192ee15ba0fd5a5e28e8b9265'
        }
    ).json()
