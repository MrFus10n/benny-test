import * as mui from '@mui/material'
import React from 'react'


export function LogoutLink({refetchUser}: {refetchUser: CallableFunction}) {
  function handleLogout() {
    fetch('/logout/', {method: 'POST', headers: {'X-CSRFToken': window.GLOBAL_CONFIG.CSRF}})
      .then(() => refetchUser())
  }

  return <mui.Link onClick={handleLogout} sx={{ cursor: 'pointer' }}>Logout</mui.Link>
}