from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from threading import Thread
# Initialize Flask app and SocketIO
app_flask = Flask( name )
app_flask.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app_flask)
# Global variable to store messages
messages = []
# Define Kivy UI components
class PushNotificationApp(App):
def build(self):
self.layout = FloatLayout(size=(400, 300))
# Messages Label
self.messages_label = Label(text='Messages will appear here', font_size='20sp',

size_hint=(None, None),
1, 1))

1, 0, 1))

size=(300, 200), pos_hint={'center_x': 0.5, 'center_y': 0.7}, color=(0, 0,

self.layout.add_widget(self.messages_label)
# Notification Label
self.notification_label = Label(text='', font_size='16sp', size_hint=(None, None),
size=(300, 30), pos_hint={'center_x': 0.5, 'center_y': 0.1}, color=(0,

self.layout.add_widget(self.notification_label)
# Message Input
self.message_input = TextInput(hint_text='Enter message', font_size='16sp',

size_hint=(None, None),

size=(200, 30), pos_hint={'center_x': 0.5, 'center_y': 0.4})

self.layout.add_widget(self.message_input)

40),

# Send Button
send_button = Button(text='Send', font_size='16sp', size_hint=(None, None), size=(100,
pos_hint={'center_x': 0.5, 'center_y': 0.3}, background_color=(0, 1, 0, 1))

send_button.bind(on_press=self.send_message)
self.layout.add_widget(send_button)
return self.layout
def send_message(self, instance):
message = self.message_input.text
if message:
messages.append(message)
self.messages_label.text = '\n'.join(messages)
self.message_input.text = ''
# Emit the message to connected clients
socketio.emit('new_message', {'message': message}, namespace='/test')
# Update notification label
self.notification_label.text = 'Notification pushed successfully'
# Flask routes
@app_flask.route('/')
def index():
return render_template('index.html')
# WebSocket event handlers
@socketio.on('connect', namespace='/test')
def test_connect():
emit('welcome', {'data': 'Welcome!'})
if name == ' main ':
# Start Flask-SocketIO server in a separate thread
Thread(target=lambda:socketio.run(app_flask, host='0.0.0.0', port=5000)).start()
# Start the Kivy application
PushNotificationApp().run()
