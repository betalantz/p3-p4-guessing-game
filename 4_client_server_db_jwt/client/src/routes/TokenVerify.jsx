import React, { useEffect, useState } from 'react'
import {useLocation, useNavigation, Outlet} from 'react-router-dom'
import {useAuth} from '../providers/authProvider'
import StatusDetail from '../components/StatusDetail'


function TokenVerify() {
  const [ message, setMessage ] = useState('')
 
  const { isTokenExpired } = useAuth()

  const location = useLocation()

  const navigate = useNavigation()

  useEffect(() => {
    console.log("🚀 ~ file: TokenVerify.jsx:15 ~ useEffect ~ isTokenExpired():", isTokenExpired())
    if (isTokenExpired()) {
     setMessage('You will be logged out in 10 seconds due to inactivity.')
    }
  }, [location, navigate, isTokenExpired])

  return (
    <>
      {message && 
        <StatusDetail
          message={message}
          isError={true}
          onCloseHandler={() => setMessage('')}
        />
      }
      <Outlet />
    </>
  )
}

export default TokenVerify