import { useState } from 'react'
import { Hero } from './components'
import styles from './style'

function App() {

  return (
    <div className='bg-primary w-full overflow-hidden'>
      
      <div className={`bg-primary ${styles.flexStart}`}>
        <div className={`${styles.boxWidth}`}>
          <Hero></Hero>
        </div>
      </div>

    </div>
  )
}

export default App
