type ErrorMessageProps = {
  error: unknown
}

export function ErrorMessage({ error }: ErrorMessageProps) {
  const message = error instanceof Error ? error.message : 'Something went wrong.'
  return (
    <p role="alert" className="error-message">
      {message}
    </p>
  )
}
