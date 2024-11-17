import React, { useEffect } from 'react';
import './App.css';
import Login from './components/login/login';
import Register from './components/register/register';
import { useSelector, useDispatch } from 'react-redux';
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import 'react-toastify/dist/ReactToastify.css';
import Home from './components/home/home';

function App() {

  const count = useSelector((state) => state.count);
  const dispatch = useDispatch();

  const increment = () => {
    dispatch({ type: 'INCREMENT' });
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />}/>
        <Route path="/register" element={<Register />}/>
        <Route path="/home" element={<Home/>}/>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
