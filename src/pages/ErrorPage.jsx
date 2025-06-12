import { useEffect } from 'react'
import { useNavigate } from 'react-router'

export const ErrorPage = () => {
    const navigate = useNavigate()

    useEffect(() => {
        setTimeout(() => {
            navigate("/")
        }, 3000)
    })
    return (
        <h1 className="text-center">Error 404</h1>
    )
}