import { Health } from '@/features/health/Health'

export function HomePage() {
  return (
    <>
      <h1>Welcome</h1>
      <p>React + Vite frontend talking to a FastAPI backend.</p>
      <Health />
    </>
  )
}
