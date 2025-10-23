import React, { useState, useEffect } from 'react'
import { FiSettings, FiCheck, FiX, FiRefreshCw } from 'react-icons/fi'
import axios from 'axios'

export default function MyNagaSetup() {
  const [authToken, setAuthToken] = useState('')
  const [syncInterval, setSyncInterval] = useState(5)
  const [isLoading, setIsLoading] = useState(false)
  const [syncStatus, setSyncStatus] = useState(null)
  const [testResult, setTestResult] = useState(null)
  const [showSuccess, setShowSuccess] = useState(false)

  useEffect(() => {
    // Fetch sync status on mount
    fetchSyncStatus()
  }, [])

  const fetchSyncStatus = async () => {
    try {
      const res = await axios.get('/api/mynaga/sync/status')
      setSyncStatus(res.data)
    } catch (error) {
      console.error('Error fetching sync status:', error)
    }
  }

  const testConnection = async () => {
    if (!authToken.trim()) {
      alert('Please enter your auth token')
      return
    }

    setIsLoading(true)
    setTestResult(null)

    try {
      const res = await axios.post('/api/mynaga/test-connection', null, {
        params: { auth_token: authToken }
      })

      setTestResult({
        success: true,
        message: res.data.message,
        sample_count: res.data.sample_count
      })
    } catch (error) {
      setTestResult({
        success: false,
        message: error.response?.data?.detail || 'Connection failed'
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleConfigure = async () => {
    if (!authToken.trim()) {
      alert('Please enter your auth token')
      return
    }

    setIsLoading(true)

    try {
      const res = await axios.post('/api/mynaga/config', {
        auth_token: authToken,
        sync_interval_minutes: syncInterval
      })

      setShowSuccess(true)
      setTimeout(() => setShowSuccess(false), 3000)

      // Fetch updated status
      fetchSyncStatus()
    } catch (error) {
      alert('Configuration failed: ' + (error.response?.data?.detail || error.message))
    } finally {
      setIsLoading(false)
    }
  }

  const handleManualSync = async () => {
    if (!authToken.trim()) {
      alert('Please configure MyNaga first')
      return
    }

    setIsLoading(true)

    try {
      const res = await axios.post('/api/mynaga/sync/manual', null, {
        params: { auth_token: authToken }
      })

      alert(
        `Sync successful!\n` +
        `Created: ${res.data.stats.created}\n` +
        `Updated: ${res.data.stats.updated}\n` +
        `Errors: ${res.data.stats.errors}`
      )

      fetchSyncStatus()
    } catch (error) {
      alert('Manual sync failed: ' + (error.response?.data?.detail || error.message))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container py-8">
      <div className="mb-8">
        <div className="flex items-center space-x-3 mb-2">
          <FiSettings size={28} className="text-blue-600" />
          <h1 className="text-3xl font-bold">MyNaga Real-time Integration</h1>
        </div>
        <p className="text-gray-600">
          Connect your MyNaga App account to automatically sync data in real-time
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Setup Card */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-bold mb-6">Setup MyNaga Connection</h2>

            <div className="space-y-6">
              {/* Auth Token Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  MyNaga Auth Token *
                </label>
                <textarea
                  value={authToken}
                  onChange={(e) => setAuthToken(e.target.value)}
                  placeholder="Paste your MyNaga authentication token here..."
                  className="input h-24"
                />
                <p className="text-sm text-gray-500 mt-2">
                  Get your token from: MyNaga App → Settings → API → Generate Token
                </p>
              </div>

              {/* Sync Interval */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sync Interval (minutes)
                </label>
                <input
                  type="number"
                  min="1"
                  max="60"
                  value={syncInterval}
                  onChange={(e) => setSyncInterval(parseInt(e.target.value))}
                  className="input w-32"
                />
                <p className="text-sm text-gray-500 mt-2">
                  How often to sync data from MyNaga (1-60 minutes)
                </p>
              </div>

              {/* Test Connection */}
              <div className="border-t pt-6">
                <button
                  onClick={testConnection}
                  disabled={isLoading}
                  className="btn btn-secondary"
                >
                  <FiRefreshCw className="mr-2" />
                  {isLoading ? 'Testing...' : 'Test Connection'}
                </button>

                {testResult && (
                  <div
                    className={`mt-4 p-4 rounded-lg ${
                      testResult.success
                        ? 'bg-green-50 border border-green-200'
                        : 'bg-red-50 border border-red-200'
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      {testResult.success ? (
                        <FiCheck className="text-green-600 mt-1" size={20} />
                      ) : (
                        <FiX className="text-red-600 mt-1" size={20} />
                      )}
                      <div>
                        <p
                          className={`font-medium ${
                            testResult.success ? 'text-green-800' : 'text-red-800'
                          }`}
                        >
                          {testResult.message}
                        </p>
                        {testResult.sample_count && (
                          <p className="text-sm text-gray-600 mt-1">
                            Found {testResult.sample_count} sample records
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Configure Button */}
              <div className="border-t pt-6">
                <button
                  onClick={handleConfigure}
                  disabled={isLoading || !authToken}
                  className="btn btn-primary w-full"
                >
                  {isLoading ? 'Configuring...' : 'Configure MyNaga Connection'}
                </button>

                {showSuccess && (
                  <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center space-x-3">
                    <FiCheck className="text-green-600" size={20} />
                    <span className="text-green-800">
                      Configuration saved! Real-time sync is now active.
                    </span>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Status Card */}
        <div>
          <div className="card">
            <h3 className="font-bold mb-4">Sync Status</h3>

            {syncStatus ? (
              <div className="space-y-4">
                <div>
                  <p className="text-sm text-gray-600">Status</p>
                  <p className={`text-lg font-bold ${syncStatus.is_syncing ? 'text-yellow-600' : 'text-green-600'}`}>
                    {syncStatus.is_syncing ? '🔄 Syncing...' : '✅ Ready'}
                  </p>
                </div>

                {syncStatus.last_sync_time && (
                  <div>
                    <p className="text-sm text-gray-600">Last Sync</p>
                    <p className="font-mono text-sm">
                      {new Date(syncStatus.last_sync_time).toLocaleString()}
                    </p>
                  </div>
                )}

                {syncStatus.last_sync_status && (
                  <div>
                    <p className="text-sm text-gray-600 mb-2">Latest Stats</p>
                    <div className="space-y-1 text-sm">
                      {syncStatus.last_sync_status.created && (
                        <p>✨ Created: {syncStatus.last_sync_status.created}</p>
                      )}
                      {syncStatus.last_sync_status.updated && (
                        <p>📝 Updated: {syncStatus.last_sync_status.updated}</p>
                      )}
                      {syncStatus.last_sync_status.errors > 0 && (
                        <p className="text-red-600">
                          ⚠️ Errors: {syncStatus.last_sync_status.errors}
                        </p>
                      )}
                    </div>
                  </div>
                )}

                <button
                  onClick={handleManualSync}
                  disabled={isLoading || !authToken}
                  className="btn btn-secondary w-full text-sm"
                >
                  <FiRefreshCw className="mr-1" size={16} />
                  Sync Now
                </button>
              </div>
            ) : (
              <p className="text-gray-500 text-center py-4">
                Configure connection to view status
              </p>
            )}
          </div>

          {/* Help Card */}
          <div className="card mt-6 bg-blue-50 border border-blue-200">
            <h4 className="font-bold text-blue-900 mb-3">💡 How It Works</h4>
            <ol className="text-sm text-blue-800 space-y-2 list-decimal list-inside">
              <li>Enter your MyNaga auth token</li>
              <li>Test the connection</li>
              <li>Configure sync interval</li>
              <li>Data syncs automatically</li>
              <li>All changes appear in dashboard</li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  )
}
