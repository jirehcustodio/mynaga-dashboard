import React, { useEffect, useState } from 'react'
import { statsAPI, caseAPI } from '../services/api'
import MyNagaStatusCard from '../components/MyNagaStatusCard'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  useEffect(() => {
    loadStats()
    
    // Auto-refresh every 10 seconds for real-time updates
    const refreshInterval = setInterval(() => {
      loadStats()
    }, 10000) // 10 seconds
    
    return () => clearInterval(refreshInterval)
  }, [])

  const loadStats = async () => {
    try {
      const res = await statsAPI.getAll()
      setStats(res.data)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Error loading stats:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return (
      <div className="container py-12 text-center">
        <p className="text-gray-500">Loading dashboard...</p>
      </div>
    )
  }

  if (!stats) {
    return (
      <div className="container py-12 text-center">
        <p className="text-gray-500">Error loading statistics</p>
      </div>
    )
  }

  const chartData = [
    {
      name: 'OPEN',
      value: stats.open_cases,
    },
    {
      name: 'RESOLVED',
      value: stats.resolved_cases,
    },
    {
      name: 'FOR REROUTING',
      value: stats.rerouting_cases,
    },
  ]

  return (
    <div className="container py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <div className="flex items-center gap-4">
          <div className="text-sm text-gray-500">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </div>
          <button
            onClick={loadStats}
            className="btn btn-secondary"
            title="Refresh dashboard"
          >
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* MyNaga App Status Section */}
      <div className="mb-8">
        <MyNagaStatusCard />
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <StatCard
          title="Total Cases"
          value={stats.total_cases}
          color="bg-blue-50 text-blue-600"
        />
        <StatCard
          title="Open Cases"
          value={stats.open_cases}
          color="bg-yellow-50 text-yellow-600"
        />
        <StatCard
          title="Resolved Cases"
          value={stats.resolved_cases}
          color="bg-green-50 text-green-600"
        />
        <StatCard
          title="For Rerouting"
          value={stats.rerouting_cases}
          color="bg-orange-50 text-orange-600"
        />
        <StatCard
          title="Total Offices"
          value={stats.total_offices}
          color="bg-purple-50 text-purple-600"
        />
        <StatCard
          title="Total Clusters"
          value={stats.total_clusters}
          color="bg-pink-50 text-pink-600"
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold mb-4">Cases by Status</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold mb-4">Statistics</h2>
          <div className="space-y-3">
            <div>
              <p className="text-gray-600">Average Case Aging</p>
              <p className="text-2xl font-bold">
                {stats.average_case_aging.toFixed(1)} days
              </p>
            </div>
            <div>
              <p className="text-gray-600">Resolution Rate</p>
              <p className="text-2xl font-bold">
                {stats.total_cases > 0
                  ? ((stats.resolved_cases / stats.total_cases) * 100).toFixed(1)
                  : 0}
                %
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, color }) {
  return (
    <div className={`${color} rounded-lg p-6`}>
      <p className="text-sm font-medium opacity-75">{title}</p>
      <p className="text-4xl font-bold mt-2">{value}</p>
    </div>
  )
}
