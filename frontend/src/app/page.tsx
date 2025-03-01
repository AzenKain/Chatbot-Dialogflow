"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [isMounted, setIsMounted] = useState(false);

  useEffect(() => {
    setIsMounted(true);
    const script = document.createElement("script");
    script.src = "https://www.gstatic.com/dialogflow-console/fast/messenger/bootstrap.js?v=1";
    script.async = true;
    document.body.appendChild(script);

    return () => {
      if (document.body.contains(script)) {
        document.body.removeChild(script);
      }
    };
  }, []);

  if (!isMounted) {
    return null;
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-100 to-blue-300">
      <h1 className="text-4xl font-bold mb-6 text-blue-700">
        Welcome to ChatBot!
      </h1>
      <p className="text-lg text-blue-600 mb-10">
        Hãy trò chuyện cùng chatbot để nhận tư vấn nhanh!
      </p>
      <div dangerouslySetInnerHTML={{ __html: `
        <df-messenger
          chat-icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWSelbDC9W4qFTKefb4AplWMgg4FcCkwK-ueztFVvk3hEGqmW3nQ2yWs0U0ETE05Z3Ohg&usqp=CAU"
          intent="WELCOME"
          chat-title="ChatBot"
          agent-id="7a2d84d7-5772-4bc1-acb9-e95ff842061f"
          language-code="vi">
        </df-messenger>` 
      }}></div>
    </div>
  );
}
