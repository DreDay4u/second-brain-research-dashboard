import { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { MarkdownInput } from "@/components/MarkdownInput"
import { A2UIRendererList } from "@/components/A2UIRenderer"
import { LoadingSkeleton } from "@/components/LoadingSkeleton"
import type { A2UIComponent } from "@/lib/a2ui-catalog"
import { FileText, Sparkles, ArrowLeft, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"

type ViewState = 'input' | 'loading' | 'dashboard'

function App() {
  const [dashboardComponents, setDashboardComponents] = useState<A2UIComponent[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  const [viewState, setViewState] = useState<ViewState>('input')
  const [lastMarkdown, setLastMarkdown] = useState<string>('')

  const handleGenerate = useCallback(async (content: string, file?: File) => {
    console.log('Generate dashboard called:', { contentLength: content.length, file })
    setIsGenerating(true)
    setViewState('loading')
    setDashboardComponents([])
    setLastMarkdown(content)

    try {
      // Use VITE_BACKEND_URL env var or default to localhost:8000
      const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'
      console.log('Fetching from', `${backendUrl}/ag-ui/stream`)
      const response = await fetch(`${backendUrl}/ag-ui/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ markdown: content, user_id: 'demo-user' })
      })

      console.log('Response received:', response.status, response.ok)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      if (!response.body) {
        throw new Error('No response body received')
      }

      // Process Server-Sent Events (SSE) stream
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''
      const components: A2UIComponent[] = []

      while (true) {
        const { done, value } = await reader.read()

        if (done) {
          break
        }

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6).trim()

            if (data === '[DONE]') {
              continue
            }

            try {
              const component = JSON.parse(data) as A2UIComponent

              // Skip error components
              if (component.type === 'error') {
                console.error('Error from backend:', component)
                continue
              }

              components.push(component)
              setDashboardComponents([...components])
              console.log('Received component:', component.type, 'Total:', components.length)
            } catch (parseError) {
              console.error('Failed to parse component:', data, parseError)
            }
          }
        }
      }

      console.log(`Dashboard generation complete. Received ${components.length} components.`)

      // Switch to dashboard view when complete
      if (components.length > 0) {
        setViewState('dashboard')
      } else {
        setViewState('input')
        alert('No components were generated. Please try again with different content.')
      }
    } catch (error) {
      console.error('Error generating dashboard:', error)
      setViewState('input')
      alert(`Failed to generate dashboard: ${error instanceof Error ? error.message : 'Unknown error'}`)
    } finally {
      setIsGenerating(false)
    }
  }, [])

  const handleBackToInput = useCallback(() => {
    setViewState('input')
  }, [])

  const handleRegenerate = useCallback(() => {
    if (lastMarkdown) {
      handleGenerate(lastMarkdown)
    }
  }, [lastMarkdown, handleGenerate])

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Compact Header for Dashboard View, Full Header for Input View */}
      <AnimatePresence mode="wait">
        {viewState === 'dashboard' ? (
          <motion.header
            key="compact-header"
            className="sticky top-0 z-50 border-b border-blue-500/20 bg-card/95 backdrop-blur-sm shadow-lg shadow-black/10"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <div className="px-4 py-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleBackToInput}
                    className="gap-2 text-muted-foreground hover:text-foreground"
                  >
                    <ArrowLeft className="h-4 w-4" />
                    Back to Input
                  </Button>
                  <div className="h-6 w-px bg-border" />
                  <div className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-blue-400" />
                    <span className="font-semibold text-sm">Research Dashboard</span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-muted-foreground">
                    {dashboardComponents.length} components
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleRegenerate}
                    className="gap-2"
                  >
                    <RotateCcw className="h-3 w-3" />
                    Regenerate
                  </Button>
                </div>
              </div>
            </div>
            <div className="h-px bg-gradient-to-r from-transparent via-blue-500/50 to-transparent" />
          </motion.header>
        ) : (
          <motion.header
            key="full-header"
            className="border-b border-blue-500/20 bg-gradient-to-r from-card via-card to-secondary/30 shadow-lg shadow-black/20"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
          >
            <div className="px-6 py-4">
              <div className="flex items-center gap-3">
                <motion.div
                  initial={{ rotate: -180, scale: 0 }}
                  animate={{ rotate: 0, scale: 1 }}
                  transition={{ duration: 0.5, ease: "easeOut", delay: 0.2 }}
                  className="relative"
                >
                  <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-xl" />
                  <Sparkles className="h-8 w-8 text-blue-400 relative" />
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, ease: "easeOut", delay: 0.3 }}
                >
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                    Second Brain Research Dashboard
                  </h1>
                  <p className="text-sm text-muted-foreground">
                    Transform your markdown research into interactive, AI-powered dashboards
                  </p>
                </motion.div>
              </div>
            </div>
            <div className="h-px bg-gradient-to-r from-transparent via-blue-500/50 to-transparent" />
          </motion.header>
        )}
      </AnimatePresence>

      {/* Main Content Area */}
      <AnimatePresence mode="wait">
        {/* Input View - Full Screen */}
        {viewState === 'input' && (
          <motion.main
            key="input-view"
            className="min-h-[calc(100vh-5rem)]"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <div className="max-w-4xl mx-auto px-4 py-8">
              <motion.div
                className="mb-6"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.2 }}
              >
                <div className="flex items-center gap-2 mb-2">
                  <FileText className="h-5 w-5 text-blue-400" />
                  <h2 className="text-lg font-semibold text-foreground">Enter Your Research</h2>
                </div>
                <p className="text-sm text-muted-foreground">
                  Paste your markdown research content below or drag and drop a .md file.
                  The AI will analyze your content and generate an interactive dashboard.
                </p>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: 0.3 }}
                className="bg-card rounded-xl border border-border p-6 shadow-xl"
              >
                <MarkdownInput
                  onGenerate={handleGenerate}
                  placeholder="# Your Research Title

## Introduction
Enter your research content here...

## Key Findings
- Finding 1
- Finding 2

## Data & Statistics
- 85% improvement in efficiency
- $2.5M cost savings

## Code Examples
```python
def analyze_data(content):
    return insights
```

## Conclusion
Your conclusions here..."
                  initialValue={lastMarkdown}
                />
              </motion.div>

              {/* Sample document hints */}
              <motion.div
                className="mt-6 text-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.4, delay: 0.5 }}
              >
                <p className="text-xs text-muted-foreground">
                  Tip: Include statistics, code blocks, links, and structured sections for best results
                </p>
              </motion.div>
            </div>
          </motion.main>
        )}

        {/* Loading View - Full Screen */}
        {viewState === 'loading' && (
          <motion.main
            key="loading-view"
            className="min-h-[calc(100vh-5rem)]"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="max-w-6xl mx-auto px-4 py-8">
              <div className="text-center mb-8">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                  className="inline-block"
                >
                  <Sparkles className="h-8 w-8 text-blue-400" />
                </motion.div>
                <h2 className="text-xl font-semibold mt-4">Generating Your Dashboard</h2>
                <p className="text-sm text-muted-foreground mt-2">
                  AI is analyzing your content and creating components...
                </p>
                {dashboardComponents.length > 0 && (
                  <p className="text-sm text-blue-400 mt-2">
                    {dashboardComponents.length} components generated
                  </p>
                )}
              </div>

              {/* Show components as they stream in */}
              {dashboardComponents.length > 0 ? (
                <div className="space-y-6 animate-fade-in">
                  <A2UIRendererList
                    components={dashboardComponents}
                    spacing="lg"
                    showErrors={true}
                  />
                </div>
              ) : (
                <LoadingSkeleton />
              )}
            </div>
          </motion.main>
        )}

        {/* Dashboard View - Full Screen */}
        {viewState === 'dashboard' && (
          <motion.main
            key="dashboard-view"
            className="min-h-[calc(100vh-3rem)]"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4 }}
          >
            <div className="max-w-7xl mx-auto px-4 py-6">
              {/* Dashboard Grid */}
              <div className="space-y-6">
                <A2UIRendererList
                  components={dashboardComponents}
                  spacing="lg"
                  showErrors={true}
                />
              </div>
            </div>
          </motion.main>
        )}
      </AnimatePresence>
    </div>
  )
}

export default App
