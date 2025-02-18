import { useEffect, useState } from "react";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { useChat } from "@/contexts/ChatContext";
import { getAllMessages, streamChatResponse } from "@/api/chat";
import { Loader2, MessageSquare } from "lucide-react";

interface Message {
  id: string;
  content: string;
  isUser: boolean;
}

export function ChatContainer() {
  const { activeConversation } = useChat();
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const loadMessages = async () => {
      if (activeConversation) {
        setIsLoading(true);
        try {
          const apiMessages = await getAllMessages(activeConversation.id);
          const convertedMessages = apiMessages.map(msg => ({
            id: msg.id,
            content: msg.content,
            isUser: msg.role === "user"
          }));
          setMessages(convertedMessages);
        } catch (error) {
          console.error("Failed to load messages:", error);
        } finally {
          setIsLoading(false);
        }
      }
    };

    loadMessages();
  }, [activeConversation]);

  // ChatContainer.tsx
const handleSendMessage = async (content: string) => {
  if (!activeConversation) return;

  // Generate temporary IDs for optimistic updates
  const tempUserId = `temp-${Date.now()}`;
  const tempAssistantId = `temp-${Date.now() + 1}`;

  // Optimistically add user message
  const userMessage: Message = {
    id: tempUserId,
    content,
    isUser: true,
  };

  // Optimistically add assistant message with empty content
  const assistantMessage: Message = {
    id: tempAssistantId,
    content: "",
    isUser: false,
  };

  setMessages(prev => [...prev, userMessage, assistantMessage]);

  try {
    await streamChatResponse(
      activeConversation.id,
      content,
      // onData callback
      (token) => {
        console.log("Receive token: ", token);
        setMessages(prev => prev.map(msg => {
          if (msg.id === tempAssistantId) {
            return { ...msg, content: token };
          }
          return msg;
        }));
      },
      // onError callback
      (error) => {
          setMessages(prev => prev.map(msg => {
            if (msg.id === tempAssistantId) {
              return { ...msg, content: `Error: ${error}` };
            }
            return msg;
          }));
        },
        // onComplete callback
        async () => {
          // Stream finished, reload messages from server
          const apiMessages = await getAllMessages(activeConversation.id);
          const convertedMessages = apiMessages.map(msg => ({
            id: msg.id,
            content: msg.content,
            isUser: msg.role === "user"
          }));
          setMessages(convertedMessages);
        }
      );
    } catch (error) {
      console.error("Failed to send message:", error);
      setMessages(prev => prev.map(msg => {
        if (msg.id === tempAssistantId) {
          return { ...msg, content: `Error: ${(error as Error).message}` };
        }
        return msg;
      }));
    }
  };
  

  return (
    <div className="flex h-screen flex-col bg-[#F8FAFB]">
      {/* Chat Header */}
      <div className="border-b border-[#E5E9EB] bg-white p-4">
        <h2 className="text-lg font-medium text-gray-900">{activeConversation?.title || "HeathChat AI"}</h2>
      </div>


      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto px-4">
        {!activeConversation ? (
          <div className="flex h-full flex-col items-center justify-center text-center space-y-4">
            <MessageSquare size={48} className="text-indigo-200" />
            <div className="space-y-2">
              <h3 className="text-lg font-medium text-gray-900">
                How can I assist you today?
              </h3>
              <p className="text-sm text-gray-500">
                Start a new chat to begin your conversation
              </p>
            </div>
          </div>
        ) : isLoading ? (
          <div className="flex h-full items-center justify-center">
            <Loader2 className="h-8 w-8 animate-spin text-gray-400" />
          </div>
        ) : (
          <div className="mx-auto max-w-[850px] px-4">
          {messages.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center py-20 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-[#E6F5F4]">
                <svg 
                  width="32" 
                  height="32" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  className="text-[#00A19B]"
                >
                  <path 
                    d="M20 12v-4a8 8 0 0 0-16 0v4M4 12h16" 
                    strokeWidth="2" 
                    strokeLinecap="round"
                  />
                  <path 
                    d="M12 16v-4M8 16v-4M16 16v-4" 
                    strokeWidth="2" 
                    strokeLinecap="round"
                  />
                </svg>
              </div>
              <h3 className="mt-6 text-xl font-medium text-gray-900">Welcome to HealthChat AI</h3>
              <p className="mt-2 max-w-sm text-sm text-gray-500">
                Feel free to ask me anything about your health concerns. I'm here to help provide medical information and guidance.
              </p>
              <p className="mt-4 text-sm text-gray-400">
                Example questions:
              </p>
              <div className="mt-2 space-y-2">
                <button className="rounded-lg bg-white px-4 py-2 text-sm text-gray-600 shadow-sm hover:bg-gray-50">
                  What are common symptoms of the flu?
                </button>
                <button className="rounded-lg bg-white px-4 py-2 text-sm text-gray-600 shadow-sm hover:bg-gray-50">
                  How can I improve my sleep quality?
                </button>
                <button className="rounded-lg bg-white px-4 py-2 text-sm text-gray-600 shadow-sm hover:bg-gray-50">
                  What should I know about maintaining a healthy diet?
                </button>
              </div>
            </div>
          ) : (
            // Existing messages code
            messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message.content}
                isUser={message.isUser}
              />
            ))
          )}
        </div>
        )}
        
      </div>
      <ChatInput onSend={handleSendMessage} />
    </div>
  );
}
