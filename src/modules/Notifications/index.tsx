import { useState } from 'react'

interface Notification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  time: string
  read: boolean
}

const initialNotifications: Notification[] = [
  {
    id: '1',
    type: 'success',
    title: 'Payment Received',
    message: 'You received a payment of $150 from John Doe.',
    time: '2 minutes ago',
    read: false,
  },
  {
    id: '2',
    type: 'info',
    title: 'New User Registered',
    message: 'A new user has registered on the platform.',
    time: '15 minutes ago',
    read: false,
  },
  {
    id: '3',
    type: 'warning',
    title: 'Storage Almost Full',
    message: 'Your storage is 90% full. Consider upgrading your plan.',
    time: '1 hour ago',
    read: true,
  },
  {
    id: '4',
    type: 'error',
    title: 'Failed Login Attempt',
    message: 'There was a failed login attempt from an unknown device.',
    time: '2 hours ago',
    read: true,
  },
  {
    id: '5',
    type: 'info',
    title: 'System Update Available',
    message: 'A new system update is available. Please update to the latest version.',
    time: '3 hours ago',
    read: true,
  },
  {
    id: '6',
    type: 'success',
    title: 'Report Generated',
    message: 'Your monthly analytics report has been generated successfully.',
    time: '5 hours ago',
    read: true,
  },
]

const Notifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>(initialNotifications)
  const [filter, setFilter] = useState<'all' | 'unread'>('all')

  const filteredNotifications = filter === 'unread'
    ? notifications.filter((n) => !n.read)
    : notifications

  const unreadCount = notifications.filter((n) => !n.read).length

  const markAsRead = (id: string) => {
    setNotifications(notifications.map((n) =>
      n.id === id ? { ...n, read: true } : n
    ))
  }

  const markAllAsRead = () => {
    setNotifications(notifications.map((n) => ({ ...n, read: true })))
  }

  const deleteNotification = (id: string) => {
    setNotifications(notifications.filter((n) => n.id !== id))
  }

  const clearAll = () => {
    setNotifications([])
  }

  const getTypeIcon = (type: Notification['type']) => {
    switch (type) {
      case 'success': return '✓'
      case 'warning': return '⚠'
      case 'error': return '✕'
      default: return 'ℹ'
    }
  }

  const getTypeColor = (type: Notification['type']) => {
    switch (type) {
      case 'success': return '#22c55e'
      case 'warning': return '#f59e0b'
      case 'error': return '#ef4444'
      default: return '#3b82f6'
    }
  }

  return (
    <div data-testid="notifications">
      <div className="page-header">
        <h1>Notifications</h1>
        <p>Stay updated with the latest alerts and messages.</p>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              className={`btn ${filter === 'all' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setFilter('all')}
              data-testid="filter-all"
            >
              All ({notifications.length})
            </button>
            <button
              className={`btn ${filter === 'unread' ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setFilter('unread')}
              data-testid="filter-unread"
            >
              Unread ({unreadCount})
            </button>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              className="btn btn-secondary"
              onClick={markAllAsRead}
              disabled={unreadCount === 0}
              data-testid="mark-all-read"
            >
              Mark All as Read
            </button>
            <button
              className="btn btn-danger"
              onClick={clearAll}
              disabled={notifications.length === 0}
              data-testid="clear-all"
            >
              Clear All
            </button>
          </div>
        </div>
      </div>

      <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
        {filteredNotifications.length === 0 ? (
          <div
            style={{
              padding: '4rem 2rem',
              textAlign: 'center',
              color: 'var(--text-secondary)',
            }}
            data-testid="empty-state"
          >
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔔</div>
            <h3 style={{ marginBottom: '0.5rem', color: 'var(--text-primary)' }}>
              {filter === 'unread' ? 'No unread notifications' : 'No notifications'}
            </h3>
            <p>You're all caught up!</p>
          </div>
        ) : (
          <div data-testid="notifications-list">
            {filteredNotifications.map((notification) => (
              <div
                key={notification.id}
                className={`notification-item ${!notification.read ? 'unread' : ''}`}
                data-testid={`notification-${notification.id}`}
              >
                <div
                  className="notification-icon"
                  style={{
                    backgroundColor: `${getTypeColor(notification.type)}20`,
                    color: getTypeColor(notification.type),
                  }}
                >
                  {getTypeIcon(notification.type)}
                </div>
                <div className="notification-content">
                  <div className="notification-title">{notification.title}</div>
                  <div className="notification-message">{notification.message}</div>
                  <div className="notification-time">{notification.time}</div>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                  {!notification.read && (
                    <button
                      className="btn btn-secondary"
                      onClick={() => markAsRead(notification.id)}
                      data-testid={`mark-read-${notification.id}`}
                      style={{ padding: '0.5rem 0.75rem', fontSize: '0.8rem' }}
                    >
                      Mark as Read
                    </button>
                  )}
                  <button
                    className="btn btn-danger"
                    onClick={() => deleteNotification(notification.id)}
                    data-testid={`delete-${notification.id}`}
                    style={{ padding: '0.5rem 0.75rem', fontSize: '0.8rem' }}
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Notifications
