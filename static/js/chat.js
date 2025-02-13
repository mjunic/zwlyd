class AIChat {
    constructor(mountPoint, options = {}) {
        this.currentSessionId = null;
        this.serverUrl = options.serverUrl || 'http://localhost:8080';
        this.mountPoint = mountPoint;
        this.init();
    }

    init() {
        this.bindEvents();
    }

    bindEvents() {
        const input = this.mountPoint.querySelector('.ai-chat-input');
        const sendButton = this.mountPoint.querySelector('.ai-chat-send');
        const buttons = this.mountPoint.querySelectorAll('.ai-chat-button');

        sendButton.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        buttons.forEach(button => {
            button.addEventListener('click', () => {
                const questions = ["请为我推荐一些课程", "体育课选什么课既能锻炼自己又轻松",
                    "有什么课程限制专业或年级需要注意的吗", "高数老师会捞人的推荐", "形策老师推荐", "大英老师避雷"]
                input.value = questions[Math.floor(Math.random() * questions.length)];
                this.sendMessage();
            });
        });
    }

    async sendMessage() {
        const input = this.mountPoint.querySelector('.ai-chat-input');
        const userMessage = input.value.trim();

        if (!userMessage) return;

        this.appendMessage(userMessage, 'user');
        input.value = '';

        try {
            const response = await fetch(`${this.serverUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: userMessage,
                    session_id: this.currentSessionId
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.currentSessionId = data.session_id;
                this.appendMessage(data.response, 'ai');
            } else {
                this.appendMessage('错误: ' + data.error, 'error');
            }
        } catch (error) {
            this.appendMessage('发送消息时出错: ' + error.message, 'error');
        }
    }

    appendMessage(message, type) {
        const messagesContainer = this.mountPoint.querySelector('.ai-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-chat-message ${type}-message`;
        messageDiv.innerHTML = type === 'user' ? '你: ' + message : '选课小助手: ' + message;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}