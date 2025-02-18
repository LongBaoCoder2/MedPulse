import apiClient from '@/lib/axios';
import type { 
  LoginRequest, 
  LoginResponse, 
  SignupRequest, 
  SignupResponse, 
  ErrorResponse, 
  ProfileResponse
} from '@/schema/auth';

export const login = async (data: LoginRequest): Promise<LoginResponse> => {
  try {
    const response = await apiClient.post<LoginResponse>('/auth/login', data);
    return response.data;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    if (error.response) {
      throw error.response.data as ErrorResponse;
    }
    throw new Error('Đã xảy ra lỗi khi đăng nhập');
  }
};

export const signup = async (data: SignupRequest): Promise<SignupResponse> => {
  try {
    const response = await apiClient.post<SignupResponse>('/auth/signup', data);
    return response.data;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    if (error.response) {
      throw error.response.data as ErrorResponse;
    }
    throw new Error('Đã xảy ra lỗi khi đăng ký');
  }
}; 


export const getProfile = async (): Promise<ProfileResponse> => {
  try {
    const response = await apiClient.get<ProfileResponse>('/auth/users/me');
    return response.data;
  } catch (error: any) {
    if (error.response) {
      throw error.response.data as ErrorResponse;
    }
    throw new Error('Đã xảy ra lỗi khi đăng ký');
  }
}