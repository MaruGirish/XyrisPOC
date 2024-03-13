import React from 'react'
import { Button } from '@mui/material'

function SigninPage() {


    const ssologin = () => {
        window.location.href = ("/redirection")
    }

    return (
        <div>
            Signin
            <Button onClick={ssologin}> sso </Button>
        </div>
    )
}

export default SigninPage
