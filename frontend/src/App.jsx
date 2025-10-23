import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import CasesPage from './pages/CasesPage'
import MyNagaSetup from './pages/MyNagaSetup'
import GoogleSheetsSetup from './pages/GoogleSheetsSetup'
import { officeAPI, clusterAPI, caseAPI } from './services/api'
import { useOfficeStore, useClusterStore } from './store'
import { FiMenu } from 'react-icons/fi'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const setOffices = useOfficeStore((state) => state.setOffices)
  const setClusters = useClusterStore((state) => state.setClusters)

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      const [offices, clusters] = await Promise.all([
        officeAPI.getAll(),
        clusterAPI.getAll(),
      ])
      setOffices(offices.data)
      setClusters(clusters.data)
    } catch (error) {
      console.error('Error loading initial data:', error)
    }
  }

  return (
    <Router>
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar isOpen={sidebarOpen} toggle={() => setSidebarOpen(!sidebarOpen)} />
        
        <main className="flex-1 overflow-auto">
          <header className="lg:hidden flex items-center justify-between bg-white p-4 shadow">
            <h1 className="text-2xl font-bold text-blue-600">MyNaga</h1>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-700"
            >
              <FiMenu size={24} />
            </button>
          </header>

          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/cases" element={<CasesPage />} />
            <Route path="/mynaga" element={<MyNagaSetup />} />
            <Route path="/google-sheets" element={<GoogleSheetsSetup />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
