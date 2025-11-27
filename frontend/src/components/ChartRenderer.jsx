import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, ScatterChart, Scatter,
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, Cell
} from 'recharts'

// Modern color palette
const COLORS = [
  '#8b5cf6', // Purple
  '#ec4899', // Pink
  '#06b6d4', // Cyan
  '#10b981', // Green
  '#f59e0b', // Amber
  '#ef4444', // Red
  '#6366f1', // Indigo
  '#14b8a6', // Teal
]

// Custom tooltip styling
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-gray-900/95 backdrop-blur-sm border border-purple-500/30 rounded-lg p-3 shadow-xl">
        <p className="text-white font-semibold mb-2">{label}</p>
        {payload.map((entry, index) => (
          <p key={index} className="text-sm" style={{ color: entry.color }}>
            {entry.name}: {typeof entry.value === 'number' ? entry.value.toLocaleString() : entry.value}
          </p>
        ))}
      </div>
    )
  }
  return null
}

function ChartRenderer({ chartConfig, data }) {
  if (!chartConfig || !data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-400">
        <p>No data to display</p>
      </div>
    )
  }

  const { type, x_axis, y_axis, title } = chartConfig

  // Common chart props
  const commonProps = {
    data: data,
    margin: { top: 20, right: 30, left: 20, bottom: 20 }
  }

  const renderChart = () => {
    switch (type) {
      case 'bar':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey={x_axis} 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
                tickFormatter={(value) => value.toLocaleString()}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ color: '#e5e7eb', fontSize: '13px' }}
              />
              <Bar 
                dataKey={y_axis} 
                fill={COLORS[0]}
                radius={[8, 8, 0, 0]}
                animationDuration={800}
              />
            </BarChart>
          </ResponsiveContainer>
        )

      case 'line':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <LineChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey={x_axis} 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
                tickFormatter={(value) => value.toLocaleString()}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ color: '#e5e7eb', fontSize: '13px' }}
              />
              <Line 
                type="monotone"
                dataKey={y_axis} 
                stroke={COLORS[0]}
                strokeWidth={3}
                dot={{ fill: COLORS[0], r: 5 }}
                activeDot={{ r: 7 }}
                animationDuration={800}
              />
            </LineChart>
          </ResponsiveContainer>
        )

      case 'area':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart {...commonProps}>
              <defs>
                <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={COLORS[0]} stopOpacity={0.8}/>
                  <stop offset="95%" stopColor={COLORS[0]} stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey={x_axis} 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
                tickFormatter={(value) => value.toLocaleString()}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ color: '#e5e7eb', fontSize: '13px' }}
              />
              <Area 
                type="monotone"
                dataKey={y_axis} 
                stroke={COLORS[0]}
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorGradient)"
                animationDuration={800}
              />
            </AreaChart>
          </ResponsiveContainer>
        )

      case 'pie':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                dataKey={y_axis}
                nameKey={x_axis}
                cx="50%"
                cy="50%"
                outerRadius={120}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                labelLine={{ stroke: '#d1d5db' }}
                animationDuration={800}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ color: '#e5e7eb', fontSize: '13px' }}
              />
            </PieChart>
          </ResponsiveContainer>
        )

      case 'scatter':
        return (
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey={x_axis} 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
                type="number"
              />
              <YAxis 
                dataKey={y_axis}
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
                tickFormatter={(value) => value.toLocaleString()}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
              <Legend 
                wrapperStyle={{ color: '#e5e7eb', fontSize: '13px' }}
              />
              <Scatter 
                name={y_axis}
                data={data}
                fill={COLORS[0]}
                animationDuration={800}
              />
            </ScatterChart>
          </ResponsiveContainer>
        )

      default:
        return (
          <ResponsiveContainer width="100%" height="100%">
            <BarChart {...commonProps}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis 
                dataKey={x_axis} 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
              />
              <YAxis 
                stroke="#d1d5db"
                style={{ fontSize: '12px' }}
                tickFormatter={(value) => value.toLocaleString()}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend 
                wrapperStyle={{ color: '#e5e7eb', fontSize: '13px' }}
              />
              <Bar 
                dataKey={y_axis} 
                fill={COLORS[0]}
                radius={[8, 8, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        )
    }
  }

  return (
    <div className="w-full h-full flex flex-col">
      {/* Chart Title */}
      {title && (
        <h3 className="text-lg font-semibold text-white text-center mb-4">
          {title}
        </h3>
      )}
      
      {/* Chart */}
      <div className="flex-1 min-h-0">
        {renderChart()}
      </div>
    </div>
  )
}

export default ChartRenderer
