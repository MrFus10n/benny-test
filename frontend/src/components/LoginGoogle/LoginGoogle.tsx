import React from 'react'
import GoogleIcon from '@mui/icons-material/Google'

import { LoginButton } from '../LoginButton'

export function LoginGoogle() {
  return (
    <LoginButton
      url={"/accounts/google/login/"}
      icon={<GoogleIcon />}
      name="Google"
    />
  )
}