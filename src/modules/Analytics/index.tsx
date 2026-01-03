import { useState } from 'react'

type TimeRange = '7d' | '30d' | '90d' | '1y'

interface MetricData {
  label: string
  value: string
  trend: 'up' | 'down' | 'neutral'
  percentage: string
}

interface ChartData {
  label: string
  value: number
  color: string
}

const Analytics = () => {
  const [timeRange, setTimeRange] = useState<TimeRange>('30d')

  const metrics: MetricData[] = [
    { label: 'Page Views', value: '284,582', trend: 'up', percentage: '+18.2%' },
    { label: 'Unique Visitors', value: '45,291', trend: 'up', percentage: '+12.5%' },
    { label: 'Avg. Session Duration', value: '4m 32s', trend: 'down', percentage: '-3.1%' },
    { label: 'Conversion Rate', value: '3.42%', trend: 'up', percentage: '+0.8%' },
  ]

  const trafficSources: ChartData[] = [
    { label: 'Organic Search', value: 45, color: '#3b82f6' },
    { label: 'Direct', value: 25, color: '#22c55e' },
    { label: 'Referral', value: 15, color: '#f59e0b' },
    { label: 'Social Media', value: 10, color: '#ef4444' },
    { label: 'Email', value: 5, color: '#8b5cf6' },
  ]

  const topPages = [
    { page: '/home', views: '45,892', avgTime: '2m 15s', bounceRate: '28%' },
    { page: '/products', views: '32,451', avgTime: '3m 45s', bounceRate: '35%' },
    { page: '/about', views: '18,294', avgTime: '1m 52s', bounceRate: '42%' },
    { page: '/contact', views: '12,847', avgTime: '1m 20s', bounceRate: '38%' },
    { page: '/blog', views: '9,283', avgTime: '4m 30s', bounceRate: '25%' },
  ]

  const getTrendIcon = (trend: 'up' | 'down' | 'neutral') => {
    switch (trend) {
      case 'up': return '↑'
      case 'down': return '↓'
      default: return '→'
    }
  }

  const getTrendColor = (trend: 'up' | 'down' | 'neutral') => {
    switch (trend) {
      case 'up': return 'var(--success-color)'
      case 'down': return 'var(--danger-color)'
      default: return 'var(--text-secondary)'
    }
  }

  return (
    <div data-testid="analytics">
      <div className="page-header">
        <h1>Analytics</h1>
        <p>Track your website performance and user behavior.</p>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {(['7d', '30d', '90d', '1y'] as TimeRange[]).map((range) => (
            <button
              key={range}
              className={`btn ${timeRange === range ? 'btn-primary' : 'btn-secondary'}`}
              onClick={() => setTimeRange(range)}
              data-testid={`time-range-${range}`}
            >
              {range === '7d' ? 'Last 7 Days' :
               range === '30d' ? 'Last 30 Days' :
               range === '90d' ? 'Last 90 Days' :
               'Last Year'}
            </button>
          ))}
        </div>
      </div>

      <div className="stats-grid" data-testid="metrics-grid">
        {metrics.map((metric, index) => (
          <div key={index} className="stat-card">
            <div className="stat-label">{metric.label}</div>
            <div className="stat-value">{metric.value}</div>
            <div
              className="stat-change"
              style={{ color: getTrendColor(metric.trend) }}
            >
              {getTrendIcon(metric.trend)} {metric.percentage}
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem', marginBottom: '1.5rem' }}>
        <div className="card" data-testid="traffic-chart">
          <div className="card-header">
            <h2 className="card-title">Traffic Overview</h2>
          </div>
          <div className="chart-container">
            <div style={{ textAlign: 'center' }}>
              <p>📈 Chart visualization would go here</p>
              <p style={{ fontSize: '0.85rem', marginTop: '0.5rem' }}>
                Showing data for {timeRange === '7d' ? 'last 7 days' :
                                  timeRange === '30d' ? 'last 30 days' :
                                  timeRange === '90d' ? 'last 90 days' :
                                  'last year'}
              </p>
            </div>
          </div>
        </div>

        <div className="card" data-testid="sources-chart">
          <div className="card-header">
            <h2 className="card-title">Traffic Sources</h2>
          </div>
          <div style={{ padding: '1rem' }}>
            {trafficSources.map((source, index) => (
              <div
                key={index}
                style={{ marginBottom: '1rem' }}
                data-testid={`source-${index}`}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                  <span>{source.label}</span>
                  <span style={{ fontWeight: '600' }}>{source.value}%</span>
                </div>
                <div
                  style={{
                    height: '8px',
                    backgroundColor: 'var(--border-color)',
                    borderRadius: '4px',
                    overflow: 'hidden',
                  }}
                >
                  <div
                    style={{
                      width: `${source.value}%`,
                      height: '100%',
                      backgroundColor: source.color,
                      borderRadius: '4px',
                      transition: 'width 0.3s ease',
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card" data-testid="top-pages">
        <div className="card-header">
          <h2 className="card-title">Top Pages</h2>
          <button className="btn btn-secondary">Export Report</button>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Page</th>
              <th>Views</th>
              <th>Avg. Time</th>
              <th>Bounce Rate</th>
            </tr>
          </thead>
          <tbody>
            {topPages.map((page, index) => (
              <tr key={index} data-testid={`page-row-${index}`}>
                <td><code>{page.page}</code></td>
                <td>{page.views}</td>
                <td>{page.avgTime}</td>
                <td>{page.bounceRate}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Analytics
