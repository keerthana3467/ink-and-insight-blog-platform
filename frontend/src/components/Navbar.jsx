import React from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { api, csrf } from '../services/api'
export default function Navbar({user,setUser}) {
  const navigate=useNavigate()
  async function signout(){try{await csrf();await api.post('/auth/logout/');setUser(null);navigate('/')}catch{}}
  return <nav className="navbar navbar-expand-lg site-nav sticky-top"><div className="container">
    <Link className="navbar-brand brand" to="/"><span className="brand-mark">i.</span> ink & insight</Link>
    <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMain"><span className="navbar-toggler-icon"></span></button>
    <div className="collapse navbar-collapse" id="navMain">
      <div className="navbar-nav ms-auto align-items-lg-center gap-lg-3">
        <NavLink className="nav-link" to="/stories">Explore</NavLink><NavLink className="nav-link" to="/about">About</NavLink>
        {user ? <><NavLink className="nav-link" to="/dashboard">Dashboard</NavLink><Link className="btn btn-ink btn-sm px-3" to="/write"><i className="bi bi-plus-lg me-1"></i>Write</Link><div className="dropdown">
          <button className="avatar-button dropdown-toggle" data-bs-toggle="dropdown" aria-label="Account menu">{user.avatar?<img src={user.avatar} alt=""/>:<span>{user.username?.[0]?.toUpperCase()}</span>}</button>
          <ul className="dropdown-menu dropdown-menu-end"><li><Link className="dropdown-item" to={`/profile/${user.username}`}>My profile</Link></li><li><Link className="dropdown-item" to="/profile/edit">Edit profile</Link></li><li><button className="dropdown-item" onClick={signout}>Sign out</button></li></ul>
        </div></> : <><Link className="nav-link" to="/login">Sign in</Link><Link className="btn btn-ink btn-sm px-3" to="/register">Get started</Link></>}
      </div>
    </div>
  </div></nav>
}
