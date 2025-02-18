import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Link, useNavigate } from "react-router-dom";
import * as authHandler from "@/api/auth";
import { useAuth } from "@/contexts/AuthContext";

export function LoginForm() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const loginResponse = await authHandler.login({ email, password });
      if (loginResponse.access_token) {
        login(loginResponse.access_token);
        navigate('/conversation');
      }
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    } catch (error: any) {
      setError(error.message || "Đã xảy ra lỗi khi đăng nhập");
    }
  };

  return (
    <div className="w-full max-w-md space-y-8 p-8 rounded-xl shadow-lg bg-white">
      <div className="text-center">
        <h2 className="text-3xl font-bold tracking-tight">Đăng nhập</h2>
        <p className="mt-2 text-sm text-gray-600">
          Hoặc{" "}
          <Link to="/signup" className="font-medium text-primary hover:underline">
            đăng ký tài khoản mới
          </Link>
        </p>
      </div>
      <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
        {error && (
          <div className="p-3 text-sm text-red-500 bg-red-50 rounded-md">
            {error}
          </div>
        )}
        <div className="space-y-4">
          <div>
            <label htmlFor="email" className="block text-sm font-medium">
              Email
            </label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-1"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-sm font-medium">
              Mật khẩu
            </label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-1"
            />
          </div>
        </div>
        <Button type="submit" className="w-full">
          Đăng nhập
        </Button>
      </form>
    </div>
  );
} 