import { useEffect, useMemo, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { Bot, BrainCircuit, FileSearch, Lightbulb, Search, Send, ShieldAlert, Sparkles } from "lucide-react";

import Card from "../components/common/Card.jsx";
import { fetchSOCAssistantHistory, sendSOCAssistantMessage } from "../services/socAssistantApi.js";
import { cn } from "../utils/cn.js";

const starterPrompts = [
  {
    label: "Explain alert",
    icon: ShieldAlert,
    prompt: "Explain this critical alert: impossible travel and privileged login anomaly mapped to T1078.",
  },
  {
    label: "Explain CVE",
    icon: FileSearch,
    prompt: "Explain CVE risk for a remote code execution vulnerability on an internet-facing gateway.",
  },
  {
    label: "Mitigation",
    icon: Lightbulb,
    prompt: "Recommend mitigations for suspected credential abuse and suspicious PowerShell execution.",
  },
  {
    label: "Threat intel",
    icon: Search,
    prompt: "Search threat intelligence for valid account abuse, ransomware precursors, and related MITRE techniques.",
  },
  {
    label: "Summarize incident",
    icon: BrainCircuit,
    prompt: "Summarize an incident involving impossible travel, encoded PowerShell, and sensitive file access.",
  },
];

const fallbackAnswer = {
  answer:
    "SOC Assistant is connected to the backend endpoint, but the RAG service is unavailable or requires authentication. In production this response will include alert/CVE explanation, mitigations, incident summary, threat intelligence citations, and analyst next steps.",
  citations: [],
  recommendations: [
    "Validate related logs and affected assets.",
    "Map the activity to MITRE ATT&CK.",
    "Document containment and remediation actions.",
  ],
};

function TypingText({ text }) {
  const [visibleText, setVisibleText] = useState("");

  useEffect(() => {
    setVisibleText("");
    const words = text.split(" ");
    let index = 0;
    const interval = window.setInterval(() => {
      index += 1;
      setVisibleText(words.slice(0, index).join(" "));
      if (index >= words.length) {
        window.clearInterval(interval);
      }
    }, 18);
    return () => window.clearInterval(interval);
  }, [text]);

  return <p className="whitespace-pre-line leading-7">{visibleText}</p>;
}

function MessageBubble({ message }) {
  const isUser = message.role === "user";
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={cn("flex", isUser ? "justify-end" : "justify-start")}
    >
      <div
        className={cn(
          "max-w-[86%] rounded-lg border p-4 text-sm shadow-lg",
          isUser
            ? "border-blue-400/30 bg-blue-600 text-white"
            : "border-slate-800 bg-slate-950 text-slate-200",
        )}
      >
        <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-wide opacity-80">
          {isUser ? <Sparkles size={14} /> : <Bot size={14} />}
          {isUser ? "Analyst" : "AI SOC Assistant"}
        </div>
        {message.streaming ? <TypingText text={message.text} /> : <p className="whitespace-pre-line leading-7">{message.text}</p>}
        {message.recommendations?.length > 0 && (
          <div className="mt-4 rounded-lg border border-emerald-400/20 bg-emerald-500/10 p-3">
            <p className="mb-2 text-xs font-semibold uppercase text-emerald-200">Recommendations</p>
            <ul className="space-y-1 text-sm text-emerald-50">
              {message.recommendations.map((item) => (
                <li key={item}>- {item}</li>
              ))}
            </ul>
          </div>
        )}
        {message.citations?.length > 0 && (
          <div className="mt-4 space-y-2">
            <p className="text-xs font-semibold uppercase text-cyan-200">Citations</p>
            {message.citations.slice(0, 4).map((citation) => (
              <div key={`${citation.source}-${citation.citation}`} className="rounded-lg bg-white/[0.04] p-2 text-xs text-slate-300">
                {citation.source} - {citation.title || citation.citation}
              </div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}

export default function SOCAssistant() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "I can explain alerts and CVEs, recommend mitigations, search threat intelligence, and summarize incidents using the existing RAG pipeline.",
      recommendations: ["Start with an alert, CVE, IOC, MITRE technique, or incident timeline."],
    },
  ]);
  const [input, setInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [historyLoaded, setHistoryLoaded] = useState(false);
  const scrollerRef = useRef(null);

  useEffect(() => {
    async function loadHistory() {
      try {
        const history = await fetchSOCAssistantHistory();
        if (history?.length) {
          const mapped = history
            .slice()
            .reverse()
            .flatMap((item) => [
              { role: "user", text: item.message },
              {
                role: "assistant",
                text: item.answer,
                citations: item.citations || [],
                recommendations: item.recommendations || [],
              },
            ]);
          setMessages((items) => [...items, ...mapped]);
        }
      } catch {
        // History is optional when backend auth/RAG dependencies are unavailable.
      } finally {
        setHistoryLoaded(true);
      }
    }
    loadHistory();
  }, []);

  useEffect(() => {
    scrollerRef.current?.scrollTo({ top: scrollerRef.current.scrollHeight, behavior: "smooth" });
  }, [messages]);

  const capabilityText = useMemo(
    () => ["Explain alerts", "Explain CVEs", "Recommend mitigation", "Search threat intelligence", "Summarize incidents"],
    [],
  );

  async function sendMessage(messageText = input) {
    const text = messageText.trim();
    if (!text) return;

    setInput("");
    setIsSending(true);
    setMessages((items) => [...items, { role: "user", text }]);

    try {
      const response = await sendSOCAssistantMessage({
        message: text,
        context: {
          source: "soc_assistant_ui",
          requested_capabilities: capabilityText,
        },
      });
      setMessages((items) => [
        ...items,
        {
          role: "assistant",
          text: response.answer,
          citations: response.citations || [],
          recommendations: response.recommendations || [],
          streaming: true,
        },
      ]);
    } catch {
      setMessages((items) => [
        ...items,
        {
          role: "assistant",
          text: fallbackAnswer.answer,
          citations: fallbackAnswer.citations,
          recommendations: fallbackAnswer.recommendations,
          streaming: true,
        },
      ]);
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="space-y-6">
      <section className="rounded-lg border border-slate-800 bg-slate-950 p-5 text-white shadow-2xl shadow-slate-950/30">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <div className="flex items-center gap-2 text-sm font-semibold text-cyan-300">
              <Bot size={18} />
              AI SOC Assistant
            </div>
            <h1 className="mt-2 text-2xl font-semibold md:text-3xl">Analyst Copilot For Security Operations</h1>
            <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
              Ask about alerts, CVEs, mitigations, incidents, IOCs, and MITRE techniques. Responses use the existing Threat Intelligence RAG pipeline and preserve citations when available.
            </p>
          </div>
          <span className={cn("rounded-full px-3 py-1 text-xs font-semibold ring-1", historyLoaded ? "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30" : "bg-amber-500/15 text-amber-200 ring-amber-400/30")}>
            {historyLoaded ? "History ready" : "Loading history"}
          </span>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[0.72fr_1.28fr]">
        <div className="space-y-4">
          <Card className="border-slate-800 bg-slate-950 text-white" title="Capabilities">
            <div className="space-y-2">
              {capabilityText.map((item) => (
                <div key={item} className="rounded-lg border border-slate-800 bg-slate-900/70 px-3 py-2 text-sm text-slate-300">
                  {item}
                </div>
              ))}
            </div>
          </Card>
          <Card className="border-slate-800 bg-slate-950 text-white" title="Prompt Starters">
            <div className="space-y-2">
              {starterPrompts.map((starter) => {
                const Icon = starter.icon;
                return (
                  <button
                    key={starter.label}
                    type="button"
                    onClick={() => sendMessage(starter.prompt)}
                    className="flex w-full items-center gap-3 rounded-lg border border-slate-800 bg-slate-900/70 p-3 text-left text-sm text-slate-200 transition hover:border-cyan-400/40 hover:bg-slate-900"
                  >
                    <Icon className="text-cyan-300" size={17} />
                    <span>{starter.label}</span>
                  </button>
                );
              })}
            </div>
          </Card>
        </div>

        <Card className="border-slate-800 bg-slate-950 text-white" title="Conversation">
          <div className="flex h-[42rem] flex-col">
            <div ref={scrollerRef} className="flex-1 space-y-4 overflow-y-auto pr-2">
              <AnimatePresence initial={false}>
                {messages.map((message, index) => (
                  <MessageBubble key={`${message.role}-${index}-${message.text.slice(0, 12)}`} message={message} />
                ))}
              </AnimatePresence>
            </div>

            <form
              onSubmit={(event) => {
                event.preventDefault();
                sendMessage();
              }}
              className="mt-4 flex gap-2"
            >
              <input
                value={input}
                onChange={(event) => setInput(event.target.value)}
                className="min-w-0 flex-1 rounded-lg border border-slate-800 bg-slate-900 px-3 py-3 text-sm text-slate-100 outline-none transition placeholder:text-slate-500 focus:border-cyan-400"
                placeholder="Ask about an alert, CVE, incident, IOC, or mitigation"
              />
              <button
                type="submit"
                disabled={isSending}
                className="inline-flex items-center gap-2 rounded-lg bg-cyan-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-cyan-300 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Send size={17} />
                {isSending ? "Thinking" : "Send"}
              </button>
            </form>
          </div>
        </Card>
      </section>
    </div>
  );
}
