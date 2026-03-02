import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  // Function to fetch metrics from the FastAPI backend
  const fetchMetrics = () => {
    setRefreshing(true)
    // Adding ?t= ensures the browser doesn't show "old" cached data
    axios.get(`http://127.0.0.1:8000/metrics/?t=${Date.now()}`)
      .then(response => {
        setData(response.data)
        setLoading(false)
        setRefreshing(false)
      })
      .catch(error => {
        console.error("Error fetching data:", error)
        setRefreshing(false)
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchMetrics()
    // Auto-refresh every 10 seconds to keep the dashboard live
    const interval = setInterval(fetchMetrics, 10000) 
    return () => clearInterval(interval)
  }, [])

  // 1. Loading State: Prevents crashing before data arrives
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-xl font-bold text-blue-600 animate-pulse">Connecting to Factory API...</div>
      </div>
    )
  }

  // 2. Error State: Shows a message if the backend is off instead of a blank screen
  if (!data || !data.factory || !data.workers) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 text-center p-6">
        <h2 className="text-2xl font-bold text-red-600 mb-2">Data Unavailable</h2>
        <p className="text-gray-600 mb-4">Check if your FastAPI server is running at http://127.0.0.1:8000</p>
        <button onClick={fetchMetrics} className="bg-blue-600 text-white px-6 py-2 rounded shadow">Retry Connection</button>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <header className="mb-8 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900">Worker Productivity Dashboard</h1>
          <p className="text-slate-500 text-sm">Real-time MLOps Factory Monitoring</p>
        </div>
        <button 
          onClick={fetchMetrics} 
          disabled={refreshing}
          className={`${refreshing ? 'bg-blue-300' : 'bg-blue-600 hover:bg-blue-700'} text-white font-bold py-2 px-6 rounded-lg transition-all shadow-md`}
        >
          {refreshing ? 'Refreshing...' : 'Refresh Data'}
        </button>
      </header>

      {/* Factory Summary Section */}
      <section className="mb-10">
        <h2 className="text-xl font-semibold mb-4 text-slate-700">Factory Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border-l-4 border-blue-500">
            <p className="text-xs font-bold text-slate-400 uppercase">Total Productive Time</p>
            <p className="text-3xl font-black text-slate-800">{data.factory.total_productive_time} <span className="text-lg font-normal">sec</span></p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border-l-4 border-green-500">
            <p className="text-xs font-bold text-slate-400 uppercase">Total Units Produced</p>
            <p className="text-3xl font-black text-slate-800">{data.factory.total_production_count}</p>
          </div>
        </div>
      </section>

      {/* Individual Worker Cards */}
      <section>
        <h2 className="text-xl font-semibold mb-4 text-slate-700">Worker Metrics</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.workers.map((worker) => (
            <div key={worker.worker_id} className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow">
              <h3 className="text-lg font-bold text-slate-800 mb-4 border-b pb-2">Worker {worker.worker_id}</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-slate-500">Active Time:</span>
                  <span className="font-bold">{worker.active_time}s</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Units Produced:</span>
                  <span className="font-bold">{worker.units_produced}</span>
                </div>
                <div className="mt-4 pt-4 border-t">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs font-bold text-slate-500 uppercase">Utilization:</span>
                    <span className={`text-lg font-black ${worker.utilization > 50 ? 'text-green-600' : 'text-slate-400'}`}>
                      {worker.utilization}%
                    </span>
                  </div>
                  {/* Progress Bar Visualization */}
                  <div className="w-full bg-slate-100 rounded-full h-2.5">
                    <div 
                      className="bg-blue-600 h-2.5 rounded-full transition-all duration-1000" 
                      style={{ width: `${worker.utilization}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default App