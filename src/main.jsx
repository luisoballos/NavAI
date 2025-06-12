import React from 'react'
import ReactDOM from 'react-dom/client'
import { RouterProvider } from "react-router-dom";
import { router } from "./routes";

const Main = () => {
    return (
        <React.StrictMode>  
            {/* Provide global state to all components 
            <StoreProvider>*/}
                {/* Set up routing for the application */} 
                <RouterProvider router={router}>
                </RouterProvider>
            {/*</StoreProvider>*/}
        </React.StrictMode>
    );
}

ReactDOM.createRoot(document.getElementById('root')).render(<Main />)