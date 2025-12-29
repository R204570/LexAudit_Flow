import React, { useState } from 'react'
import Dashboard from './components/Dashboard'
import { triggerCrawl } from './api'

function App() {
  const [crawlUrl, setCrawlUrl] = useState('')
  const [crawling, setCrawling] = useState(false)
  const [showCrawlForm, setShowCrawlForm] = useState(false)

  const handleCrawl = async () => {
    if (!crawlUrl.trim()) {
      alert('Please enter a valid URL')
      return
    }

    try {
      setCrawling(true)
      const result = await triggerCrawl(crawlUrl)
      alert(`Crawl completed! Found ${result.downloaded_files.length} documents.`)
      setCrawlUrl('')
      setShowCrawlForm(false)
    } catch (error) {
      console.error('Crawl error:', error)
      alert('Crawl failed. Check console for details.')
    } finally {
      setCrawling(false)
    }
  }

  return (
    <div className="w-full h-screen">
      {/* Crawl Modal */}
      {showCrawlForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-40">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Crawl Website</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Website URL
                </label>
                <input
                  type="url"
                  value={crawlUrl}
                  onChange={(e) => setCrawlUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div className="flex gap-3 pt-4">
                <button
                  onClick={() => {
                    setShowCrawlForm(false)
                    setCrawlUrl('')
                  }}
                  disabled={crawling}
                  className="flex-1 px-4 py-2 bg-gray-300 text-gray-900 rounded-lg hover:bg-gray-400 disabled:bg-gray-200 transition"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCrawl}
                  disabled={crawling}
                  className="flex-1 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 transition font-medium"
                >
                  {crawling ? 'Crawling...' : 'Start Crawl'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Main Dashboard */}
      <Dashboard />
    </div>
  )
}

export default App
