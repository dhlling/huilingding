import { describe, it, expect } from 'vitest'
import { render, screen } from '../../test/test-utils'
import userEvent from '@testing-library/user-event'
import UserManagement from './index'

describe('UserManagement', () => {
  it('renders the user management page', () => {
    render(<UserManagement />)
    expect(screen.getByTestId('user-management')).toBeInTheDocument()
    expect(screen.getByText('User Management')).toBeInTheDocument()
  })

  it('displays users table', () => {
    render(<UserManagement />)
    expect(screen.getByTestId('users-table')).toBeInTheDocument()
    expect(screen.getByTestId('user-row-1')).toBeInTheDocument()
  })

  it('filters users by search term', async () => {
    const user = userEvent.setup()
    render(<UserManagement />)

    const searchInput = screen.getByTestId('search-input')
    await user.type(searchInput, 'John')

    expect(screen.getByTestId('user-row-1')).toBeInTheDocument()
    expect(screen.queryByTestId('user-row-2')).not.toBeInTheDocument()
  })

  it('filters users by role', async () => {
    const user = userEvent.setup()
    render(<UserManagement />)

    const roleFilter = screen.getByTestId('role-filter')
    await user.selectOptions(roleFilter, 'admin')

    expect(screen.getByTestId('user-row-1')).toBeInTheDocument()
    expect(screen.queryByTestId('user-row-2')).not.toBeInTheDocument()
  })

  it('opens add user modal', async () => {
    const user = userEvent.setup()
    render(<UserManagement />)

    const addButton = screen.getByTestId('add-user-btn')
    await user.click(addButton)

    expect(screen.getByTestId('add-user-modal')).toBeInTheDocument()
    expect(screen.getByText('Add New User')).toBeInTheDocument()
  })

  it('adds a new user', async () => {
    const user = userEvent.setup()
    render(<UserManagement />)

    await user.click(screen.getByTestId('add-user-btn'))
    await user.type(screen.getByTestId('new-user-name'), 'New User')
    await user.type(screen.getByTestId('new-user-email'), 'new@example.com')
    await user.click(screen.getByTestId('confirm-add-user'))

    expect(screen.getByText('New User')).toBeInTheDocument()
    expect(screen.getByText('new@example.com')).toBeInTheDocument()
  })

  it('deletes a user', async () => {
    const user = userEvent.setup()
    render(<UserManagement />)

    const deleteButton = screen.getByTestId('delete-user-1')
    await user.click(deleteButton)

    expect(screen.queryByTestId('user-row-1')).not.toBeInTheDocument()
  })

  it('toggles user status', async () => {
    const user = userEvent.setup()
    render(<UserManagement />)

    const toggleButton = screen.getByTestId('toggle-status-1')
    expect(toggleButton).toHaveTextContent('Deactivate')

    await user.click(toggleButton)
    expect(toggleButton).toHaveTextContent('Activate')
  })
})
