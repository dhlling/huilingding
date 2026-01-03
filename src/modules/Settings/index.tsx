import { useState } from 'react'

interface SettingsState {
  general: {
    siteName: string
    siteUrl: string
    timezone: string
    language: string
  }
  notifications: {
    emailNotifications: boolean
    pushNotifications: boolean
    weeklyDigest: boolean
    marketingEmails: boolean
  }
  security: {
    twoFactorAuth: boolean
    sessionTimeout: string
    ipWhitelist: boolean
  }
  appearance: {
    theme: 'light' | 'dark' | 'system'
    compactMode: boolean
    showAvatars: boolean
  }
}

const Settings = () => {
  const [settings, setSettings] = useState<SettingsState>({
    general: {
      siteName: 'Module Dashboard',
      siteUrl: 'https://example.com',
      timezone: 'UTC',
      language: 'en',
    },
    notifications: {
      emailNotifications: true,
      pushNotifications: false,
      weeklyDigest: true,
      marketingEmails: false,
    },
    security: {
      twoFactorAuth: false,
      sessionTimeout: '30',
      ipWhitelist: false,
    },
    appearance: {
      theme: 'light',
      compactMode: false,
      showAvatars: true,
    },
  })

  const [activeTab, setActiveTab] = useState<'general' | 'notifications' | 'security' | 'appearance'>('general')
  const [saved, setSaved] = useState(false)

  const handleSave = () => {
    setSaved(true)
    setTimeout(() => setSaved(false), 3000)
  }

  const updateGeneralSetting = (key: keyof SettingsState['general'], value: string) => {
    setSettings((prev) => ({
      ...prev,
      general: { ...prev.general, [key]: value },
    }))
  }

  const toggleNotification = (key: keyof SettingsState['notifications']) => {
    setSettings((prev) => ({
      ...prev,
      notifications: { ...prev.notifications, [key]: !prev.notifications[key] },
    }))
  }

  const toggleSecurity = (key: keyof SettingsState['security']) => {
    if (typeof settings.security[key] === 'boolean') {
      setSettings((prev) => ({
        ...prev,
        security: { ...prev.security, [key]: !prev.security[key] },
      }))
    }
  }

  const updateSecuritySetting = (key: keyof SettingsState['security'], value: string) => {
    setSettings((prev) => ({
      ...prev,
      security: { ...prev.security, [key]: value },
    }))
  }

  const updateAppearance = (key: keyof SettingsState['appearance'], value: string | boolean) => {
    setSettings((prev) => ({
      ...prev,
      appearance: { ...prev.appearance, [key]: value },
    }))
  }

  const tabs = [
    { id: 'general', label: 'General', icon: '⚙️' },
    { id: 'notifications', label: 'Notifications', icon: '🔔' },
    { id: 'security', label: 'Security', icon: '🔒' },
    { id: 'appearance', label: 'Appearance', icon: '🎨' },
  ] as const

  return (
    <div data-testid="settings">
      <div className="page-header">
        <h1>Settings</h1>
        <p>Manage your application settings and preferences.</p>
      </div>

      {saved && (
        <div
          style={{
            backgroundColor: 'var(--success-color)',
            color: 'white',
            padding: '1rem',
            borderRadius: '8px',
            marginBottom: '1rem',
          }}
          data-testid="save-notification"
        >
          ✓ Settings saved successfully!
        </div>
      )}

      <div style={{ display: 'flex', gap: '1.5rem' }}>
        <div className="card" style={{ width: '240px', flexShrink: 0, padding: '0.5rem' }}>
          <nav>
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                data-testid={`tab-${tab.id}`}
                style={{
                  width: '100%',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.75rem',
                  padding: '0.75rem 1rem',
                  border: 'none',
                  background: activeTab === tab.id ? 'var(--background-color)' : 'transparent',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  textAlign: 'left',
                  fontWeight: activeTab === tab.id ? '600' : '400',
                  color: activeTab === tab.id ? 'var(--primary-color)' : 'var(--text-primary)',
                }}
              >
                <span>{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        <div className="card" style={{ flex: 1 }}>
          {activeTab === 'general' && (
            <div data-testid="general-settings">
              <h2 style={{ marginBottom: '1.5rem' }}>General Settings</h2>
              <div className="form-group">
                <label className="form-label">Site Name</label>
                <input
                  type="text"
                  className="form-input"
                  value={settings.general.siteName}
                  onChange={(e) => updateGeneralSetting('siteName', e.target.value)}
                  data-testid="site-name-input"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Site URL</label>
                <input
                  type="url"
                  className="form-input"
                  value={settings.general.siteUrl}
                  onChange={(e) => updateGeneralSetting('siteUrl', e.target.value)}
                  data-testid="site-url-input"
                />
              </div>
              <div className="form-group">
                <label className="form-label">Timezone</label>
                <select
                  className="form-select"
                  value={settings.general.timezone}
                  onChange={(e) => updateGeneralSetting('timezone', e.target.value)}
                  data-testid="timezone-select"
                >
                  <option value="UTC">UTC</option>
                  <option value="EST">Eastern Time (EST)</option>
                  <option value="PST">Pacific Time (PST)</option>
                  <option value="GMT">Greenwich Mean Time (GMT)</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Language</label>
                <select
                  className="form-select"
                  value={settings.general.language}
                  onChange={(e) => updateGeneralSetting('language', e.target.value)}
                  data-testid="language-select"
                >
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                </select>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div data-testid="notification-settings">
              <h2 style={{ marginBottom: '1.5rem' }}>Notification Settings</h2>
              {Object.entries(settings.notifications).map(([key, value]) => (
                <div
                  key={key}
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    padding: '1rem 0',
                    borderBottom: '1px solid var(--border-color)',
                  }}
                >
                  <div>
                    <div style={{ fontWeight: '500' }}>
                      {key.replace(/([A-Z])/g, ' $1').replace(/^./, (s) => s.toUpperCase())}
                    </div>
                    <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                      Receive {key.replace(/([A-Z])/g, ' $1').toLowerCase()}
                    </div>
                  </div>
                  <label className="toggle-switch">
                    <input
                      type="checkbox"
                      checked={value}
                      onChange={() => toggleNotification(key as keyof SettingsState['notifications'])}
                      data-testid={`toggle-${key}`}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'security' && (
            <div data-testid="security-settings">
              <h2 style={{ marginBottom: '1.5rem' }}>Security Settings</h2>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem 0',
                  borderBottom: '1px solid var(--border-color)',
                }}
              >
                <div>
                  <div style={{ fontWeight: '500' }}>Two-Factor Authentication</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                    Add an extra layer of security to your account
                  </div>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    checked={settings.security.twoFactorAuth}
                    onChange={() => toggleSecurity('twoFactorAuth')}
                    data-testid="toggle-2fa"
                  />
                  <span className="toggle-slider"></span>
                </label>
              </div>
              <div className="form-group" style={{ marginTop: '1.5rem' }}>
                <label className="form-label">Session Timeout (minutes)</label>
                <select
                  className="form-select"
                  value={settings.security.sessionTimeout}
                  onChange={(e) => updateSecuritySetting('sessionTimeout', e.target.value)}
                  data-testid="session-timeout-select"
                >
                  <option value="15">15 minutes</option>
                  <option value="30">30 minutes</option>
                  <option value="60">1 hour</option>
                  <option value="120">2 hours</option>
                </select>
              </div>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem 0',
                  borderBottom: '1px solid var(--border-color)',
                }}
              >
                <div>
                  <div style={{ fontWeight: '500' }}>IP Whitelist</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                    Only allow access from specific IP addresses
                  </div>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    checked={settings.security.ipWhitelist}
                    onChange={() => toggleSecurity('ipWhitelist')}
                    data-testid="toggle-ip-whitelist"
                  />
                  <span className="toggle-slider"></span>
                </label>
              </div>
            </div>
          )}

          {activeTab === 'appearance' && (
            <div data-testid="appearance-settings">
              <h2 style={{ marginBottom: '1.5rem' }}>Appearance Settings</h2>
              <div className="form-group">
                <label className="form-label">Theme</label>
                <div style={{ display: 'flex', gap: '1rem' }}>
                  {(['light', 'dark', 'system'] as const).map((theme) => (
                    <button
                      key={theme}
                      onClick={() => updateAppearance('theme', theme)}
                      data-testid={`theme-${theme}`}
                      style={{
                        padding: '1rem 2rem',
                        border: settings.appearance.theme === theme
                          ? '2px solid var(--primary-color)'
                          : '1px solid var(--border-color)',
                        borderRadius: '8px',
                        background: theme === 'dark' ? '#1e293b' : 'white',
                        color: theme === 'dark' ? 'white' : 'var(--text-primary)',
                        cursor: 'pointer',
                        textTransform: 'capitalize',
                      }}
                    >
                      {theme}
                    </button>
                  ))}
                </div>
              </div>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem 0',
                  borderBottom: '1px solid var(--border-color)',
                }}
              >
                <div>
                  <div style={{ fontWeight: '500' }}>Compact Mode</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                    Reduce spacing and padding throughout the UI
                  </div>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    checked={settings.appearance.compactMode}
                    onChange={() => updateAppearance('compactMode', !settings.appearance.compactMode)}
                    data-testid="toggle-compact-mode"
                  />
                  <span className="toggle-slider"></span>
                </label>
              </div>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1rem 0',
                  borderBottom: '1px solid var(--border-color)',
                }}
              >
                <div>
                  <div style={{ fontWeight: '500' }}>Show Avatars</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                    Display user avatars in lists and comments
                  </div>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    checked={settings.appearance.showAvatars}
                    onChange={() => updateAppearance('showAvatars', !settings.appearance.showAvatars)}
                    data-testid="toggle-show-avatars"
                  />
                  <span className="toggle-slider"></span>
                </label>
              </div>
            </div>
          )}

          <div style={{ marginTop: '2rem', display: 'flex', justifyContent: 'flex-end', gap: '1rem' }}>
            <button className="btn btn-secondary">Reset to Default</button>
            <button className="btn btn-primary" onClick={handleSave} data-testid="save-settings">
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
