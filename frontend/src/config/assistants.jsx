export const ASSISTANTS = {

    agent: {

        id: "agent",

        name: "Inbox Assistant",

        icon: "🤖",

        endpoint: "/agent/execute",

        inputPlaceholder:
            "Ask AetherMail anything about your inbox...",

        welcomeTitle:
            "How can I help with your inbox?",

        subtitle:
            "Ask me anything about your emails — I can search, organize, summarize, draft replies, and manage your inbox at scale.",

        suggestions: [

            {
                icon: "🔍",
                text: "Find all emails from my boss this week and summarize them"
            },

            {
                icon: "🗑️",
                text: "Delete all promotional emails from last month"
            },

            {
                icon: "✍️",
                text: "Draft a polite reply to the last email from HR"
            },

            {
                icon: "📂",
                text: "Create a label 'Project Alpha' and move related emails there"
            }

        ]
    },

    benefits: {

        id: "benefits",

        name: "Benefits Assistant",

        icon: "🏥",

        endpoint: "/benefits/ask",

        inputPlaceholder:
            "Ask about your employee benefits...",

        welcomeTitle:
            "How can I help with your benefits?",

        subtitle:
            "Ask questions about medical, dental, vision, life insurance, wellness programs, deductibles, copays, eligibility, and other employee benefits.",

        suggestions: [

            {
                icon: "🦷",
                text: "What dental services are covered?"
            },

            {
                icon: "👓",
                text: "Does the vision plan cover contact lenses?"
            },

            {
                icon: "🏥",
                text: "What is my deductible?"
            },

            {
                icon: "💊",
                text: "Does the medical plan cover prescriptions?"
            }

        ]
    }

};