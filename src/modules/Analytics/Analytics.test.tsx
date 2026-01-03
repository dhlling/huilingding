import { describe, it, expect } from 'vitest'
import { render, screen } from '../../test/test-utils'
import userEvent from '@testing-library/user-event'
import Analytics from './index'

describe('Analytics', () => {
  it('renders the analytics page', () => {
    render(<Analytics />)
    expect(screen.getByTestId('analytics')).toBeInTheDocument()
    expect(screen.getByText('Analytics')).toBeInTheDocument()
  })

  it('displays metrics grid', () => {
    render(<Analytics />)
    expect(screen.getByTestId('metrics-grid')).toBeInTheDocument()
    expect(screen.getByText('Page Views')).toBeInTheDocument()
    expect(screen.getByText('Unique Visitors')).toBeInTheDocument()
  })

  it('displays traffic chart', () => {
    render(<Analytics />)
    expect(screen.getByTestId('traffic-chart')).toBeInTheDocument()
    expect(screen.getByText('Traffic Overview')).toBeInTheDocument()
  })

  it('displays traffic sources', () => {
    render(<Analytics />)
    expect(screen.getByTestId('sources-chart')).toBeInTheDocument()
    expect(screen.getByText('Traffic Sources')).toBeInTheDocument()
    expect(screen.getByTestId('source-0')).toBeInTheDocument()
  })

  it('displays top pages table', () => {
    render(<Analytics />)
    expect(screen.getByTestId('top-pages')).toBeInTheDocument()
    expect(screen.getByText('/home')).toBeInTheDocument()
  })

  it('changes time range on button click', async () => {
    const user = userEvent.setup()
    render(<Analytics />)

    const btn7d = screen.getByTestId('time-range-7d')
    await user.click(btn7d)

    expect(btn7d.classList.contains('btn-primary')).toBe(true)
  })

  it('displays correct metric values', () => {
    render(<Analytics />)
    expect(screen.getByText('284,582')).toBeInTheDocument()
    expect(screen.getByText('45,291')).toBeInTheDocument()
    expect(screen.getByText('4m 32s')).toBeInTheDocument()
    expect(screen.getByText('3.42%')).toBeInTheDocument()
  })
})
