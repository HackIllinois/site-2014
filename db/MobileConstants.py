MAP = [{'building':'Siebel', 'floor':'Basement', 'room_number':'SC 0216', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'Basement', 'room_number':'SC 0224', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'Basement', 'room_number':'SC Basement', 'room_type':'hacker space' ,'room_name':'Basement Open Space', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1103', 'room_type':'sleep room' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1105', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1109', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1112', 'room_type':'game room' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1131', 'room_type':'game room' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1214', 'room_type':'sleep room' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1302', 'room_type':'Interactive Intelligence room' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1304', 'room_type':'Special sponsor room' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1404', 'room_type':'Kickoff and Tech Talks' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC Atrium', 'room_type':'sponsor tables and food serving' ,'room_name':'1st Floor Atrium', 'image_url':''},
       {'building':'Siebel', 'floor':'1', 'room_number':'SC 1312', 'room_type':'Mission Control Annex' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'2', 'room_number':'SC 2405', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'2', 'room_number':'SC 2235', 'room_type':'sponsor interview' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'2', 'room_number':'SC 2237', 'room_type':'sponsor interview' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'2', 'room_number':'SC 2nd Atrium', 'room_type':'sponsor tables' ,'room_name':'2nd floor Atrium', 'image_url':''},
       {'building':'Siebel', 'floor':'2', 'room_number':'SC 2102', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'2', 'room_number':'SC 2124', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'2', 'room_number':'SC 2407', 'room_type':'Mission Control' ,'room_name':'Mission Control', 'image_url':''},
       {'building':'Siebel', 'floor':'3', 'room_number':'SC 3401', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'3', 'room_number':'SC 3403', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'3', 'room_number':'SC 3405', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'3', 'room_number':'SC 3102', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'3', 'room_number':'SC 3124', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'4', 'room_number':'SC 4102', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'4', 'room_number':'SC 4124', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'4', 'room_number':'SC 4403', 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'4', 'room_number':'SC 4405', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'Siebel', 'floor':'4', 'room_number':'SC 4407', 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
       {'building':'DCL', 'floor':'1', 'room_number':'DC 1310', 'room_type':'tech talks' ,'room_name':'', 'image_url':''},
       {'building':'DCL', 'floor':'1', 'room_number':'DC 1320', 'room_type':'hacker space' ,'room_name':'', 'image_url':''},
       {'building':'DCL', 'floor':'2', 'room_number':'DC 2320', 'room_type':'hardware hacker space' ,'room_name':'', 'image_url':''},
       {'building':'DCL', 'floor':'2', 'room_number':'DC 2436', 'room_type':'hardware hacker space' ,'room_name':'', 'image_url':''}]

SUPPORT = {
    'General':['Events', 'Schedule', 'Rules', 'Comments or Suggestions'],
    'Requests':['Food & Drinks', 'Medical', 'Equipment', 'Other'],
    'Technical':['WIFI', 'Power', 'Locked Out', 'Other']
    }

SCHEDULE = {
    'Friday':[{
              'event_name':'First event',
              'description':'Lets kickoff hackillinois',
              'location':
              {'building':'Siebel', 'floor':'4', 'room_number':4407, 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
              'time':77782722,
              'icon_url':'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSNwVLUS8TsSni5_gXYPWDVBehYxMHnQj5RIWITO11uACXHhky5'
              },
              {
              'event_name':'First event',
              'description':'Lets kickoff hackillinois',
              'location':
              {'building':'Siebel', 'floor':'4', 'room_number':4407, 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
              'time':77782725,
              'icon_url':'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSNwVLUS8TsSni5_gXYPWDVBehYxMHnQj5RIWITO11uACXHhky5'
              },
              {
              'event_name':'First event',
              'description':'Lets kickoff hackillinois',
              'location':
              {'building':'Siebel', 'floor':'4', 'room_number':4407, 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
              'time':77782727,
              'icon_url':'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSNwVLUS8TsSni5_gXYPWDVBehYxMHnQj5RIWITO11uACXHhky5'
              }],
    'Saturday':[{
                'event_name':'First event',
                'description':'Lets kickoff hackillinois',
                'location':
                {'building':'Siebel', 'floor':'4', 'room_number':4407, 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
                'time':2342342,
                'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png'
                },
                {
                'event_name':'First event',
                'description':'Lets kickoff hackillinois',
                'location':
                {'building':'Siebel', 'floor':'4', 'room_number':4407, 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
                'time':241234134,
                'icon_url':'http://www.tarkettsportsindoor.com/sites/tarkett_indoor/assets/Resicore-PU-Midnight-Blue.png'
                }],
    'Sunday':[{
                'event_name':'First event',
                'description':'Lets kickoff hackillinois',
                'location':
                {'building':'Siebel', 'floor':'4', 'room_number':4407, 'room_type':'sponsor room' ,'room_name':'', 'image_url':''},
                'time':4532452435,
                'icon_url':'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcSNwVLUS8TsSni5_gXYPWDVBehYxMHnQj5RIWITO11uACXHhky5'		
                }]
          }

FAKE_MENTOR_DATA = [{'name':'Jacob Fuss',
            'email':'fuss1@illinois.edu', 
            'company':'Amazon', 
            'job_title':'SDE', 
            'skills':['ios', 'python', 'objective-c', 'html', 'css', 'java'], 
            'fb_url':'', 
            'status':'available', 
            'database_key':30000, 
            'time':0,
            'type':'mentor'}]