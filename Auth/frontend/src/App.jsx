import './App.css'
import LoginPage from './components/LoginPage.jsx'
import SignupPage from './components/SignupPage.jsx'
import { useState } from 'react'
import { Routes,Route,Navigate } from "react-router-dom"
import { Toaster } from 'react-hot-toast';


function App() {
  
  return (
    <>
      <Toaster position='top-center'/>
      <Routes>
        <Route
          path='/'
          element={<LoginPage />}
        ></Route>
        <Route
          path='/login'
          element={<LoginPage />}
        ></Route>
        
        <Route
          path='/signup'
          element={<SignupPage />}
        ></Route>
      </Routes>
    </>
  )
}

export default App
