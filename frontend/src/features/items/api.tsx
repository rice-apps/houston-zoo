import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { apiClient } from '@/lib/apiClient'
import type { Item, ItemCreate, ItemUpdate } from './types'

export const itemKeys = {
  all: ['items'] as const,
  detail: (id: number) => ['items', id] as const,
}

export const itemsApi = {
  list: () => apiClient.get<Item[]>('/items'),
  get: (id: number) => apiClient.get<Item>(`/items/${id}`),
  create: (data: ItemCreate) => apiClient.post<Item>('/items', data),
  update: (id: number, data: ItemUpdate) => apiClient.patch<Item>(`/items/${id}`, data),
  remove: (id: number) => apiClient.delete(`/items/${id}`),
}

export function useItems() {
  return useQuery({ queryKey: itemKeys.all, queryFn: itemsApi.list })
}

export function useItem(id: number) {
  return useQuery({ queryKey: itemKeys.detail(id), queryFn: () => itemsApi.get(id) })
}

export function useCreateItem() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: itemsApi.create,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: itemKeys.all }),
  })
}

export function useUpdateItem() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ItemUpdate }) => itemsApi.update(id, data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: itemKeys.all }),
  })
}

export function useDeleteItem() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: itemsApi.remove,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: itemKeys.all }),
  })
}
