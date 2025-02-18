import { User } from "lucide-react";
import { useEffect, useState } from "react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { MarkdownComponents } from "./MarkdownComponents";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
}

export function ChatMessage({ message, isUser }: ChatMessageProps) {
  const [displayedMessage, setDisplayedMessage] = useState(message);

  // Effect to handle streaming updates
  useEffect(() => {
    setDisplayedMessage(message);
  }, [message]);


  return (
    <div className="my-4 flex w-full gap-4">
      {!isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#E6F5F4] ring-4 ring-[#E6F5F4]/50">
          <svg 
            width="20" 
            height="20" 
            viewBox="0 0 24 24" 
            fill="none" 
            className="text-[#00A19B]"
          >
            <path
              d="M9.5 15.5V15.525C9.5 16.8917 10.6083 18 11.975 18H16.5L21 21V11.975C21 10.6083 19.8917 9.5 18.525 9.5H18.5"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M13.5 7.5V7.525C13.5 8.89175 12.3917 10 11.025 10H5.5L3 13V3.975C3 2.60825 4.10825 1.5 5.475 1.5H11.025C12.3917 1.5 13.5 2.60825 13.5 3.975V7.5Z"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
      )}
      <div 
        className={`group relative flex-1 rounded-2xl px-5 py-4 ${
          isUser 
            ? 'bg-[#00A19B] text-white ml-15' 
            : 'bg-white text-gray-800 shadow-sm mr-15'
        }`}
      >
        <div className={`text-[15px] leading-relaxed prose-sm ${isUser && "text-right"}`}>
          <ReactMarkdown 
            remarkPlugins={[remarkGfm]}
            components={MarkdownComponents}
            className={`${isUser ? 'text-white prose-invert' : 'text-gray-800'}`}
          >
            {displayedMessage}
          </ReactMarkdown>
        </div>
        <span className="absolute bottom-1 right-5 text-xs opacity-0 transition-opacity group-hover:opacity-60">
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </span>
      </div>
      {isUser && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#00A19B] ring-4 ring-[#00A19B]/20">
          <User size={18} className="text-white" />
        </div>
      )}
    </div>
  );
}