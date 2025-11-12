export interface Invitation {
  id: string
  inviteeEmail: string
  status: 'pending' | 'accepted' | 'expired'
  createdAt: string
  expiresAt: string
}

export interface SharedAccountUser {
  id: string
  email: string
  name: string
  createdAt: string
}

export interface SharedAccount {
  id: string
  createdAt: string
  users: SharedAccountUser[]
}

export interface InviteSpouseData {
  email: string
}

export interface AcceptInviteData {
  invitationId: string
}
