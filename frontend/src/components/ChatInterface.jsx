import { useState, useRef, useEffect } from 'react'
import { Send, Loader2 } from 'lucide-react'
import axios from 'axios'
import MessageBubble from './MessageBubble'

function ChatInterface({ sessionId, onChartUpdate }) {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('/api/chat', {
        message: input,
        session_id: sessionId
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.data.message,
        data: response.data.data,
        chart_config: response.data.chart_config,
        chart_data: response.data.chart_data,
        sources: response.data.sources,
        tool_used: response.data.tool_used,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, assistantMessage])
      
      // Update chart in parent component if chart config and data exist
      if (response.data.chart_config && response.data.chart_data && onChartUpdate) {
        onChartUpdate(response.data.chart_config, response.data.chart_data)
      }
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
        error: true
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass rounded-2xl shadow-2xl flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20">
            <p className="text-xl mb-2">👋 Welcome!</p>
            <p>Ask me about sales data, upload documents, or request visualizations.</p>
          </div>
        )}
        
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}
        
        {loading && (
          <div className="flex items-center space-x-2 text-gray-400">
            <Loader2 className="w-5 h-5 animate-spin" />
            <span>Thinking...</span>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <form onSubmit={sendMessage} className="p-4 border-t border-white/10">
        <div className="flex space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything..."
            className="flex-1 bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-purple-500 text-white placeholder-gray-400"
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-xl flex items-center space-x-2 transition-all"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </form>
    </div>
  )
}

export default ChatInterface
