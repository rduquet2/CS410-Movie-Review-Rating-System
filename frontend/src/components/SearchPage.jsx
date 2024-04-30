import React from 'react'
import axios from 'axios'
import { useState } from 'react'
import { useEffect } from 'react'

function SearchPage() {
 const [movieTitle, setMovieTitle] = useState('')
 const [recommendation, setRecommendation] = useState('')
 const [percent, setPercent] = useState('')

 useEffect(() => {
   axios.get('/getTitle')
     .then(res => res.data())
     .then(data => setRecommendation(data[0]))
 })

 const handleChange = (e) => {
   setMovieTitle(e.target.value)
 }

 const sendMovieTitle = (e) => {
   e.preventDefault()
   axios.post('/getTitle', {title: movieTitle})
       .then(res => console.log('hi', res.data))
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
