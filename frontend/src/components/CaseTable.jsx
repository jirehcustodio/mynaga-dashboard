import React from 'react'
import { FiEdit2, FiTrash2, FiEye } from 'react-icons/fi'
import { caseAPI } from '../services/api'
import { useCaseStore } from '../store'

export default function CaseTable({ cases, onEdit }) {
  const deleteCase = useCaseStore((state) => state.deleteCase)

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this case?')) return

    try {
      await caseAPI.delete(id)
      deleteCase(id)
    } catch (error) {
      console.error('Error deleting case:', error)
      alert('Error deleting case')
    }
  }

  const getStatusBadge = (status) => {
    const classes = {
      OPEN: 'bg-blue-100 text-blue-800',
      RESOLVED: 'bg-green-100 text-green-800',
      'FOR REROUTING': 'bg-yellow-100 text-yellow-800',
    }
    return classes[status] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
      {/* Spreadsheet Container with Fixed Header */}
      <div className="overflow-auto" style={{ maxHeight: '70vh' }}>
        <table className="w-full border-collapse">
          {/* Fixed Header */}
          <thead className="bg-gray-50 sticky top-0 z-10">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Control No.
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Date Created
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Category
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Barangay
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Location
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Description
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Reported By
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Contact
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                Status
              </th>
              <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 border-r border-gray-200">
                MyNaga Status
              </th>
              <th className="px-4 py-3 text-center text-xs font-semibold text-gray-700 uppercase tracking-wider border-b-2 border-gray-300 sticky right-0 bg-gray-50">
                Actions
              </th>
            </tr>
          </thead>
          
          {/* Spreadsheet Body */}
          <tbody className="bg-white divide-y divide-gray-200">
            {cases.length === 0 ? (
              <tr>
                <td colSpan="11" className="px-4 py-8 text-center text-gray-500">
                  No cases found. Import an Excel file or sync from MyNaga to get started.
                </td>
              </tr>
            ) : (
              cases.map((caseItem, idx) => (
                <tr 
                  key={caseItem.id} 
                  className={`hover:bg-blue-50 ${idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}`}
                >
                  <td className="px-4 py-3 text-sm font-medium text-gray-900 border-r border-gray-200 whitespace-nowrap">
                    {caseItem.control_no}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700 border-r border-gray-200 whitespace-nowrap">
                    {caseItem.date_created ? new Date(caseItem.date_created).toLocaleDateString() : '-'}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700 border-r border-gray-200">
                    {caseItem.category || '-'}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700 border-r border-gray-200">
                    {caseItem.barangay || '-'}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700 border-r border-gray-200 max-w-xs truncate" title={caseItem.sender_location}>
                    {caseItem.sender_location || '-'}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700 border-r border-gray-200 max-w-md truncate" title={caseItem.description}>
                    {caseItem.description || '-'}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700 border-r border-gray-200">
                    {caseItem.reported_by || '-'}
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700 border-r border-gray-200 whitespace-nowrap">
                    {caseItem.contact_number || '-'}
                  </td>
                  <td className="px-4 py-3 text-sm border-r border-gray-200">
                    <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusBadge(caseItem.status)}`}>
                      {caseItem.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-gray-700 border-r border-gray-200">
                    {caseItem.mynaga_app_status || '-'}
                  </td>
                  <td className="px-4 py-3 text-sm sticky right-0 bg-inherit">
                    <div className="flex justify-center space-x-2">
                      <button
                        onClick={() => onEdit(caseItem)}
                        className="p-1.5 text-blue-600 hover:bg-blue-100 rounded-md transition-colors"
                        title="Edit"
                      >
                        <FiEdit2 size={16} />
                      </button>
                      <button
                        onClick={() => handleDelete(caseItem.id)}
                        className="p-1.5 text-red-600 hover:bg-red-100 rounded-md transition-colors"
                        title="Delete"
                      >
                        <FiTrash2 size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      
      {/* Footer with row count */}
      <div className="bg-gray-50 px-4 py-3 border-t border-gray-300 text-sm text-gray-600">
        Showing {cases.length} {cases.length === 1 ? 'case' : 'cases'}
      </div>
    </div>
  )
}
