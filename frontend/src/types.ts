export type Item = {
  id: number
  title: string
  url: string
  content: string | null
  summary: string | null
  tags: string[] | null
  processing_error: string | null
  processing_status: string
}

export type LoginRequest = {
  username: string
  password: string
}

export type LoginResponse = {
  access_token: string
  token_type: string
}

export type ItemCreateRequest = {
  title: string
  url: string
}