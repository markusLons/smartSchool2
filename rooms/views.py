from django.shortcuts import render
import requests

# Create your views here.
ip = {
    205 : "192.168.0.155",
}
class rooms_controller:
    def __init__(self, room_id, room_name, room_ip):
        self.room_id = room_id
        self.room_name = room_name
        self.room_ip = room_ip

    def get_state(self):
        s = requests.get(f'http://{self.room_ip}/')
        # { 'temp' :22.00, 'led1': 'off','led2' :'off' }
        s = s.text
        temp = s.split('&&')[0]
        state1 = s.split('&&')[1]
        if state1 == 'on':
            state1 = 1
        else:
            state1 = 0

        state2 = s.split('&&')[2]
        if state2 == 'on':
            state2 = 1
        else:
            state2 = 0
        alarm = s.split('&&')[3].replace("\r\n", "")
        alarm = int(alarm)
        return {'temp': temp, 'door': state1, 'light': state2, 'alarm': alarm, 'room_number': self.room_id, 'room_name': self.room_name}

    def open_door(self):
        #/green/on
        s = requests.get(f'http://{self.room_ip}/green/on')
        print('open_door')
        return s.text

    def close_door(self):
        #/green/off
        s = requests.get(f'http://{self.room_ip}/green/off')
        print('close_door')
        return s.text

    def open_light(self):
        #/red/on
        s = requests.get(f'http://{self.room_ip}/red/on')
        print('open_light')
        return s.text

    def close_light(self):
        #/red/off
        s = requests.get(f'http://{self.room_ip}/red/off')
        print('close_light')
        return s.text



def room(request, room_id):
    room = rooms_controller(room_id, 'room_name', ip[room_id])
    if request.method == 'POST':
        if request.POST.get('light') != None:
            if request.POST.get('light') == 'Включить свет':
                room.open_light()
            else:
                room.close_light()
        if request.POST.get('door') != None:

            if request.POST.get('door') == 'Открыть дверь' :
                room.open_door()
            else:
                room.close_door()
    state = room.get_state()
    # отчистка запроса

    return render(request, 'rooms/room.html',  state)


def allRooms(request):

    return None