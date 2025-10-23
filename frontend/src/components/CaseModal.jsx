import React, { useState, useEffect } from 'react'
import { caseAPI, officeAPI, clusterAPI } from '../services/api'
import { useCaseStore, useOfficeStore, useClusterStore } from '../store'
import { FiX, FiPlus, FiExternalLink, FiCalendar, FiMapPin, FiUser, FiPhone, FiFileText, FiAlertCircle, FiImage, FiVideo, FiMaximize2 } from 'react-icons/fi'

// Media Gallery Component
function MediaGallery({ mediaUrls }) {
  const [selectedMedia, setSelectedMedia] = useState(null)
  const [imageErrors, setImageErrors] = useState({})
  const [showUrlHelp, setShowUrlHelp] = useState(false)
  
  // Parse media URLs - could be comma-separated or newline-separated
  const parseMediaUrls = (urls) => {
    if (!urls) return []
    // Split by comma, newline, or semicolon
    return urls.split(/[,\n;]+/).map(url => url.trim()).filter(url => url.length > 0)
  }
  
  const mediaList = parseMediaUrls(mediaUrls)
  
  // Convert filename to full URL if needed
  const getMediaUrl = (urlOrFilename) => {
    // If already a full URL, return as-is
    if (urlOrFilename.startsWith('http://') || urlOrFilename.startsWith('https://')) {
      return urlOrFilename
    }
    
    // ============================================================================
    // MYNAGA STORAGE CONFIGURATION
    // ============================================================================
    // TODO: Update this to match your actual MyNaga storage location
    // 
    // INSTRUCTIONS TO FIND THE CORRECT URL:
    // 1. Contact MyNaga app developers and ask: "Where are report attachments stored?"
    // 2. Check MyNaga mobile app code for Firebase or storage configuration
    // 3. Open a report in MyNaga website/app, right-click an image, "Copy image address"
    // 4. Check Firebase Console → Storage section
    //
    // COMMON PATTERNS TO TRY:
    
    // Option A: Firebase Storage (MOST COMMON for mobile apps)
    // Uncomment and update with correct bucket name:
    // const FIREBASE_BUCKET = 'mynaga-app.appspot.com'  // or mynagaapp.appspot.com, naga-app.appspot.com
    // const MYNAGA_STORAGE_BASE = `https://firebasestorage.googleapis.com/v0/b/${FIREBASE_BUCKET}/o/`
    // return MYNAGA_STORAGE_BASE + encodeURIComponent(urlOrFilename) + '?alt=media'
    
    // Option B: Direct Server Storage
    // const MYNAGA_STORAGE_BASE = 'https://mynaga.app/api/storage/'
    // return MYNAGA_STORAGE_BASE + urlOrFilename
    
    // Option C: AWS S3 or Google Cloud Storage
    // const MYNAGA_STORAGE_BASE = 'https://mynaga-storage.s3.amazonaws.com/'
    // return MYNAGA_STORAGE_BASE + urlOrFilename
    
    // Current placeholder (will show filenames but not load images)
    const MYNAGA_STORAGE_BASE = 'https://mynaga.app/storage/reports/'
    
    console.log('🔗 Attempting to load media:', MYNAGA_STORAGE_BASE + urlOrFilename)
    console.log('💡 If this fails, update MYNAGA_STORAGE_BASE in CaseModal.jsx')
    return MYNAGA_STORAGE_BASE + urlOrFilename
  }
  
  // Determine if URL is video or image
  const isVideo = (url) => {
    const videoExtensions = ['.mp4', '.webm', '.ogg', '.mov', '.avi', '.m4v']
    const lowerUrl = url.toLowerCase()
    return videoExtensions.some(ext => lowerUrl.includes(ext)) || lowerUrl.includes('video')
  }
  
  // Lightbox Modal for full-screen view
  const Lightbox = ({ media, onClose }) => {
    const [mediaError, setMediaError] = useState(false)
    const filename = media.split('/').pop()
    const isVideoFile = isVideo(media)
    
    return (
      <div 
        className="fixed inset-0 z-[100] bg-black bg-opacity-90 flex items-center justify-center p-4"
        onClick={onClose}
      >
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 text-white hover:text-gray-300 z-[101]"
        >
          <FiX size={32} />
        </button>
        <div className="max-w-6xl max-h-full" onClick={(e) => e.stopPropagation()}>
          {mediaError ? (
            <div className="bg-gray-800 rounded-lg p-8 text-center max-w-2xl">
              <FiAlertCircle className="text-yellow-400 mx-auto mb-4" size={48} />
              <h3 className="text-white text-xl font-bold mb-4">Media Not Available</h3>
              <p className="text-gray-300 mb-4">The media file couldn't be loaded from the current storage URL.</p>
              <div className="bg-gray-900 rounded p-4 mb-4 text-left">
                <p className="text-gray-400 text-sm mb-2">File: <span className="text-white">{filename}</span></p>
                <p className="text-gray-400 text-sm mb-2">Attempted URL:</p>
                <p className="text-xs text-gray-500 font-mono break-all">{media}</p>
              </div>
              <p className="text-sm text-gray-400 mb-4">
                To fix this, update the <code className="bg-gray-700 px-2 py-1 rounded">MYNAGA_STORAGE_BASE</code> URL in CaseModal.jsx
              </p>
              <button 
                onClick={onClose}
                className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              >
                Close
              </button>
            </div>
          ) : (
            <>
              {isVideoFile ? (
                <video 
                  src={media} 
                  controls 
                  autoPlay
                  className="max-w-full max-h-[90vh] rounded-lg"
                  onError={() => {
                    console.error('❌ Failed to load video:', media)
                    setMediaError(true)
                  }}
                />
              ) : (
                <img 
                  src={media} 
                  alt="Full size" 
                  className="max-w-full max-h-[90vh] rounded-lg object-contain"
                  onError={() => {
                    console.error('❌ Failed to load image:', media)
                    setMediaError(true)
                  }}
                />
              )}
            </>
          )}
        </div>
      </div>
    )
  }
  
  if (mediaList.length === 0) return null
  
  // Check if any images failed to load
  const hasErrors = Object.keys(imageErrors).length > 0
  
  return (
    <>
      <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 px-6 py-3 border-b border-gray-200">
          <div className="flex items-center gap-2 justify-between">
            <div className="flex items-center gap-2">
              <FiImage className="text-purple-600" size={20} />
              <h3 className="text-lg font-semibold text-gray-900">Attached Media</h3>
              <span className="ml-2 text-sm text-gray-600">({mediaList.length} {mediaList.length === 1 ? 'file' : 'files'})</span>
            </div>
            {hasErrors && (
              <button 
                onClick={() => setShowUrlHelp(!showUrlHelp)}
                className="text-xs text-purple-600 hover:text-purple-800 underline"
              >
                {showUrlHelp ? 'Hide Help' : 'Images not loading?'}
              </button>
            )}
          </div>
        </div>
        
        {showUrlHelp && hasErrors && (
          <div className="bg-amber-50 border-b border-amber-200 px-6 py-4">
            <div className="flex gap-3">
              <FiAlertCircle className="text-amber-600 mt-0.5 flex-shrink-0" size={20} />
              <div className="text-sm text-gray-700">
                <p className="font-semibold text-amber-900 mb-2">Configuration Needed: Update Storage URL</p>
                <p className="mb-2">The media files are stored in the MyNaga app's storage, but we need the correct URL.</p>
                <p className="mb-2">To fix this, update the <code className="bg-amber-100 px-1 py-0.5 rounded text-xs">MYNAGA_STORAGE_BASE</code> URL in:</p>
                <p className="font-mono text-xs bg-white p-2 rounded border border-amber-200 mb-2">
                  frontend/src/components/CaseModal.jsx (line ~36)
                </p>
                <p className="text-xs text-gray-600">Check the browser console (F12) to see the URLs being attempted.</p>
              </div>
            </div>
          </div>
        )}
        
        <div className="p-6">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {mediaList.map((urlOrFilename, index) => {
              const fullUrl = getMediaUrl(urlOrFilename)
              const isVideoFile = isVideo(urlOrFilename)
              const filename = urlOrFilename.split('/').pop()
              
              return (
                <div 
                  key={index}
                  className="relative group cursor-pointer rounded-lg overflow-hidden border-2 border-gray-200 hover:border-purple-400 transition-all shadow-sm hover:shadow-md"
                  onClick={() => setSelectedMedia(fullUrl)}
                >
                  {isVideoFile ? (
                    <div className="relative aspect-video bg-gray-900">
                      {imageErrors[index] ? (
                        <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900 p-4">
                          <FiVideo className="text-gray-400 mb-2" size={32} />
                          <p className="text-xs text-gray-300 text-center font-medium mb-1">📹 Video File</p>
                          <p className="text-xs text-gray-400 text-center truncate w-full px-2">{filename}</p>
                          <p className="text-[10px] text-gray-500 mt-2 text-center">Click for details</p>
                        </div>
                      ) : (
                        <>
                          <video 
                            src={fullUrl} 
                            className="w-full h-full object-cover"
                            preload="metadata"
                            onError={(e) => {
                              setImageErrors(prev => ({...prev, [index]: true}))
                              e.target.style.display = 'none'
                            }}
                          />
                          <div className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center group-hover:bg-opacity-30 transition-all">
                            <FiVideo className="text-white" size={32} />
                          </div>
                        </>
                      )}
                    </div>
                  ) : (
                    <div className="relative aspect-video bg-gray-100">
                      {imageErrors[index] ? (
                        <div className="w-full h-full flex flex-col items-center justify-center bg-gradient-to-br from-purple-100 to-pink-100 p-4">
                          <FiImage className="text-purple-300 mb-2" size={32} />
                          <p className="text-xs text-gray-600 text-center font-medium mb-1">📎 Image File</p>
                          <p className="text-xs text-gray-500 text-center truncate w-full px-2">{filename}</p>
                          <p className="text-[10px] text-gray-400 mt-2 text-center">Click for details</p>
                        </div>
                      ) : (
                        <>
                          <img 
                            src={fullUrl} 
                            alt={`Media ${index + 1}`}
                            className="w-full h-full object-cover"
                            onError={(e) => {
                              console.warn('❌ Failed to load image:', fullUrl)
                              setImageErrors(prev => ({...prev, [index]: true}))
                              e.target.style.display = 'none'
                            }}
                          />
                          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all">
                            <FiMaximize2 className="text-white drop-shadow-lg" size={24} />
                          </div>
                        </>
                      )}
                    </div>
                  )}
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black via-black/70 to-transparent p-2">
                    <p className="text-white text-xs font-medium truncate">
                      {isVideoFile ? '📹 Video' : '🖼️ Image'} {index + 1}
                    </p>
                    <p className="text-white/80 text-[10px] truncate">{filename}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
      
      {/* Lightbox */}
      {selectedMedia && (
        <Lightbox media={selectedMedia} onClose={() => setSelectedMedia(null)} />
      )}
    </>
  )
}

export default function CaseModal({ isOpen, onClose, caseData }) {
  const [formData, setFormData] = useState(caseData || {})
  const [offices, setOffices] = useState([])
  const [clusters, setClusters] = useState([])
  const [viewMode, setViewMode] = useState('view') // 'view' or 'edit'
  const [mynagaLink, setMynagaLink] = useState(null)
  const [loadingLink, setLoadingLink] = useState(false)
  const updateCase = useCaseStore((state) => state.updateCase)
  const addCase = useCaseStore((state) => state.addCase)

  useEffect(() => {
    if (isOpen) {
      loadOfficesAndClusters()
      // If creating new case, start in edit mode
      setViewMode(caseData?.id ? 'view' : 'edit')
      // Pre-populate form data with case data
      if (caseData) {
        setFormData(caseData)
      }
      // Fetch MyNaga link
      if (caseData?.control_no) {
        fetchMynagaLink(caseData.control_no)
      }
    }
  }, [isOpen, caseData])

  const fetchMynagaLink = async (control_no) => {
    setLoadingLink(true)
    try {
      const response = await fetch(`http://localhost:8000/api/mynaga/report-link/${control_no}`)
      const data = await response.json()
      
      if (data.success && data.link) {
        setMynagaLink(data.link)
        console.log('✅ Fetched MyNaga link:', data.link)
      } else {
        console.log('ℹ️ No MyNaga link found for:', control_no)
        setMynagaLink(null)
      }
    } catch (error) {
      console.error('❌ Error fetching MyNaga link:', error)
      setMynagaLink(null)
    } finally {
      setLoadingLink(false)
    }
  }

  const loadOfficesAndClusters = async () => {
    try {
      const [officeRes, clusterRes] = await Promise.all([
        officeAPI.getAll(),
        clusterAPI.getAll(),
      ])
      setOffices(officeRes.data)
      setClusters(clusterRes.data)
    } catch (error) {
      console.error('Error loading data:', error)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      if (caseData?.id) {
        const res = await caseAPI.update(caseData.id, formData)
        updateCase(caseData.id, res.data)
      } else {
        const res = await caseAPI.create(formData)
        addCase(res.data)
      }
      onClose()
    } catch (error) {
      console.error('Error saving case:', error)
      alert('Error saving case: ' + error.response?.data?.detail || error.message)
    }
  }

  if (!isOpen) return null

  // Format date for display
  const formatDate = (dateString) => {
    if (!dateString) return '--'
    const date = new Date(dateString)
    return date.toLocaleString('en-US', {
      month: '2-digit',
      day: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })
  }

  // Get status badge color
  const getStatusColor = (status) => {
    const colors = {
      'In Progress': 'bg-blue-100 text-blue-800 border-blue-300',
      'Pending Confirmation': 'bg-amber-100 text-amber-800 border-amber-300',
      'Resolved': 'bg-green-100 text-green-800 border-green-300',
      'No Status Yet': 'bg-gray-100 text-gray-800 border-gray-300',
      'Under Review': 'bg-indigo-100 text-indigo-800 border-indigo-300',
      'Rejected': 'bg-red-100 text-red-800 border-red-300'
    }
    return colors[status] || 'bg-gray-100 text-gray-800 border-gray-300'
  }

  // View Mode - Display detailed information
  if (viewMode === 'view' && caseData?.id) {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
        <div className="w-full max-w-4xl mx-auto bg-white rounded-lg shadow-2xl max-h-[90vh] overflow-y-auto">
          {/* Header */}
          <div className="sticky top-0 bg-gradient-to-r from-blue-700 to-blue-800 text-white p-6 border-b border-blue-900">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold">Case Details</h2>
                <p className="text-blue-100 text-sm mt-1">Control No: {caseData.control_no}</p>
              </div>
              <button
                onClick={onClose}
                className="text-white hover:bg-blue-600 rounded-full p-2 transition-colors"
              >
                <FiX size={24} />
              </button>
            </div>
          </div>

          <div className="p-6 space-y-6">
            {/* MyNaga App Status Banner */}
            {caseData.mynaga_app_status && (
              <div className="bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-1">
                      MyNaga App Status
                    </h3>
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold border ${getStatusColor(caseData.mynaga_app_status)}`}>
                      {caseData.mynaga_app_status}
                    </span>
                  </div>
                  {/* View in MyNaga App Button - Dynamically fetched link */}
                  {mynagaLink && (
                    <a
                      href={mynagaLink}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors text-sm font-medium shadow-sm hover:shadow-md"
                      title={`View ${caseData.control_no} in MyNaga App`}
                      onClick={(e) => {
                        console.log('🔗 Opening MyNaga report:', e.currentTarget.href)
                        console.log('📋 Control No:', caseData.control_no)
                        console.log('🎯 Dynamically fetched link!')
                      }}
                    >
                      <FiExternalLink />
                      View in MyNaga App
                    </a>
                  )}
                  {loadingLink && (
                    <div className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-600 rounded text-sm">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600"></div>
                      Loading MyNaga link...
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Attached Media Section */}
            {caseData.attached_media && caseData.attached_media.trim() !== '' && (
              <MediaGallery mediaUrls={caseData.attached_media} />
            )}

            {/* Reported Information Section */}
            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <div className="bg-gray-50 px-6 py-3 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Reported Information</h3>
              </div>
              
              <div className="p-6 space-y-4">
                {/* Created Date */}
                <div className="flex items-start gap-3">
                  <FiCalendar className="text-gray-400 mt-1" size={20} />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-500">Created</div>
                    <div className="text-base text-gray-900">{formatDate(caseData.date_created)}</div>
                  </div>
                </div>

                {/* Location */}
                <div className="flex items-start gap-3">
                  <FiMapPin className="text-gray-400 mt-1" size={20} />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-500">Location</div>
                    <div className="text-base text-gray-900">{caseData.sender_location || '--'}</div>
                  </div>
                </div>

                {/* Barangay */}
                <div className="flex items-start gap-3">
                  <FiMapPin className="text-gray-400 mt-1" size={20} />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-500">Barangay</div>
                    <div className="text-base text-gray-900">{caseData.barangay || '--'}</div>
                  </div>
                </div>

                {/* Cluster */}
                {caseData.cluster && (
                  <div className="flex items-start gap-3">
                    <FiMapPin className="text-gray-400 mt-1" size={20} />
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-500">Cluster</div>
                      <div className="text-base text-gray-900 font-medium">{caseData.cluster}</div>
                    </div>
                  </div>
                )}

                {/* Office */}
                {caseData.office && (
                  <div className="flex items-start gap-3">
                    <FiFileText className="text-gray-400 mt-1" size={20} />
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-500">Assigned Office</div>
                      <div className="text-base text-gray-900 font-medium">{caseData.office}</div>
                    </div>
                  </div>
                )}

                {/* Priority - You can add this field if needed */}
                <div className="flex items-start gap-3">
                  <FiAlertCircle className="text-gray-400 mt-1" size={20} />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-500">Priority</div>
                    <div className="text-base text-gray-900">--</div>
                  </div>
                </div>

                {/* Submitted by */}
                <div className="flex items-start gap-3">
                  <FiUser className="text-gray-400 mt-1" size={20} />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-500">Submitted by</div>
                    <div className="text-base text-gray-900">{caseData.reported_by || '--'}</div>
                  </div>
                </div>

                {/* Contact Number */}
                <div className="flex items-start gap-3">
                  <FiPhone className="text-gray-400 mt-1" size={20} />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-500">Contact Number</div>
                    <div className="text-base text-gray-900">{caseData.contact_number || '--'}</div>
                  </div>
                </div>

                {/* Category */}
                <div className="flex items-start gap-3">
                  <FiFileText className="text-gray-400 mt-1" size={20} />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-500">Category</div>
                    <div className="text-base text-gray-900">{caseData.category || '--'}</div>
                  </div>
                </div>

                {/* Description */}
                <div className="flex items-start gap-3">
                  <FiFileText className="text-gray-400 mt-1" size={20} />
                  <div className="flex-1">
                    <div className="text-sm font-medium text-gray-500">Description</div>
                    <div className="text-base text-gray-900 whitespace-pre-wrap leading-relaxed">
                      {caseData.description || '--'}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Additional Information Section */}
            <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
              <div className="bg-gray-50 px-6 py-3 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900">Additional Information</h3>
              </div>
              
              <div className="p-6 grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm font-medium text-gray-500">Status</div>
                  <div className="text-base text-gray-900 mt-1">
                    <span className={`badge badge-${caseData.status?.toLowerCase() || 'open'}`}>
                      {caseData.status || 'OPEN'}
                    </span>
                  </div>
                </div>

                <div>
                  <div className="text-sm font-medium text-gray-500">Case Aging</div>
                  <div className="text-base text-gray-900 mt-1">{caseData.case_aging || '--'} days</div>
                </div>

                <div>
                  <div className="text-sm font-medium text-gray-500">Month</div>
                  <div className="text-base text-gray-900 mt-1">{caseData.month || '--'}</div>
                </div>

                <div>
                  <div className="text-sm font-medium text-gray-500">Refined Category</div>
                  <div className="text-base text-gray-900 mt-1">{caseData.refined_category || '--'}</div>
                </div>

                {caseData.screened_by && (
                  <div>
                    <div className="text-sm font-medium text-gray-500">Screened By</div>
                    <div className="text-base text-gray-900 mt-1">{caseData.screened_by}</div>
                  </div>
                )}

                {caseData.last_status_update_datetime && (
                  <div>
                    <div className="text-sm font-medium text-gray-500">Last Update</div>
                    <div className="text-base text-gray-900 mt-1">{formatDate(caseData.last_status_update_datetime)}</div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Auto-Response Message Section */}
          {caseData.updates_sent_to_user_new && (
            <div className="mx-6 mb-6">
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <div className="flex items-start gap-3 mb-3">
                  <FiFileText className="text-blue-600 mt-1" size={20} />
                  <div>
                    <h3 className="text-lg font-semibold text-blue-900">Updates Sent to User</h3>
                    <p className="text-sm text-blue-700 mt-1">Auto-response message generated based on office assignment</p>
                  </div>
                </div>
                <div className="bg-white rounded border border-blue-200 p-4 mt-3">
                  <div className="text-sm text-gray-800 whitespace-pre-wrap leading-relaxed">
                    {caseData.updates_sent_to_user_new}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Footer Actions */}
          <div className="sticky bottom-0 bg-gray-50 px-6 py-4 border-t border-gray-200 flex justify-between items-center">
            <button
              onClick={() => {
                setFormData(caseData) // Refresh form data with current case data
                setViewMode('edit')
              }}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors font-medium"
            >
              Edit Case
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition-colors font-medium"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    )
  }

  // Edit Mode - Original form for editing
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div className="w-full max-w-2xl mx-auto bg-white rounded-lg shadow-lg max-h-screen overflow-y-auto">
        <div className="sticky top-0 flex items-center justify-between p-6 border-b">
          <h2 className="text-xl font-bold">
            {caseData?.id ? 'Edit Case' : 'New Case'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <FiX size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Control No. *
              </label>
              <input
                type="text"
                name="control_no"
                value={formData.control_no || ''}
                onChange={handleInputChange}
                className="input"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category *
              </label>
              <input
                type="text"
                name="category"
                value={formData.category || ''}
                onChange={handleInputChange}
                className="input"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Barangay
              </label>
              <input
                type="text"
                name="barangay"
                value={formData.barangay || ''}
                onChange={handleInputChange}
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Cluster
              </label>
              <input
                type="text"
                name="cluster"
                value={formData.cluster || ''}
                onChange={handleInputChange}
                className="input"
                placeholder="e.g., Cluster A"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Office
              </label>
              <select
                name="office"
                value={formData.office || ''}
                onChange={handleInputChange}
                className="input"
              >
                <option value="">Select Office</option>
                <option value="PSO">PSO - Public Safety Office</option>
                <option value="GSO">GSO - General Services Office</option>
                <option value="CEO">CEO - CMO Special Unit for Engineering</option>
                <option value="SWMO">SWMO - Solid Waste Management Office</option>
                <option value="CENRO">CENRO - City Environment and Natural Resources Office</option>
                <option value="CVO">CVO - City Veterinary Office</option>
                <option value="CSWD">CSWD - City Social Welfare and Development</option>
                <option value="NCGH">NCGH - Naga City General Hospital</option>
                <option value="CHO">CHO - City Health Office</option>
                <option value="CPRFMO">CPRFMO - City Parks & Recreational Facilities Management</option>
                <option value="CTO">CTO - City Treasurer's Office</option>
                <option value="MEPO">MEPO - Market Enterprise and Promotions Office</option>
                <option value="HSDO">HSDO - Housing and Development Office</option>
                <option value="BCS">BCS - Bicol Central Station</option>
                <option value="CPDO">CPDO - City Planning and Development Office</option>
                <option value="SP-SEC">SP-SEC - Sangguniang Panlunsod Secretariat</option>
                <option value="CEPPIO">CEPPIO - City Events, Protocol & Public Information</option>
                <option value="MNWD">MNWD - Metro Naga Water District</option>
                <option value="CASURECO">CASURECO</option>
                <option value="DOLE">DOLE</option>
                <option value="PSA">PSA - Philippine Statistics Authority</option>
                <option value="DTI">DTI</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                MyNaga App Status
              </label>
              <select
                name="mynaga_app_status"
                value={formData.mynaga_app_status || ''}
                onChange={handleInputChange}
                className="input"
              >
                <option value="">Select Status</option>
                <option value="In Progress">In Progress</option>
                <option value="Pending Confirmation">Pending Confirmation</option>
                <option value="Pending Review">Pending Review</option>
                <option value="Under Review">Under Review</option>
                <option value="Resolved">Resolved</option>
                <option value="Rejected - Out of Scope">Rejected - Out of Scope</option>
                <option value="Rejected - Unclear Report">Rejected - Unclear Report</option>
                <option value="Rejected - Test">Rejected - Test</option>
                <option value="Rejected">Rejected</option>
                <option value="Withdrawn">Withdrawn</option>
                <option value="No Status Yet">No Status Yet</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                name="status"
                value={formData.status || 'OPEN'}
                onChange={handleInputChange}
                className="input"
              >
                <option value="OPEN">OPEN</option>
                <option value="RESOLVED">RESOLVED</option>
                <option value="FOR REROUTING">FOR REROUTING</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Sender's Location
            </label>
            <input
              type="text"
              name="sender_location"
              value={formData.sender_location || ''}
              onChange={handleInputChange}
              className="input"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description || ''}
              onChange={handleInputChange}
              rows="4"
              className="input"
            ></textarea>
          </div>

          {formData.updates_sent_to_user_new && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Updates Sent to User (Auto-Response)
              </label>
              <textarea
                name="updates_sent_to_user_new"
                value={formData.updates_sent_to_user_new || ''}
                readOnly
                rows="6"
                className="input bg-gray-50 text-gray-600 cursor-not-allowed"
                placeholder="Auto-response message will appear here after office assignment..."
              ></textarea>
              <p className="text-xs text-gray-500 mt-1">
                This message is automatically generated based on the assigned office
              </p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Reported by
              </label>
              <input
                type="text"
                name="reported_by"
                value={formData.reported_by || ''}
                onChange={handleInputChange}
                className="input"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Contact Number
              </label>
              <input
                type="tel"
                name="contact_number"
                value={formData.contact_number || ''}
                onChange={handleInputChange}
                className="input"
              />
            </div>
          </div>

          <div className="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              onClick={() => {
                if (caseData?.id) {
                  setViewMode('view')
                } else {
                  onClose()
                }
              }}
              className="btn btn-secondary"
            >
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              {caseData?.id ? 'Update' : 'Create'} Case
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
