import { useState, useEffect } from 'react'
import { Upload, File, Trash2, Loader2 } from 'lucide-react'
import axios from 'axios'

function DocumentPanel() {
  const [documents, setDocuments] = useState([])
  const [uploading, setUploading] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDocuments()
  }, [])

  const fetchDocuments = async () => {
    try {
      const response = await axios.get('/api/documents')
      setDocuments(response.data)
    } catch (error) {
      console.error('Error fetching documents:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)

    setUploading(true)
    try {
      await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      fetchDocuments()
    } catch (error) {
      console.error('Error uploading file:', error)
      alert('Error uploading file')
    } finally {
      setUploading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this document?')) return

    try {
      await axios.delete(`/api/documents/${id}`)
      fetchDocuments()
    } catch (error) {
      console.error('Error deleting document:', error)
    }
  }

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
  }

  return (
    <div className="glass rounded-2xl shadow-2xl p-6 h-[calc(100vh-200px)] flex flex-col">
      <h2 className="text-xl font-bold mb-4">Document Library</h2>

      {/* Upload Area */}
      <label className="glass glass-hover border-2 border-dashed border-white/20 rounded-xl p-6 cursor-pointer flex flex-col items-center space-y-2 mb-4">
        <input
          type="file"
          onChange={handleFileUpload}
          accept=".pdf,.docx,.txt,.md"
          className="hidden"
          disabled={uploading}
        />
        {uploading ? (
          <Loader2 className="w-8 h-8 animate-spin text-purple-400" />
        ) : (
          <Upload className="w-8 h-8 text-purple-400" />
        )}
        <span className="text-sm text-gray-300">
          {uploading ? 'Uploading...' : 'Click to upload'}
        </span>
        <span className="text-xs text-gray-500">PDF, DOCX, TXT, MD</span>
      </label>

      {/* Documents List */}
      <div className="flex-1 overflow-y-auto space-y-2">
        {loading ? (
          <div className="flex justify-center items-center h-full">
            <Loader2 className="w-6 h-6 animate-spin text-purple-400" />
          </div>
        ) : documents.length === 0 ? (
          <p className="text-center text-gray-400 mt-8">No documents uploaded</p>
        ) : (
          documents.map((doc) => (
            <div
              key={doc.id}
              className="glass glass-hover rounded-xl p-3 flex items-center justify-between"
            >
              <div className="flex items-center space-x-3 flex-1 min-w-0">
                <File className="w-5 h-5 text-purple-400 flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">
                    {doc.original_filename}
                  </p>
                  <p className="text-xs text-gray-400">
                    {formatFileSize(doc.file_size)} • {doc.chunk_count} chunks
                  </p>
                </div>
              </div>
              <button
                onClick={() => handleDelete(doc.id)}
                className="text-red-400 hover:text-red-300 p-2 rounded-lg hover:bg-red-500/10 transition-colors"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default DocumentPanel
