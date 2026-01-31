import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Upload } from "lucide-react"

interface MarkdownInputProps {
  onGenerate?: (content: string, file?: File) => void
  placeholder?: string
  className?: string
}

export function MarkdownInput({
  onGenerate,
  placeholder = "Enter your markdown content or drag and drop a file...",
  className
}: MarkdownInputProps) {
  const [content, setContent] = React.useState("")
  const [isDragging, setIsDragging] = React.useState(false)
  const [uploadedFile, setUploadedFile] = React.useState<File | null>(null)
  const fileInputRef = React.useRef<HTMLInputElement>(null)

  // Calculate character and word count
  const charCount = content.length
  const wordCount = content.trim() === "" ? 0 : content.trim().split(/\s+/).length

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      const file = files[0]
      setUploadedFile(file)

      // Read file content if it's a text/markdown file
      if (file.type.startsWith('text/') || file.name.endsWith('.md')) {
        const text = await file.text()
        setContent(text)
      }
    }
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      const file = files[0]
      setUploadedFile(file)

      // Read file content if it's a text/markdown file
      if (file.type.startsWith('text/') || file.name.endsWith('.md')) {
        const text = await file.text()
        setContent(text)
      }
    }
  }

  const handleGenerate = () => {
    if (onGenerate) {
      onGenerate(content, uploadedFile || undefined)
    }
  }

  return (
    <div className={cn("w-full space-y-4", className)}>
      <div
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          "relative rounded-lg border-2 border-dashed transition-colors",
          isDragging
            ? "border-primary bg-primary/5"
            : "border-muted-foreground/25 bg-background"
        )}
      >
        <div className="p-6">
          <div className="space-y-4">
            {/* File Upload Section */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Upload className="h-5 w-5 text-muted-foreground" />
                <span className="text-sm text-muted-foreground">
                  {uploadedFile ? uploadedFile.name : "Drag and drop a file or click to upload"}
                </span>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileSelect}
                className="hidden"
                accept=".md,.txt,text/*"
              />
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => fileInputRef.current?.click()}
              >
                Browse Files
              </Button>
            </div>

            {/* Textarea */}
            <Textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder={placeholder}
              className="min-h-[200px] resize-y font-mono text-sm"
              rows={10}
            />

            {/* Stats and Actions */}
            <div className="flex items-center justify-between">
              <div className="flex gap-4 text-sm text-muted-foreground">
                <span data-testid="char-count">
                  {charCount} character{charCount !== 1 ? 's' : ''}
                </span>
                <span data-testid="word-count">
                  {wordCount} word{wordCount !== 1 ? 's' : ''}
                </span>
              </div>
              <Button
                onClick={handleGenerate}
                disabled={content.trim() === ""}
                size="lg"
              >
                Generate Dashboard
              </Button>
            </div>
          </div>
        </div>

        {/* Drag overlay */}
        {isDragging && (
          <div className="absolute inset-0 flex items-center justify-center bg-primary/10 rounded-lg">
            <div className="text-center">
              <Upload className="h-12 w-12 mx-auto mb-2 text-primary" />
              <p className="text-lg font-medium text-primary">Drop file here</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
