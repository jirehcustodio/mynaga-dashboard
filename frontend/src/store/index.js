import { create } from 'zustand'

export const useCaseStore = create((set) => ({
  cases: [],
  filters: {
    status: null,
    category: null,
    barangay: null,
    search: null,
  },
  
  setCases: (cases) => set({ cases }),
  setCasesWithFilters: (cases, filters) => set({ cases, filters }),
  
  setFilters: (filters) => set((state) => ({
    filters: { ...state.filters, ...filters },
  })),
  
  addCase: (newCase) => set((state) => ({
    cases: [newCase, ...state.cases],
  })),
  
  updateCase: (id, updatedCase) => set((state) => ({
    cases: state.cases.map((c) => (c.id === id ? { ...c, ...updatedCase } : c)),
  })),
  
  deleteCase: (id) => set((state) => ({
    cases: state.cases.filter((c) => c.id !== id),
  })),
}))

export const useOfficeStore = create((set) => ({
  offices: [],
  setOffices: (offices) => set({ offices }),
  addOffice: (office) => set((state) => ({
    offices: [...state.offices, office],
  })),
}))

export const useClusterStore = create((set) => ({
  clusters: [],
  setClusters: (clusters) => set({ clusters }),
  addCluster: (cluster) => set((state) => ({
    clusters: [...state.clusters, cluster],
  })),
  updateCluster: (id, updatedCluster) => set((state) => ({
    clusters: state.clusters.map((c) => (c.id === id ? { ...c, ...updatedCluster } : c)),
  })),
}))

export const useStatsStore = create((set) => ({
  stats: null,
  setStats: (stats) => set({ stats }),
}))

export const useUIStore = create((set) => ({
  selectedCase: null,
  selectedCluster: null,
  isLoading: false,
  error: null,
  
  setSelectedCase: (caseItem) => set({ selectedCase: caseItem }),
  setSelectedCluster: (cluster) => set({ selectedCluster: cluster }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}))
