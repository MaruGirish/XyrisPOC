import React from 'react'
import { BrowserRouter, Route, Routes, Navigate,} from 'react-router-dom'
import AuthFailure from './components/AuthFailure'
import AuthSuccess from './components/AuthSuccess'
import SigninPage from './Pages/SigninPage'
import Redirection from './redirections/Redirection'

function App() {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path='/' element={<SigninPage></SigninPage>} />
          <Route path='/redirection' element={<Redirection></Redirection>} />
          <Route path='/Authsuccess' element={<AuthSuccess></AuthSuccess>}/>
          <Route path='/AuthFailure' element={<AuthFailure></AuthFailure>}/>
          {/* <Route path="*" element={<Navigate to='/'/>} /> */}
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
