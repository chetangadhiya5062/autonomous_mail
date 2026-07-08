// src/context/ChatContext.jsx
import { createContext, useContext, useState, useCallback } from 'react';
import { useAuth } from './AuthContext';
import { CONFIG } from '../config';
import { ASSISTANTS } from "../config/assistants";

const ChatContext = createContext(null);

function genId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 6);
}

const STORAGE_KEY = 'am_convs';

function loadConvs() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
  catch { return []; }
}
function saveConvs(convs) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(convs));
}

export function ChatProvider({ children }) {
  const { authFetch } = useAuth();
  const [conversations, setConversations] = useState(loadConvs);
  const [activeId,      setActiveId]      = useState(null);
  const [thinking,      setThinking]      = useState(false);
  // const [chatMode, setChatMode] = useState("benefits");
  const [assistant, setAssistant] = useState("agent");
  const assistantConfig = ASSISTANTS[assistant];

  const activeConv = conversations.find(c => c.id === activeId) || null;

  const persistConvs = useCallback((convs) => {
    setConversations(convs);
    saveConvs(convs);
  }, []);

  const startNewChat = useCallback(() => {
    const id = genId();
    // const conv = { id, title: 'New conversation', messages: [] };
    const conv = {
        id,
        assistant,
        title: 'New conversation',
        messages: []
    };
    persistConvs([conv, ...conversations]);
    setActiveId(id);
    return id;
  }, [
      conversations,
      persistConvs,
      assistant,
  ]);

  const switchConv = useCallback((id) => {

      const conv = conversations.find(c => c.id === id);

      if (conv?.assistant) {
          setAssistant(conv.assistant);
      }

      setActiveId(id);

  }, [conversations]);

  const sendMessage = useCallback(async (prompt) => {
    if (!prompt.trim() || thinking) return;

    // Ensure there's an active conversation
    let convId = activeId;
    let updatedConvs = [...conversations];

    if (!convId || !updatedConvs.find(c => c.id === convId)) {
      const id = genId();
      // const newConv = { id, title: prompt.slice(0, 48), messages: [] };
      const newConv = {
          id,
          assistant,
          title: prompt.slice(0, 48),
          messages: []
      };
      updatedConvs = [newConv, ...updatedConvs];
      convId = id;
      setActiveId(id);
    }
    

    // Add user message
    const userMsg = { id: genId(), role: 'user', content: prompt };
    updatedConvs = updatedConvs.map(c => {
      if (c.id !== convId) return c;
      const updated = { ...c, messages: [...c.messages, userMsg] };
      // Set title from first message
      if (c.messages.length === 0) {
        updated.title = prompt.slice(0, 52) + (prompt.length > 52 ? '…' : '');
      }
      return updated;
    });
    persistConvs(updatedConvs);
    setThinking(true);

    try {

        let payload;

        switch (assistant) {

            case "benefits":
                payload = {
                    question: prompt,
                };
                break;

            case "agent":
            default:
                payload = {
                    prompt,
                };
                break;
        }

        const res = await authFetch(
            `${CONFIG.API_BASE}${assistantConfig.endpoint}`,
            {
                method: "POST",
                body: JSON.stringify(payload),
            }
        );

        if (!res.ok) {

            const err = await res.json().catch(() => ({}));

            throw new Error(
                err.detail || `Server error (${res.status})`
            );
        }

        const data = await res.json();

        let aiMessage;

        switch (assistant) {

            case "benefits":

                aiMessage = {

                    id: genId(),

                    role: "ai",

                    content: data.answer,

                    confidence: data.confidence,

                    sources: data.sources || [],

                };

                break;

            case "agent":
            default:

                aiMessage = {

                    id: genId(),

                    role: "ai",

                    content:
                        data.agent_response ||
                        "No response received.",

                };

                break;
        }

        updatedConvs = updatedConvs.map(c =>
            c.id === convId
                ? {
                      ...c,
                      messages: [...c.messages, aiMessage],
                  }
                : c
        );


    } catch (err) {
      const errMsg = {
        id: genId(),
        role: 'ai',
        content: `⚠️ **Error:** ${err.message}\n\nMake sure the backend server is running at \`${CONFIG.API_BASE}\`.`,
        isError: true,
      };
      updatedConvs = updatedConvs.map(c =>
        c.id === convId
          ? { ...c, messages: [...c.messages, errMsg] }
          : c
      );
    } finally {
      persistConvs(updatedConvs);
      setThinking(false);
    }
  }, [
      activeId,
      conversations,
      authFetch,
      thinking,
      persistConvs,
      assistant,
      assistantConfig,
  ]);

  return (
    <ChatContext.Provider
        value={{
            conversations,
            activeConv,
            activeId,

            thinking,

            // chatMode,
            // setChatMode,

            startNewChat,
            switchConv,
            sendMessage,

            assistant,
            setAssistant,
            assistantConfig,
        }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export const useChat = () => useContext(ChatContext);
