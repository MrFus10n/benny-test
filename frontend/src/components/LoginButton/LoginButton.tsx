import * as mui from '@mui/material'
import React from 'react'

export function LoginButton({url, icon, name}: {url: string, icon: React.ReactNode, name: string}) {
  return (
    <form action={url} method="post">
        <input type="hidden" name="csrfmiddlewaretoken" value={window.GLOBAL_CONFIG.CSRF} />

        <mui.Button
          color="primary"
          startIcon={icon}
          type="submit"
          variant="contained"
        >
            Login with {name}
        </mui.Button>
    </form>
  )
}