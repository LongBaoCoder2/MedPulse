// api/chat.ts
import { axiosInstance } from "@/lib/axios";
import { Conversation } from "@/contexts/ChatContext";
import Cookies from "js-cookie";
import { RenameConversationRequest } from "@/schema/chat";

export interface Message {
  id: string;
  content: string;
  role: "user" | "assistant";
  created_at: string;
  updated_at: string;
  conversation_id: string;
  status: string;
}

export interface ConversationWithMessages extends Conversation {
  messages: Message[];
}

export async function getConversations(): Promise<Conversation[]> {
  const response = await axiosInstance.get<Conversation[]>("/chat");
  return response.data;
}

export async function createConversation(): Promise<Conversation> {
  const response = await axiosInstance.post<Conversation>("/chat");
  return response.data;
}

export async function renameConversation(conversation_id: string, data: RenameConversationRequest): Promise<string> {
  const response = await axiosInstance.patch<string>(`/chat/${conversation_id}/rename`, data);
  return response.data;
}

export async function deleteConversation(conversation_id: string): Promise<string> {
  const response = await axiosInstance.delete<string>(`/chat/${conversation_id}`);
  return response.data;
}

export async function getAllMessages(
  conversation_id: string
): Promise<Message[]> {
  const response = await axiosInstance.get<ConversationWithMessages>(
    `/chat/${conversation_id}`
  );
  return response.data.messages;
}

export async function streamChatResponse(
  conversation_id: string,
  message: string,
  onData: (token: string) => void,
  onError: (error: string) => void,
  onComplete: () => void
): Promise<void> {
  try {
    const response = await fetch(`http://localhost:8000/api/v1/chat/${conversation_id}/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${Cookies.get('access_token')}` 
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error('Failed to start streaming');
    }

    const reader = response.body?.getReader();
    const decoder = new TextDecoder();

    let accumulatedContent = '';
    
    while (true) {
      const { done, value } = await reader!.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });
      const lines = chunk.split('\n\n').filter(line => line.trim());

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const content = line.slice(6).trim();

          if (content === '[DONE]') {
            onComplete();
          } else if (content.startsWith('Error: ')) {
            onError(content.slice(7));
          } else {
            try {
              const tokenData = JSON.parse(content);
              console.log("Token data: ", tokenData);
              accumulatedContent += tokenData.p;
              console.log("Accumulated content: ", accumulatedContent);
              
              onData(accumulatedContent);
            } catch (e) {
              onError(`Failed to parse token data: ${e}`);
            }
          }
        }
      }
    }
  } catch (error) {
    onError((error as Error).message);
  }
}


