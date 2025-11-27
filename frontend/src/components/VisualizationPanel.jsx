import { useState, useEffect } from 'react'
import { BarChart3, X, ChevronDown } from 'lucide-react'
import ChartRenderer from './ChartRenderer'

const CHART_TYPES = [
  { value: 'bar', label: 'Bar Chart' },
  { value: 'line', label: 'Line Chart' },
  { value: 'area', label: 'Area Chart' },
  { value: 'pie', label: 'Pie Chart' },
  { value: 'scatter', label: 'Scatter Plot' },
]

function VisualizationPanel({ chartConfig, chartData, onClear }) {
  const [selectedChartType, setSelectedChartType] = useState(null)

  // Reset selected chart type when new chart config comes in
  useEffect(() => {
    if (chartConfig) {
      setSelectedChartType(chartConfig.type)
    }
  }, [chartConfig])

  if (!chartConfig || !chartData) {
    return (
      <div className="glass rounded-2xl shadow-2xl p-6 h-full flex flex-col items-center justify-center">
        <BarChart3 className="w-16 h-16 text-gray-400 mb-4" />
        <p className="text-gray-400 text-center">
          No visualization yet.<br />
          Ask me to visualize data!
        </p>
      </div>
    )
  }

  // Create modified config with user-selected chart type
  const modifiedConfig = {
    ...chartConfig,
    type: selectedChartType || chartConfig.type
  }

  return (
    <div className="glass rounded-2xl shadow-2xl p-6 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <BarChart3 className="w-5 h-5 text-purple-400" />
          <h3 className="text-lg font-semibold text-white">Visualization</h3>
        </div>
        <div className="flex items-center space-x-2">
          {/* Chart Type Dropdown */}
          <div className="relative">
            <select
              value={selectedChartType || chartConfig.type}
              onChange={(e) => setSelectedChartType(e.target.value)}
              className="appearance-none bg-white/10 border border-white/20 rounded-lg px-3 py-1.5 pr-8 text-sm text-white focus:outline-none focus:ring-2 focus:ring-purple-500 cursor-pointer hover:bg-white/15 transition-colors"
            >
              {CHART_TYPES.map((type) => (
                <option key={type.value} value={type.value} className="bg-gray-800 text-white">
                  {type.label}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
          <button
            onClick={onClear}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
            title="Clear visualization"
          >
            <X className="w-5 h-5 text-gray-400" />
          </button>
        </div>
      </div>

      {/* Chart */}
      <div className="flex-1 bg-gradient-to-br from-white/5 to-white/10 rounded-xl p-6 overflow-hidden">
        <ChartRenderer chartConfig={modifiedConfig} data={chartData} />
      </div>
    </div>
  )
}

export default VisualizationPanel
