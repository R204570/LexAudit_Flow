import React, { useState, useEffect } from 'react';
import { AlertCircle, CheckCircle, XCircle, Loader } from 'lucide-react';
import { getPendingUpdates, acceptUpdate, getEvidenceFile } from '../api';
import PDFViewer from './PDFViewer';
import NotificationBadge from './NotificationBadge';

export const Dashboard = () => {
  const [updates, setUpdates] = useState([]);
  const [selectedUpdate, setSelectedUpdate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [notificationCount, setNotificationCount] = useState(0);

  // Fetch updates on component mount
  useEffect(() => {
    fetchUpdates();
    
    // Set up polling every 30 seconds
    const interval = setInterval(fetchUpdates, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchUpdates = async () => {
    try {
      setLoading(true);
      const data = await getPendingUpdates();
      setUpdates(data);
      setNotificationCount(data.length);
      
      // Auto-select first update if none selected
      if (data.length > 0 && !selectedUpdate) {
        setSelectedUpdate(data[0]);
      }
    } catch (error) {
      console.error('Failed to fetch updates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAccept = async () => {
    if (!selectedUpdate) return;
    
    try {
      setProcessing(true);
      await acceptUpdate(selectedUpdate.id, true);
      
      // Remove from list
      setUpdates(updates.filter(u => u.id !== selectedUpdate.id));
      setSelectedUpdate(null);
      
      // Refresh updates
      await fetchUpdates();
    } catch (error) {
      console.error('Failed to accept update:', error);
      alert('Failed to accept update. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  const handleReject = async () => {
    if (!selectedUpdate) return;
    
    try {
      setProcessing(true);
      await acceptUpdate(selectedUpdate.id, false);
      
      // Remove from list
      setUpdates(updates.filter(u => u.id !== selectedUpdate.id));
      setSelectedUpdate(null);
      
      // Refresh updates
      await fetchUpdates();
    } catch (error) {
      console.error('Failed to reject update:', error);
      alert('Failed to reject update. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  const handleSelectUpdate = (update) => {
    setSelectedUpdate(update);
  };

  return (
    <div className="w-full h-screen flex flex-col bg-gray-50">
      <NotificationBadge count={notificationCount} />
      
      {/* Header */}
      <div className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <h1 className="text-3xl font-bold text-gray-900">LexAudit Flow</h1>
        <p className="text-gray-600 mt-1">Tax Compliance Intelligence System</p>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden p-6 gap-6">
        {/* Left Panel - Updates List */}
        <div className="w-96 bg-white rounded-lg shadow overflow-hidden flex flex-col">
          <div className="bg-gray-100 px-4 py-3 border-b border-gray-200">
            <h2 className="font-semibold text-gray-900">Tax Change Alerts</h2>
            <p className="text-sm text-gray-600">{updates.length} pending</p>
          </div>

          {/* Updates List */}
          <div className="flex-1 overflow-y-auto">
            {loading && updates.length === 0 ? (
              <div className="flex items-center justify-center h-full">
                <Loader className="animate-spin text-blue-500" />
              </div>
            ) : updates.length === 0 ? (
              <div className="flex items-center justify-center h-full text-gray-500">
                <p>No pending updates</p>
              </div>
            ) : (
              <div className="divide-y divide-gray-200">
                {updates.map((update) => (
                  <div
                    key={update.id}
                    onClick={() => handleSelectUpdate(update)}
                    className={`p-4 cursor-pointer hover:bg-gray-50 transition border-l-4 ${
                      selectedUpdate?.id === update.id
                        ? 'bg-blue-50 border-l-blue-500'
                        : 'border-l-gray-200'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <AlertCircle className="text-orange-500 flex-shrink-0 mt-1" size={20} />
                      <div className="flex-1">
                        <p className="font-semibold text-gray-900">{update.detected_item}</p>
                        <div className="mt-2 text-sm space-y-1">
                          <p className="text-gray-600">
                            Old: <span className="line-through">{update.current_db_val}%</span>
                          </p>
                          <p className="text-green-600 font-semibold">
                            New: {update.new_web_val}%
                          </p>
                        </div>
                        <p className="text-xs text-gray-500 mt-2">
                          {new Date(update.created_at).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Refresh Button */}
          <div className="border-t border-gray-200 p-4">
            <button
              onClick={fetchUpdates}
              disabled={loading}
              className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 transition font-medium"
            >
              {loading ? 'Refreshing...' : 'Refresh Updates'}
            </button>
          </div>
        </div>

        {/* Right Panel - PDF Viewer */}
        <div className="flex-1 flex flex-col">
          {selectedUpdate ? (
            <>
              <div className="bg-white rounded-lg shadow p-4 mb-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Evidence for: {selectedUpdate.detected_item}
                </h3>
                <div className="grid grid-cols-3 gap-4 text-sm">
                  <div>
                    <p className="text-gray-600">Current Rate</p>
                    <p className="text-xl font-bold text-gray-900">
                      {selectedUpdate.current_db_val}%
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-600">Proposed Rate</p>
                    <p className="text-xl font-bold text-green-600">
                      {selectedUpdate.new_web_val}%
                    </p>
                  </div>
                  <div>
                    <p className="text-gray-600">Change</p>
                    <p className="text-xl font-bold text-blue-600">
                      {(selectedUpdate.new_web_val - selectedUpdate.current_db_val).toFixed(1)}%
                    </p>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <p className="text-sm text-gray-600">Quote from document:</p>
                  <p className="mt-2 p-3 bg-yellow-50 border-l-4 border-yellow-400 text-gray-800 italic">
                    "{selectedUpdate.evidence_quote}"
                  </p>
                </div>
              </div>

              <PDFViewer
                pdfPath={selectedUpdate.evidence_pdf_path}
                onAccept={handleAccept}
                onReject={handleReject}
                loading={processing}
              />
            </>
          ) : (
            <div className="bg-white rounded-lg shadow flex items-center justify-center h-full">
              <p className="text-gray-500 text-lg">Select an update to view evidence</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
