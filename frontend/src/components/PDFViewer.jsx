import React from 'react';

export const PDFViewer = ({ pdfPath, onAccept, onReject, loading = false }) => {
  if (!pdfPath) {
    return (
      <div className="h-full flex items-center justify-center bg-gray-100 rounded-lg">
        <p className="text-gray-500">Select an update to view evidence</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow">
      {/* PDF Viewer */}
      <div className="flex-1 overflow-hidden bg-gray-100 p-4">
        <iframe
          src={pdfPath}
          className="w-full h-full border-0 rounded"
          title="Evidence PDF"
        />
      </div>

      {/* Action Buttons */}
      <div className="border-t border-gray-200 p-4 flex gap-4 justify-end">
        <button
          onClick={onReject}
          disabled={loading}
          className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:bg-gray-300 transition"
        >
          {loading ? 'Processing...' : 'Reject'}
        </button>
        <button
          onClick={onAccept}
          disabled={loading}
          className="px-6 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:bg-gray-300 transition"
        >
          {loading ? 'Processing...' : 'Accept Update'}
        </button>
      </div>
    </div>
  );
};

export default PDFViewer;
