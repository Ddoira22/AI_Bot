from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

template = """
<!doctype html>
<html>
<head>
    <title>My Personal AI Bot</title>
</head>
<body>
    <h1>Talk to your AI Bot</h1>
    <form id="chat-form">
        <input type="text" id="user-input" placeholder="Say something..." required>
        <button type="submit">Send</button>
    </form>
    <div id="chat-log"></div>

    <script>
    const form = document.getElementById('chat-form');
    const chatLog = document.getElementById('chat-log');

    form.onsubmit = async (e) => {
        e.preventDefault();
        const input = document.getElementById('user-input');
        const userText = input.value.trim();
        if (!userText) return;
        input.value = '';
        chatLog.innerHTML += `<p><b>You:</b> ${userText}</p>`;

        try {
            const res = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: userText })
            });
            const data = await res.json();
            chatLog.innerHTML += `<p><b>Bot:</b> ${data.response}</p>`;
        } catch (error) {
            chatLog.innerHTML += `<p><b>Bot:</b> Error: ${error.message}</p>`;
        }
    };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(template)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'response': 'Invalid request'}), 400

    user_message = data['message']
    try:
        output = f"You said: {user_message}"
        return jsonify({'response': output})
    except Exception as e:
        return jsonify({'response': f"Error: {str(e)}"}), 500

# In restricted environments, skip server start to avoid SystemExit
if __name__ == '__main__':
    import os
    if os.environ.get("FLASK_RUN_FROM_CLI") != "true":
        print("Flask app is ready. Run with a proper server if needed.")
