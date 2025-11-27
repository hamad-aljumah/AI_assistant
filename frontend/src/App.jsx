import { useState, useEffect } from 'react'
import ChatInterface from './components/ChatInterface'
import DocumentPanel from './components/DocumentPanel'
import VisualizationPanel from './components/VisualizationPanel'
import Header from './components/Header'
import { v4 as uuidv4 } from 'uuid'

function App() {
  const [sessionId, setSessionId] = useState('')
  const [showDocuments, setShowDocuments] = useState(false)
  const [currentChartConfig, setCurrentChartConfig] = useState(null)
  const [currentChartData, setCurrentChartData] = useState(null)

  useEffect(() => {
    // Generate session ID on mount
    const id = uuidv4()
    setSessionId(id)
  }, [])

  const handleChartUpdate = (chartConfig, chartData) => {
    setCurrentChartConfig(chartConfig)
    setCurrentChartData(chartData)
  }

  const handleClearChart = () => {
    setCurrentChartConfig(null)
    setCurrentChartData(null)
  }

  return (
    <div className="h-screen flex flex-col overflow-hidden">
      {/* Header */}
      <div className="p-4">
        <div className="max-w-full mx-auto">
          <Header 
            onToggleDocuments={() => setShowDocuments(!showDocuments)}
            showDocuments={showDocuments}
          />
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 flex gap-4 px-4 pb-4 overflow-hidden">
        {/* Left Side - Visualization Panel */}
        <div className="w-[660px] h-[60vh] flex-shrink-0">
          <VisualizationPanel 
            chartConfig={currentChartConfig}
            chartData={currentChartData}
            onClear={handleClearChart}
          />
        </div>

        {/* Right Side - Chat and Documents */}
        <div className="flex-1 flex gap-4 min-w-0 h-full">
          {/* Chat Interface */}
          <div className={showDocuments ? "flex-1 min-w-0 h-full" : "flex-1 h-full"}>
            <ChatInterface 
              sessionId={sessionId}
              onChartUpdate={handleChartUpdate}
            />
          </div>
          
          {/* Document Panel */}
          {showDocuments && (
            <div className="w-[350px] flex-shrink-0">
              <DocumentPanel />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
