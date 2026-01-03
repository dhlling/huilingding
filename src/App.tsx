import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './modules/Dashboard'
import UserManagement from './modules/UserManagement'
import Analytics from './modules/Analytics'
import Settings from './modules/Settings'
import Notifications from './modules/Notifications'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="users" element={<UserManagement />} />
        <Route path="analytics" element={<Analytics />} />
        <Route path="settings" element={<Settings />} />
        <Route path="notifications" element={<Notifications />} />
      </Route>
    </Routes>
  )
}

export default App
