import React, { useState, useEffect } from 'react'
import { FiRefreshCw, FiCheck, FiAlertCircle, FiExternalLink } from 'react-icons/fi'
import axios from 'axios'

export default function GoogleSheetsSetup() {
  const [sheetUrl, setSheetUrl] = useState('')
  const [credentialsJson, setCredentialsJson] = useState('')
  const [useServiceAccount, setUseServiceAccount] = useState(false)
  const [isTesting, setIsTesting] = useState(false)
  const [isSyncing, setIsSyncing] = useState(false)
  const [testResult, setTestResult] = useState(null)
  const [syncResult, setSyncResult] = useState(null)
  const [autoSyncEnabled, setAutoSyncEnabled] = useState(false)
  const [syncStatus, setSyncStatus] = useState(null)

  useEffect(() => {
    // Check auto-sync status on load
    checkAutoSyncStatus()
  }, [])

  const checkAutoSyncStatus = async () => {
    try {
      const response = await axios.get('/api/google-sheets/status')
      setSyncStatus(response.data)
      setAutoSyncEnabled(response.data.configured && response.data.last_sync_time !== null)
    } catch (error) {
      console.error('Error checking sync status:', error)
    }
  }

  const handleEnableAutoSync = async () => {
    if (!sheetUrl.trim()) {
      alert('Please enter a Google Sheets URL first')
      return
    }

    if (useServiceAccount && !credentialsJson) {
      alert('Please upload service account credentials')
      return
    }

    try {
      const response = await axios.post('/api/google-sheets/auto-sync/start', {
        sheet_url: sheetUrl,
        credentials_json: useServiceAccount ? credentialsJson : null,
        interval_minutes: 5
      })

      setAutoSyncEnabled(true)
      alert('✅ Auto-sync enabled! Dashboard will update every 5 minutes.')
      checkAutoSyncStatus()
    } catch (error) {
      alert('❌ Failed to enable auto-sync: ' + error.response?.data?.detail || error.message)
    }
  }

  const handleDisableAutoSync = async () => {
    try {
      await axios.post('/api/google-sheets/auto-sync/stop')
      setAutoSyncEnabled(false)
      alert('Auto-sync disabled')
      checkAutoSyncStatus()
    } catch (error) {
      alert('Failed to disable auto-sync')
    }
  }

  const handleFileUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target.result)
          setCredentialsJson(JSON.stringify(json))
          setUseServiceAccount(true)
          alert('✅ Service account credentials loaded!')
        } catch (error) {
          alert('❌ Invalid JSON file. Please upload a valid service account key.')
        }
      }
      reader.readAsText(file)
    }
  }

  const handleTestConnection = async () => {
    if (!sheetUrl.trim()) {
      alert('Please enter a Google Sheets URL')
      return
    }

    if (useServiceAccount && !credentialsJson) {
      alert('Please upload service account credentials or switch to CSV method')
      return
    }

    setIsTesting(true)
    setTestResult(null)

    try {
      const response = await axios.post('/api/google-sheets/test-connection', {
        sheet_url: sheetUrl,
        credentials_json: useServiceAccount ? credentialsJson : null
      })

      setTestResult({
        success: true,
        message: response.data.message,
        rowCount: response.data.row_count,
        columns: response.data.columns,
        authMethod: response.data.auth_method
      })
    } catch (error) {
      setTestResult({
        success: false,
        message: error.response?.data?.detail || error.message
      })
    } finally {
      setIsTesting(false)
    }
  }

  const handleSync = async () => {
    if (!sheetUrl.trim()) {
      alert('Please enter a Google Sheets URL')
      return
    }

    if (useServiceAccount && !credentialsJson) {
      alert('Please upload service account credentials first')
      return
    }

    if (!confirm('This will sync data from Google Sheets to the database. Continue?')) {
      return
    }

    setIsSyncing(true)
    setSyncResult(null)

    try {
      const response = await axios.post('/api/google-sheets/sync', {
        sheet_url: sheetUrl,
        credentials_json: useServiceAccount ? credentialsJson : null
      })

      setSyncResult({
        success: true,
        message: response.data.message,
        stats: response.data.stats
      })
    } catch (error) {
      setSyncResult({
        success: false,
        message: error.response?.data?.detail || error.message
      })
    } finally {
      setIsSyncing(false)
    }
  }

  return (
    <div className="container py-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Google Sheets Sync</h1>
          <p className="text-gray-600">
            Sync case data from a published Google Sheets spreadsheet
          </p>
        </div>

        {/* Configuration Card */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <FiExternalLink className="mr-2" />
            Sheet Configuration
          </h2>

          {/* Authentication Method Selection */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Authentication Method
            </label>
            <div className="space-y-3">
              <label className="flex items-start space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input
                  type="radio"
                  checked={!useServiceAccount}
                  onChange={() => setUseServiceAccount(false)}
                  className="mt-1"
                />
                <div>
                  <div className="font-medium">Published CSV (Simple)</div>
                  <div className="text-sm text-gray-600">
                    Publish your sheet to web as CSV. Quick setup, sheet becomes accessible via URL.
                  </div>
                </div>
              </label>
              
              <label className="flex items-start space-x-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50">
                <input
                  type="radio"
                  checked={useServiceAccount}
                  onChange={() => setUseServiceAccount(true)}
                  className="mt-1"
                />
                <div>
                  <div className="font-medium">Service Account (Private) 🔒</div>
                  <div className="text-sm text-gray-600">
                    Keep your sheet fully private. Requires Google Cloud service account setup.
                  </div>
                </div>
              </label>
            </div>
          </div>

          {/* Instructions based on method */}
          {!useServiceAccount ? (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-blue-900 mb-2">📋 CSV Method Setup:</h3>
              <ol className="list-decimal list-inside space-y-2 text-sm text-blue-800">
                <li>Open your Google Sheet with case data</li>
                <li>Click <strong>File → Share → Publish to web</strong></li>
                <li>Select <strong>Sheet tab</strong> and format as <strong>CSV</strong></li>
                <li>Click <strong>Publish</strong> and copy the CSV URL</li>
                <li>Paste the URL below and test the connection</li>
              </ol>
            </div>
          ) : (
            <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
              <h3 className="font-semibold text-purple-900 mb-2">🔐 Service Account Setup:</h3>
              <ol className="list-decimal list-inside space-y-2 text-sm text-purple-800">
                <li>Create Google Cloud project and enable Sheets API</li>
                <li>Create service account and download JSON key</li>
                <li>Share your private sheet with service account email</li>
                <li>Upload the JSON key file below</li>
                <li>Enter your sheet URL (regular /edit URL works!)</li>
              </ol>
              <a 
                href="https://github.com/yourusername/mynaga-dashboard/blob/main/GOOGLE_SHEETS_PRIVATE.md"
                target="_blank"
                className="text-xs text-purple-600 hover:text-purple-800 underline mt-2 inline-block"
              >
                📖 Full setup guide in GOOGLE_SHEETS_PRIVATE.md
              </a>
            </div>
          )}

          {/* Service Account Credentials Upload */}
          {useServiceAccount && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Service Account Credentials
              </label>
              <input
                type="file"
                accept=".json"
                onChange={handleFileUpload}
                className="block w-full text-sm text-gray-500
                  file:mr-4 file:py-2 file:px-4
                  file:rounded-lg file:border-0
                  file:text-sm file:font-semibold
                  file:bg-purple-600 file:text-white
                  hover:file:bg-purple-700
                  cursor-pointer"
              />
              <p className="mt-2 text-xs text-gray-500">
                Upload the JSON key file from Google Cloud Console
              </p>
              {credentialsJson && (
                <div className="mt-2 flex items-center text-sm text-green-600">
                  <FiCheck className="mr-1" />
                  Credentials loaded
                </div>
              )}
            </div>
          )}

          {/* Sheet URL Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Google Sheets URL
            </label>
            <input
              type="text"
              value={sheetUrl}
              onChange={(e) => setSheetUrl(e.target.value)}
              placeholder="https://docs.google.com/spreadsheets/d/..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <p className="mt-2 text-sm text-gray-500">
              Enter the published Google Sheets URL or the regular sheet link
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex space-x-3">
            <button
              onClick={handleTestConnection}
              disabled={isTesting || !sheetUrl.trim()}
              className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isTesting ? (
                <>
                  <FiRefreshCw className="animate-spin mr-2" />
                  Testing...
                </>
              ) : (
                <>
                  <FiCheck className="mr-2" />
                  Test Connection
                </>
              )}
            </button>

            <button
              onClick={handleSync}
              disabled={isSyncing || !sheetUrl.trim()}
              className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isSyncing ? (
                <>
                  <FiRefreshCw className="animate-spin mr-2" />
                  Syncing...
                </>
              ) : (
                <>
                  <FiRefreshCw className="mr-2" />
                  Sync Now
                </>
              )}
            </button>

            {/* Auto-Sync Toggle */}
            {autoSyncEnabled ? (
              <button
                onClick={handleDisableAutoSync}
                className="flex items-center px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-colors"
              >
                🔴 Disable Auto-Sync
              </button>
            ) : (
              <button
                onClick={handleEnableAutoSync}
                disabled={!sheetUrl.trim()}
                className="flex items-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                ⚡ Enable Auto-Sync (5 min)
              </button>
            )}
          </div>
        </div>

        {/* Auto-Sync Status */}
        {autoSyncEnabled && syncStatus && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
            <div className="flex items-start">
              <div className="flex-shrink-0">
                <FiCheck className="h-5 w-5 text-purple-600" />
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-purple-800">
                  ⚡ Auto-Sync Enabled
                </h3>
                <div className="mt-2 text-sm text-purple-700">
                  <p>Your dashboard updates automatically every 5 minutes from Google Sheets.</p>
                  {syncStatus.last_sync_time && (
                    <p className="mt-1">Last sync: {new Date(syncStatus.last_sync_time).toLocaleString()}</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Test Result */}
        {testResult && (
          <div className={`rounded-lg p-4 mb-6 ${
            testResult.success 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-start">
              {testResult.success ? (
                <FiCheck className="text-green-600 mt-0.5 mr-3 flex-shrink-0" size={20} />
              ) : (
                <FiAlertCircle className="text-red-600 mt-0.5 mr-3 flex-shrink-0" size={20} />
              )}
              <div className="flex-1">
                <h3 className={`font-semibold mb-1 ${
                  testResult.success ? 'text-green-900' : 'text-red-900'
                }`}>
                  {testResult.success ? 'Connection Successful!' : 'Connection Failed'}
                </h3>
                <p className={`text-sm ${
                  testResult.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  {testResult.message}
                </p>
                
                {testResult.success && (
                  <div className="mt-3 text-sm text-green-800">
                    <p><strong>Authentication:</strong> {testResult.authMethod || 'Published CSV'}</p>
                    <p><strong>Rows found:</strong> {testResult.rowCount}</p>
                    <p><strong>Columns:</strong> {testResult.columns.join(', ')}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Sync Result */}
        {syncResult && (
          <div className={`rounded-lg p-4 mb-6 ${
            syncResult.success 
              ? 'bg-green-50 border border-green-200' 
              : 'bg-red-50 border border-red-200'
          }`}>
            <div className="flex items-start">
              {syncResult.success ? (
                <FiCheck className="text-green-600 mt-0.5 mr-3 flex-shrink-0" size={20} />
              ) : (
                <FiAlertCircle className="text-red-600 mt-0.5 mr-3 flex-shrink-0" size={20} />
              )}
              <div className="flex-1">
                <h3 className={`font-semibold mb-1 ${
                  syncResult.success ? 'text-green-900' : 'text-red-900'
                }`}>
                  {syncResult.success ? 'Sync Completed!' : 'Sync Failed'}
                </h3>
                <p className={`text-sm ${
                  syncResult.success ? 'text-green-800' : 'text-red-800'
                }`}>
                  {syncResult.message}
                </p>
                
                {syncResult.success && syncResult.stats && (
                  <div className="mt-3 grid grid-cols-2 gap-4 text-sm text-green-800">
                    <div>
                      <strong>Fetched:</strong> {syncResult.stats.fetched}
                    </div>
                    <div>
                      <strong>Created:</strong> {syncResult.stats.created}
                    </div>
                    <div>
                      <strong>Updated:</strong> {syncResult.stats.updated}
                    </div>
                    <div>
                      <strong>Skipped:</strong> {syncResult.stats.skipped}
                    </div>
                    {syncResult.stats.errors.length > 0 && (
                      <div className="col-span-2">
                        <strong>Errors:</strong>
                        <ul className="list-disc list-inside mt-1">
                          {syncResult.stats.errors.slice(0, 5).map((error, idx) => (
                            <li key={idx}>{error}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Info Card */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="font-semibold text-gray-900 mb-3">Expected Columns</h3>
          <p className="text-sm text-gray-600 mb-3">
            Your Google Sheet should have the following columns (flexible naming):
          </p>
          <ul className="grid grid-cols-2 gap-2 text-sm text-gray-700">
            <li>• Control No. / ID / Case No</li>
            <li>• Category / Type</li>
            <li>• Sender's Location / Location</li>
            <li>• Barangay / Brgy</li>
            <li>• Description / Details</li>
            <li>• Date Created / Date</li>
            <li>• Reported by / Reporter</li>
            <li>• Contact Number / Phone</li>
            <li>• Status</li>
            <li>• MyNaga App Status</li>
          </ul>
          <p className="text-sm text-gray-500 mt-3">
            Only <strong>Control No.</strong> is required. Other fields will use default values if missing.
          </p>
        </div>
      </div>
    </div>
  )
}
