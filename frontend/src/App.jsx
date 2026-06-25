import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'
import './index.css'

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Aloha! I am Astro-GPT, An AI Assistant for Space Science. How can I help you today?',
      context: null
    }
  ])
  const [input, setInput] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)

  const fileInputRef = useRef(null)
  const chatEndRef = useRef(null)

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setIsUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
      })
      const data = await res.json()
      if (data.status === 'success') {
        alert(`Successfully mapped ${data.chunks} data chunks into the stars!`)
      } else {
        alert('Error: ' + data.message)
      }
    } catch (err) {
      alert('Upload failed: Ensure FastAPI backend is running.')
    }
    setIsUploading(false)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input, context: null }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsTyping(true)

    try {
      // Map existing messages to strict text logs, skipping the generic startup greeting
      const historyItems = messages.slice(1).map(msg => ({ role: msg.role, content: msg.content }))
      
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: input, history: historyItems })
      })
      const data = await res.json()

      if (data.status === 'success') {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.response,
          context: data.context
        }])
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: `Error: ${data.message}` }])
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Connection to Astro-GPT core failed.' }])
    }
    setIsTyping(false)
  }

  return (
    <div className="app-container">
      <div className="stars"></div>

      {/* Sidebar Configurations */}
      <aside className="sidebar">
        <h2>🛠 System Config</h2>

        <div className="config-section">
          <label style={{ display: 'block', marginBottom: '0.5rem', color: 'var(--text-dim)' }}>Knowledge Ingestion</label>
          <div className="upload-box" onClick={() => fileInputRef.current?.click()}>
            {isUploading ? <div className="loader"></div> : <span>📡 Upload Data</span>}
          </div>
          <input
            type="file"
            ref={fileInputRef}
            accept=".pdf,.csv,.pptx,.ppt,.txt"
            style={{ display: 'none' }}
            onChange={handleUpload}
          />
        </div>
      </aside>

      {/* Main Chat Interface */}
      <main className="main-content">
        <header className="header">
          <img src="/Stitch.jpg" alt="Stitch" width="80" height="80" />
          <div className="title-area">
            <h1>Astro-GPT</h1>
            <p>Your beautiful local RAG interface for the stars.</p>
          </div>
        </header>

        <div className="chat-container">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message-row ${msg.role}`}>
              {msg.role === 'assistant' && <img src="/Stitch.jpg" alt="Stitch Avatar" className="bot-avatar" />}
              <div className={`message ${msg.role}`}>
                <ReactMarkdown>{msg.content}</ReactMarkdown>
                {msg.context && msg.context.length > 0 && (
                  <div className="context-box">
                    <strong>📚 Retrieved Context:</strong>
                    <br />- {msg.context[0].substring(0, 150)}...
                  </div>
                )}
              </div>
            </div>
          ))}
          {isTyping && (
             <div className="message-row assistant">
              <img src="/Stitch.jpg" alt="Stitch Avatar" className="bot-avatar" />
              <div className="message assistant">
                <div className="loader"></div>
              </div>
            </div>
          )}
          <div ref={chatEndRef} />
        </div>

        <div className="input-area">
          <form className="chat-form" onSubmit={handleSend}>
            <input
              type="text"
              className="chat-input"
              placeholder="Ask Stitch about the galaxy..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button type="submit" className="send-btn" disabled={isTyping}>
              {isTyping ? '...' : 'Send 🚀'}
            </button>
          </form>
        </div>
      </main>
    </div>
  )
}

export default App
