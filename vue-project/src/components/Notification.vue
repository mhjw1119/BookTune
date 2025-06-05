<template>
  <div class="notification-container">
    <transition-group name="notification">
      <div v-for="notification in notifications" 
           :key="notification.id" 
           class="notification"
           :class="notification.type">
        <div class="notification-content">
          <h4>{{ notification.title }}</h4>
          <p>{{ notification.message }}</p>
        </div>
        <button class="close-button" @click="removeNotification(notification.id)">×</button>
      </div>
    </transition-group>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { websocketService } from '../utils/websocket';

export default {
  name: 'Notification',
  setup() {
    const notifications = ref([]);
    let notificationId = 0;

    const addNotification = (data) => {
      const notification = {
        id: notificationId++,
        title: data.title || '새로운 음악',
        message: `음악 "${data.title}"이(가) ${data.status === 'completed' ? '생성되었습니다' : '생성 중입니다'}`,
        type: data.status === 'completed' ? 'success' : 'info'
      };
      
      notifications.value.push(notification);
    };

    const removeNotification = (id) => {
      notifications.value = notifications.value.filter(n => n.id !== id);
    };

    onMounted(() => {
      websocketService.addListener('song_notification', addNotification);
    });
    onUnmounted(() => {
      websocketService.removeListener('song_notification', addNotification);
    });

    return {
      notifications,
      removeNotification
    };
  }
};
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 1000;
}

.notification {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-width: 300px;
  margin-bottom: 10px;
  padding: 15px;
  border-radius: 8px;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.notification.success {
  border-left: 4px solid #4CAF50;
}

.notification.info {
  border-left: 4px solid #2196F3;
}

.notification-content {
  flex: 1;
}

.notification-content h4 {
  margin: 0 0 5px 0;
  font-size: 16px;
}

.notification-content p {
  margin: 0;
  font-size: 14px;
  color: #666;
}

.close-button {
  background: none;
  border: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  padding: 0 5px;
  transition: color 0.2s ease;
}

.close-button:hover {
  color: #666;
}

/* 트랜지션 효과 */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.notification-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style> 