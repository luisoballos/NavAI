import { Navbar } from "../components/Navbar"
import { Footer } from "../components/Footer"
import { Outlet } from "react-router-dom";

export const Layout = () => {
    return (
        <div className="bg-dark">
            <Navbar />
                <Outlet />
            <Footer />
        </div>
    )
}