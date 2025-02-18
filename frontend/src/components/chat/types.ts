export interface Message {
    id: string;
    content: string;
    isUser: boolean;
  }
  
  export interface Conversation {
    id: string;
    title: string;
    messages: Message[];
  }