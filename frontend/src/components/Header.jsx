import { Brain, FileText } from 'lucide-react'

function Header({ onToggleDocuments, showDocuments }) {
  return (
    <div className="glass rounded-2xl p-6 shadow-2xl">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="bg-gradient-to-br from-purple-500 to-pink-500 p-3 rounded-xl">
            <Brain className="w-8 h-8 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
              AI Assistant
            </h1>
            <p className="text-gray-300 text-sm">
              Powered by GPT-4 with SQL, RAG & Visualization
            </p>
          </div>
        </div>
        
        <button
          onClick={onToggleDocuments}
          className={`glass glass-hover px-4 py-2 rounded-xl flex items-center space-x-2 ${
            showDocuments ? 'bg-purple-500/30' : ''
          }`}
        >
          <FileText className="w-5 h-5" />
          <span>Documents</span>
        </button>
      </div>
    </div>
  )
}

export default Header
