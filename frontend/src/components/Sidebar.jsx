import React from 'react'
import { FiMenu, FiHome, FiFileText, FiTag, FiSettings, FiLogOut, FiZap, FiCloud } from 'react-icons/fi'

export default function Sidebar({ isOpen, toggle }) {
  return (
    <aside className={`${isOpen ? 'translate-x-0' : '-translate-x-full'} fixed inset-y-0 left-0 z-50 w-64 bg-blue-600 text-white transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:w-64 lg:z-auto`}>
      <div className="flex items-center justify-between p-6 lg:justify-start">
        <div className="flex items-center space-x-3">
          {/* Add your logo image here */}
          <img 
            src="/logo.png" 
            alt="MyNaga Logo" 
            className="h-10 w-10 rounded-lg"
          />
          <h1 className="text-2xl font-bold">MyNaga App</h1>
        </div>
        <button onClick={toggle} className="lg:hidden">
          <FiMenu size={24} />
        </button>
      </div>

      <nav className="mt-8 space-y-2 px-4">
        <NavLink icon={<FiHome />} label="Dashboard" href="/" />
        <NavLink icon={<FiFileText />} label="Cases" href="/cases" />
        <NavLink icon={<FiTag />} label="Clusters" href="/clusters" />
        <NavLink icon={<FiSettings />} label="Offices" href="/offices" />
        <NavLink icon={<FiZap />} label="MyNaga Sync" href="/mynaga" />
        <NavLink icon={<FiCloud />} label="Google Sheets" href="/google-sheets" />
      </nav>

      <div className="absolute bottom-0 w-full p-4 border-t border-blue-500">
        <button className="flex items-center w-full space-x-3 text-left hover:bg-blue-700 rounded-lg p-3 transition">
          <FiLogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </aside>
  )
}

function NavLink({ icon, label, href }) {
  return (
    <a href={href} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-blue-700 transition">
      <span className="text-xl">{icon}</span>
      <span>{label}</span>
    </a>
  )
}
