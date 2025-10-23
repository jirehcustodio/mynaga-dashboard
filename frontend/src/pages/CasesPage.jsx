import React, { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { FiDownload, FiUpload, FiPlus, FiSearch } from 'react-icons/fi'
import { caseAPI, fileAPI } from '../services/api'
import { useCaseStore } from '../store'
import CaseModal from '../components/CaseModal'
import CaseTable from '../components/CaseTable'

export default function CasesPage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const cases = useCaseStore((state) => state.cases)
  const setCases = useCaseStore((state) => state.setCases)
  const filters = useCaseStore((state) => state.filters)
  const setFilters = useCaseStore((state) => state.setFilters)

  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedCase, setSelectedCase] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [mynagaStatusFilter, setMynagaStatusFilter] = useState('')

  useEffect(() => {
    // Check if there's a mynaga_status filter from URL
    const statusFromUrl = searchParams.get('mynaga_status')
    if (statusFromUrl) {
      setMynagaStatusFilter(statusFromUrl)
    }
  }, [searchParams])

  useEffect(() => {
    loadCases()
  }, [filters, mynagaStatusFilter])

  const loadCases = async () => {
    setIsLoading(true)
    try {
      // Request all cases (10000 limit - effectively no limit for most use cases)
      const res = await caseAPI.getAll(0, 10000, {
        status: filters.status,
        category: filters.category,
        barangay: filters.barangay,
        search: filters.search,
      })
      
      // Filter by MyNaga status if specified
      let filteredCases = res.data
      if (mynagaStatusFilter) {
        filteredCases = res.data.filter(c => c.mynaga_app_status === mynagaStatusFilter)
      }
      
      setCases(filteredCases)
    } catch (error) {
      console.error('Error loading cases:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSearch = (e) => {
    const value = e.target.value
    setSearchTerm(value)
    setFilters({ search: value })
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setIsLoading(true)
    try {
      const res = await fileAPI.importExcel(file)
      alert(`Successfully imported ${res.data.imported_count} cases`)
      if (res.data.errors.length > 0) {
        alert('Errors:\n' + res.data.errors.join('\n'))
      }
      loadCases()
    } catch (error) {
      console.error('Error importing file:', error)
      alert('Error importing file: ' + error.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="container py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Cases</h1>
          {mynagaStatusFilter && (
            <div className="mt-2 inline-flex items-center gap-2 px-3 py-1 bg-blue-50 border border-blue-200 rounded text-sm">
              <span className="font-medium text-blue-700">Filtered by MyNaga Status:</span>
              <span className="font-semibold text-blue-900">{mynagaStatusFilter}</span>
              <button
                onClick={() => {
                  setMynagaStatusFilter('')
                  setSearchParams({})
                }}
                className="ml-2 text-blue-600 hover:text-blue-800 font-bold"
              >
                ✕
              </button>
            </div>
          )}
        </div>
        <div className="flex space-x-3">
          <label className="btn btn-secondary cursor-pointer">
            <FiUpload className="mr-2" /> Import Excel
            <input
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
          <button
            onClick={() => {
              setSelectedCase(null)
              setIsModalOpen(true)
            }}
            className="btn btn-primary"
          >
            <FiPlus className="mr-2" /> New Case
          </button>
        </div>
      </div>

      <div className="card mb-6">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <FiSearch className="absolute left-3 top-3 text-gray-400" />
            <input
              type="text"
              placeholder="Search cases..."
              value={searchTerm}
              onChange={handleSearch}
              className="input pl-10"
            />
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-12">
          <p className="text-gray-500">Loading cases...</p>
        </div>
      ) : cases.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No cases found</p>
        </div>
      ) : (
        <CaseTable
          cases={cases}
          onEdit={(caseItem) => {
            setSelectedCase(caseItem)
            setIsModalOpen(true)
          }}
        />
      )}

      <CaseModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false)
          setSelectedCase(null)
        }}
        caseData={selectedCase}
      />
    </div>
  )
}
