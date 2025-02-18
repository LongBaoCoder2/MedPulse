import { MessageSquare, MoreVertical, Pencil, Plus, Search, Settings, Trash2, User } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { Conversation, useChat } from "@/contexts/ChatContext";
import { createConversation, deleteConversation, getConversations, renameConversation } from "@/api/chat";
import { useAuth } from "@/contexts/AuthContext";

export function Sidebar() {
  const { email } = useAuth();
  const { conversations, setConversations, activeConversation, setActiveConversation } = useChat();
  const [ openMenuId, setOpenMenuId ] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const menuRef = useRef<HTMLDivElement>(null);
  const editRef = useRef<HTMLInputElement>(null); 

  const handleRename = (conversation: any) => {
    setEditingId(conversation.id);
    setEditTitle(conversation.title || 'New conversation');
    setOpenMenuId(null);
  }

  const handleSaveRename = async (conversation: any) => {
    try {
      // Assuming you have an API function to update the conversation
      await renameConversation(conversation.id, { title: editTitle });
      
      setConversations(conversations.map(conv => 
        conv.id === conversation.id 
          ? { ...conv, title: editTitle }
          : conv
      ));
      setEditingId(null);
    } catch (error) {
      console.error("Failed to rename conversation:", error);
    }
  }

  const handleDelete = async (conversation: any) => {
    try {
      // Assuming you have an API function to delete the conversation
      await deleteConversation(conversation.id);
      
      setConversations(conversations.filter(conv => conv.id !== conversation.id));
      setOpenMenuId(null);
      
      if (activeConversation?.id === conversation.id) {
        setActiveConversation(null);
      }
    } catch (error) {
      console.error("Failed to delete conversation:", error);
    }
  }


  useEffect(() => {
    const fetchConversations = async () => {
      try {
        const data = await getConversations();
        const sortedData = data.sort((a: Conversation, b: Conversation) => 
          new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
        );
        setConversations(sortedData);
      } catch (error) {
        console.error("Failed to fetch conversations:", error);
      }
    };
    fetchConversations();
  }, [setConversations]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      // Handle menu close
      if (openMenuId && menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setOpenMenuId(null);
      }

      // Handle edit cancel
      if (editingId && editRef.current && !editRef.current.contains(event.target as Node)) {
        setEditingId(null);
        setEditTitle(""); // Reset edit title
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [openMenuId, editingId]);

  // Handler for creating a new conversation
  const handleCreateConversation = async () => {
    try {
      const newConversation = await createConversation();
      console.log("New conversation created:", newConversation);

      // Add the new conversation to the list
      setConversations([newConversation, ...conversations]);

      // Set the new conversation as active
      setActiveConversation(newConversation);
    } catch (error) {
      console.error("Failed to create conversation:", error);
    }
  };

  return (
    <div className="flex h-screen w-[280px] flex-none flex-col bg-[#00A19B]">
      {/* Header */}
      <div className="flex items-center gap-3 p-6">
        <h1 className="text-xl font-semibold text-white/90">HealthChat AI</h1>
        <div className="h-2 w-2 rounded-full bg-white/60 animate-pulse" />
      </div>


      {/* Main Content */}
      <div className="flex flex-1 flex-col overflow-hidden">
          {/* New Chat Button */}
          <div className="space-y-3 p-4">
            <button
              onClick={handleCreateConversation}
              className="flex w-full items-center justify-between rounded-xl bg-white/10 px-4 py-3.5 text-sm font-medium text-white/90 transition-all hover:bg-white/15 active:scale-[0.98]"
            >
              <div className="flex items-center gap-3">
                <Plus size={18} className="shrink-0" />
                <span>New Consultation</span>
              </div>
            </button>
        

        {/* Search with medical icon */}
        <div className="group relative">
            <Search size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-white/40" />
            <input
              type="text"
              placeholder="Search medical history..."
              className="w-full rounded-xl border border-white/10 bg-white/5 py-3 pl-10 pr-4 text-sm text-white/90 transition-all placeholder:text-white/40 focus:border-white/20 focus:bg-white/10 focus:outline-none"
            />
          </div>
        </div>

        {/* Conversations List */}
        <div className="flex-1 overflow-y-auto px-2">
          {conversations.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center px-4 space-y-4">
              <svg className="w-12 h-12 text-teal-200" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
                <rect x="10" y="6" width="4" height="12" fill="currentColor" />
                <rect x="6" y="10" width="12" height="4" fill="currentColor" />
              </svg>

              <div className="space-y-2">
                <h3 className="text-lg font-medium text-gray-900">No consultations yet</h3>
                <p className="text-sm text-gray-500">Start a new consultation to begin</p>
              </div>
            </div>
          ) : (
            <nav className="space-y-1.5 py-2">
              {conversations.map((item) => (
              <div key={item.id} className="group relative">
                <div
                    onClick={() => setActiveConversation(item)}
                    className={`flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-sm transition-all cursor-pointer ${
                      activeConversation?.id === item.id
                        ? 'bg-white/15 text-white/90'
                        : 'text-white/70 hover:bg-white/10 hover:text-white/90'
                    }`}
                  >
                  <MessageSquare size={16} className={`shrink-0 ${
                    activeConversation?.id === item.id 
                      ? 'text-white/90' 
                      : 'text-white/50 group-hover:text-white/70'
                  }`} />
                
                {editingId === item.id ? (
                  <input
                    ref={editRef}
                    type="text"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter') handleSaveRename(item);
                      if (e.key === 'Escape') setEditingId(null);
                    }}
                    className="flex-1 bg-transparent text-white/90 focus:outline-none"
                    autoFocus
                  />
                ) : (
                  <span className="truncate text-left flex-1">
                    {item.title || 'New conversation'}
                  </span>
                )}

                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setOpenMenuId(openMenuId === item.id ? null : item.id);
                  }}
                  className="opacity-0 group-hover:opacity-100 p-1 hover:bg-white/10 rounded-lg transition-all"
                >
                  <MoreVertical size={16} className="text-white/70" />
                </button>
              </div>

                  {/* Updated Dropdown Menu */}
                  {openMenuId === item.id && (
                    <div 
                      ref={menuRef}
                      className="absolute right-0 top-full mt-1 z-10 w-48 rounded-lg bg-[#2A2B32] border border-white/10 shadow-lg"
                    >
                      <div className="py-1">
                        <button
                          onClick={() => handleRename(item)}
                          className="flex w-full items-center gap-2 px-4 py-2.5 text-sm text-white/90 hover:bg-white/10"
                        >
                          <Pencil size={16} className="text-white/70" />
                          Rename
                        </button>
                        <button
                          onClick={() => handleDelete(item)}
                          className="flex w-full items-center gap-2 px-4 py-2.5 text-sm text-red-400 hover:bg-white/10"
                        >
                          <Trash2 size={16} />
                          Delete
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </nav>
          )}
      </div>

        {/* Bottom Navigation */}
        <div className="mt-auto border-t border-white/10">
            <div className="p-3 space-y-1">
              <button className="flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-sm text-white/70 transition-all hover:bg-white/10 hover:text-white/90">
                <Settings size={16} className="shrink-0 text-white/50" />
                <span>Settings</span>
              </button>
              
              <button className="flex w-full items-center gap-3 rounded-xl px-3.5 py-3 text-sm transition-all hover:bg-white/10">
                <User size={16} className="shrink-0 text-white/50" />
                <div className="flex flex-1 items-center justify-between">
                  <span className="text-white/70">{email}</span>
                  <span className="rounded-full bg-white/10 px-2.5 py-1 text-xs text-white/60">
                    Pro Plan
                  </span>
                </div>
              </button>
            </div>
          </div>
        </div>
    </div>
  );
}