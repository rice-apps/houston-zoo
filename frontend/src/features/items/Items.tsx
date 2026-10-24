import { Button } from '@/components/Button'
import { ErrorMessage } from '@/components/ErrorMessage'
import { useCreateItem, useDeleteItem, useItems } from './api'

export function Items() {
  const { data: items, isPending, error } = useItems()
  const createItem = useCreateItem()
  const deleteItem = useDeleteItem()

  function handleCreate(formData: FormData) {
    const name = String(formData.get('name') ?? '').trim()
    const description = String(formData.get('description') ?? '').trim()
    if (!name) return
    createItem.mutate({ name, description: description || null })
  }

  return (
    <section className="items">
      <form action={handleCreate} className="items__form">
        <input name="name" placeholder="Name" required maxLength={100} />
        <input name="description" placeholder="Description (optional)" maxLength={500} />
        <Button type="submit" disabled={createItem.isPending}>
          {createItem.isPending ? 'Adding…' : 'Add item'}
        </Button>
      </form>

      {createItem.error && <ErrorMessage error={createItem.error} />}
      {deleteItem.error && <ErrorMessage error={deleteItem.error} />}

      {isPending && <p>Loading items…</p>}
      {error && <ErrorMessage error={error} />}

      {items && items.length === 0 && <p className="muted">No items yet. Add one above.</p>}

      {items && items.length > 0 && (
        <ul className="items__list">
          {items.map((item) => (
            <li key={item.id} className="items__row">
              <div>
                <strong>{item.name}</strong>
                {item.description && <p className="muted">{item.description}</p>}
              </div>
              <Button
                variant="danger"
                onClick={() => deleteItem.mutate(item.id)}
                disabled={deleteItem.isPending}
              >
                Delete
              </Button>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
