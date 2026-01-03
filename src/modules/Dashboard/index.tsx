import { useState, useEffect } from 'react'

interface StatCard {
  id: string
  label: string
  value: string
  change: string
  changeType: 'positive' | 'negative'
  color: string
}

interface RecentActivity {
  id: string
  user: string
  action: string
  time: string
}

const Dashboard = () => {
  const [stats, setStats] = useState<StatCard[]>([])
  const [activities, setActivities] = useState<RecentActivity[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate data fetching
    const fetchData = async () => {
      await new Promise((resolve) => setTimeout(resolve, 500))

      setStats([
        {
          id: '1',
          label: 'Total Users',
          value: '12,847',
          change: '+12.5%',
          changeType: 'positive',
          color: '#3b82f6',
        },
        {
          id: '2',
          label: 'Active Sessions',
          value: '1,234',
          change: '+8.2%',
          changeType: 'positive',
          color: '#22c55e',
        },
        {
          id: '3',
          label: 'Revenue',
          value: '$48,290',
          change: '+23.1%',
          changeType: 'positive',
          color: '#f59e0b',
        },
        {
          id: '4',
          label: 'Bounce Rate',
          value: '32.4%',
          change: '-4.3%',
          changeType: 'negative',
          color: '#ef4444',
        },
      ])

      setActivities([
        { id: '1', user: 'John Doe', action: 'Created a new project', time: '2 minutes ago' },
        { id: '2', user: 'Jane Smith', action: 'Updated user settings', time: '15 minutes ago' },
        { id: '3', user: 'Mike Johnson', action: 'Uploaded new files', time: '1 hour ago' },
        { id: '4', user: 'Sarah Wilson', action: 'Completed onboarding', time: '2 hours ago' },
        { id: '5', user: 'Tom Brown', action: 'Generated report', time: '3 hours ago' },
      ])

      setLoading(false)
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div data-testid="dashboard-loading">
        <div className="page-header">
          <h1>Dashboard</h1>
          <p>Loading...</p>
        </div>
      </div>
    )
  }

  return (
    <div data-testid="dashboard">
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Welcome back! Here's an overview of your platform.</p>
      </div>

      <div className="stats-grid" data-testid="stats-grid">
        {stats.map((stat) => (
          <div key={stat.id} className="stat-card" data-testid={`stat-${stat.id}`}>
            <div
              className="stat-icon"
              style={{ backgroundColor: `${stat.color}20`, color: stat.color }}
            >
              📊
            </div>
            <div className="stat-value">{stat.value}</div>
            <div className="stat-label">{stat.label}</div>
            <div className={`stat-change ${stat.changeType}`}>
              {stat.change} from last month
            </div>
          </div>
        ))}
      </div>

      <div className="card" data-testid="activity-card">
        <div className="card-header">
          <h2 className="card-title">Recent Activity</h2>
          <button className="btn btn-secondary">View All</button>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>User</th>
              <th>Action</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {activities.map((activity) => (
              <tr key={activity.id} data-testid={`activity-${activity.id}`}>
                <td>{activity.user}</td>
                <td>{activity.action}</td>
                <td>{activity.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Dashboard
