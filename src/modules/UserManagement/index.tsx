import { useState } from 'react'

interface User {
  id: string
  name: string
  email: string
  role: 'admin' | 'user' | 'moderator'
  status: 'active' | 'inactive' | 'pending'
  joinedDate: string
}

const initialUsers: User[] = [
  { id: '1', name: 'John Doe', email: 'john@example.com', role: 'admin', status: 'active', joinedDate: '2024-01-15' },
  { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'user', status: 'active', joinedDate: '2024-02-20' },
  { id: '3', name: 'Mike Johnson', email: 'mike@example.com', role: 'moderator', status: 'pending', joinedDate: '2024-03-10' },
  { id: '4', name: 'Sarah Wilson', email: 'sarah@example.com', role: 'user', status: 'inactive', joinedDate: '2024-01-05' },
  { id: '5', name: 'Tom Brown', email: 'tom@example.com', role: 'user', status: 'active', joinedDate: '2024-04-01' },
]

const UserManagement = () => {
  const [users, setUsers] = useState<User[]>(initialUsers)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterRole, setFilterRole] = useState<string>('all')
  const [showAddModal, setShowAddModal] = useState(false)
  const [newUser, setNewUser] = useState<{ name: string; email: string; role: User['role'] }>({ name: '', email: '', role: 'user' })

  const filteredUsers = users.filter((user) => {
    const matchesSearch = user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         user.email.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesRole = filterRole === 'all' || user.role === filterRole
    return matchesSearch && matchesRole
  })

  const handleAddUser = () => {
    if (newUser.name && newUser.email) {
      const user: User = {
        id: String(users.length + 1),
        ...newUser,
        status: 'pending',
        joinedDate: new Date().toISOString().split('T')[0],
      }
      setUsers([...users, user])
      setNewUser({ name: '', email: '', role: 'user' })
      setShowAddModal(false)
    }
  }

  const handleDeleteUser = (id: string) => {
    setUsers(users.filter((user) => user.id !== id))
  }

  const handleToggleStatus = (id: string) => {
    setUsers(users.map((user) => {
      if (user.id === id) {
        return { ...user, status: user.status === 'active' ? 'inactive' : 'active' }
      }
      return user
    }))
  }

  const getStatusBadge = (status: User['status']) => {
    const badges = {
      active: 'badge badge-success',
      inactive: 'badge badge-danger',
      pending: 'badge badge-warning',
    }
    return badges[status]
  }

  const getRoleBadge = (role: User['role']) => {
    const badges = {
      admin: 'badge badge-info',
      moderator: 'badge badge-warning',
      user: 'badge badge-success',
    }
    return badges[role]
  }

  return (
    <div data-testid="user-management">
      <div className="page-header">
        <h1>User Management</h1>
        <p>Manage your users, roles, and permissions.</p>
      </div>

      <div className="card" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
          <input
            type="text"
            className="form-input"
            placeholder="Search users..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ maxWidth: '300px' }}
            data-testid="search-input"
          />
          <select
            className="form-select"
            value={filterRole}
            onChange={(e) => setFilterRole(e.target.value)}
            style={{ maxWidth: '150px' }}
            data-testid="role-filter"
          >
            <option value="all">All Roles</option>
            <option value="admin">Admin</option>
            <option value="moderator">Moderator</option>
            <option value="user">User</option>
          </select>
          <button
            className="btn btn-primary"
            onClick={() => setShowAddModal(true)}
            data-testid="add-user-btn"
            style={{ marginLeft: 'auto' }}
          >
            + Add User
          </button>
        </div>
      </div>

      <div className="card">
        <table className="data-table" data-testid="users-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Joined</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map((user) => (
              <tr key={user.id} data-testid={`user-row-${user.id}`}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td><span className={getRoleBadge(user.role)}>{user.role}</span></td>
                <td><span className={getStatusBadge(user.status)}>{user.status}</span></td>
                <td>{user.joinedDate}</td>
                <td>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <button
                      className="btn btn-secondary"
                      onClick={() => handleToggleStatus(user.id)}
                      data-testid={`toggle-status-${user.id}`}
                    >
                      {user.status === 'active' ? 'Deactivate' : 'Activate'}
                    </button>
                    <button
                      className="btn btn-danger"
                      onClick={() => handleDeleteUser(user.id)}
                      data-testid={`delete-user-${user.id}`}
                    >
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filteredUsers.length === 0 && (
          <p style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
            No users found.
          </p>
        )}
      </div>

      {showAddModal && (
        <div
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
          }}
          data-testid="add-user-modal"
          onClick={() => setShowAddModal(false)}
        >
          <div
            className="card"
            style={{ width: '400px', maxWidth: '90%' }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 style={{ marginBottom: '1.5rem' }}>Add New User</h2>
            <div className="form-group">
              <label className="form-label">Name</label>
              <input
                type="text"
                className="form-input"
                value={newUser.name}
                onChange={(e) => setNewUser({ ...newUser, name: e.target.value })}
                data-testid="new-user-name"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-input"
                value={newUser.email}
                onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                data-testid="new-user-email"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Role</label>
              <select
                className="form-select"
                value={newUser.role}
                onChange={(e) => setNewUser({ ...newUser, role: e.target.value as User['role'] })}
                data-testid="new-user-role"
              >
                <option value="user">User</option>
                <option value="moderator">Moderator</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
              <button
                className="btn btn-secondary"
                onClick={() => setShowAddModal(false)}
              >
                Cancel
              </button>
              <button
                className="btn btn-primary"
                onClick={handleAddUser}
                data-testid="confirm-add-user"
              >
                Add User
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default UserManagement
