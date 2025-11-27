import { User, Bot, Database, FileText, BarChart3 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

function MessageBubble({ message }) {
  const isUser = message.role === 'user'
  
  const getToolIcon = (tool) => {
    switch(tool) {
      case 'sql_agent':
        return <Database className="w-4 h-4" />
      case 'rag_tool':
        return <FileText className="w-4 h-4" />
      case 'dashboard_tool':
        return <BarChart3 className="w-4 h-4" />
      default:
        return null
    }
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex space-x-3 max-w-3xl ${isUser ? 'flex-row-reverse space-x-reverse' : ''}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser ? 'bg-gradient-to-br from-blue-500 to-cyan-500' : 'bg-gradient-to-br from-purple-500 to-pink-500'
        }`}>
          {isUser ? <User className="w-5 h-5" /> : <Bot className="w-5 h-5" />}
        </div>

        {/* Message Content */}
        <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
          <div className={`inline-block p-4 rounded-2xl ${
            isUser 
              ? 'bg-gradient-to-br from-blue-500 to-cyan-500' 
              : 'glass'
          }`}>
            {/* Tool Badge - Skip for visualization tools since chart is in separate panel */}
            {!isUser && message.tool_used && message.tool_used !== 'query_and_visualize' && (
              <div className="flex items-center space-x-1 text-xs text-gray-300 mb-2">
                {getToolIcon(message.tool_used)}
                <span className="capitalize">{message.tool_used.replace('_', ' ')}</span>
              </div>
            )}

            {/* Message Text */}
            <div className="prose prose-invert prose-sm max-w-none">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>

            {/* Chart is displayed in separate panel - no indication needed in chat */}

            {/* Sources */}
            {message.sources && message.sources.length > 0 && (
              <div className="mt-3 space-y-2">
                <p className="text-xs text-gray-300 font-semibold">Sources:</p>
                {message.sources.map((source, idx) => (
                  <div key={idx} className="bg-white/5 rounded-lg p-2 text-xs">
                    <p className="text-gray-400">{source.content}</p>
                    {source.metadata && (
                      <p className="mt-1">
                        <span className="text-blue-400 font-medium">{source.metadata.source}</span>
                        <span className="text-gray-500"> - </span>
                        <span className="text-blue-300">Chunk {source.metadata.chunk + 1}</span>
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Timestamp */}
          <p className="text-xs text-gray-500 mt-1 px-2">
            {new Date(message.timestamp).toLocaleTimeString()}
          </p>
        </div>
      </div>
    </div>
  )
}

export default MessageBubble
