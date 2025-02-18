import { Send } from "lucide-react";
import { ChangeEvent, useState } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
}

export function ChatInput({ onSend }: ChatInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      console.log("Message sent: ", message);
      onSend(message);
      setMessage("");
    }
  };

  const handleOnChange = (e: ChangeEvent<HTMLInputElement>) => {
    setMessage(e.target.value);
  }

  return (
  <div className="border-t border-[#E5E9EB] bg-white p-4">
      <div className="mx-auto max-w-[850px]">
        <div className="flex gap-4">
          <input
            type="text"
            onChange={handleOnChange}
            value={message}
            placeholder="What's in your mind..."
            className="flex-1 rounded-xl border border-[#E5E9EB] bg-[#F8FAFB] px-4 py-3.5 text-sm transition-colors placeholder:text-gray-400 focus:border-[#00A19B] focus:ring-1 focus:ring-[#00A19B]/10"
          />
          <button 
            onClick={handleSubmit}
            className="rounded-xl bg-[#00A19B] p-3.5 text-white transition-colors hover:bg-[#008F8A] active:scale-95">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
