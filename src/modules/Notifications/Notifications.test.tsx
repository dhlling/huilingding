import { describe, it, expect } from 'vitest'
import { render, screen } from '../../test/test-utils'
import userEvent from '@testing-library/user-event'
import Notifications from './index'

describe('Notifications', () => {
  it('renders the notifications page', () => {
    render(<Notifications />)
    expect(screen.getByTestId('notifications')).toBeInTheDocument()
    expect(screen.getByText('Notifications')).toBeInTheDocument()
  })

  it('displays notifications list', () => {
    render(<Notifications />)
    expect(screen.getByTestId('notifications-list')).toBeInTheDocument()
    expect(screen.getByTestId('notification-1')).toBeInTheDocument()
  })

  it('filters to show only unread notifications', async () => {
    const user = userEvent.setup()
    render(<Notifications />)

    await user.click(screen.getByTestId('filter-unread'))

    // Unread notifications should be visible
    expect(screen.getByTestId('notification-1')).toBeInTheDocument()
    expect(screen.getByTestId('notification-2')).toBeInTheDocument()

    // Read notifications should not be visible
    expect(screen.queryByTestId('notification-3')).not.toBeInTheDocument()
  })

  it('marks a notification as read', async () => {
    const user = userEvent.setup()
    render(<Notifications />)

    const markReadBtn = screen.getByTestId('mark-read-1')
    await user.click(markReadBtn)

    // The button should no longer exist for that notification
    expect(screen.queryByTestId('mark-read-1')).not.toBeInTheDocument()
  })

  it('deletes a notification', async () => {
    const user = userEvent.setup()
    render(<Notifications />)

    const deleteBtn = screen.getByTestId('delete-1')
    await user.click(deleteBtn)

    expect(screen.queryByTestId('notification-1')).not.toBeInTheDocument()
  })

  it('marks all notifications as read', async () => {
    const user = userEvent.setup()
    render(<Notifications />)

    await user.click(screen.getByTestId('mark-all-read'))

    // No more "mark as read" buttons should exist
    expect(screen.queryByTestId('mark-read-1')).not.toBeInTheDocument()
    expect(screen.queryByTestId('mark-read-2')).not.toBeInTheDocument()
  })

  it('clears all notifications', async () => {
    const user = userEvent.setup()
    render(<Notifications />)

    await user.click(screen.getByTestId('clear-all'))

    expect(screen.getByTestId('empty-state')).toBeInTheDocument()
    expect(screen.getByText("You're all caught up!")).toBeInTheDocument()
  })

  it('shows empty state for unread filter when no unread', async () => {
    const user = userEvent.setup()
    render(<Notifications />)

    // Mark all as read first
    await user.click(screen.getByTestId('mark-all-read'))

    // Filter to unread
    await user.click(screen.getByTestId('filter-unread'))

    expect(screen.getByTestId('empty-state')).toBeInTheDocument()
    expect(screen.getByText('No unread notifications')).toBeInTheDocument()
  })

  it('displays correct notification types', () => {
    render(<Notifications />)

    expect(screen.getByText('Payment Received')).toBeInTheDocument()
    expect(screen.getByText('Storage Almost Full')).toBeInTheDocument()
    expect(screen.getByText('Failed Login Attempt')).toBeInTheDocument()
  })
})
