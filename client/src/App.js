import React, { useState, useEffect } from "react"
import "./App.css"

const DOMAIN = "http://localhost:5000"

function App() {
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchReport()
  }, [])

  const fetchReport = () => {
    fetch(`${DOMAIN}/report/latest`)
      .then((res) => res.json())
      .then((data) => setReport(data))
      .catch((error) => setError(error))
  }

  if (error) {
    return <div className="text-red-500">Error: {error.message}</div>
  }

  if (!report) {
    return <div className="text-gray-500">Loading...</div>
  }

  return (
    <div className="bg-gray-100 min-h-screen p-8">
      <h1 className="text-4xl font-extrabold mb-8 text-center text-gray-900">
        {report.metadata.report_title}
      </h1>
      <div className="mb-8 p-6 bg-white rounded-lg shadow-md">
        <p className="text-xl">
          Overall Sentiment:{" "}
          <span className="font-semibold">
            {report.metadata.overall_sentiment}
          </span>
        </p>
        <p className="text-lg text-gray-700">
          {report.metadata.sentiment_description}
        </p>
      </div>

      <div className="mb-8 p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-3xl font-bold mt-6 mb-4">Themes</h2>
        <ul className="list-disc list-inside pl-4">
          {report.themes.map((theme, index) => (
            <li key={index} className="mb-2">
              <strong className="text-lg">{theme.name}:</strong>{" "}
              {theme.description}
            </li>
          ))}
        </ul>
      </div>

      <div className="mb-8 p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-3xl font-bold mt-6 mb-4">Issues</h2>
        <ul className="list-disc list-inside pl-4">
          {report.issues.map((issue, index) => (
            <li key={index} className="mb-2">
              <strong className="text-lg">{issue.name}:</strong>{" "}
              {issue.description}
            </li>
          ))}
        </ul>
      </div>

      <div className="p-6 bg-white rounded-lg shadow-md">
        <h2 className="text-3xl font-bold mt-6 mb-4">Insights</h2>
        <ul className="list-disc list-inside pl-4">
          {report.insights.map((insight, index) => (
            <li key={index} className="mb-4">
              <strong className="text-lg">Recommendation {insight.id}:</strong>{" "}
              {insight.recommendation}
              <br />
              <strong className="text-lg">Reason:</strong> {insight.reason}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default App
