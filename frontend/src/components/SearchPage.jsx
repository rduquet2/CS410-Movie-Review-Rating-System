import React from 'react'
import axios from 'axios'
import { useState } from 'react'

function SearchPage() {
  const [movieTitle, setMovieTitle] = useState('')

  const handleChange = (e) => {
    setMovieTitle(e.target.value)
  }

  const sendMovieTitle = (e) => {
    e.preventDefault()
    console.log('here')
    axios.post('/getTitle', {data: movieTitle})
        .then(res => console.log(res.data))
        .catch(error => console.error(error));
  }

  return (
    <div className='search-container' onSubmit={sendMovieTitle}>
        <h1 className='search-title'>Search a Movie</h1>
        <form className='search-form'>
            <input type='text' onChange={handleChange}></input>
            <button type='submit'>
              <i className="fa-solid fa-arrow-right"></i>
            </button>
        </form>
    </div>
  )
}

export default SearchPage