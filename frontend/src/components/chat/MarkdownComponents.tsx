export const MarkdownComponents = {
    // Override paragraph to remove default margins
    p: ({ children }: any) => <p className="mb-2 last:mb-0">{children}</p>,
    
    // Style links
    a: ({ href, children }: any) => (
      <a href={href} className="text-blue-500 hover:underline" target="_blank" rel="noopener noreferrer">
        {children}
      </a>
    ),
    
    // Style code blocks
    code: ({ node, inline, children, ...props }: any) => (
      inline ? 
        <code className="bg-gray-100 px-1 py-0.5 rounded text-sm" {...props}>{children}</code> :
        <pre className="bg-gray-100 p-3 rounded-lg my-2 overflow-x-auto">
          <code {...props}>{children}</code>
        </pre>
    ),
    
    // Style lists
    ul: ({ children }: any) => <ul className="list-disc ml-6 mb-2">{children}</ul>,
    ol: ({ children }: any) => <ol className="list-decimal ml-6 mb-2">{children}</ol>,
    li: ({ children }: any) => <li className="mb-1">{children}</li>,
    
    // Style headings
    h1: ({ children }: any) => <h1 className="text-2xl font-bold mb-2">{children}</h1>,
    h2: ({ children }: any) => <h2 className="text-xl font-bold mb-2">{children}</h2>,
    h3: ({ children }: any) => <h3 className="text-lg font-bold mb-2">{children}</h3>,
    
    // Style blockquotes
    blockquote: ({ children }: any) => (
      <blockquote className="border-l-4 border-gray-300 pl-4 my-2">{children}</blockquote>
    ),
  };
