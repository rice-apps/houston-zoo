import { useQuery } from '@tanstack/react-query'
import { apiClient } from '@/lib/apiClient'
import type { HealthStatus } from './types'

export const healthKeys = {
  status: ['health'] as const,
}

export const healthApi = {
  get: () => apiClient.get<HealthStatus>('/health'),
}

export function useHealth() {
  return useQuery({ queryKey: healthKeys.status, queryFn: healthApi.get, retry: false })
}
