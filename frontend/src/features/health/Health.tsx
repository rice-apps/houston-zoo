import { useHealth } from './api'

export function Health() {
  const { data, isPending, isError } = useHealth()

  if (isPending) {
    return <p className="health">Checking API…</p>
  }

  if (isError) {
    return <p className="health health--down">API unreachable</p>
  }

  return (
    <p className="health health--up">
      {data.app} is up ({data.environment})
    </p>
  )
}
