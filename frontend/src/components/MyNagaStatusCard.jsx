import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const MyNagaStatusCard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    'In Progress': 0,
    'No Status Yet': 0,
    'Pending Confirmation': 0,
    'Rejected': 0,
    'Resolved': 0,
    'Under Review': 0,
    'total': 0
  });
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [selectedStatus, setSelectedStatus] = useState(null);

  const fetchStats = async () => {
    try {
      setIsRefreshing(true);
      const response = await api.get('/mynaga-stats');
      setStats(response.data);
      setLastUpdated(new Date());
      setLoading(false);
      setTimeout(() => setIsRefreshing(false), 500);
    } catch (error) {
      console.error('Error fetching MyNaga stats:', error);
      setLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    fetchStats();
    
    // Auto-refresh every 10 seconds (10000 milliseconds)
    const interval = setInterval(fetchStats, 10000);
    
    return () => clearInterval(interval);
  }, []);

  // Handle status card click - navigate to cases with filter
  const handleStatusClick = (statusName) => {
    navigate(`/cases?mynaga_status=${encodeURIComponent(statusName)}`);
  };

  const statusItems = [
    {
      name: 'In Progress',
      count: stats['In Progress'],
      color: 'bg-blue-600',
      borderColor: 'border-blue-600',
      textColor: 'text-blue-700',
      bgLight: 'bg-blue-50',
      icon: '●',
      description: 'Cases currently being processed'
    },
    {
      name: 'Pending Confirmation',
      count: stats['Pending Confirmation'],
      color: 'bg-amber-600',
      borderColor: 'border-amber-600',
      textColor: 'text-amber-700',
      bgLight: 'bg-amber-50',
      icon: '●',
      description: 'Awaiting stakeholder confirmation'
    },
    {
      name: 'Resolved',
      count: stats['Resolved'],
      color: 'bg-green-600',
      borderColor: 'border-green-600',
      textColor: 'text-green-700',
      bgLight: 'bg-green-50',
      icon: '●',
      description: 'Successfully completed cases'
    },
    {
      name: 'No Status Yet',
      count: stats['No Status Yet'],
      color: 'bg-slate-600',
      borderColor: 'border-slate-600',
      textColor: 'text-slate-700',
      bgLight: 'bg-slate-50',
      icon: '●',
      description: 'Cases awaiting initial review'
    },
    {
      name: 'Under Review',
      count: stats['Under Review'],
      color: 'bg-indigo-600',
      borderColor: 'border-indigo-600',
      textColor: 'text-indigo-700',
      bgLight: 'bg-indigo-50',
      icon: '●',
      description: 'Cases under investigation'
    },
    {
      name: 'Rejected',
      count: stats['Rejected'],
      color: 'bg-red-600',
      borderColor: 'border-red-600',
      textColor: 'text-red-700',
      bgLight: 'bg-red-50',
      icon: '●',
      description: 'Cases that were declined'
    }
  ];

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="space-y-3">
            <div className="h-8 bg-gray-200 rounded"></div>
            <div className="h-8 bg-gray-200 rounded"></div>
            <div className="h-8 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-8 border border-gray-200">
      {/* Header */}
      <div className="flex justify-between items-center mb-8 pb-6 border-b border-gray-200">
        <div>
          <h2 className="text-2xl font-semibold text-gray-900 tracking-tight">
            MyNaga App Status
          </h2>
          <p className="text-sm text-gray-600 mt-1">Real-time Case Management System</p>
        </div>
        <div className="flex flex-col items-end gap-3">
          {lastUpdated && (
            <div className="flex items-center gap-2 text-xs text-gray-600 bg-gray-50 px-4 py-2 rounded border border-gray-200">
              <span className={`inline-block w-1.5 h-1.5 rounded-full ${isRefreshing ? 'bg-green-600' : 'bg-gray-400'}`}></span>
              <span className="font-medium">Updated: {lastUpdated.toLocaleTimeString()}</span>
            </div>
          )}
          <button
            onClick={fetchStats}
            disabled={isRefreshing}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed border border-blue-700"
          >
            <svg 
              className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {isRefreshing ? 'Updating...' : 'Refresh Data'}
          </button>
        </div>
      </div>

      {/* Total Count Card */}
      <div className="mb-8 p-6 bg-gradient-to-r from-blue-700 to-blue-800 rounded border border-blue-900 shadow-sm">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-xs font-semibold text-blue-200 uppercase tracking-wider mb-1">
              Total Cases
            </div>
            <div className="text-4xl font-bold text-white mb-1">
              {stats.total.toLocaleString()}
            </div>
            <div className="text-xs text-blue-200">
              Cumulative Records
            </div>
          </div>
          <div className="text-5xl text-blue-600 opacity-20">
            <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
              <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd"/>
            </svg>
          </div>
        </div>
      </div>

      {/* Status Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {statusItems.map((item, index) => (
          <button
            key={item.name}
            onClick={() => handleStatusClick(item.name)}
            className={`
              relative text-left
              border-2 rounded p-5 cursor-pointer
              transform transition-all duration-200
              hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0
              ${selectedStatus === item.name 
                ? `${item.borderColor} shadow-md` 
                : 'border-gray-200 hover:border-gray-300'
              }
            `}
            style={{
              animation: `fadeInUp 0.4s ease-out ${index * 0.08}s both`
            }}
          >
            {/* Status Indicator */}
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <span className={`text-2xl ${item.textColor}`}>{item.icon}</span>
                <div>
                  <div className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-0.5">
                    {item.name}
                  </div>
                  <div className="text-sm text-gray-600">
                    {item.description}
                  </div>
                </div>
              </div>
            </div>
            
            {/* Count Display */}
            <div className="mb-3">
              <div className="text-3xl font-bold text-gray-900">
                {item.count.toLocaleString()}
              </div>
            </div>
            
            {/* Progress Bar */}
            <div className="w-full bg-gray-100 rounded-full h-1.5 mb-3">
              <div 
                className={`h-1.5 rounded-full ${item.color} transition-all duration-500`}
                style={{ width: stats.total > 0 ? `${(item.count / stats.total) * 100}%` : '0%' }}
              ></div>
            </div>
            
            {/* Statistics */}
            <div className="flex justify-between items-center">
              <span className="text-xs text-gray-500 font-medium">
                {stats.total > 0 
                  ? `${((item.count / stats.total) * 100).toFixed(1)}% of total`
                  : '0.0% of total'
                }
              </span>
              <span className={`text-xs font-semibold px-2.5 py-1 rounded ${item.bgLight} ${item.textColor}`}>
                {item.count}
              </span>
            </div>

            {/* Click Indicator */}
            <div className="absolute top-3 right-3 text-gray-400 text-xs opacity-0 group-hover:opacity-100 transition-opacity">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </button>
        ))}
      </div>

      {/* Footer Info */}
      <div className="mt-8 pt-6 border-t border-gray-200">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-3 text-gray-600">
            <div className="flex items-center gap-2">
              <div className={`w-1.5 h-1.5 rounded-full ${isRefreshing ? 'bg-green-600' : 'bg-blue-600'}`}></div>
              <span className="font-medium">Auto-refresh interval: 10 seconds</span>
            </div>
          </div>
          <div className="flex items-center gap-2 text-gray-500 bg-gray-50 px-3 py-1.5 rounded border border-gray-200">
            <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd"/>
            </svg>
            <span className="font-medium">Secure Live Connection</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MyNagaStatusCard;
