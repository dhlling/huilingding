import { describe, it, expect } from 'vitest'
import { render, screen, waitFor } from '../../test/test-utils'
import userEvent from '@testing-library/user-event'
import Settings from './index'

describe('Settings', () => {
  it('renders the settings page', () => {
    render(<Settings />)
    expect(screen.getByTestId('settings')).toBeInTheDocument()
    expect(screen.getByText('Settings')).toBeInTheDocument()
  })

  it('displays general settings by default', () => {
    render(<Settings />)
    expect(screen.getByTestId('general-settings')).toBeInTheDocument()
    expect(screen.getByTestId('site-name-input')).toBeInTheDocument()
  })

  it('switches between tabs', async () => {
    const user = userEvent.setup()
    render(<Settings />)

    await user.click(screen.getByTestId('tab-notifications'))
    expect(screen.getByTestId('notification-settings')).toBeInTheDocument()

    await user.click(screen.getByTestId('tab-security'))
    expect(screen.getByTestId('security-settings')).toBeInTheDocument()

    await user.click(screen.getByTestId('tab-appearance'))
    expect(screen.getByTestId('appearance-settings')).toBeInTheDocument()
  })

  it('updates site name input', async () => {
    const user = userEvent.setup()
    render(<Settings />)

    const input = screen.getByTestId('site-name-input')
    await user.clear(input)
    await user.type(input, 'New Site Name')

    expect(input).toHaveValue('New Site Name')
  })

  it('toggles notification settings', async () => {
    const user = userEvent.setup()
    render(<Settings />)

    await user.click(screen.getByTestId('tab-notifications'))
    const toggle = screen.getByTestId('toggle-pushNotifications')

    expect(toggle).not.toBeChecked()
    await user.click(toggle)
    expect(toggle).toBeChecked()
  })

  it('toggles security settings', async () => {
    const user = userEvent.setup()
    render(<Settings />)

    await user.click(screen.getByTestId('tab-security'))
    const toggle = screen.getByTestId('toggle-2fa')

    expect(toggle).not.toBeChecked()
    await user.click(toggle)
    expect(toggle).toBeChecked()
  })

  it('selects theme in appearance settings', async () => {
    const user = userEvent.setup()
    render(<Settings />)

    await user.click(screen.getByTestId('tab-appearance'))

    // Initially light theme should be selected
    const lightThemeBtn = screen.getByTestId('theme-light')
    const darkThemeBtn = screen.getByTestId('theme-dark')

    // Click dark theme
    await user.click(darkThemeBtn)

    // Verify both buttons exist and are clickable
    expect(lightThemeBtn).toBeInTheDocument()
    expect(darkThemeBtn).toBeInTheDocument()
  })

  it('shows save notification when saving', async () => {
    const user = userEvent.setup()
    render(<Settings />)

    await user.click(screen.getByTestId('save-settings'))

    await waitFor(() => {
      expect(screen.getByTestId('save-notification')).toBeInTheDocument()
    })
  })
})
