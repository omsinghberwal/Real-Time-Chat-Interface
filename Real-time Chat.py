from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Store messages in a list (in-memory storage)
messages = []

# HTML template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Interface</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        #chat {
            border: 1px solid #ccc;
            height: 300px;
            overflow-y: scroll;
            padding: 10px;
            margin-bottom: 10px;
            background-color:rgba(255, 255, 255, 0.186);
        }
        .message {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
        }
        #message {
            width: 80%;
        }
        #body{
            background-color: rgb(39, 39, 39);
        }
        #send{
            background-color: rgba(255, 255, 255, 0.195);
            border-radius: 5px;
            border-style: initial;
            color: white;
        }
    </style>
</head>
<body id="body">
    <div id="chat"></div>
    <input type="text" id="message" placeholder="Type your message here...">
    <button id="send">Send</button>

    <script>
        $(document).ready(function() {
            $('#send').click(function() {
                var message = $('#message').val();
                $.post('/send', { message: message }, function(data) {
                    $('#chat').append('<div class="message"><span>' + data.message + '</span><button class="delete" data-id="' + data.id + '">Delete</button></div>');
                    $('#message').val(''); // Clear input
                });
            });

            // Fetch messages periodically
            setInterval(function() {
                $.get('/messages', function(data) {
                    $('#chat').empty(); // Clear chat
                    data.forEach(function(msg) {
                        $('#chat').append('<div class="message"><span>' + msg.text + '</span><button class="delete" data-id="' + msg.id + '">Delete</button></div>');
                    });
                });
            }, 1000); // Update every second

            // Delete message
            $(document).on('click', '.delete', function() {
                var messageId = $(this).data('id');
                $.ajax({
                    url: '/delete/' + messageId,
                    type: 'DELETE',
                    success: function(result) {
                        // Remove the message from the chat
                        $('[data-id="' + messageId + '"]').parent().remove();
                    }
                });
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send', methods=['POST'])
def send():
    message = request.form['message']
    message_id = len(messages)  # Simple ID based on the index
    messages.append({'id': message_id, 'text': message})  # Store the message with ID
    return jsonify({'status': 'success', 'message': message, 'id': message_id})

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/delete/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    global messages
    messages = [msg for msg in messages if msg['id'] != message_id]  # Remove the message by ID
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    # Run the app on all IP addresses of the machine
    app.run(debug=True, host='0.0.0.0', port=5003)