import { createContext, useContext, useState, ReactNode } from "react";

export interface Conversation {
  id: string;
  title: string;
  user_id: string;
  created_at: Date;
  updated_at: Date;
  document_id: string | null;
  active?: boolean;
}

interface ChatContextType {
  conversations: Conversation[];
  setConversations: (conversations: Conversation[]) => void;
  activeConversation: Conversation | null;
  setActiveConversation: (conversation: Conversation | null) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function ChatProvider({ children }: { children: ReactNode }) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversation, setActiveConversation] = useState<Conversation | null>(null);

  return (
    <ChatContext.Provider
      value={{
        conversations,
        setConversations,
        activeConversation,
        setActiveConversation,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  const context = useContext(ChatContext);
  if (context === undefined) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
} 