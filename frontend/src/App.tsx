import * as mui from '@mui/material'
import React from 'react'

import * as api from 'api/api'

import { LoginGoogle } from './components/LoginGoogle'
import { LogoutLink } from './components/LogoutLink'
import { Parser } from './components/Parser'

function App() {
  console.log('Double fetch is due to react strict mode in development, this is normal')
  const currentUser = api.useCurrentUser()
  return (
    <mui.Container maxWidth="lg">
      <mui.Typography variant="h2" color="text.secondary" align="center" py={10}>
        Welcome to the test task!
      </mui.Typography>
      <mui.Box display="flex" justifyContent="center">
        {currentUser.data && (
          !currentUser.data.data.is_authenticated
          ? <LoginGoogle/>
          : <mui.Typography>
              You are logged in as {currentUser.data.data.first_name} {currentUser.data.data.last_name}. {' '}
              <LogoutLink refetchUser={currentUser.refetch}/>
            </mui.Typography>
        )}
      </mui.Box>
      <Parser/>
    </mui.Container>
  )
}

export default App
