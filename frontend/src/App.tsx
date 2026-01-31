import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { MarkdownInput } from "@/components/MarkdownInput"
import { A2UIRendererList } from "@/components/A2UIRenderer"
import { getRegisteredTypes, type A2UIComponent } from "@/lib/a2ui-catalog"

// Sample A2UI components to demonstrate the catalog
const sampleA2UIComponents: A2UIComponent[] = [
  {
    id: 'demo-headline-1',
    type: 'a2ui.HeadlineCard',
    props: {
      title: 'A2UI Catalog Successfully Registered',
      summary: 'The component catalog maps 45+ backend component types to React components for dynamic rendering.',
      source: 'System',
      published_at: new Date().toISOString(),
      sentiment: 'positive',
    },
  },
  {
    id: 'demo-stat-1',
    type: 'a2ui.StatCard',
    props: {
      label: 'Registered Components',
      value: String(getRegisteredTypes().length),
      trend: '+45 new',
      icon: '📦',
    },
  },
  {
    id: 'demo-tldr-1',
    type: 'a2ui.TLDR',
    props: {
      summary: 'A2UI catalog enables backend-to-frontend component rendering with full support for layouts, styling, and nested children.',
      key_points: [
        'News, media, data, list, and resource components',
        'Summary, comparison, and instructional components',
        'Layout components (Section, Grid, Tabs, Accordion)',
        'Tag components (Badge, Status, Priority)',
      ],
    },
  },
];

function App() {
  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-2">Tailwind CSS + Shadcn/ui</h1>
          <p className="text-muted-foreground">Component library setup with dark theme</p>
          <div className="flex gap-2 justify-center mt-4">
            <Badge>Setup Complete</Badge>
            <Badge variant="secondary">Dark Mode</Badge>
            <Badge variant="outline">Ready</Badge>
          </div>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Button Components</CardTitle>
            <CardDescription>Various button styles and variants</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-wrap gap-3">
            <Button>Default</Button>
            <Button variant="secondary">Secondary</Button>
            <Button variant="destructive">Destructive</Button>
            <Button variant="outline">Outline</Button>
            <Button variant="ghost">Ghost</Button>
            <Button variant="link">Link</Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Markdown Input</CardTitle>
            <CardDescription>Create a dashboard from markdown content</CardDescription>
          </CardHeader>
          <CardContent>
            <MarkdownInput
              onGenerate={(content, file) => {
                console.log('Generate clicked:', { content, file })
                alert(`Dashboard generation started!\nContent length: ${content.length}\nFile: ${file?.name || 'None'}`)
              }}
            />
          </CardContent>
        </Card>

        <Tabs defaultValue="forms" className="w-full">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="forms">Forms</TabsTrigger>
            <TabsTrigger value="accordion">Accordion</TabsTrigger>
            <TabsTrigger value="a2ui">A2UI Catalog</TabsTrigger>
            <TabsTrigger value="info">Info</TabsTrigger>
          </TabsList>
          <TabsContent value="forms">
            <Card>
              <CardHeader>
                <CardTitle>Form Components</CardTitle>
                <CardDescription>Input and textarea elements</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Input Field</label>
                  <Input placeholder="Type something..." />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Textarea Field</label>
                  <Textarea placeholder="Enter your message..." />
                </div>
              </CardContent>
              <CardFooter>
                <Button className="w-full">Submit</Button>
              </CardFooter>
            </Card>
          </TabsContent>
          <TabsContent value="accordion">
            <Card>
              <CardHeader>
                <CardTitle>Accordion Component</CardTitle>
                <CardDescription>Collapsible content sections</CardDescription>
              </CardHeader>
              <CardContent>
                <Accordion type="single" collapsible className="w-full">
                  <AccordionItem value="item-1">
                    <AccordionTrigger>What is Tailwind CSS?</AccordionTrigger>
                    <AccordionContent>
                      Tailwind CSS is a utility-first CSS framework for rapidly building custom user interfaces.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-2">
                    <AccordionTrigger>What is Shadcn/ui?</AccordionTrigger>
                    <AccordionContent>
                      Shadcn/ui is a collection of re-usable components built using Radix UI and Tailwind CSS.
                    </AccordionContent>
                  </AccordionItem>
                  <AccordionItem value="item-3">
                    <AccordionTrigger>Why use these tools?</AccordionTrigger>
                    <AccordionContent>
                      They provide a great developer experience with accessible, customizable components and rapid development.
                    </AccordionContent>
                  </AccordionItem>
                </Accordion>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="a2ui">
            <Card>
              <CardHeader>
                <CardTitle>A2UI Component Catalog</CardTitle>
                <CardDescription>
                  Dynamic component rendering system - {getRegisteredTypes().length} components registered
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-muted/50 p-4 rounded-lg">
                  <h3 className="font-semibold mb-2 text-sm">Registered Component Types</h3>
                  <div className="flex flex-wrap gap-1.5 max-h-32 overflow-y-auto">
                    {getRegisteredTypes().map((type) => (
                      <Badge key={type} variant="secondary" className="text-xs">
                        {type.replace('a2ui.', '')}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold mb-3">Sample Components</h3>
                  <A2UIRendererList components={sampleA2UIComponents} spacing="md" />
                </div>

                <div className="bg-blue-500/10 border border-blue-500 p-4 rounded-lg">
                  <p className="text-sm">
                    <strong>How it works:</strong> The backend generates A2UI component specs
                    (with type, props, and children). The A2UIRenderer looks up the type in the
                    catalog and renders the corresponding React component.
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
          <TabsContent value="info">
            <Card>
              <CardHeader>
                <CardTitle>Configuration Info</CardTitle>
                <CardDescription>Setup details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Tailwind CSS</Badge>
                  <span className="text-sm text-muted-foreground">Installed and configured</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Shadcn/ui</Badge>
                  <span className="text-sm text-muted-foreground">Components ready</span>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="secondary">Dark Mode</Badge>
                  <span className="text-sm text-muted-foreground">Default theme</span>
                </div>
                <div className="mt-4 p-4 bg-muted rounded-md">
                  <p className="text-sm font-mono">
                    Components: button, card, input, textarea, badge, tabs, accordion
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  )
}

export default App
