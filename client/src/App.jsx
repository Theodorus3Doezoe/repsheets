import React from 'react'
import Login from './Login'
import { Routes, Route } from 'react-router-dom';


export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login/>}/>
    </Routes>
  )
}
