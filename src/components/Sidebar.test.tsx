import { describe, it, expect } from 'vitest'
import { render, screen } from '../test/test-utils'
import Sidebar from './Sidebar'

describe('Sidebar', () => {
  it('renders the sidebar with header', () => {
    render(<Sidebar />)
    expect(screen.getByTestId('sidebar')).toBeInTheDocument()
    expect(screen.getByText('Module Dashboard')).toBeInTheDocument()
  })

  it('renders all navigation items', () => {
    render(<Sidebar />)
    expect(screen.getByTestId('nav-dashboard')).toBeInTheDocument()
    expect(screen.getByTestId('nav-user-management')).toBeInTheDocument()
    expect(screen.getByTestId('nav-analytics')).toBeInTheDocument()
    expect(screen.getByTestId('nav-settings')).toBeInTheDocument()
    expect(screen.getByTestId('nav-notifications')).toBeInTheDocument()
  })

  it('navigation links have correct paths', () => {
    render(<Sidebar />)
    expect(screen.getByTestId('nav-dashboard')).toHaveAttribute('href', '/')
    expect(screen.getByTestId('nav-user-management')).toHaveAttribute('href', '/users')
    expect(screen.getByTestId('nav-analytics')).toHaveAttribute('href', '/analytics')
    expect(screen.getByTestId('nav-settings')).toHaveAttribute('href', '/settings')
    expect(screen.getByTestId('nav-notifications')).toHaveAttribute('href', '/notifications')
  })
})
