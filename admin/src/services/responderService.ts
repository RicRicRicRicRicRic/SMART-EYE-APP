/**
 * src/services/responderService.ts
 */
import api from './api'

export interface Responder {
  responder_id: string
  full_name: string
  email: string
  contact_number?: string
  profile_picture_url?: string
  responder_role: string
  approval_status: string
  is_active: string
  created_at: string
  updated_at?: string
}

export const responderService = {

  async getAll() {
    const response = await api.get('/admin/responders')
    return response.data
  },

  async updateStatus(responderId: string, data: { approval_status?: string; is_active?: string }) {
    const response = await api.patch(`/admin/responders/${responderId}/status`, data)
    return response.data
  },

  async getStats() {
    const response = await api.get('/admin/responders/stats')
    return response.data
  }
}

export const passwordResetService = {
  async resetPassword(email: string) {
    const response = await api.post('/admin/password-reset', { email })
    return response.data
  }
}