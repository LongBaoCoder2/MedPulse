import { Navigate, Route, Routes as ReactRouterRoutes } from "react-router-dom";
import { LoginForm } from "@/components/auth/LoginForm";
import { SignupForm } from "@/components/auth/SignupForm";
import { Sidebar } from "@/components/chat/Sidebar";
import { ChatContainer } from "@/components/chat/ChatContainer";
import { useAuth } from "@/contexts/AuthContext";

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />;
}

export function AppRoutes() {
  const { isAuthenticated } = useAuth();

  return (
    <ReactRouterRoutes>
      <Route
        path="/login"
        element={
          isAuthenticated ? (
            <Navigate to="/conversation" replace />
          ) : (
            <div className="flex h-screen items-center justify-center bg-[hsl(var(--background))]">
              <LoginForm />
            </div>
          )
        }
      />
      <Route
        path="/signup"
        element={
          isAuthenticated ? (
            <Navigate to="/conversation" replace />
          ) : (
            <div className="flex h-screen items-center justify-center bg-[hsl(var(--background))]">
              <SignupForm />
            </div>
          )
        }
      />
      <Route
        path="/conversation/*"
        element={
          <ProtectedRoute>
            <div className="flex h-screen overflow-hidden bg-[hsl(var(--background))]">
              <Sidebar />
              <main className="flex-1">
                <ChatContainer />
              </main>
            </div>
          </ProtectedRoute>
        }
      />
      <Route path="/" element={<Navigate to="/conversation" replace />} />
    </ReactRouterRoutes>
  );
}