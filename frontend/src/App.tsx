import "./App.css"

import {
  type SubmitEvent,
  useEffect,
  useState,
} from "react"

import {
  createItem,
  deleteItem,
  updateItem,
  getItems,
  UnauthorizedError,
} from "./api"

const API_BASE_URL =
  import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000"

type Item = {
  id: number
  title: string
  url: string
  content: string | null
  summary: string | null
  tags: string[] | null
  processing_error: string | null
  processing_status: string
}

async function login(username: string, password: string) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  })

  if (!response.ok) {
    throw new Error("Login failed")
  }

  return response.json()
}

function App() {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [title, setTitle] = useState("")
  const [url, setUrl] = useState("")
  const [search, setSearch] = useState("")
  const [tag, setTag] = useState("")
  const [editingItemId, setEditingItemId] = useState<number | null>(null)
  const [editTitle, setEditTitle] = useState("")
  const [editUrl, setEditUrl] = useState("")
  const [items, setItems] = useState<Item[]>([])
  const [loggedIn, setLoggedIn] = useState(
    Boolean(localStorage.getItem("access_token")),
  )

  function handleUnauthorized() {
    localStorage.removeItem("access_token")
    setLoggedIn(false)
    setItems([])
    setUsername("")
    setPassword("")
  }

  function handleLogout() {
    localStorage.removeItem("access_token")
    setLoggedIn(false)
    setItems([])
    setUsername("")
    setPassword("")
  }

  useEffect(() => {
    if (!loggedIn) {
      return
    }

    getItems()
      .then((data) => {
        setItems(data)
      })
      .catch((error) => {
        if (error instanceof UnauthorizedError) {
          handleUnauthorized()
          return
        }

        console.error(error)
      })
  }, [loggedIn])

  async function handleSubmit(event: SubmitEvent) {
    event.preventDefault()

    try {
      const data = await login(username, password)

      localStorage.setItem("access_token", data.access_token)
      setLoggedIn(true)
      setPassword("")
    } catch (error) {
      console.error(error)
    }
  }

  async function handleCreateItem(event: SubmitEvent) {
    event.preventDefault()

    try {
      await createItem(title, url)

      setTitle("")
      setUrl("")

      const updatedItems = await getItems()
      setItems(updatedItems)
    } catch (error) {
      if (error instanceof UnauthorizedError) {
        handleUnauthorized()
        return
      }

      console.error(error)
    }
  }

  async function handleDeleteItem(itemId: number) {
    try {
      await deleteItem(itemId)

      const updatedItems = await getItems(search, tag)
      setItems(updatedItems)
    } catch (error) {
      if (error instanceof UnauthorizedError) {
        handleUnauthorized()
        return
      }

      console.error(error)
    }
  }


  async function handleSearch(event: SubmitEvent) {
    event.preventDefault()

    try {
      const results = await getItems(search, tag)
      setItems(results)
    } catch (error) {
      if (error instanceof UnauthorizedError) {
        handleUnauthorized()
        return
      }

      console.error(error)
    }
  }

  function handleClearFilters() {
    setSearch("")
    setTag("")

    getItems()
      .then((data) => {
        setItems(data)
      })
      .catch((error) => {
        if (error instanceof UnauthorizedError) {
          handleUnauthorized()
          return
        }

        console.error(error)
      })
  }
  return (
    <main className="page">
      {!loggedIn ? (
        <section className="login-card">
          <p className="eyebrow">PERSONAL INBOX</p>

          <h1>Welcome back</h1>

          <p className="login-description">
            Sign in to access your saved resources.
          </p>

          <form onSubmit={handleSubmit} className="login-form">
            <label>
              Username
              <input
                value={username}
                onChange={(event) => setUsername(event.target.value)}
                required
              />
            </label>

            <label>
              Password
              <input
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
            </label>

            <button type="submit">Login</button>
          </form>
        </section>
      ) : (
        <>
          <header className="page-header">
            <div>
              <p className="eyebrow">PERSONAL INBOX</p>
              <h1>Your resources</h1>
              <p>Save useful resources. Find them later.</p>
            </div>

            <button
              type="button"
              className="logout-button"
              onClick={handleLogout}
            >
              Log out
            </button>
          </header>

          <section className="save-card">
            <h2>Save a resource</h2>

            <form onSubmit={handleCreateItem} className="save-form">
              <label>
                Title
                <input
                  value={title}
                  onChange={(event) => setTitle(event.target.value)}
                  required
                />
              </label>

              <label>
                URL
                <input
                  value={url}
                  onChange={(event) => setUrl(event.target.value)}
                  required
                />
              </label>

              <button type="submit">Save</button>
            </form>
          </section>

          <section className="search-section">
            <form onSubmit={handleSearch}>
              <input
                type="search"
                placeholder="Search your resources..."
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />

              <input
                type="text"
                placeholder="Filter by tag..."
                value={tag}
                onChange={(event) => setTag(event.target.value)}
              />

              <button type="submit">Search</button>
              <button
                type="button"
                onClick={handleClearFilters}
              >
                Clear
              </button>
            </form>
          </section>

          <section className="items-section">
            <div className="section-heading">
              <h2>Your resources</h2>
              <p>{items.length} saved</p>
            </div>

            <div className="items-list">
              {items.length === 0 ? (
                <div className="empty-state">
                  <h3>No resources found</h3>
                  <p>
                    Try a different search or clear your filters.
                  </p>
                </div>
              ) : (
                items.map((item) => (
                  <article key={item.id} className="item-card">
                    {editingItemId === item.id ? (
                      <form
                        onSubmit={async (event) => {
                          event.preventDefault()

                          try {
                            await updateItem(item.id, editTitle, editUrl)

                            const updatedItems = await getItems(search, tag)
                            setItems(updatedItems)

                            setEditingItemId(null)
                            setEditTitle("")
                            setEditUrl("")
                          } catch (error) {
                            if (error instanceof UnauthorizedError) {
                              handleUnauthorized()
                              return
                            }

                            console.error(error)
                          }
                        }}
                      >
                        <input
                          value={editTitle}
                          onChange={(event) => setEditTitle(event.target.value)}
                          required
                        />

                        <input
                          type="url"
                          value={editUrl}
                          onChange={(event) => setEditUrl(event.target.value)}
                          required
                        />

                        <button type="submit">
                          Save changes
                        </button>

                        <button
                          type="button"
                          onClick={() => {
                            setEditingItemId(null)
                            setEditTitle("")
                            setEditUrl("")
                          }}
                        >
                          Cancel
                        </button>
                      </form>
                    ) : (
                      <>
                        <div className="item-card-header">
                          <div>
                            <h3>{item.title}</h3>

                            <a
                              href={item.url}
                              target="_blank"
                              rel="noreferrer"
                            >
                              {item.url}
                            </a>
                          </div>

                          <span
                            className={`status status-${item.processing_status}`}
                          >
                            {item.processing_status === "pending" &&
                              "Waiting"}

                            {item.processing_status === "processing" &&
                              "Processing"}

                            {item.processing_status === "completed" &&
                              "Ready"}

                            {item.processing_status === "failed" &&
                              "Failed"}
                          </span>
                        </div>

                        <div>
                          <button
                            type="button"
                            onClick={() => {
                              setEditingItemId(item.id)
                              setEditTitle(item.title)
                              setEditUrl(item.url)
                            }}
                          >
                            Edit
                          </button>

                          <button
                            type="button"
                            onClick={() => handleDeleteItem(item.id)}
                          >
                            Delete
                          </button>
                        </div>

                        {item.summary && (
                          <p className="item-summary">
                            {item.summary}
                          </p>
                        )}

                        {item.tags && item.tags.length > 0 && (
                          <div className="item-tags">
                            {item.tags.map((tag) => (
                              <span key={tag} className="tag">
                                #{tag}
                              </span>
                            ))}
                          </div>
                        )}
                      </>
                    )}
                  </article>
                ))
              )}
            </div>
          </section>
        </>
      )}
    </main>
  )
}

export default App