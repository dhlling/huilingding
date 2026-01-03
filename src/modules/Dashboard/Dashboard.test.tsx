import { describe, it, expect } from 'vitest'
import { render, screen, waitFor } from '../../test/test-utils'
import Dashboard from './index'

describe('Dashboard', () => {
  it('shows loading state initially', () => {
    render(<Dashboard />)
    expect(screen.getByTestId('dashboard-loading')).toBeInTheDocument()
  })

  it('renders dashboard after loading', async () => {
    render(<Dashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('dashboard')).toBeInTheDocument()
    }, { timeout: 1000 })
  })

  it('displays stats grid with all stat cards', async () => {
    render(<Dashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('stats-grid')).toBeInTheDocument()
    }, { timeout: 1000 })

    expect(screen.getByTestId('stat-1')).toBeInTheDocument()
    expect(screen.getByTestId('stat-2')).toBeInTheDocument()
    expect(screen.getByTestId('stat-3')).toBeInTheDocument()
    expect(screen.getByTestId('stat-4')).toBeInTheDocument()
  })

  it('displays activity card with recent activities', async () => {
    render(<Dashboard />)
    await waitFor(() => {
      expect(screen.getByTestId('activity-card')).toBeInTheDocument()
    }, { timeout: 1000 })

    expect(screen.getByText('Recent Activity')).toBeInTheDocument()
    expect(screen.getByTestId('activity-1')).toBeInTheDocument()
  })

  it('displays correct stat values', async () => {
    render(<Dashboard />)
    await waitFor(() => {
      expect(screen.getByText('12,847')).toBeInTheDocument()
      expect(screen.getByText('Total Users')).toBeInTheDocument()
    }, { timeout: 1000 })
  })
})
