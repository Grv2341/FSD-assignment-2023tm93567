import './home.css';
import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from "react-router-dom";
import Nav from '../nav/nav';
import Search from '../search/search';

function Home() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const sessionId = useSelector((state) => state.sessionId);
    const currentPage = useSelector((state) => state.currentPage);

    useEffect(() => {
        if(!sessionId){
          navigate("/login")
        }
      }, [sessionId]);

    return (
        <div class = "cantainer">
            <Nav></Nav>
            <div class = "main-container">
                <Search></Search>
            </div>
        </div>
    )
}

export default Home;