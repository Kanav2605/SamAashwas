import urllib.request, json

req = urllib.request.urlopen('http://127.0.0.1:8000/api/v1/master-tickets')
tickets = json.loads(req.read().decode())
print(f'Fetched {len(tickets)} master tickets from local server.')

if tickets:
    t0 = tickets[0]
    t_id = t0['master_ticket_id']
    print(f'Testing live endorsement on ticket: {t_id}')
    post_data = json.dumps({'citizen_name': 'Live Test Citizen', 'citizen_phone': '9811099888'}).encode('utf-8')
    endorse_req = urllib.request.Request(
        f'http://127.0.0.1:8000/api/v1/master-tickets/{t_id}/endorse',
        data=post_data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    res = urllib.request.urlopen(endorse_req)
    print('Endorsement response:', res.read().decode())
