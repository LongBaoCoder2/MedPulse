export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface SignupRequest {
  email: string;
  password: string;
}

export interface SignupResponse {
  id: string;
  email: string;
}

export interface ErrorResponse {
  detail: string;
  status_code: number;
} 

export interface ProfileResponse {
  email: string;
  id: string;
}