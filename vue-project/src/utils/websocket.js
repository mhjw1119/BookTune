class WebSocketService {
    constructor() {
        this.socket = null;
        this.listeners = new Map();
    }

    connect() {
        // Django 서버의 WebSocket URL
        const wsUrl = 'ws://localhost:8000/ws/songs/';
        
        this.socket = new WebSocket(wsUrl);

        this.socket.onopen = () => {
            console.log('WebSocket 연결이 성공적으로 설정되었습니다.');
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'song_notification') {
                this.notifyListeners('song_notification', data.message);
            }
        };

        this.socket.onclose = () => {
            console.log('WebSocket 연결이 종료되었습니다.');
            // 연결이 끊어지면 5초 후 재연결 시도
            setTimeout(() => this.connect(), 5000);
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket 에러:', error);
        };
    }

    addListener(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, new Set());
        }
        if (![...this.listeners.get(event)].includes(callback)) {
            this.listeners.get(event).add(callback);
        }
    }

    removeListener(event, callback) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).delete(callback);
        }
    }

    notifyListeners(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => callback(data));
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

export const websocketService = new WebSocketService(); 