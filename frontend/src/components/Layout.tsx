import { NavLink, Outlet } from 'react-router'

export function Layout() {
  return (
    <div className="layout">
      <header className="layout__header">
        <div className="layout__bar">
          <span className="layout__brand">Starter App</span>
          <nav className="layout__nav">
            <NavLink to="/" end>
              Home
            </NavLink>
            <NavLink to="/items">Items</NavLink>
          </nav>
        </div>
      </header>
      <main className="layout__main">
        <Outlet />
      </main>
    </div>
  )
}
