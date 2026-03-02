import { useState, useEffect } from 'react'
import api from './api'

// Helper function to get proper datetime-local format
function getDefaultTimestamp() {
  const now = new Date()
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
  return now.toISOString().slice(0, 16) // Format: YYYY-MM-DDTHH:mm
}

export default function WorkerEvents() {
  const [workers, setWorkers] = useState([])
  const [workstations, setWorkstations] = useState([])
  
  const [formData, setFormData] = useState({
    worker_id: '',
    station_id: '',
    event_type: 'working',
    count: 0,
    notes: '',
    timestamp: getDefaultTimestamp()
  })
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [messageType, setMessageType] = useState('')
  const [events, setEvents] = useState([])
  const [loadingEvents, setLoadingEvents] = useState(true)

  // Fetch workers, workstations, and events on mount
  useEffect(() => {
    fetchWorkers()
    fetchWorkstations()
    fetchEvents()
  }, [])

  const fetchWorkers = async () => {
    try {
      const response = await api.get('/workers')
      setWorkers(response.data.workers || [])
    } catch (error) {
      console.error("Error fetching workers:", error)
    }
  }

  const fetchWorkstations = async () => {
    try {
      const response = await api.get('/workstations')
      setWorkstations(response.data.workstations || [])
    } catch (error) {
      console.error("Error fetching workstations:", error)
    }
  }

  const fetchEvents = async () => {
    try {
      setLoadingEvents(true)
      const response = await api.get('/events')
      setEvents(response.data.events || [])
    } catch (error) {
      console.error("Error fetching events:", error)
    } finally {
      setLoadingEvents(false)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name === 'count' ? (value === '' ? 0 : parseInt(value)) : value
    }))
  }

  const handleDateTimeChange = (e) => {
    const { value } = e.target
    setFormData(prev => ({
      ...prev,
      timestamp: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const payload = {
        timestamp: new Date(formData.timestamp).toISOString(),
        worker_id: parseInt(formData.worker_id),
        station_id: parseInt(formData.station_id),
        event_type: formData.event_type,
        confidence: 0.95,
        count: formData.event_type === 'product_count' ? parseInt(formData.count) || 0 : 0,
        notes: formData.notes
      }

      console.log("📤 Posting AI event:", payload)
      
      const response = await api.post('/events', payload, {
        headers: {
          'Content-Type': 'application/json',
        }
      })
      
      console.log("✅ Response:", response.data)
      
      if (response.data.success) {
        setMessageType('success')
        setMessage(`✓ ${response.data.message}`)
        setFormData({
          worker_id: '',
          station_id: '',
          event_type: 'working',
          count: 0,
          notes: '',
          timestamp: getDefaultTimestamp()
        })
        // Refresh events list after posting
        fetchEvents()
      }
    } catch (error) {
      console.error("❌ Error posting event:", error)
      setMessageType('error')
      const errorMsg = error.response?.data?.message || error.response?.statusText || error.message || "Unknown error"
      setMessage(`✗ Error: ${errorMsg}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-2xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-extrabold text-slate-900">AI Event Ingestion</h1>
          <p className="text-slate-500 text-sm mt-1">Record events from AI/CCTV monitoring system</p>
        </header>

        <div className="bg-white rounded-xl shadow-sm p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Timestamp */}
            <div>
              <label htmlFor="timestamp" className="block text-sm font-bold text-slate-700 mb-2">
                Timestamp *
              </label>
              <input
                type="datetime-local"
                id="timestamp"
                value={formData.timestamp}
                onChange={handleDateTimeChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Worker ID */}
            <div>
              <label htmlFor="worker_id" className="block text-sm font-bold text-slate-700 mb-2">
                Worker *
              </label>
              <select
                id="worker_id"
                name="worker_id"
                value={formData.worker_id}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a worker...</option>
                {workers.map(w => (
                  <option key={w.worker_id} value={w.worker_id}>
                    {w.name} (Worker {w.worker_id})
                  </option>
                ))}
              </select>
            </div>

            {/* Station ID */}
            <div>
              <label htmlFor="station_id" className="block text-sm font-bold text-slate-700 mb-2">
                Workstation *
              </label>
              <select
                id="station_id"
                name="station_id"
                value={formData.station_id}
                onChange={handleInputChange}
                required
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Select a workstation...</option>
                {workstations.map(s => (
                  <option key={s.station_id} value={s.station_id}>
                    {s.name} (Station {s.station_id})
                  </option>
                ))}
              </select>
            </div>

            {/* Event Type */}
            <div>
              <label htmlFor="event_type" className="block text-sm font-bold text-slate-700 mb-2">
                Event Type *
              </label>
              <select
                id="event_type"
                name="event_type"
                value={formData.event_type}
                onChange={handleInputChange}
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="working">Working</option>
                <option value="idle">Idle</option>
                <option value="absent">Absent</option>
                <option value="product_count">Product Count</option>
              </select>
            </div>

            {/* Product Count (conditional) */}
            {formData.event_type === 'product_count' && (
              <div>
                <label htmlFor="count" className="block text-sm font-bold text-slate-700 mb-2">
                  Number of Units Produced *
                </label>
                <input
                  type="number"
                  id="count"
                  name="count"
                  value={formData.count}
                  onChange={handleInputChange}
                  required={formData.event_type === 'product_count'}
                  min="0"
                  step="1"
                  className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., 5, 10, 25..."
                />
              </div>
            )}

            {/* Notes */}
            <div>
              <label htmlFor="notes" className="block text-sm font-bold text-slate-700 mb-2">
                Notes
              </label>
              <textarea
                id="notes"
                name="notes"
                value={formData.notes}
                onChange={handleInputChange}
                rows="3"
                className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Additional context or observations..."
              />
            </div>

            {/* Message */}
            {message && (
              <div className={`p-4 rounded-lg ${
                messageType === 'success' 
                  ? 'bg-green-50 text-green-800 border border-green-200' 
                  : 'bg-red-50 text-red-800 border border-red-200'
              }`}>
                {message}
              </div>
            )}

            {/* Submit Button */}
            <div className="flex gap-4 pt-4">
              <button
                type="submit"
                disabled={loading}
                className={`${
                  loading 
                    ? 'bg-blue-300' 
                    : 'bg-blue-600 hover:bg-blue-700'
                } text-white font-bold py-2 px-6 rounded-lg transition-all shadow-md flex-1`}
              >
                {loading ? 'Posting...' : 'Record Event'}
              </button>
              <button
                type="reset"
                onClick={() => setFormData({
                  worker_id: '',
                  station_id: '',
                  event_type: 'working',
                  count: 0,
                  notes: '',
                  timestamp: getDefaultTimestamp()
                })}
                className="bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold py-2 px-6 rounded-lg transition-all"
              >
                Clear
              </button>
            </div>
          </form>
        </div>

        {/* Posted Events Section */}
        <div className="mt-8">
          <h2 className="text-2xl font-bold text-slate-900 mb-4">Event Log</h2>
          
          {loadingEvents ? (
            <div className="text-center py-8 text-slate-500">
              Loading events...
            </div>
          ) : events.length === 0 ? (
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-8 text-center text-slate-500">
              No AI events recorded yet
            </div>
          ) : (
            <div className="space-y-3">
              {events.slice().reverse().map((event, index) => (
                <div key={index} className="bg-white border border-slate-200 rounded-lg p-4 hover:shadow-md transition">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="font-bold text-slate-900">Worker {event.worker_id}</span>
                        <span className="text-slate-600">→</span>
                        <span className="font-bold text-slate-900">Station {event.station_id}</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                          event.event_type === 'working' ? 'bg-green-100 text-green-800' :
                          event.event_type === 'idle' ? 'bg-yellow-100 text-yellow-800' :
                          event.event_type === 'absent' ? 'bg-red-100 text-red-800' :
                          'bg-blue-100 text-blue-800'
                        }`}>
                          {event.event_type}
                        </span>
                      </div>
                      {event.count > 0 && (
                        <p className="text-sm text-slate-600 mb-1">
                          <strong>Count:</strong> {event.count} units
                        </p>
                      )}
                      {event.notes && (
                        <p className="text-sm text-slate-600">
                          <strong>Notes:</strong> {event.notes}
                        </p>
                      )}
                      <p className="text-xs text-slate-500 mt-1">
                        <strong>Confidence:</strong> {(event.confidence * 100).toFixed(0)}%
                      </p>
                    </div>
                    <div className="text-xs text-slate-400 ml-4 text-right">
                      {new Date(event.timestamp).toLocaleString()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Help Section */}
        <div className="mt-8 bg-blue-50 border-l-4 border-blue-500 p-6 rounded">
          <h3 className="font-bold text-blue-900 mb-2">Event Types</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li><strong>Working:</strong> Worker actively performing tasks</li>
            <li><strong>Idle:</strong> Worker idle or waiting (not performing productive work)</li>
            <li><strong>Absent:</strong> Worker not present at workstation</li>
            <li><strong>Product Count:</strong> Count of units produced at this event</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
