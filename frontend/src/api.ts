const API_BASE_URL =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000"

export class UnauthorizedError extends Error {
  constructor() {
    super("Session expired")
    this.name = "UnauthorizedError"
  }
}

async function handleResponse(response: Response) {
  if (response.status === 401) {
    localStorage.removeItem("access_token")
    throw new UnauthorizedError()
  }

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }

  return response.json()
}

export async function createItem(title: string, url: string) {
  const token = localStorage.getItem("access_token")

  const response = await fetch(`${API_BASE_URL}/items/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      title,
      url,
    }),
  })

  return handleResponse(response)
}

export async function getItems(search = "", tag = "") {
  const token = localStorage.getItem("access_token")

  const params = new URLSearchParams()

  if (search.trim()) {
    params.set("q", search.trim())
  }

  if (tag.trim()) {
    params.set("tag", tag.trim())
  }

  const query = params.toString()

  const url = query
    ? `${API_BASE_URL}/items/?${query}`
    : `${API_BASE_URL}/items/`

  const response = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  return handleResponse(response)
}

export async function deleteItem(itemId: number) {
  const token = localStorage.getItem("access_token")

  const response = await fetch(
    `${API_BASE_URL}/items/${itemId}`,
    {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    },
  )

  return handleResponse(response)
}

export async function updateItem(
  itemId: number,
  title: string,
  url: string,
) {
  const token = localStorage.getItem("access_token")

  const response = await fetch(
    `${API_BASE_URL}/items/${itemId}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        title,
        url,
      }),
    },
  )

  return handleResponse(response)
}