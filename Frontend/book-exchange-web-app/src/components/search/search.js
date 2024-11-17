import './search.css';
import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from "react-router-dom";
import Nav from '../nav/nav';
import { GET_BOOK_BULK_URL } from '../../constants/constants';

function Search() {
    const dispatch = useDispatch();
    const navigate = useNavigate();
    const sessionId = useSelector((state) => state.sessionId);
    const [books, setBooks] = useState([])

    useEffect(() => {
        if(!sessionId){
          navigate("/login")
        }
      }, [sessionId]);

      useEffect(() => {
        getBooks();
      }, []);

    const getBooks = async () => {
        try {
            const response = await fetch(GET_BOOK_BULK_URL, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'session-id': sessionId
              },
              body: JSON.stringify({
                "perPage":20
                
              }),
            });
      
            const data = await response.json();
      
            if (response.ok) {
              console.log(data);
              setBooks(data)
            }
          } catch (error) {
            console.error('Error during login:', error);
          }
    }

    return (
        <div class = "search-container">
            <input type="text" placeholder="Search..." class="search-input" />
            <button class="search-button">Search</button>
            <div class="card-container">
                {books.map((book, index) => (
                    <div className="card" key={index}>
                    <h3 className="title">{book.title}</h3>
                    <p className="author">Author: {book.author}</p>
                    <p className="location">Location: {book.location}</p>
                    <p className="condition">Availability: {book.availability}</p>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Search;